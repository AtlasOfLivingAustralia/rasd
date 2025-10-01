"""RASD FastAPI Metadata REST API Endpoints."""


# Standard
import uuid

# Third-Party
import boto3
import fastapi
import pydantic

# Local
from rasd_fastapi import utils
from rasd_fastapi.db import session
from rasd_fastapi.core import security
from rasd_fastapi.crud import metadata as metadata_crud
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.models import metadata as metadata_models
from rasd_fastapi.models.metadata_vocabs import access_rights
from rasd_fastapi.models.metadata_vocabs import collection_methods
from rasd_fastapi.models.metadata_vocabs import formats
from rasd_fastapi.models.metadata_vocabs import keywords
from rasd_fastapi.models.metadata_vocabs import locations
from rasd_fastapi.models.metadata_vocabs import security_classifications
from rasd_fastapi.schemas import auth
from rasd_fastapi.schemas import metadata as metadata_schemas
from rasd_fastapi.schemas import pagination

# Typing
from typing import Optional


# Router
router = fastapi.APIRouter()


@router.get(r"", response_model=pagination.PaginatedResult[metadata_models.RASDMetadata])
async def list_metadata(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    limit: Optional[int] = None,
    cursor: Optional[uuid.UUID] = None,
) -> pagination.PaginatedResult[metadata_models.RASDMetadata]:
    """List Metadata endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active metadata.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[uuid.UUID]): Optional pagination cursor.

    Returns:
        pagination.PaginatedResult[metadata_models.RASDMetadata]: Retrieved
            page of Metadata.
    """
    # Retrieve User's Organisation ID
    # The retrieved Metadata is restricted to the User's Organisation, except
    # for Administrators who can retrieve Metadata for *all* Organisations.
    org_id = user.organisation_id if not user.is_admin() else None

    # Build Filter
    filters = metadata_crud.metadata.build_filter(
        active_only,
        organisation_id=org_id,  # Restrict to user's Organisation (if applicable)
    )

    # Scan Metadata and Return
    return metadata_crud.metadata.scan(
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/search", response_model=pagination.PaginatedResult[metadata_schemas.RASDMetadataSummary])
async def search_metadata(
    *,
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    title: Optional[str] = None,
    abstract: Optional[str] = None,
    keywords: Optional[set[keywords.Keyword]] = fastapi.Query(None),  # noqa: B008
    locations: Optional[set[locations.Location]] = fastapi.Query(None),  # noqa: B008
    organisation_id: Optional[uuid.UUID] = None,
    limit: Optional[int] = None,
    cursor: Optional[uuid.UUID] = None,
) -> pagination.PaginatedResult[metadata_schemas.RASDMetadataSummary]:
    """List Metadata endpoint for REST API.

    Args:
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active metadata.
        title (Optional[str]): Filter results based on `title`.
        abstract (Optional[str]): Filter results based on `abstract`.
        keywords (Optional[set[keywords.Keyword]]): Filter results based on `keywords`.
        locations (Optional[set[locations.Location]]): Filter results based on `locations`.
        organisation_id (Optional[uuid.UUID]): Filter results based on `organisation_id`.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[uuid.UUID]): Optional pagination cursor.

    Returns:
        pagination.PaginatedResult[metadata_schemas.RASDMetadataSummary]:
            Retrieved page of Non-Sensitive Metadata.
    """
    # Build Filter
    filters = metadata_crud.metadata.build_filter(
        active_only,
        title,
        abstract,
        keywords,
        locations,
        organisation_id,
    )

    # Scan Metadata and Return
    # This will be automatically cast to the Non-Sensitive model by `fastapi`
    return metadata_crud.metadata.scan(  # type: ignore[return-value]
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/access-rights", response_model=list[access_rights.AccessRights])
async def list_metadata_access_rights() -> list[access_rights.AccessRights]:
    """List Metadata Access Rights endpoint for REST API.

    Returns:
        list[access_rights.AccessRights]: Retrieved list of Access Rights.
    """
    # Return Metadata Access Rights
    return list(access_rights.AccessRights)


@router.get(r"/collection-methods", response_model=list[collection_methods.CollectionMethod])
async def list_metadata_collection_methods() -> list[collection_methods.CollectionMethod]:
    """List Metadata Collection Methods endpoint for REST API.

    Returns:
        list[collection_methods.CollectionMethod]: Retrieved list of Collection Methods.
    """
    # Return Metadata Collection Methods
    return list(collection_methods.CollectionMethod)


@router.get(r"/formats", response_model=list[formats.Format])
async def list_metadata_formats() -> list[formats.Format]:
    """List Metadata Formats endpoint for REST API.

    Returns:
        list[formats.Format]: Retrieved list of Formats.
    """
    # Return Metadata Formats
    return list(formats.Format)


@router.get(r"/keywords", response_model=list[keywords.Keyword])
async def list_metadata_keywords() -> list[keywords.Keyword]:
    """List Metadata Keywords endpoint for REST API.

    Returns:
        list[keywords.Keyword]: Retrieved list of Keywords.
    """
    # Return Metadata Keywords
    return list(keywords.Keyword)


@router.get(r"/locations", response_model=list[locations.Location])
async def list_metadata_locations() -> list[locations.Location]:
    """List Metadata Locations endpoint for REST API.

    Returns:
        list[locations.Location]: Retrieved list of Locations.
    """
    # Return Metadata Locations
    return list(locations.Location)


@router.get(r"/security-classifications", response_model=list[security_classifications.SecurityClassification])
async def list_metadata_security_classifications() -> list[security_classifications.SecurityClassification]:
    """List Metadata Security Classifications endpoint for REST API.

    Returns:
        list[security_classifications.SecurityClassification]: Retrieved list of Security Classifications.
    """
    # Return Metadata Security Classifications
    return list(security_classifications.SecurityClassification)


@router.get(r"/{pk}", response_model=metadata_models.RASDMetadata)
async def read_metadata(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> metadata_models.RASDMetadata:
    """Read Metadata endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Metadata to read.

    Returns:
        metadata_models.RASDMetadata: Retrieved Metadata.
    """
    # Retrieve Metadata
    metadata = utils.unwrap_or_404(
        value=metadata_crud.metadata.get(db_session, pk=pk),
    )

    # Check Permissions
    # Administrators can retrieve *any* Metadata, whereas Data Custodians can
    # only retrieve Metadata for *their* Organisation.
    if not user.is_admin() and metadata.organisation_id != user.organisation_id:
        # Not allowed, Data Custodian can only retrieve *their* Metadata
        # We raise a `404` (rather than `403`) so that information is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Return Metadata
    return metadata


@router.post(r"", response_model=metadata_models.RASDMetadata)
async def create_metadata(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    metadata_in: metadata_schemas.RASDMetadataCreate,
) -> metadata_models.RASDMetadata:
    """Create Metadata endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        metadata_in (metadata_schemas.RASDMetadataCreate): Create data.

    Returns:
        metadata_models.RASDMetadata: Created Metadata.
    """
    # Retrieve User Organisation
    org = org_crud.organisation.get(db_session, pk=user.organisation_id)

    # Check Organisation
    if not org:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=f"User associated with non-existant Organisation: '{user.organisation_id}'"
        )

    # Handle Creation Errors
    # There are extra validation checks performed within the Metadata model, so
    # we need to handle and wrap any errors that occur.
    try:
        # Create Metadata
        obj = metadata_crud.metadata.create_with_org(
            db_session,
            obj_in=metadata_in,
            org=org,
        )

    except pydantic.ValidationError as exc:
        # Error
        raise fastapi.exceptions.RequestValidationError(
            errors=exc.raw_errors,
        ) from exc

    # Return
    return obj


@router.patch(r"/{pk}", response_model=metadata_models.RASDMetadata)
async def update_metadata(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
    metadata_in: metadata_schemas.RASDMetadataUpdate,
) -> metadata_models.RASDMetadata:
    """Update Metadata endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Metadata to read.
        metadata_in (metadata_schemas.RASDMetadataUpdate): Update data.

    Returns:
        metadata_models.RASDMetadata: Updated Metadata.
    """
    # Retrieve Metadata
    metadata = utils.unwrap_or_404(
        value=metadata_crud.metadata.get(db_session, pk=pk),
    )

    # Check Permissions
    # Administrators can update *any* Metadata, whereas Data Custodians can
    # only update Metadata for *their* Organisation.
    if not user.is_admin() and metadata.organisation_id != user.organisation_id:
        # Not allowed, Data Custodian can only update *their* Metadata
        # We raise a `404` (rather than `403`) so that information is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Update Errors
    # There are extra validation checks performed within the Metadata model, so
    # we need to handle and wrap any errors that occur.
    try:
        # Update Metadata
        obj = metadata_crud.metadata.update(
            db_session,
            db_obj=metadata,
            obj_in=metadata_in,
        )

    except pydantic.ValidationError as exc:
        # Error
        raise fastapi.exceptions.RequestValidationError(
            errors=exc.raw_errors,
        ) from exc

    # Return
    return obj


@router.delete(r"/{pk}", response_model=metadata_models.RASDMetadata)
async def delete_metadata(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: uuid.UUID,
) -> metadata_models.RASDMetadata:
    """Delete Metadata endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (uuid.UUID): Primary key of the Metadata to delete.

    Returns:
        metadata_models.RASDMetadata: Deleted Metadata.
    """
    # Retrieve Metadata
    metadata = utils.unwrap_or_404(
        value=metadata_crud.metadata.get(db_session, pk=pk),
    )

    # Check Permissions
    # Administrators can delete *any* Metadata, whereas Data Custodians can
    # only delete Metadata for *their* Organisation.
    if not user.is_admin() and metadata.organisation_id != user.organisation_id:
        # Not allowed, Data Custodian can only delete *their* Metadata
        # We raise a `404` (rather than `403`) so that information is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Delete Metadata
    deleted_metadata = metadata_crud.metadata.delete(
        db_session,
        pk=pk,
    )

    # Check if deletion was successful
    if not deleted_metadata:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Return the deleted metadata
    return deleted_metadata

