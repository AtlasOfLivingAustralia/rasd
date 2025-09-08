"""RASD FastAPI Auth REST API Endpoints."""


# Third-Party
import fastapi
import pydantic

# Local
from rasd_fastapi.auth import cognito
from rasd_fastapi.core import security
from rasd_fastapi.schemas import auth


# Router
router = fastapi.APIRouter()


@router.get(r"/whoami", response_model=auth.User, response_model_by_alias=False)
async def whoami(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
) -> auth.User:
    """Current user check endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.

    Returns:
        users.User: The current logged in user.
    """
    # Return Current Logged in User
    return user


@router.post(r"/login")
async def login(
    *,
    username: pydantic.EmailStr = fastapi.Form(),  # noqa: B008
    password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
) -> fastapi.responses.JSONResponse:
    """Login endpoint for REST API.

    Args:
        username (pydantic.EmailStr): Username to login with.
        password (pydantic.SecretStr): Password to login with.

    Returns:
        fastapi.responses.JSONResponse: Authentication response.
    """
    # Handle Login Errors
    try:
        # Login
        response = cognito.login(username, password)

    except Exception as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

    # Return
    return fastapi.responses.JSONResponse(response)


@router.post(r"/password/set")
async def set_password(
    *,
    username: pydantic.EmailStr = fastapi.Form(),  # noqa: B008
    temp_password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
    new_password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
) -> fastapi.Response:
    """Set initial password endpoint for REST API.

    Args:
        username (pydantic.EmailStr): Username to set password for.
        temp_password (pydantic.SecretStr): Temporary password to be changed.
        new_password (pydantic.SecretStr): New password to change to.

    Returns:
        fastapi.Response: Authentication response.
    """
    # Handle Auth Errors
    try:
        # Login
        cognito.set_password(username, temp_password, new_password)

    except Exception as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.post(r"/password/change")
async def change_password(
    *,
    user: auth.User = fastapi.Depends(security.require_user),  # noqa: B008
    old_password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
    new_password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
) -> fastapi.Response:
    """Change password endpoint for REST API.

    Args:
        user (auth.User): Currently logged in user via dependency injection.
        old_password (pydantic.SecretStr): Old password to be changed.
        new_password (pydantic.SecretStr): New password to change to.

    Returns:
        fastapi.Response: Authentication response.
    """
    # Handle Login Errors
    try:
        # Login
        cognito.change_password(user.email, old_password, new_password)

    except Exception as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.post(r"/password/forgot")
async def forgot_password(
    *,
    username: pydantic.EmailStr = fastapi.Form(),  # noqa: B008
) -> fastapi.Response:
    """Forgot password endpoint for REST API.

    Args:
        username (pydantic.EmailStr): Username to initiate forgotten password.

    Returns:
        fastapi.Response: Authentication response.
    """
    # Handle Login Errors
    try:
        # Login
        cognito.forgot_password(username)

    except Exception as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.get(r"/user-status/{username}")
async def check_user_status(
    *,
    user: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    username: str,
) -> dict:
    """Check if user needs temporary password resend (Admin only).

    Args:
        user (auth.User): Currently logged in admin user via dependency injection.
        username (str): Username to check.

    Returns:
        dict: User status information.
    """
    try:
        needs_temp_password = cognito.check_user_needs_temp_password(username)
        return {"needsTempPassword": needs_temp_password}
    except Exception as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@router.post(r"/password/resend-temp")
async def resend_temporary_password(
    *,
    user: auth.User = fastapi.Depends(security.require_admin),  # noqa: B008
    username: pydantic.EmailStr = fastapi.Form(),  # noqa: B008
) -> fastapi.Response:
    """Resend temporary password endpoint for REST API (Admin only).

    Args:
        user (auth.User): Currently logged in admin user via dependency injection.
        username (pydantic.EmailStr): Username to resend temporary password for.

    Returns:
        fastapi.Response: Authentication response.
    """
    try:
        cognito.resend_temporary_password(username)
    except Exception as exc:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)


@router.post(r"/password/forgot/confirm")
async def forgot_password_confirm(
    *,
    username: pydantic.EmailStr = fastapi.Form(),  # noqa: B008
    password: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
    code: pydantic.SecretStr = fastapi.Form(),  # noqa: B008
) -> fastapi.Response:
    """Forgot password confirmation endpoint for REST API.

    Args:
        username (pydantic.EmailStr): Username to confirm forgotten password.
        password (pydantic.SecretStr): New password to login with.
        code (pydantic.SecretStr): Confirmation code for forgotten password.

    Returns:
        fastapi.Response: Authentication response.
    """
    # Handle Login Errors
    try:
        # Login
        cognito.forgot_password_confirm(username, password, code)

    except Exception as exc:
        # Error
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    # Return
    return fastapi.Response(status_code=fastapi.status.HTTP_204_NO_CONTENT)
