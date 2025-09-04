"""RASD FastAPI ISO8601 DOI Custom Data Type."""


# Standard
import re

# Typing
from typing import Any, Callable, Iterator


class DOI(str):
    r"""Data Object Identifier.

    Source 1: https://www.doi.org/the-identifier/resources/handbook/2_numbering
        The DOI name is case-insensitive, and can incorporate any printable
        characters from the legal graphic characters of Unicode. A DOI name
        consists of a DOI prefix and a DOI suffix separated by a forward slash.
        There is no defined limit on the length of the DOI name, or of the DOI
        prefix or DOI suffix. The prefix consists of the number 10, a dot ".",
        and the registrant code.

    Source 2: https://support.datacite.org/docs/doi-basics
        The registrant code is currently always numeric, and can be subdivided
        with additional dots ".". The suffix for a DOI can be (almost) any
        string.

    Source 3: https://en.wikipedia.org/wiki/Digital_object_identifier
        Example DOIs:
        - 10.1000/182
        - 10.1000.10/182
        - 10.1002/(sici)1099-1409(199908/10)3:6/7<672::aid-jpp192>3.0.co;2-8

    This validator is only intended to confirm that the string being entered
    into the data source field is similar to the expected pattern for a DOI.
    The variability in naming options makes strict checking impractical and
    likely to exclude false negatives.

    Regex option 1: \b(10[.][0-9])
        Very simplistic. Checks for the mandatory '10', followed by a '.',
        followed by a single digit number. This method should be valid as long
        as the first character of the registrant code is numeric.

    Regex option 2: \b10\.(\d+\.*)+[\ /]
        More specific than option 1. Checks for the mandatory '10', followed by
        a '.', followed by any length of registrant code with any amount of
        subdivision, followed by a '/'. This method should be valid as long as
        all parts of the DOI prefix (10.Registrant_Code+Optional_Subdivisions)
        are all numeric.
    """

    # Constants
    # See docstring for additional info.
    DOI_REGEX = re.compile(r"\b10\.(\d+\.*)+[\ /]")

    @classmethod
    def __get_validators__(cls) -> Iterator[Callable[[Any], "DOI"]]:
        """Yields the validators for the DOI.

        Yields:
            Callable[[Any], "DOI"]: Validator functions for a DOI.
        """
        # Yield the DOI Format Validator
        yield cls.validate_format

    @classmethod
    def validate_format(cls, v: Any) -> "DOI":
        """Validates a DOI.

        Args:
            v (Any): Value to be validated

        Raises:
            TypeError: Raised if the supplied value is the wrong type.
            ValueError: Raised if the supplied value is invalid.

        Returns:
            DOI: Validated DOI if applicable.
        """
        # Check if value is already a `DOI`
        if isinstance(v, cls):
            return v

        # Check that the supplied value is a string
        if not isinstance(v, str):
            raise TypeError("DOI must be parsed from string")

        # Validate DOI
        if not cls.DOI_REGEX.match(v):
            raise ValueError("Invalid DOI format")

        # Return DOI
        return cls(v)

    def __repr__(self) -> str:
        """Provides a representation of the validated DOI.

        Returns:
            str: String representation of the validated DOI.
        """
        return f"DOI({super().__repr__()})"
