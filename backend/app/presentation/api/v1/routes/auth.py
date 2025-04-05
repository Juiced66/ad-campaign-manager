import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr 

from app.application.schemas.token import Token as TokenResponseSchema, RefreshTokenRequest
from app.application.use_cases.auth.services import ( 
    AuthService,
    AuthenticationError,
    AuthorizationError,
)

from app.presentation.api.v1.dependencies.auth import get_auth_service

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=TokenResponseSchema)
def login(
    credentials: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = auth_service.login_user(
            email=credentials.email, password=credentials.password
        )
        return tokens
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except AuthorizationError as e:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected login error for {credentials.email}: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during login.")

@router.post("/refresh", response_model=TokenResponseSchema)
def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service) # Inject service
):
    try:
        new_tokens = auth_service.refresh_access_token(
            refresh_token_value=request.refresh_token
        )
        return new_tokens
    except AuthenticationError as e:
         raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer error=\"invalid_token\""},
        )
    except Exception as e:
        logger.error(f"Unexpected token refresh error: {e}", exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during token refresh.")


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        auth_service.logout_user(refresh_token_value=request.refresh_token)
    except Exception as e:
         logger.error(f"Unexpected logout error: {e}", exc_info=True)
         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during logout.")
