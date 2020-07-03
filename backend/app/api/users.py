from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Security

from app.core.security.utils import get_current_user
from app.core.security.errors import unauth_error
from app.crud import users as crud
from app.models.pydantic.users import CreateUserPayloadSchema, GetUserSchema, UserResponseSchema, PatchUserSchema
from app.models.tortoise.users import User


router = APIRouter()


@router.post("/", response_model=GetUserSchema, status_code=201)
async def create_user(payload: CreateUserPayloadSchema) -> GetUserSchema:
    user_id = await crud.post(payload)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username/email already exists")
    response_object = {
        "id": user_id,
        "username": payload.username,
    }
    return response_object


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(user: User = Security(get_current_user, scopes=["admin"])) -> List[UserResponseSchema]:
    return await crud.get_all()


@router.get("/me/", response_model=UserResponseSchema)
async def get_me(user: User = Security(get_current_user)) -> UserResponseSchema:
    me = await crud.get(username=user.username)
    return me[0]


@router.get("/{username}/", response_model=UserResponseSchema)
async def get(username: str, user: User = Security(get_current_user, scopes=[])) -> UserResponseSchema:
    if user.username != username and "admin" not in user.scopes:
        raise unauth_error("Not enough permissions", f'Bearer scope="admin"')
    user = await crud.get(username=username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return user[0]


@router.patch("/{username}/", response_model=UserResponseSchema)
async def patch(
    username: str, payload: PatchUserSchema, user: User = Security(get_current_user, scopes=[])
) -> UserResponseSchema:
    user = crud.patch(username=username, **payload)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found")
    return user[0]
