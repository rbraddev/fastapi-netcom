from typing import List

from fastapi import HTTPException, status

from app.models.pydantic.users import UserPayloadSchema
from app.models.tortoise.users import User


async def post(payload: UserPayloadSchema) -> int:
    user = await User.filter(username=payload.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    user = User(username=payload.username, email=payload.email, full_name=payload.full_name)
    user.set_password(payload.password)
    await user.save()
    return user.id


async def get_all() -> List:
    users = await User.all().values()
    return users
