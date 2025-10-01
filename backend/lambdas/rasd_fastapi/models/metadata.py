"""RASD FastAPI Metadata Data Model."""


# Standard
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi.models import base
from rasd_fastapi.models import metadata_vocabs

# Typing
from typing import Any, Optional


class RASDMetadata(base.BaseModel):
    """RASDMetadata Model."""
    id: uuid.UUID = pydantic.Field(default_factory=uuid.uuid4)  # noqa: A003
    title: str = pydantic.Field(max_length=200)
    abstract: str = pydantic.Field(max_length=2000)
    keywords: list[metadata_vocabs.keywords.Keyword]
    locations: list[metadata_vocabs.locations.Location]
    organisation_id: uuid.UUID
    custodian: str = pydantic.Field(max_length=200)
    temporal_coverage_from: types.date.ISO8601Date
    temporal_coverage_to: types.date.ISO8601Date
    north_bounding_coordinate: int = pydantic.Field(ge=-90, le=90)
    south_bounding_coordinate: int = pydantic.Field(ge=-90, le=90)
    east_bounding_coordinate: int = pydantic.Field(ge=-180, le=180)
    west_bounding_coordinate: int = pydantic.Field(ge=-180, le=180)
    taxa_covered: str = pydantic.Field(max_length=200)
    collection_methods: list[metadata_vocabs.collection_methods.CollectionMethod]
    data_source_doi: Optional[types.doi.DOI]
    data_source_url: Optional[pydantic.HttpUrl]
    embargoed: bool
    embargo_release_date: Optional[types.date.ISO8601Date]
    contact_organisation: str = pydantic.Field(max_length=200)
    contact_position: str = pydantic.Field(max_length=200)
    contact_email: pydantic.EmailStr
    stored_format: metadata_vocabs.formats.Format
    available_formats: Optional[list[metadata_vocabs.formats.Format]]
    access_rights: metadata_vocabs.access_rights.AccessRights
    use_restrictions: str = pydantic.Field(max_length=500)
    security_classification: metadata_vocabs.security_classifications.SecurityClassification
    generalisations: str = pydantic.Field(max_length=500)

    # Database only computed fields
    title_lower: Optional[str] = pydantic.Field(max_length=200)  # database only field for searching
    abstract_lower: Optional[str] = pydantic.Field(max_length=2000)  # database only field for searching

    @pydantic.root_validator
    def validate_data_sources(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Validates the `data_source` fields.

        This validator ensures that *at least one* of `data_source_url` or
        `data_source_doi` is provided.

        Args:
            values (dict[str, Any]): Pre-validated values for the model.

        Returns:
            dict[str, Any]: Validated values for the model.
        """
        # Check `data_source_url` and `data_source_doi` values
        if not values.get("data_source_url") and not values.get("data_source_doi"):
            # Error
            raise ValueError("At least one of `data_source_url` or `data_source_doi` is required")

        # Return validated values
        return values

    @pydantic.validator("title_lower", always=True)
    def set_title_lower(cls, v: Optional[str], values: dict[str, Any]) -> Optional[str]:
        """Sets the computed `title_lower` field.

        This validator forces the `title_lower` field to *always* be the
        lowercase form of the `title` field. This lets us store it in the
        database for searching.

        Args:
            v (Optional[str]): Supplied value, should be `None` (not used).
            values (dict[str, Any]): Values of the previously validated fields.

        Returns:
            Optional[str]: The title as lowercase.
        """
        # Retrieve Title, Transform to Lower Case, Return
        # `title` will not be in `values` if it fails validation
        title = values.get("title")
        title = title.lower() if isinstance(title, str) else title
        return title

    @pydantic.validator("abstract_lower", always=True)
    def set_abstract_lower(cls, v: Optional[str], values: dict[str, Any]) -> Optional[str]:
        """Sets the computed `abstract_lower` field.

        This validator forces the `abstract_lower` field to *always* be the
        lowercase form of the `abstract` field. This lets us store it in the
        database for searching.

        Args:
            v (Optional[str]): Supplied value, should be `None` (not used).
            values (dict[str, Any]): Values of the previously validated fields.

        Returns:
            Optional[str]: The abstract as lowercase.
        """
        # Retrieve Abstract, Transform to Lower Case, Return
        # `abstract` will not be in `values` if it fails validation
        abstract = values.get("abstract")
        abstract = abstract.lower() if isinstance(abstract, str) else abstract
        return abstract
