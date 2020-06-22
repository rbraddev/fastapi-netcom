from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class CreateUserPayloadSchema(User):
    password: str


class UserResponseSchema(User):
    id: int
    role: str


class GetUserSchema(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
