from fastapi import APIRouter, Depends, HTTPException

from app.application.schemas.user import User, UserCreate, UserUpdate
from app.application.use_cases.user import services as user_services
from app.domain.entities.user import User as DomainUser
from app.domain.interfaces.user_repository import IUserRepository
from app.presentation.api.v1.dependencies.auth import get_current_user
from app.presentation.api.v1.dependencies.repositories import get_user_repository

router = APIRouter()


@router.get("/me", response_model=User, tags=["Users"])
def get_me(
    current_user: DomainUser = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository),  # <-- ici
):
    return user_services.get_user(repo, current_user.id)


@router.put("/me", response_model=User, tags=["Users"])
def update_me(
    payload: UserUpdate,
    current_user: DomainUser = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository),
):
    # Only allow updating email and password
    update_payload = UserUpdate()

    if payload.email:
        update_payload.email = payload.email

    if payload.password:
        update_payload.password = payload.password

    return user_services.update_user(repo, current_user.id, update_payload)


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    _: User = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository)):
    user = user_services.get_user(repo, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=User)
def get_user_by_email(
    email: str,
    _: User = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository)
):
    user = user_services.get_user_by_email(repo, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=User, status_code=201)
def create_user(
    user_in: UserCreate,
    repo: IUserRepository = Depends(get_user_repository)
):
    return user_services.create_user(repo, user_in)


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    _: User = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository),
):
    updated = user_services.update_user(repo, user_id, user_in)
    if updated is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated


@router.delete("/{user_id}", response_model=User)
def delete_user(
    user_id: int, 
    _: User = Depends(get_current_user),
    repo: IUserRepository = Depends(get_user_repository)
):
    deleted = user_services.delete_user(repo, user_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted
