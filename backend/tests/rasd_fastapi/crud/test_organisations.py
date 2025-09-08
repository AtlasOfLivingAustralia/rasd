"""RASD FastAPI Organisations CRUD Unit Tests."""


# Local
from rasd_fastapi.crud import organisations as org_crud
from rasd_fastapi.db import session
from rasd_fastapi.schemas import organisations as org_schemas
from tests import conftest


def test_organisations_crud(mock_dynamodb_tables, mock_abn_responses) -> None:
    """Tests the Organisation CRUD abstraction."""
    # Create Database Session
    db_session = session.db_session()

    # Load Data
    data = conftest.load_data_json("organisation.json")

    # Create Organisation
    org = org_crud.organisation.create_unique(
        db_session,
        obj_in=org_schemas.OrganisationCreate.parse_obj(data)
    )

    # Assert
    assert conftest.matches(data, org)

    # Retrieve Organisation
    org = org_crud.organisation.get(  # type: ignore[assignment]
        db_session,
        pk=org.id,
    )

    # Assert
    assert org
    assert conftest.matches(data, org)

    # List Organisations
    page = org_crud.organisation.scan(
        db_session,
    )

    # Assert
    assert page.count >= 1

    # Change Organisation Email
    data["email"] = "test2@example.com"

    # Update Organisation
    org = org_crud.organisation.update(
        db_session,
        db_obj=org,
        obj_in=org_schemas.OrganisationUpdate.parse_obj(
            {
                "email": data["email"],
            }
        )
    )

    # Check
    assert conftest.matches(data, org)

    # Delete Organisation
    org = org_crud.organisation.delete(  # type: ignore[assignment]
        db_session,
        pk=org.id,
    )

    # Assert
    assert org
    assert conftest.matches(data, org)
