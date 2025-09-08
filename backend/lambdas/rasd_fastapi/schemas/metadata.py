"""RASD FastAPI Metadata REST API Schemas."""


# Standard
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi import types
from rasd_fastapi.schemas import base
from rasd_fastapi.models import metadata_vocabs

# Typing
from typing import Optional


class RASDMetadataCreate(base.BaseSchema):
    """RASDMetadata Create Schema."""
    title: str = pydantic.Field(max_length=200)
    abstract: str = pydantic.Field(max_length=2000)
    keywords: list[metadata_vocabs.keywords.Keyword]
    temporal_coverage_from: types.date.ISO8601Date
    temporal_coverage_to: types.date.ISO8601Date
    north_bounding_coordinate: int = pydantic.Field(ge=-90, le=90)
    south_bounding_coordinate: int = pydantic.Field(ge=-90, le=90)
    east_bounding_coordinate: int = pydantic.Field(ge=-180, le=180)
    west_bounding_coordinate: int = pydantic.Field(ge=-180, le=180)
    locations: list[metadata_vocabs.locations.Location]
    taxa_covered: str = pydantic.Field(max_length=200)
    collection_methods: list[metadata_vocabs.collection_methods.CollectionMethod]
    data_source_url: Optional[pydantic.HttpUrl]
    data_source_doi: Optional[types.doi.DOI]
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


class RASDMetadataUpdate(base.BaseSchema):
    """RASDMetadata Update Schema."""
    title: Optional[str] = pydantic.Field(max_length=200)
    abstract: str = pydantic.Field(max_length=2000)
    keywords: Optional[list[metadata_vocabs.keywords.Keyword]]
    temporal_coverage_from: Optional[types.date.ISO8601Date]
    temporal_coverage_to: Optional[types.date.ISO8601Date]
    north_bounding_coordinate: Optional[int] = pydantic.Field(ge=-90, le=90)
    south_bounding_coordinate: Optional[int] = pydantic.Field(ge=-90, le=90)
    east_bounding_coordinate: Optional[int] = pydantic.Field(ge=-180, le=180)
    west_bounding_coordinate: Optional[int] = pydantic.Field(ge=-180, le=180)
    locations: Optional[list[metadata_vocabs.locations.Location]]
    taxa_covered: Optional[str] = pydantic.Field(max_length=200)
    collection_methods: Optional[list[metadata_vocabs.collection_methods.CollectionMethod]]
    data_source_url: Optional[pydantic.HttpUrl]
    data_source_doi: Optional[types.doi.DOI]
    embargoed: Optional[bool]
    embargo_release_date: Optional[Optional[types.date.ISO8601Date]]
    contact_organisation: Optional[str] = pydantic.Field(max_length=200)
    contact_position: Optional[str] = pydantic.Field(max_length=200)
    contact_email: Optional[pydantic.EmailStr]
    stored_format: Optional[metadata_vocabs.formats.Format]
    available_formats: Optional[list[metadata_vocabs.formats.Format]]
    access_rights: Optional[metadata_vocabs.access_rights.AccessRights]
    use_restrictions: Optional[str] = pydantic.Field(max_length=500)
    security_classification: Optional[metadata_vocabs.security_classifications.SecurityClassification]
    generalisations: Optional[str] = pydantic.Field(max_length=500)


class RASDMetadataSummary(base.BaseSchema):
    """RASDMetadata Summary Schema."""
    active: bool
    id: uuid.UUID  # noqa: A003
    title: str
    title_lower: Optional[str]
    abstract: str = pydantic.Field(max_length=2000)
    abstract_lower: Optional[str] = pydantic.Field(max_length=2000)
    keywords: list[metadata_vocabs.keywords.Keyword]
    locations: list[metadata_vocabs.locations.Location]
    organisation_id: uuid.UUID
    custodian: str
