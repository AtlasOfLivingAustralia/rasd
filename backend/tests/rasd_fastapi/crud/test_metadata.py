"""RASD FastAPI Metadata CRUD Unit Tests."""


# Local
from rasd_fastapi.crud import metadata as metadata_crud
from rasd_fastapi.db import session
from rasd_fastapi.models import organisations as org_models
from rasd_fastapi.schemas import metadata as metadata_schemas
from tests import conftest


def test_metadata_crud(mock_dynamodb_tables) -> None:
    """Tests the Meatadata CRUD abstraction."""
    # Create Database Session
    db_session = session.db_session()

    # Load Data
    data = conftest.load_data_json("metadata.json")
    del data["organisation_id"]  # Remove dummy `organisation_id`
    del data["custodian"]  # Remove dummy `custodian`
    org_data = conftest.load_data_json("organisation.json")

    # Create Metadata
    metadata = metadata_crud.metadata.create_with_org(
        db_session,
        obj_in=metadata_schemas.RASDMetadataCreate.parse_obj(data),
        org=org_models.Organisation.parse_obj(org_data)
    )

    # Assert
    assert conftest.matches(data, metadata)

    # Retrieve Metadata
    metadata = metadata_crud.metadata.get(  # type: ignore[assignment]
        db_session,
        pk=metadata.id,
    )

    # Assert
    assert metadata
    assert conftest.matches(data, metadata)

    # List Metadata
    page = metadata_crud.metadata.scan(
        db_session,
    )

    # Assert
    assert page.count >= 1

    # Change Metadata Abstract
    data["abstract"] = "This is a new unit test abstract"

    # Update Metadata
    metadata = metadata_crud.metadata.update(
        db_session,
        db_obj=metadata,
        obj_in=metadata_schemas.RASDMetadataUpdate.parse_obj(
            {
                "abstract": data["abstract"],
            }
        )
    )

    # Check
    assert conftest.matches(data, metadata)

    # Delete Metadata
    metadata = metadata_crud.metadata.delete(  # type: ignore[assignment]
        db_session,
        pk=metadata.id,
    )

    # Assert
    assert metadata
    assert conftest.matches(data, metadata)
