import logging
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from app.application.schemas.token import Token
from app.application.use_cases.user import services as user_service
from app.core.config import settings
from app.core.security import TokenError, create_access_token, verify_password
from app.domain.interfaces.token_repository import ITokenRepository
from app.domain.entities.user import User as DomainUser
from app.infrastructure.database.sql_alchemy.session import get_db
from app.presentation.api.v1.dependencies.auth import get_current_user
from app.presentation.api.v1.dependencies.repositories import (
    get_token_repository,
    get_user_repository,
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenRequest(BaseModel):
    token: str


@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    user_repo = get_user_repository(db)
    token_repo = get_token_repository(db)

    user: DomainUser | None = user_service.get_user_by_email(
        user_repo, credentials.email
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    is_valid_password = verify_password(credentials.password, user.hashed_password)

    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        access_token = create_access_token(
            {"sub": user.email}, expires_delta=access_token_expires
        )
    except TokenError as e:
        logger.error(f"Token creation failed: {e}")
        raise HTTPException(status_code=500, detail="Could not create token")

    if hasattr(token_repo, "save_token"):
        try:
            token_repo.save_token(token=access_token, user_id=user.id)
        except Exception as e:
            logger.error(f"Failed to save token to DB: {e}", exc_info=True)
    else:
        logger.warning("TokenRepository does not have a save_token method implemented.")

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(
    request: TokenRequest,
    current_user: DomainUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    token_repo = get_token_repository(db)

    if not hasattr(token_repo, "token_exists") or not token_repo.token_exists(
        request.token
    ):
        logger.warning(
            "Refresh attempt with non-existent/invalid token or unimplemented token_repo.token_exists"
        )
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    try:
        new_token = create_access_token(
            {"sub": current_user.email}, expires_delta=access_token_expires
        )
    except TokenError as e:
        logger.error(f"Token creation failed: {e}")
        raise HTTPException(status_code=500, detail="Could not create token")

    if hasattr(token_repo, "save_token"):
        token_repo.save_token(token=new_token, user_id=current_user.id)

    if hasattr(token_repo, "revoke_token"):
        token_repo.revoke_token(request.token)
    else:
        logger.warning(
            "TokenRepository does not have a revoke_token method implemented."
        )

    return {"access_token": new_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    token: str = Depends(oauth2_scheme),
    token_repo: ITokenRepository = Depends(get_token_repository),
):
    token_repo.revoke_token(token)
    return {"message": "Logged out"}