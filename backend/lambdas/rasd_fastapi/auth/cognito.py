"""RASD FastAPI Cognito Functionality."""


# Standard
import base64
import hashlib
import hmac
import secrets
import string
import uuid

# Third-Party
import boto3
import pydantic

# Local
from rasd_fastapi.core import settings
from rasd_fastapi.schemas import auth as auth_schemas

# Typing
from typing import TYPE_CHECKING

# Type-Checking
if TYPE_CHECKING:
    from mypy_boto3_cognito_idp.client import CognitoIdentityProviderClient
    from mypy_boto3_cognito_idp.type_defs import AuthenticationResultTypeTypeDef


def login(
    username: pydantic.EmailStr,
    password: pydantic.SecretStr,
) -> "AuthenticationResultTypeTypeDef":
    """Performs the 'login' authentication flow.

    Args:
        username (pydantic.EmailStr): Username to login with.
        password (pydantic.SecretStr): Password to login with.

    Returns:
        AuthenticationResultTypeTypeDef: AWS Cognito IDP authentication result.
    """
    # Get Client
    client = cognito_client()

    # Perform Login
    response = client.admin_initiate_auth(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        AuthFlow="ADMIN_USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": password.get_secret_value(),
            "SECRET_HASH": secret_hash(username),
        },
    )

    # Check for Challenge
    if challenge := response.get("ChallengeName"):
        # Error
        raise ValueError(f"Unable to authenticate: {challenge}")

    # Return Authentication Result
    return response["AuthenticationResult"]


def register(
    username: pydantic.EmailStr,
    given_name: str,
    family_name: str,
    organisation_id: uuid.UUID,
    group: auth_schemas.Group,
) -> pydantic.SecretStr:
    """Performs the 'registration' authentication flow.

    Args:
        username (pydantic.EmailStr): Username to register with.
        given_name (str): Given name to register with.
        family_name (str): Family name to register with.
        organisation_id (uuid.UUID): Organisation ID to register with.
        group (auth_schemas.Group): Group to register with.

    Returns:
        pydantic.SecretStr: Temporary password generated for the user.
    """
    # Get Client
    client = cognito_client()

    # Generate Temporary Password
    password = temporary_password()

    # Perform Registration
    client.admin_create_user(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        Username=username,
        TemporaryPassword=password.get_secret_value(),
        UserAttributes=[
            {"Name": "given_name", "Value": given_name},
            {"Name": "family_name", "Value": family_name},
            {"Name": "custom:organisation_id", "Value": str(organisation_id)},
        ],
        MessageAction="SUPPRESS",  # Don't send in-built emails!
    )

    # Add to Group
    client.admin_add_user_to_group(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        Username=username,
        GroupName=group,
    )

    # Return
    return password


def set_password(
    username: pydantic.EmailStr,
    temp_password: pydantic.SecretStr,
    new_password: pydantic.SecretStr,
) -> None:
    """Performs the 'set initial password' authentication flow.

    Args:
        username (pydantic.EmailStr): Username to set password for.
        temp_password (pydantic.SecretStr): Temporary password to be changed.
        new_password (pydantic.SecretStr): New password to change to.
    """
    # Get Client
    client = cognito_client()

    # Perform Login
    # We need the AWS Challenge to set the user's password
    response = client.admin_initiate_auth(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        AuthFlow="ADMIN_USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": temp_password.get_secret_value(),
            "SECRET_HASH": secret_hash(username),
        },
    )

    # Get Challenge
    if response.get("ChallengeName") != "NEW_PASSWORD_REQUIRED":
        # Error
        raise ValueError("User's password has already been set")

    # Response to Challenge
    client.admin_respond_to_auth_challenge(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        ChallengeName=response["ChallengeName"],
        ChallengeResponses={
            "NEW_PASSWORD":  new_password.get_secret_value(),
            "USERNAME": username,
            "SECRET_HASH": secret_hash(username),
        },
        Session=response["Session"],
    )

    # Verify Email Address
    # This must be done manually as we confirm the users manually
    # If the user has reached this point then their email must be valid
    client.admin_update_user_attributes(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        Username=username,
        UserAttributes=[
            {"Name": "email_verified", "Value": "true"},
        ]
    )


def change_password(
    username: pydantic.EmailStr,
    old_password: pydantic.SecretStr,
    new_password: pydantic.SecretStr,
) -> None:
    """Performs the 'change password' authentication flow.

    Args:
        username (pydantic.EmailStr): Username to change password for.
        old_password (pydantic.SecretStr): Old password to be changed.
        new_password (pydantic.SecretStr): New password to change to.
    """
    # Get Client
    client = cognito_client()

    # Perform Login
    # We need the JWT `Access Token` to change the user's password
    response = client.admin_initiate_auth(
        UserPoolId=settings.SETTINGS.AWS_COGNITO_POOL_ID,
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        AuthFlow="ADMIN_USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": username,
            "PASSWORD": old_password.get_secret_value(),
            "SECRET_HASH": secret_hash(username),
        },
    )

    # Check for Challenge
    if challenge := response.get("ChallengeName"):
        # Error
        raise ValueError(f"Unable to authenticate: {challenge}")

    # Retrieve Access Token
    access_token = response["AuthenticationResult"]["AccessToken"]

    # Perform Password Change
    client.change_password(
        PreviousPassword=old_password.get_secret_value(),
        ProposedPassword=new_password.get_secret_value(),
        AccessToken=access_token,
    )


def forgot_password(
    username: pydantic.EmailStr,
) -> None:
    """Performs the 'forgot password' authentication flow.

    Args:
        username (pydantic.EmailStr): Username that has forgotten password.
    """
    # Get Client
    client = cognito_client()

    # Perform Forgot Password
    client.forgot_password(
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        Username=username,
        SecretHash=secret_hash(username),
    )


def forgot_password_confirm(
    username: pydantic.EmailStr,
    password: pydantic.SecretStr,
    code: pydantic.SecretStr,
) -> None:
    """Performs the 'forgot password confirmation' authentication flow.

    Args:
        username (pydantic.EmailStr): Username to confirm forgotten password.
        password (pydantic.SecretStr): Password to be set for user.
        code (pydantic.SecretStr): Confirmation code for forgotten password.
    """
    # Get Client
    client = cognito_client()

    # Perform Forgot Password Confirmation
    client.confirm_forgot_password(
        ClientId=settings.SETTINGS.AWS_COGNITO_CLIENT_ID,
        Username=username,
        ConfirmationCode=code.get_secret_value(),
        Password=password.get_secret_value(),
        SecretHash=secret_hash(username)
    )


def cognito_client() -> "CognitoIdentityProviderClient":
    """Constructs a configured and authenticated Cognito client.

    Returns:
        CognitoIdentityProviderClient: Configured and authenticated client.
    """
    # Instantiate and Return AWS Client
    return boto3.client(
        "cognito-idp",
        region_name=settings.SETTINGS.AWS_DEFAULT_REGION,
        aws_access_key_id=settings.SETTINGS.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.SETTINGS.AWS_SECRET_ACCESS_KEY,
        aws_session_token=settings.SETTINGS.AWS_SESSION_TOKEN,
    )


def temporary_password() -> pydantic.SecretStr:
    """Generates a secure temporary password.

    The generated password is cryptographically secure, is 16 characters long
    and contains at least 1 symbol, 1 lowercase character, 1 uppercase
    character and 1 digit.

    Returns:
        pydantic.SecretStr: Securely generated temporary password.
    """
    # Define alphabet
    alphabet = string.ascii_letters + string.digits + string.punctuation

    # Loop until we generate a password with the required characteristics
    # See: https://docs.python.org/3/library/secrets.html#recipes-and-best-practices
    while True:
        # Generate 16 character password
        password = "".join(secrets.choice(alphabet) for _ in range(16))

        # Check characteristics of password
        if (
            sum(c in string.punctuation for c in password) >= 1  # At least 1 symbol
            and sum(c.islower() for c in password) >= 1  # At least 1 lowercase character
            and sum(c.isupper() for c in password) >= 1  # At least 1 uppercase character
            and sum(c.isdigit() for c in password) >= 1  # At least 1 digit
        ):
            # Return Password
            return pydantic.SecretStr(password)


def secret_hash(username: pydantic.EmailStr) -> str:
    """Generates an AWS Cognito secret hash with the supplied username.

    Args:
        username (pydantic.EmailStr): Username to generate secret hash with.

    Returns:
        str: Generated secret hash.
    """
    # Calculate and Return Secret Hash
    return base64.b64encode(
         s=hmac.new(
            key=settings.SETTINGS.AWS_COGNITO_CLIENT_SECRET_KEY.encode(),
            msg=(username + settings.SETTINGS.AWS_COGNITO_CLIENT_ID).encode(),
            digestmod=hashlib.sha256,
        ).digest()
    ).decode()
