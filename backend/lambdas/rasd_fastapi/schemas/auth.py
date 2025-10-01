"""RASD FastAPI Users Schemas."""


# Standard
import enum
import uuid

# Third-Party
import pydantic

# Local
from rasd_fastapi.schemas import base


class Group(str, enum.Enum):
    """Group Enumeration."""
    DATA_REQUESTORS = "DataRequestors"
    DATA_CUSTODIANS = "DataCustodians"
    ADMINISTRATORS = "Administrators"


class User(base.BaseSchema):
    """Base User Schema."""
    id: uuid.UUID = pydantic.Field(alias="sub")  # noqa: A003
    given_name: str
    family_name: str
    email: pydantic.EmailStr
    organisation_id: uuid.UUID = pydantic.Field(alias="custom:organisation_id")
    groups: list[Group] = pydantic.Field(alias="cognito:groups")

    def is_requestor(self) -> bool:
        """Checks whether this user is a Data Requestor."""
        return Group.DATA_REQUESTORS in self.groups

    def is_custodian(self) -> bool:
        """Checks whether this user is a Data Custodian."""
        return Group.DATA_CUSTODIANS in self.groups

    def is_admin(self) -> bool:
        """Checks whether this user is an Administrator."""
        return Group.ADMINISTRATORS in self.groups
