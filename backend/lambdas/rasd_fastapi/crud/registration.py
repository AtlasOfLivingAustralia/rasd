"""RASD FastAPI CRUD for Registrations."""


# Standard
import functools
import operator
import uuid

# Third-Party
import boto3
import boto3.dynamodb.conditions as con
import pydantic

# Local
from rasd_fastapi.auth import cognito
from rasd_fastapi.core import settings
from rasd_fastapi.crud import base
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.emails import email
from rasd_fastapi.models import registration as reg_models
from rasd_fastapi.schemas import auth as auth_schemas
from rasd_fastapi.schemas import registration as reg_schemas
from rasd_fastapi.services import abn

# Typing
from typing import Optional


class RegistrationCRUD(
    base.CRUDBase[
        reg_models.Registration,
        reg_schemas.RegistrationCreate,
        reg_schemas.RegistrationUpdate,
        uuid.UUID,
    ],
):
    """Registration CRUD Abstraction."""

    # Filter Shortcuts
    NewOnly = con.Attr("status").eq(reg_models.Status.NEW)

    def create_unique(
        self,
        db_session: boto3.Session,
        *,
        obj_in: reg_schemas.RegistrationCreate,
    ) -> reg_models.Registration:
        """Creates a Unique Registration in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (reg_schemas.RegistrationCreate): Data to create item with.

        Returns:
            reg_models.Registration: Created Registration in the database.
        """
        # Check Groups
        if obj_in.group == auth_schemas.Group.ADMINISTRATORS:
            # Administrator registrations are currently not allowed
            raise ValueError("Registering an Administrator user is not allowed")

        # Check if an existing registration has already been created
        unique = con.Attr("username").eq(obj_in.username)
        if self.scan(db_session, filter=unique).count != 0:
            # Registration can only be performed once per email address
            raise ValueError("Registration with matching details already exists")

        # Check if an existing or a new organisation has been provided
        if isinstance(obj_in.organisation, uuid.UUID):
            # User has supplied an existing Organisation ID
            # Check whether Organisation exists
            if not org_crud.organisation.get(db_session, pk=obj_in.organisation):
                # Registration must be performed with an Organisation that exists
                raise ValueError(f"Organisation with ID '{obj_in.organisation}' does not exist")

        else:
            # User has supplied details for a new Organisation
            # Check Uniqueness
            if not org_crud.organisation.is_unique(db_session, obj_in=obj_in.organisation):
                raise ValueError("Organisation with matching details already exists")

            # Verify the ABN using external service
            if not abn.verify_registered(obj_in.organisation.abn):
                raise ValueError("ABN is not registered")
            if not abn.verify_active(obj_in.organisation.abn):
                raise ValueError("ABN is no longer active")
            if not abn.verify_name(obj_in.organisation.abn, obj_in.organisation.name):
                raise ValueError(f"ABN registered entity name does not match '{obj_in.organisation.name}'")

        # Allow super class to handle the rest of Creation
        reg = super().create(db_session, obj_in=obj_in)

        # Send Created Email
        email.registration_created.send(
            to_addresses=settings.SETTINGS.EMAIL_ADMIN_INBOX,
            registration_id=reg.id,
        )

        # Return
        return reg

    def approve(
        self,
        db_session: boto3.Session,
        *,
        db_obj: reg_models.Registration,
        override_organisation_id: Optional[uuid.UUID],
        actioned_by: pydantic.EmailStr,
    ) -> reg_models.Registration:
        """Approves a Registration.

        This method contains a large amount of logic and functionality. Upon
        approving a registration, the following occurs:
            1. The registration details are validated
                - If provided, the existing Organisation ID is checked
                - If provided, the override Organisation ID is checked
                - If provided, the new Organisation is checked and created
            2. The user is registered in Cognito
            3. The Registration is updated in the database.
            4. An email is sent to the user

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (reg_models.Registration): Registration to approve.
            override_organisation_id (Optional[uuid.UUID]): Organisation ID to
                override the registration with. If this is provided, then the
                Organisation provided by the user in their registration will
                be ignored and this will be used instead.
            actioned_by (pydantic.EmailStr): The email address of the Admin
                that this was actioned by.

        Raises:
            ValueError: Raised if an error occurs with approval.

        Returns:
            reg_models.Registration: Approved Registration from the database.
        """
        # Check current status
        if db_obj.status != reg_models.Status.NEW:
            # Error
            raise ValueError(f"Cannot decline registration with status '{db_obj.status}'")

        # Approving is quite an involved process
        # First, we have to handle the provided override Organisation ID
        org = override_organisation_id or db_obj.organisation

        # Next, handle the validity of the Organisation
        # Here we must create the Organisation if it does not already exist
        if isinstance(org, uuid.UUID):
            # Check whether Organisation exists
            if not org_crud.organisation.get(db_session, pk=org):
                # Registration must be performed with an Organisation that exists
                raise ValueError(f"Organisation with ID '{org}' does not exist")

        else:
            # Check if an organisation with matching details already exists
            existing_org = org_crud.organisation.find_existing(db_session, obj_in=org)

            if existing_org:
                # Use the existing organisation instead of creating a new one
                # Note: The existing organisation's email address takes precedence
                org = existing_org.id
            else:
                # Create the Organisation and Retrieve its ID
                org = org_crud.organisation.create_unique(db_session, obj_in=org).id

        # Now, register the user in AWS Cognito
        password = cognito.register(
            username=db_obj.username,
            given_name=db_obj.given_name,
            family_name=db_obj.family_name,
            organisation_id=org,
            group=db_obj.group,
        )

        # Finally, Update the Registration in the Database
        db_obj = self.update(
            db_session,
            db_obj=db_obj,
            obj_in=reg_schemas.RegistrationUpdate(),  # Dummy object - required for update
            status=reg_models.Status.APPROVED,
            organisation_override=override_organisation_id,
            actioned_by=actioned_by
        )

        # Send Approved Email
        email.registration_approved.send(
            to_addresses=db_obj.username,
            given_name=db_obj.given_name,
            family_name=db_obj.family_name,
            temporary_password=password.get_secret_value(),
            rasd_create_password_url=settings.SETTINGS.RASD_CREATE_PASSWORD_URL,
        )

        # Return
        return db_obj

    def decline(
        self,
        db_session: boto3.Session,
        *,
        db_obj: reg_models.Registration,
        reason: Optional[str],
        actioned_by: pydantic.EmailStr,
    ) -> reg_models.Registration:
        """Declines a Registration.

        This method contains only a small amount of logic and functionality.
        Upon declining a registration, it is just updated in the database.

        Args:
            db_session (boto3.Session): Database session to use.
            db_obj (reg_models.Registration): Registration to approve.
            reason (Optional[str]): Reason that the Registration was declined.
            actioned_by (pydantic.EmailStr): The email address of the Admin
                that this was actioned by.

        Raises:
            ValueError: Raised if an error occurs with declining.

        Returns:
            reg_models.Registration: Declined Registration from the database.
        """
        # Check current status
        if db_obj.status != reg_models.Status.NEW:
            # Error
            raise ValueError(f"Cannot decline registration with status '{db_obj.status}'")

        # Next, Update the Registration in the Database
        db_obj = self.update(
            db_session,
            db_obj=db_obj,
            obj_in=reg_schemas.RegistrationUpdate(),  # Dummy object - required for update
            status=reg_models.Status.DECLINED,
            reason=reason,
            actioned_by=actioned_by
        )

        # Send Declined Email
        email.registration_declined.send(
            to_addresses=db_obj.username,
            given_name=db_obj.given_name,
            family_name=db_obj.family_name,
            registration_id=db_obj.id,
            rasd_framework_url=settings.SETTINGS.RASD_FRAMEWORK_URL,
            rasd_support_email=settings.SETTINGS.RASD_SUPPORT_EMAIL,
        )

        # Return
        return db_obj

    def build_filter(
        self,
        active_only: bool = True,
        status: Optional[reg_models.Status] = None,
    ) -> Optional[con.ConditionBase]:
        """Builds the search filter for the Registrations table.

        Each of the provided values is combined into a single filter using a
        logical AND. That is, all of the supplied filter values must match in
        an underlying Metadata instance for the filter to return them.

        The interface that `boto3` provides for constructing DynamoDB filters
        does not cater very well for dynamic filter generation. As such, the
        syntax used to generate the filter below is slightly obscure. In order
        to be terse we utilise functional concepts like the `reduce` method to
        combine individual filters.

        Args:
            active_only (bool): Filter for `active` only metadata.
            status (Optional[reg_models.Status]): Filter results based on `status`.

        Returns:
            Optional[con.ConditionBase]: Possible built filter.
        """
        # Generate Filters
        # Here we construct all of the required filters in a list.
        # Based on the input data, the items in this list will either be an
        # individually constructed filter (if a value is supplied) or `None`.
        filters = [
            # `active` filter - `active` must equal `True`
            con.Attr("active").eq(True) if active_only else None,
            # `status` filter - `status` must equal the provided Status
            con.Attr("status").eq(status) if status else None
        ]

        # Next, we remove all of the `None`s from the filters list
        # This removes any of the filters that a value was not supplied for
        filters = [f for f in filters if f]

        # Finally, we reduce the list of filters to a single filter where all
        # of the individual filters must be true (i.e., logical AND).
        combined_filter = functools.reduce(operator.and_, filters) if filters else None

        # Return
        return combined_filter


# Instantiate Registration CRUD Singleton
registration = RegistrationCRUD(
    model=reg_models.Registration,
    table=settings.SETTINGS.AWS_DYNAMODB_TABLE_REGISTRATIONS,
    pk="id",
)
