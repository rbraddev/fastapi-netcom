from typing import List

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.crud import users as crud
from app.models.pydantic.users import CreateUserPayloadSchema, UserResponseSchema
from app.models.tortoise.users import User


router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(payload: CreateUserPayloadSchema) -> UserResponseSchema:
    user_id = await crud.post(payload)

    response_object = {
        "id": user_id,
        "email": payload.email,
        "username": payload.username,
        "full_name": payload.full_name,
        "role": "user",
    }
    return response_object


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(user: User = Depends(get_current_user)) -> List[UserResponseSchema]:
    return await crud.get_all()


@router.get("/me/", response_model=UserResponseSchema)
async def get_me(user: User = Depends(get_current_user)) -> UserResponseSchema:
    me = await crud.get(username=user.username)

    response_object = {
        "id": me.id,
        "email": me.email,
        "username": me.username,
        "full_name": me.full_name,
        "role": me.role,
    }

    return response_object


@router.get("/{username}/", response_model=UserResponseSchema)
async def get(username: str, user: User = Depends(get_current_user)) -> UserResponseSchema:
    user = await crud.get(username=username)

    response_object = {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
    }

    return response_object
