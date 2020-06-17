from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str


class UserPayloadSchema(User):
    password: str


class UserResponseSchema(User):
    id: int
    role: str
