import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import TokenError, decode_access_token
from app.domain.entities.user import User as DomainUser
from app.infrastructure.database.sql_alchemy.session import get_db
from app.presentation.api.v1.dependencies.repositories import (
    get_token_repository,
    get_user_repository,
)

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

revoked_token_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has been revoked",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> DomainUser:
    token_repo = get_token_repository(db)
    user_repo = get_user_repository(db)

    try:
        payload = decode_access_token(token)
        email: str | None = payload.get("sub")
        if email is None:
            raise credentials_exception
    except TokenError:
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token decode: {e}", exc_info=True)
        raise credentials_exception

    if hasattr(token_repo, "token_exists") and token_repo.token_exists(token):
        raise revoked_token_exception
    elif not hasattr(token_repo, "token_exists"):
        logger.warning(
            "TokenRepository may be missing 'token_exists' method for revocation check."
        )

    user = user_repo.get_by_email(email=email)
    if user is None:
        raise credentials_exception
    return user
