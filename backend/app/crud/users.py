from typing import List, Union

from app.models.pydantic.users import CreateUserPayloadSchema
from app.models.tortoise.users import User


async def post(payload: CreateUserPayloadSchema) -> Union[int, None]:
    user = await User.filter(username=payload.username).first()
    if user:
        return None
    user = User(username=payload.username, email=payload.email, full_name=payload.full_name)
    user.set_password(payload.password)
    await user.save()
    return user.id


async def get_all() -> List[User]:
    users = await User.all().values()
    return users


async def get(username: str) -> Union[User, None]:
    user = await User.filter(username=username).first().values()

    if not user:
        return None
    return user
