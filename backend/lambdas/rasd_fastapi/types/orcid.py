"""RASD FastAPI ORCID Custom Data Type."""


# Standard
import re

# Typing
from typing import Any, Callable, Iterator


class Orcid(str):
    """Open Researcher and Contributor ID."""

    # ORCID Regex
    # See: https://en.wikipedia.org/wiki/ORCID
    # See: https://www.wikidata.org/wiki/Property:P496
    ORCID_PATTERN = r"^(?:\d{4}-){3}\d{3}[0-9X]$"
    ORCID_REGEX = re.compile(ORCID_PATTERN)

    # ORCID Rules
    # See: https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
    ORCID_MODULUS = 11
    ORCID_REMAINDER = 12

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], "Orcid"]]:
        """Yields the validators for the Orcid.

        Yields:
            Callable[[Any], "Orcid"]: Validator functions for an ORCID.
        """
        # Yield the ORCID Local Validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        """Modifies the field schema for an ORCID string.

        Args:
            field_schema (dict[str, Any]): Field schema to modify in place.
        """
        # Mutate the Field Schema Dictionary in Place
        field_schema.update(
            pattern=cls.ORCID_PATTERN,
            examples=["0000-0002-3843-3472", "0000-0002-1825-0097", "0000-0002-9079-593X"],
        )

    @classmethod
    def validate(cls, v: Any) -> "Orcid":
        """Validates an ORCID locally.

        Args:
            v (Any): Value to be validated

        Raises:
            TypeError: Raised if the supplied value is the wrong type.
            ValueError: Raised if the supplied value is invalid.

        Returns:
            Orcid: Locally validated ORCID if applicable.
        """
        # Check that the supplied value is a string
        if not isinstance(v, str):
            raise TypeError("ORCID must be a string")

        # Match ORCID format using Regex
        if not cls.ORCID_REGEX.fullmatch(v):
            raise ValueError("ORCID is not in a valid format")

        # Validate ORCID using rules
        # See: https://support.orcid.org/hc/en-us/articles/360006897674-Structure-of-the-ORCID-Identifier
        checksum_digit = 10 if v[-1] == "X" else int(v[-1])  # Retrieve checksum (last character)
        base_digits = [int(character) for character in v.replace("-", "")[:-1]]  # Coerce remainder of ORCID to digits
        total = 0  # Initialise total to 0
        for digit in base_digits:  # Loop through the base digits
            total = (total + digit) * 2  # Add the digit to the total and double the total
        remainder = total % cls.ORCID_MODULUS  # Divide by required value, noting the remainder
        result = (cls.ORCID_REMAINDER - remainder) % cls.ORCID_MODULUS  # Determine the checksum result
        if result != checksum_digit:  # Compare the checksum
            raise ValueError("ORCID failed checksum verification")

        # Return the ORCID
        return cls(v)

    def __repr__(self) -> str:
        """Provides a representation of the validated ORCID.

        Returns:
            str: String representation of the validated ORCID.
        """
        return f"ORCID({super().__repr__()})"
