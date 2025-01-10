"""RASD FastAPI Settings."""


# Third-Party
import pydantic

# Typing
from typing import Optional


class Settings(pydantic.BaseSettings):
    """Settings for the RASD Backend."""
    # Application Settings
    TITLE: str = "RASD Backend"
    VERSION: str = "v1.0.0"
    API_PREFIX: str = "/api/v1"

    # CORS Settings
    ALLOW_ORIGINS: list[str] = ["*"]

    # AWS Settings
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_SESSION_TOKEN: Optional[str] = None
    AWS_DEFAULT_REGION: str = "ap-southeast-2"

    # AWS DynamoDB Settings
    AWS_DYNAMODB_TABLE_METADATA: str = "Metadata"
    AWS_DYNAMODB_TABLE_ORGANISATIONS: str = "Organisations"
    AWS_DYNAMODB_TABLE_REGISTRATIONS: str = "Registrations"
    AWS_DYNAMODB_TABLE_ACCESS_REQUESTS: str = "DataAccessRequests"

    # AWS Cognito Settings
    AWS_COGNITO_POOL_ID: str
    AWS_COGNITO_CLIENT_ID: str
    AWS_COGNITO_CLIENT_SECRET_KEY: str

    # AWS SES Settings
    EMAIL_FROM_NAME: str = "RASD"
    EMAIL_FROM_ADDRESS: str = "noreply@mail.develop.gaiadev.net.au"
    EMAIL_ADMIN_INBOX: str = "rasd-admins-develop@gaiaresources.com.au"

    # ABN Validation Settings
    ABN_LOOKUP_URL: str = "https://abr.business.gov.au/json/AbnDetails.aspx"
    ABN_LOOKUP_GUID: str

    # Email Content Settings
    RASD_URL: str = "https://www.rasd.org.au"
    RASD_CREATE_PASSWORD_URL: str = "https://www.rasd.org.au/#/create-password"
    RASD_FRAMEWORK_URL: str = "https://www.rasd.org.au/framework"
    RASD_SUPPORT_EMAIL: str = "info@rasd.org.au"


# Instantiate Settings
SETTINGS = Settings(_env_file=".env")  # type: ignore[call-arg]
