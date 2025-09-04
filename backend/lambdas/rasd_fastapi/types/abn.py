"""RASD FastAPI ABN Custom Data Type."""


# Standard
import re

# Typing
from typing import Any, Callable, ClassVar, Iterator


class Abn(str):
    """Australian Business Number."""

    # ABN Regex
    # See: https://stackoverflow.com/questions/14174738/regex-to-match-australian-business-number-abn
    ABN_PATTERN = r"^[1-9]{1}\d{1}\s?\d{3}\s?\d{3}\s?\d{3}$"
    ABN_REGEX = re.compile(ABN_PATTERN)
    WHITESPACE_REGEX = re.compile(r"\s+", flags=re.UNICODE)

    # ABN Rules
    # See: https://abr.business.gov.au/Help/AbnFormat
    ABN_FIRST_DIGIT_SUBTRACTION = 1
    ABN_WEIGHTINGS: ClassVar[list[int]] = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    ABN_MODULUS = 89
    ABN_REMAINDER = 0

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], "Abn"]]:
        """Yields the validators for the Abn.

        Yields:
            Callable[[Any], "Abn"]: Validator functions for an ABN.
        """
        # Yield the ABN Local Validator
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: dict[str, Any]) -> None:
        """Modifies the field schema for an ABN string.

        Args:
            field_schema (dict[str, Any]): Field schema to modify in place.
        """
        # Mutate the Field Schema Dictionary in Place
        field_schema.update(
            pattern=cls.ABN_PATTERN,
            examples=["94 119 508 824", "50 110 219 460", "51 824 753 556"],
        )

    @classmethod
    def validate(cls, v: Any) -> "Abn":
        """Validates an ABN locally.

        Args:
            v (Any): Value to be validated

        Raises:
            TypeError: Raised if the supplied value is the wrong type.
            ValueError: Raised if the supplied value is invalid.

        Returns:
            Abn: Locally validated ABN if applicable.
        """
        # Check that the supplied value is a string
        if not isinstance(v, str):
            raise TypeError("ABN must be a string")

        # Strip whitespace from ABN using Regex
        v = cls.WHITESPACE_REGEX.sub("", v)

        # Match ABN format using Regex
        if not cls.ABN_REGEX.fullmatch(v):
            raise ValueError("ABN is not in a valid format")

        # Validate ABN using rules
        # See: https://abr.business.gov.au/Help/AbnFormat
        digits = [int(character) for character in v]  # Coerce ABN to list of digits
        digits[0] -= cls.ABN_FIRST_DIGIT_SUBTRACTION  # Substract required value from the left most digit
        digits = [d * w for (d, w) in zip(digits, cls.ABN_WEIGHTINGS, strict=False)]  # Multiply by required weightings
        total = sum(digits)  # Sum the digits
        remainder = total % cls.ABN_MODULUS  # Divide by required value, noting the remainder
        if remainder != cls.ABN_REMAINDER:  # Ensure remainder is expected
            raise ValueError("ABN failed check digit verification")

        # Return the ABN
        return cls(v)

    def __repr__(self) -> str:
        """Provides a representation of the validated ABN.

        Returns:
            str: String representation of the validated ABN.
        """
        return f"ABN({super().__repr__()})"
