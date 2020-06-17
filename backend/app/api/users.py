from typing import List

from fastapi import APIRouter, Depends

from app.core.security import get_current_user
from app.crud import users as crud
from app.models.pydantic.users import UserPayloadSchema, UserResponseSchema
from app.models.tortoise.users import User


router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(payload: UserPayloadSchema) -> UserResponseSchema:
    user_id = await crud.post(payload)

    response_object = {
        "id": user_id,
        "email": payload.email,
        "username": payload.username,
        "full_name": payload.full_name,
        "role": "user"
    }
    return response_object


@router.get("/", response_model=List[UserResponseSchema])
async def get_all_users(user: User = Depends(get_current_user),) -> List[UserResponseSchema]:
    return await crud.get_all()
