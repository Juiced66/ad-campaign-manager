from typing import Optional

from fastapi import HTTPException

from app.application.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash
from app.domain.entities.user import User as DomainUser
from app.domain.interfaces.user_repository import IUserRepository


def get_user(repo: IUserRepository, user_id: int) -> Optional[DomainUser]:
    return repo.get(id=user_id)


def get_user_by_email(repo: IUserRepository, email: str) -> Optional[DomainUser]:
    return repo.get_by_email(email=email)


def create_user(
    repo: IUserRepository, dto: UserCreate, is_superuser: bool = False
) -> DomainUser:
    existing_user = repo.get_by_email(email=dto.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(dto.password)

    user_entity = DomainUser(
        email=dto.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=is_superuser,
    )

    return repo.create(entity=user_entity)


def update_user(
    repo: IUserRepository, user_id: int, dto: UserUpdate
) -> Optional[DomainUser]:
    existing_user = repo.get(id=user_id)
    if not existing_user:
        return None

    update_data = dto.model_dump(exclude_unset=True)

    if "password" in update_data and update_data["password"]:
        hashed_password = get_password_hash(update_data["password"])
        existing_user.hashed_password = hashed_password

    if "email" in update_data and update_data["email"]:
        existing_user.email = update_data["email"]

    if "is_active" in update_data:
        existing_user.is_active = update_data["is_active"]

    updated_user = repo.update(id=user_id, entity=existing_user)

    return updated_user


def delete_user(repo: IUserRepository, user_id: int) -> Optional[DomainUser]:
    return repo.remove(id=user_id)
