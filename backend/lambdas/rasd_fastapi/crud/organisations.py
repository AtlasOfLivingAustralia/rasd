"""RASD FastAPI CRUD for Organisations."""


# Standard
import uuid

# Third-Party
import boto3
import boto3.dynamodb.conditions

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.crud import base
from rasd_fastapi.models import organisations as org_models
from rasd_fastapi.schemas import organisations as org_schemas
from rasd_fastapi.services import abn


class OrganisationCRUD(
    base.CRUDBase[
        org_models.Organisation,
        org_schemas.OrganisationCreate,
        org_schemas.OrganisationUpdate,
        uuid.UUID,
    ],
):
    """Organisation CRUD Abstraction."""

    def create_unique(
        self,
        db_session: boto3.Session,
        *,
        obj_in: org_schemas.OrganisationCreate,
    ) -> org_models.Organisation:
        """Creates a Unique Organisation in the database.

        Additionally, this method verifies the uniqueness of the Organisation
        and the validity of the supplied ABN with an external service. This is
        performed here (in the CRUD abstraction) rather than on the Pydantic
        model so that we can reduce the number of API calls. It is initially
        satisfactory to just check the ABN with the external service upon
        *creation*, rather than each time a model is instantiated.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (org_schemas.OrganisationCreate): Data to create item with.

        Returns:
            org_models.Organisation: Created Organisation in the database.
        """
        # Check Uniqueness
        if not self.is_unique(db_session, obj_in=obj_in):
            raise ValueError("Organisation with matching details already exists")

        # Verify the ABN using external service
        if not abn.verify_registered(obj_in.abn):
            raise ValueError("ABN is not registered")
        if not abn.verify_active(obj_in.abn):
            raise ValueError("ABN is no longer active")
        if not abn.verify_name(obj_in.abn, obj_in.name):
            raise ValueError(f"ABN registered entity name does not match '{obj_in.name}'")

        # Allow super class to handle the rest of Creation
        return super().create(db_session, obj_in=obj_in)

    def is_unique(
        self,
        db_session: boto3.Session,
        *,
        obj_in: org_schemas.OrganisationCreate,
    ) -> bool:
        """Checks wther the supplied Organisation is unique.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (CreateSchemaType): Data to check uniqueness with.

        Returns:
            bool: Whether this item is unique
        """
        # Create Uniqueness Filter
        unique = (
            boto3.dynamodb.conditions.Attr("name").eq(obj_in.name)
            | boto3.dynamodb.conditions.Attr("abn").eq(obj_in.abn)
        )

        # Scan for Uniqueness
        results = self.scan(db_session, filter=unique)

        # Return Boolean Result
        # If there are results, then this is not unique
        # If there are no results, then this is unique
        return results.count == 0

    def find_existing(
        self,
        db_session: boto3.Session,
        *,
        obj_in: org_schemas.OrganisationCreate,
    ) -> org_models.Organisation | None:
        """Finds an existing Organisation by name or ABN.

        Args:
            db_session (boto3.Session): Database session to use.
            obj_in (org_schemas.OrganisationCreate): Data to search for.

        Returns:
            org_models.Organisation | None: Existing Organisation if found, None otherwise.
        """
        # Create filter to find matching organisation by name or ABN
        existing_filter = (
            boto3.dynamodb.conditions.Attr("name").eq(obj_in.name)
            | boto3.dynamodb.conditions.Attr("abn").eq(obj_in.abn)
        )

        # Scan for existing organisations
        results = self.scan(db_session, filter=existing_filter)

        # Return the first match if any exist
        if results.count > 0:
            return results.items[0]

        return None


# Instantiate Organisation CRUD Singleton
organisation = OrganisationCRUD(
    model=org_models.Organisation,
    table=settings.SETTINGS.AWS_DYNAMODB_TABLE_ORGANISATIONS,
    pk="id",
)
