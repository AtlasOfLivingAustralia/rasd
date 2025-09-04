"""RASD FastAPI Data Access Request REST API Endpoints."""


# Third-Party
import boto3
import fastapi
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi import utils
from rasd_fastapi.core import security
from rasd_fastapi.crud import requests as req_crud
from rasd_fastapi.db import session
from rasd_fastapi.models import requests as req_models
from rasd_fastapi.models.requests_vocabs import access
from rasd_fastapi.models.requests_vocabs import anzsic
from rasd_fastapi.models.requests_vocabs import anzsrc
from rasd_fastapi.models.requests_vocabs import area
from rasd_fastapi.models.requests_vocabs import frequency
from rasd_fastapi.models.requests_vocabs import purposes
from rasd_fastapi.schemas import auth
from rasd_fastapi.schemas import pagination
from rasd_fastapi.schemas import requests as req_schemas

# Typing
from typing import Optional


# Router
router = fastapi.APIRouter()


@router.get(r"", response_model=pagination.PaginatedResult[req_models.DataAccessRequest])
async def list_data_access_requests(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    limit: Optional[int] = None,
    cursor: Optional[types.rasd.RASDIdentifier] = None,
) -> pagination.PaginatedResult[req_models.DataAccessRequest]:
    """List Data Access Requests endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active Data Access Requests.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[types.request_id.RASDIdentifier]): Optional pagination
            cursor.

    Returns:
        pagination.PaginatedResult[req_models.DataAccessRequest]: Retrieved page
            of Data Access Requests.
    """
    # Build Filter
    filters = req_crud.data_access_request.build_filter(
        active_only=active_only,
    )

    # Scan Data Access Requests and Return
    return req_crud.data_access_request.scan(
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/custodian", response_model=pagination.PaginatedResult[req_models.DataAccessRequest])
async def list_data_access_requests_custodian(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    limit: Optional[int] = None,
    cursor: Optional[types.rasd.RASDIdentifier] = None,
) -> pagination.PaginatedResult[req_models.DataAccessRequest]:
    """List Data Access Requests (Custodian) endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active Data Access Requests.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[types.request_id.RASDIdentifier]): Optional pagination
            cursor.

    Returns:
        pagination.PaginatedResult[req_models.DataAccessRequest]: Retrieved page
            of Data Access Requests.
    """
    # Build Filter
    filters = req_crud.data_access_request.build_filter(
        active_only=active_only,
        custodian_id=user.organisation_id,  # Restrict to User's Organisation
    )

    # Scan Data Access Requests
    page = req_crud.data_access_request.scan(
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )

    # Censor Details for Custodian
    req_crud.data_access_request.censor_for_custodian(user, *page.results)

    # Return
    return page


@router.get(r"/requestor", response_model=pagination.PaginatedResult[req_models.DataAccessRequest])
async def list_data_access_requests_requestor(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    active_only: bool = True,
    limit: Optional[int] = None,
    cursor: Optional[types.rasd.RASDIdentifier] = None,
) -> pagination.PaginatedResult[req_models.DataAccessRequest]:
    """List Data Access Requests (Requestor) endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        active_only (bool): Show only active Data Access Requests.
        limit (Optional[int]): Optional pagination limit.
        cursor (Optional[types.request_id.RASDIdentifier]): Optional pagination
            cursor.

    Returns:
        pagination.PaginatedResult[req_models.DataAccessRequest]: Retrieved page
            of Data Access Requests.
    """
    # Build Filter
    filters = req_crud.data_access_request.build_filter(
        active_only=active_only,
        requestor_id=user.id,  # Restrict to User's Requests
    )

    # Scan Data Access Requests and Return
    return req_crud.data_access_request.scan(
        db_session,
        filter=filters,
        limit=limit,
        cursor=cursor,
    )


@router.get(r"/accesses", response_model=list[access.Access])
async def list_access_request_accesses() -> list[access.Access]:
    """List Data Access Requests Accesses endpoint for REST API.

    Returns:
        list[access.Access]: Retrieved list of Accesses.
    """
    # Return Data Access Request Frequencies
    return list(access.Access)


@router.get(r"/areas", response_model=list[area.Area])
async def list_access_request_areas() -> list[area.Area]:
    """List Data Access Requests Areas endpoint for REST API.

    Returns:
        list[area.Area]: Retrieved list of Areas.
    """
    # Return Data Access Request Areas
    return list(area.Area)


@router.get(r"/frequencies", response_model=list[frequency.Frequency])
async def list_access_request_frequencies() -> list[frequency.Frequency]:
    """List Data Access Requests Frequencies endpoint for REST API.

    Returns:
        list[frequency.Frequency]: Retrieved list of Frequencies.
    """
    # Return Data Access Request Frequencies
    return list(frequency.Frequency)


@router.get(r"/industry-classifications", response_model=list[anzsic.IndustryClassification])
async def list_access_request_industry_classifications() -> list[anzsic.IndustryClassification]:
    """List Data Access Requests Industry Classifications endpoint for REST API.

    Returns:
        list[anzsic.IndustryClassification]: Retrieved list of Industry Classifications.
    """
    # Return Data Access Request Industry Classifications
    return list(anzsic.IndustryClassification)


@router.get(r"/purposes", response_model=list[purposes.Purpose])
async def list_access_request_purposes() -> list[purposes.Purpose]:
    """List Data Access Requests Purposes endpoint for REST API.

    Returns:
        list[purposes.Purpose]: Retrieved list of Purposes.
    """
    # Return Data Access Request Purposes
    return list(purposes.Purpose)


@router.get(r"/research-classifications", response_model=list[anzsrc.ResearchClassification])
async def list_access_request_research_classifications() -> list[anzsrc.ResearchClassification]:
    """List Data Access Requests Research Classifications endpoint for REST API.

    Returns:
        list[anzsrc.ResearchClassification]: Retrieved list of Research Classifications.
    """
    # Return Data Access Request Research Classifications
    return list(anzsrc.ResearchClassification)


@router.get(r"/{pk}", response_model=req_models.DataAccessRequest)
async def read_data_access_request(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
) -> req_models.DataAccessRequest:
    """Read Data Access Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to read.

    Returns:
        req_models.DataAccessRequest: Retrieved Data Access Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Determine Permissions
    is_requestor = user.id == access_request.requestor_id
    is_custodian = user.is_custodian() and user.organisation_id in access_request.custodian_ids

    # Check Permissions
    if not user.is_admin() and not is_requestor and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Check if Custodian Censoring is Required
    if not user.is_admin() and not is_requestor and is_custodian:
        # Censor Details for Custodian
        req_crud.data_access_request.censor_for_custodian(user, access_request)

    # Return Data Access Request
    return access_request


@router.get(r"/{pk}/summary", response_model=req_schemas.DataAccessRequestSummary)
async def read_data_access_request_summary(
    *,
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
) -> req_models.DataAccessRequest:
    """Read Data Access Request Summary endpoint for REST API.

    Args:
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to read.

    Returns:
        req_schemas.DataAccessRequestSummary: Retrieved Data Access Request Summary.
    """
    # Retrieve and Return Data Access Request
    # This will be automatically cast to the Non-Sensitive model by `fastapi`
    return utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )


@router.post(r"", response_model=req_models.DataAccessRequest)
async def create_data_access_request(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    req_in: req_schemas.DataAccessRequestCreate,
) -> req_models.DataAccessRequest:
    """Create Data Access Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in requestor via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        req_in (req_schemas.DataAccessRequestCreate): Create data.

    Returns:
        req_models.DataAccessRequest: Created Data Access Request.
    """
    # Handle Creation Errors
    # There are extra validation checks performed within the DataAccessRequest
    # model, so we need to handle and wrap any errors that occur.
    try:
        # Create Data Access Request
        obj = req_crud.data_access_request.create_with_user(
            db_session,
            obj_in=req_in,
            user=user,
        )

    except pydantic.ValidationError as exc:
        # Error
        raise fastapi.exceptions.RequestValidationError(
            errors=exc.raw_errors,
        ) from exc

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        ) from exc

    # Return
    return obj


@router.patch(r"/{pk}", response_model=req_models.DataAccessRequest)
async def update_data_access_request(
    *,
    admin: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    req_in: req_schemas.DataAccessRequestUpdate,
) -> req_models.DataAccessRequest:
    """Update Data Access Request endpoint for REST API.

    Args:
        admin (auth.User): Currently logged in admin via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.rasd.RASDIdentifier): Primary key of the Data Access Request to update.
        req_in (req_schemas.DataAccessRequestUpdate): Update data.

    Returns:
        req_models.DataAccessRequest: Updated Data Access Request.
    """
    # Retrieve Data Access Request
    req = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Check Data Access Request Completion
    if not req.completed_at:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Cannot update a Data Access Request that is not complete"
        )

    # Update and Return Data Access Request
    return req_crud.data_access_request.update(db_session, db_obj=req, obj_in=req_in)


@router.get(r"/{pk}/dataset-requests/{drpk}", response_model=req_models.DatasetRequest)
async def read_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Read Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to read.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to read.

    Returns:
        req_models.DatasetRequest: Retrieved Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_requestor = user.id == access_request.requestor_id
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_requestor and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Return Dataset Request
    return dataset_request


@router.patch(r"/{pk}/dataset-requests/{drpk}", response_model=req_models.DatasetRequest)
async def update_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
    req_in: req_schemas.DatasetRequestUpdate,
) -> req_models.DatasetRequest:
    """Update Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to update.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to update.
        req_in (req_schemas.DatasetRequestUpdate): Update data.

    Returns:
        req_models.DatasetRequest: Updated Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Update and Return Dataset Request
    return req_crud.data_access_request.update_dataset_request(
        db_session,
        db_obj=access_request,
        dataset_request=dataset_request,
        obj_in=req_in,
    )


@router.post(r"/{pk}/dataset-requests/{drpk}/acknowledge", response_model=req_models.DatasetRequest)
async def acknowledge_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Acknowledge Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to acknowledge.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to acknowledge.

    Returns:
        req_models.DatasetRequest: Acknowledged Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Acknowledge Errors
    try:
        # Acknowledge Dataset Request
        dataset_request = req_crud.data_access_request.acknowledge(
            db_session,
            db_obj=access_request,
            dataset_request=dataset_request,
            actioned_by=user.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return Dataset Request
    return dataset_request


@router.post(r"/{pk}/dataset-requests/{drpk}/approve", response_model=req_models.DatasetRequest)
async def approve_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Approve Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to approve.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to approve.

    Returns:
        req_models.DatasetRequest: Approved Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Approve Errors
    try:
        # Approve Dataset Request
        dataset_request = req_crud.data_access_request.approve(
            db_session,
            db_obj=access_request,
            dataset_request=dataset_request,
            actioned_by=user.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return Dataset Request
    return dataset_request


@router.post(r"/{pk}/dataset-requests/{drpk}/decline", response_model=req_models.DatasetRequest)
async def decline_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Decline Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to decline.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to decline.

    Returns:
        req_models.DatasetRequest: Declined Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Decline Errors
    try:
        # Decline Dataset Request
        dataset_request = req_crud.data_access_request.decline(
            db_session,
            db_obj=access_request,
            dataset_request=dataset_request,
            actioned_by=user.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return Dataset Request
    return dataset_request


@router.post(r"/{pk}/dataset-requests/{drpk}/agreement-sent", response_model=req_models.DatasetRequest)
async def agreement_sent_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Agreement Sent Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to agreement sent.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to agreement sent.

    Returns:
        req_models.DatasetRequest: Agreement Sent Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Agreement Sent Errors
    try:
        # Agreement Sent Dataset Request
        dataset_request = req_crud.data_access_request.agreement_sent(
            db_session,
            db_obj=access_request,
            dataset_request=dataset_request,
            actioned_by=user.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return Dataset Request
    return dataset_request


@router.post(r"/{pk}/dataset-requests/{drpk}/complete", response_model=req_models.DatasetRequest)
async def complete_dataset_request(
    *,
    user: auth.User = fastapi.Depends(security.require_admin_or_custodian),  # noqa: B008
    db_session: boto3.Session = fastapi.Depends(session.db_session),  # noqa: B008
    pk: types.rasd.RASDIdentifier,
    drpk: types.rasd.RASDIdentifier,
) -> req_models.DatasetRequest:
    """Complete Dataset Request endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        db_session (boto3.Session): Dependency injection database session.
        pk (types.request_id.RASDIdentifier): Primary key of the Data Access
            Request to complete.
        drpk (types.request_id.RASDIdentifier): Primary key of the Dataset
            Request to complete.

    Returns:
        req_models.DatasetRequest: Completed Dataset Request.
    """
    # Retrieve Data Access Request
    access_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get(db_session, pk=pk),
    )

    # Retrieve Dataset Request
    dataset_request = utils.unwrap_or_404(
        value=req_crud.data_access_request.get_dataset_request(db_obj=access_request, pk=drpk)
    )

    # Determine Permissions
    is_custodian = user.is_custodian() and user.organisation_id == dataset_request.custodian_id

    # Check Permissions
    if not user.is_admin() and not is_custodian:
        # Not allowed. We raise a `404` (rather than `403`) so that information
        # is not leaked
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_404_NOT_FOUND,
        )

    # Handle Complete Errors
    try:
        # Complete Dataset Request
        dataset_request = req_crud.data_access_request.complete(
            db_session,
            db_obj=access_request,
            dataset_request=dataset_request,
            actioned_by=user.email,
        )

    except ValueError as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return Dataset Request
    return dataset_request
