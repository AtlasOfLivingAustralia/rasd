"""RASD FastAPI ABN Service Unit Tests."""


# Third-Party
import pytest

# Local
from rasd_fastapi.services import abn


@pytest.mark.parametrize(
    (
        "value",
        "name",
        "valid",
    ),
    [
        # Valid
        ("94 119 508 824",               "TEKNO PTY LTD",              True),  # Properly formatted
        ("50110219460",                  "EXAMPLE PTY LTD",            True),  # No spaces
        ("  5   1 82 4 75      3 556  ", "AUSTRALIAN TAXATION OFFICE", True),  # Too many spaces
        # Invalid
        (12345678910,      "FAKE NAME", False),  # Wrong type
        ("abc123",         "FAKE NAME", False),  # Garbage
        ("12345678901",    "FAKE NAME", False),  # Correct length, not an ABN
        ("12 004 045 553", "FAKE NAME", False),  # Correct format, not registered
        ("31 139 963 509", "CANCELLED", False),  # Registered, cancelled
        ("94 119 508 824", "FAKE NAME", False),  # Registered, wrong entity name
    ]
)
def test_verify_abn(mock_abn_responses, value: str, name: str, valid: bool) -> None:
    """Tests the ABN field validation.

    Args:
        value (str): ABN to to test validation of.
        name (str): ABN entity name to verify against.
        valid (bool): Whether this ABN should be valid or not
    """
    # Validate
    assert (
        abn.verify_registered(value)
        and abn.verify_active(value)
        and abn.verify_name(value, name)
    ) is valid
