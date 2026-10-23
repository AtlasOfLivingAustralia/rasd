"""RASD FastAPI Registration CRUD Unit Tests."""


# Standard
from unittest.mock import patch

# Third-Party
import pytest

# Local
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.crud import registration as reg_crud
from rasd_fastapi.db import session
from rasd_fastapi.models import registration as reg_models
from rasd_fastapi.schemas import auth as auth_schemas
from rasd_fastapi.schemas import organisations as org_schemas
from rasd_fastapi.schemas import registration as reg_schemas
from tests import conftest


@pytest.fixture
def _mock_emails():
    """Mock outgoing registration emails."""
    with patch("rasd_fastapi.emails.email.Email.send"):
        yield


def registration_create(db_session) -> reg_schemas.RegistrationCreate:
    """Creates an Organisation and returns Registration data for it."""
    # Create Organisation
    org = org_crud.organisation.create_unique(
        db_session,
        obj_in=org_schemas.OrganisationCreate.parse_obj(conftest.load_data_json("organisation.json")),
    )

    # Return Registration Data
    return reg_schemas.RegistrationCreate(
        username="test@example.com",
        given_name="Test",
        family_name="User",
        group=auth_schemas.Group.DATA_REQUESTORS,
        organisation=org.id,
        agreements=["I agree"],
    )


def create_with_status(
    db_session,
    data: reg_schemas.RegistrationCreate,
    status: reg_models.Status,
) -> reg_models.Registration:
    """Creates a Registration and sets its Status directly.

    This bypasses `approve()` and `decline()` so that Cognito is not called.
    """
    # Create Registration
    reg = reg_crud.registration.create_unique(db_session, obj_in=data)

    # Set Status and Return
    return reg_crud.registration.update(
        db_session,
        db_obj=reg,
        obj_in=reg_schemas.RegistrationUpdate(),
        status=status,
    )


@pytest.mark.usefixtures("_mock_emails")
@pytest.mark.parametrize("status", [reg_models.Status.NEW, reg_models.Status.APPROVED])
def test_registration_duplicate_rejected(mock_dynamodb_tables, mock_abn_responses, status) -> None:
    """Tests that a New or Approved Registration blocks a duplicate Registration."""
    # Create Database Session
    db_session = session.db_session()

    # Create Registration with the supplied Status
    data = registration_create(db_session)
    create_with_status(db_session, data, status)

    # Attempt Duplicate Registration
    with pytest.raises(ValueError, match="already exists"):
        reg_crud.registration.create_unique(db_session, obj_in=data)


@pytest.mark.usefixtures("_mock_emails")
def test_registration_after_decline(mock_dynamodb_tables, mock_abn_responses) -> None:
    """Tests that a declined Registration does not block a new Registration."""
    # Create Database Session
    db_session = session.db_session()

    # Create and Decline Registration
    data = registration_create(db_session)
    reg = reg_crud.registration.create_unique(db_session, obj_in=data)
    reg_crud.registration.decline(
        db_session,
        db_obj=reg,
        reason="Incorrect details",
        actioned_by="admin@example.com",
    )

    # Register Again
    new_reg = reg_crud.registration.create_unique(db_session, obj_in=data)

    # Assert
    assert new_reg.id != reg.id
    assert new_reg.status == reg_models.Status.NEW

    # Attempt Duplicate of the new pending Registration
    with pytest.raises(ValueError, match="already exists"):
        reg_crud.registration.create_unique(db_session, obj_in=data)


@pytest.mark.usefixtures("_mock_emails")
@pytest.mark.parametrize("status", [reg_models.Status.NEW, reg_models.Status.DECLINED])
def test_registration_remove(mock_dynamodb_tables, mock_abn_responses, status) -> None:
    """Tests that New and Declined Registrations can be removed."""
    # Create Database Session
    db_session = session.db_session()

    # Create Registration with the supplied Status
    reg = create_with_status(db_session, registration_create(db_session), status)

    # Remove Registration
    removed = reg_crud.registration.remove(db_session, db_obj=reg)

    # Assert
    assert removed.id == reg.id
    assert reg_crud.registration.get(db_session, pk=reg.id) is None


@pytest.mark.usefixtures("_mock_emails")
def test_registration_remove_approved_rejected(mock_dynamodb_tables, mock_abn_responses) -> None:
    """Tests that an Approved Registration cannot be removed."""
    # Create Database Session
    db_session = session.db_session()

    # Create Approved Registration
    reg = create_with_status(db_session, registration_create(db_session), reg_models.Status.APPROVED)

    # Attempt Removal
    with pytest.raises(ValueError, match="Cannot remove"):
        reg_crud.registration.remove(db_session, db_obj=reg)

    # Assert still exists
    assert reg_crud.registration.get(db_session, pk=reg.id)
