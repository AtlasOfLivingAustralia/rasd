"""RASD FastAPI Registration REST API Endpoints."""


# Standard
import uuid

# Third-Party
import boto3
import fastapi

# Local
from rasd_fastapi import utils
from rasd_fastapi.core import security
from rasd_fastapi.crud import registration as reg_crud
from rasd_fastapi.db import session
from rasd_fastapi.models import registration as reg_models
from rasd_fastapi.schemas import auth
from rasd_fastapi.schemas import pagination
from rasd_fastapi.schemas import registration as reg_schemas

# Typing
from typing import Optional


# Router
router = fastapi.APIRouter()


@router.get(r"", response_model=pagination.PaginatedResult[reg_models.Registration])
async def list_registrations(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    status: Optional[reg_models.Status] = None,
    limit: Optional[int] = None,
    cursor: Optional[uuid.UUID] = None,
) -> pagination.PaginatedResult[reg_models.Registration]:
    """List Registrations endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active Registrations.
        status (Optional[reg_models.Status]): Filter Registrations by status.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[uuid.UUID]): Optional pagination cursor.

    Returns:
        pagination.PaginatedResult[reg_models.Registration]: Retrieved page of
            Registrations.
    """
    # Build Filter
    filters = reg_crud.registration.build_filter(
        active_only=active_only,
        status=status,  # Restrict to status (if applicable)
    )

    # Scan Registrations and Return
    return reg_crud.registration.scan(
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/{pk}", response_model=reg_models.Registration)
async def read_registration(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> reg_models.Registration:
    """Read Registration endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Registration to read.

    Returns:
        reg_models.Registration: Retrieved Registration.
    """
    # Retrieve and Return Registration
    return utils.unwrap_or_404(
        value=reg_crud.registration.get(db_session, pk=pk),
    )


@router.post(r"", response_model=reg_models.Registration)
async def register(
    *,
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    reg_in: reg_schemas.RegistrationCreate,
) -> reg_models.Registration:
    """Registration endpoint for REST API.

    Args:
        db_session (boto3.Session): Dependency injection database session.
        reg_in (reg_schemas.RegistrationCreate): Create data.

    Returns:
        reg_models.Registration: Created Registration.
    """
    # Handle Creation Errors
    # The uniqueness of the Organisation is checked, and the ABN is validated
    # by an external service upon creation, so we need to handle and wrap any
    # errors that occur.
    try:
        # Create Registration
        obj = reg_crud.registration.create_unique(db_session, obj_in=reg_in)

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    # Return
    return obj


@router.post(r"/{pk}/approve", response_model=reg_models.Registration)
async def approve_registration(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
    override_organisation_id: Optional[uuid.UUID] = None,
) -> reg_models.Registration:
    """Approve Registration endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Registration to approve.
        override_organisation_id (uuid.UUID): Organisation ID to approve with.

    Returns:
        reg_models.Registration: Approved Registration.
    """
    # Retrieve Registration
    reg = utils.unwrap_or_404(
        value=reg_crud.registration.get(db_session, pk=pk),
    )

    # Handle Approval Errors
    try:
        # Approve Registration
        obj = reg_crud.registration.approve(
            db_session,
            db_obj=reg,
            override_organisation_id=override_organisation_id,
            actioned_by=admin.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return obj


@router.post(r"/{pk}/decline", response_model=reg_models.Registration)
async def decline_registration(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
    reason: Optional[str] = None,
) -> reg_models.Registration:
    """Decline Registration endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Registration to decline.
        reason (Optional[str]): Reason for declining.

    Returns:
        reg_models.Registration: Declined Registration.
    """
    # Retrieve Registration
    reg = utils.unwrap_or_404(
        value=reg_crud.registration.get(db_session, pk=pk),
    )

    # Handle Declining Errors
    try:
        # Decline Registration
        obj = reg_crud.registration.decline(
            db_session,
            db_obj=reg,
            reason=reason,
            actioned_by=admin.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return obj


@router.delete(r"/{pk}", response_model=reg_models.Registration)
async def delete_registration(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> reg_models.Registration:
    """Delete Registration endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Registration to delete.

    Returns:
        reg_models.Registration: Deleted Registration.
    """
    # Retrieve Registration
    reg = utils.unwrap_or_404(
        value=reg_crud.registration.get(db_session, pk=pk),
    )

    # Handle Removal Errors
    try:
        # Remove Registration
        obj = reg_crud.registration.remove(
            db_session,
            db_obj=reg,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return obj


@router.post(r"/{pk}/resend-password", response_model=reg_models.Registration)
async def resend_temporary_password(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> reg_models.Registration:
    """Resend Temporary Password endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Registration to resend for.

    Returns:
        reg_models.Registration: Registration the password was resent for.
    """
    # Retrieve Registration
    reg = utils.unwrap_or_404(
        value=reg_crud.registration.get(db_session, pk=pk),
    )

    # Handle Resending Errors
    try:
        # Resend Temporary Password
        obj = reg_crud.registration.resend_temporary_password(
            db_obj=reg,
            actioned_by=admin.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    # Return
    return obj
