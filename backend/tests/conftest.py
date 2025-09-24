"""RASD Unit Tests Configuration and Utilities."""


# Standard
import json
import pathlib
import os
from unittest.mock import Mock, patch

# Third-Party
import fastapi.encoders
import pydantic
import pytest
import boto3
from moto import mock_dynamodb

# Typing
from typing import Dict, Any, Union


# Set environment variables before any imports
os.environ.update({
    "AWS_ACCESS_KEY_ID": "test-key",
    "AWS_SECRET_ACCESS_KEY": "test-secret",
    "AWS_DEFAULT_REGION": "ap-southeast-2",
    "AWS_COGNITO_POOL_ID": "test-pool",
    "AWS_COGNITO_CLIENT_ID": "test-client",
    "ABN_LOOKUP_GUID": "test-guid-123"
})

# Mock boto3 client at module level to prevent AWS calls during settings import
with patch("boto3.client") as mock_client:
    mock_sm = Mock()
    mock_sm.get_secret_value.side_effect = Exception("No secrets in test")
    mock_client.return_value = mock_sm

# Mock the dynamic cognito client secret function for tests
with patch("rasd_fastapi.auth.cognito.get_cognito_client_secret") as mock_get_secret:
    mock_get_secret.return_value = "test-secret"


# Shortcuts
DictOrModel = Union[dict[str, Any], pydantic.BaseModel]

# Constants
TEST_DATA_DIRECTORY = pathlib.Path(__file__).parent / "data"


def load_data_json(name: str) -> Dict[str, Any]:
    """Loads unit test data as a `.json`.

    Args:
        name (str): Name of the unit test data to load.

    Returns:
        Dict[str, Any]: `.json` dictionary of the loaded data.
    """
    # Load, Parse and Return
    return json.loads((TEST_DATA_DIRECTORY / name).read_bytes())  # type: ignore[no-any-return]


def matches(a: DictOrModel, b: DictOrModel) -> bool:
    """Checks whether one dict or model is a subset of another dict or model.

    This utility function allows for easier assertions in unit tests.

    Args:
        a (DictOrModel): Child to be checked.
        b (DictOrModel): Parent to be checked.

    Returns:
        bool: Whether dict/model `a` is a subset of dict/model `b`.
    """
    # Encode to Dictionaries and Retrieve Items
    a_items = a.items() if isinstance(a, dict) else fastapi.encoders.jsonable_encoder(a).items()
    b_items = b.items() if isinstance(b, dict) else fastapi.encoders.jsonable_encoder(b).items()

    # Check and Return
    return all(x in b_items for x in a_items)


@pytest.fixture
def mock_dynamodb_tables():
    """Create mock DynamoDB tables for testing."""
    with mock_dynamodb():
        # Create DynamoDB resource
        dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")
        
        # Create test tables
        tables = [
            "Metadata",
            "Organisations", 
            "Registrations",
            "DataAccessRequests"
        ]
        
        for table_name in tables:
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
                AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
                BillingMode="PAY_PER_REQUEST"
            )
        
        yield dynamodb


@pytest.fixture
def mock_abn_responses():
    """Mock ABN lookup service responses."""
    responses = {
        "94119508824": {
            "Abn": "94119508824",
            "AbnStatus": "Active",
            "AbnStatusEffectiveFrom": "2000-01-01",
            "Acn": "119508824",
            "AddressPostcode": "6000",
            "AddressState": "WA",
            "BusinessName": [],
            "EntityName": "TEKNO PTY LTD",
            "EntityTypeCode": "PRV",
            "EntityTypeName": "Australian Private Company",
            "Message": ""
        },
        "50110219460": {
            "Abn": "50110219460",
            "AbnStatus": "Active",
            "AbnStatusEffectiveFrom": "2000-01-01",
            "Acn": "110219460",
            "AddressPostcode": "2000",
            "AddressState": "NSW",
            "BusinessName": [],
            "EntityName": "EXAMPLE PTY LTD",
            "EntityTypeCode": "PRV",
            "EntityTypeName": "Australian Private Company",
            "Message": ""
        },
        "51824753556": {
            "Abn": "51824753556",
            "AbnStatus": "Active",
            "AbnStatusEffectiveFrom": "2000-01-01",
            "Acn": "824753556",
            "AddressPostcode": "2600",
            "AddressState": "ACT",
            "BusinessName": [],
            "EntityName": "AUSTRALIAN TAXATION OFFICE",
            "EntityTypeCode": "GOV",
            "EntityTypeName": "Government Entity",
            "Message": ""
        },
        "62276640408": {
            "Abn": "62276640408",
            "AbnStatus": "Active",
            "AbnStatusEffectiveFrom": "2000-01-01",
            "Acn": "276640408",
            "AddressPostcode": "6000",
            "AddressState": "WA",
            "BusinessName": [],
            "EntityName": "AQUINO, TANYA NICOLE",
            "EntityTypeCode": "IND",
            "EntityTypeName": "Individual/Sole Trader",
            "Message": ""
        }
    }
    
    def mock_get(url, **kwargs):
        # Extract ABN from params
        params = kwargs.get('params', {})
        abn_param = params.get('abn', '')
        
        # Clean ABN (remove spaces and convert to string)
        abn = str(abn_param).replace(" ", "").replace("+", "")
        
        response_data = responses.get(abn, {
            "Abn": "",
            "AbnStatus": "Cancelled",
            "AbnStatusEffectiveFrom": "2000-01-01",
            "Acn": "",
            "AddressPostcode": "",
            "AddressState": "",
            "BusinessName": [],
            "EntityName": "",
            "EntityTypeCode": "",
            "EntityTypeName": "",
            "Message": "ABN not found"
        })
        
        mock_response = Mock()
        mock_response.text = f"rasd({json.dumps(response_data)})"
        mock_response.status_code = 200
        return mock_response
    
    with patch("httpx.get", side_effect=mock_get):
        yield
