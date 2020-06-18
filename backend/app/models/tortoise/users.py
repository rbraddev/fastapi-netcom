from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.context import CryptContext


class User(models.Model):
    username = fields.TextField()
    email = fields.TextField()
    full_name = fields.TextField()
    hashed_password = fields.TextField()
    role = fields.TextField(default="user")
    access_level = fields.IntField(default=1)
    created_at = fields.DatetimeField(auto_now_add=True)
    disabled = fields.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} <{self.email}>"

    @staticmethod
    def _get_password_context() -> CryptContext:
        return CryptContext(schemes=["bcrypt"], deprecated="auto")

    def set_password(self, password: str):
        self.hashed_password = self._get_password_context().hash(password)

    def verify_password(self, password: str) -> bool:
        return self._get_password_context().verify(password, self.hashed_password)

    def set_access_level(self, role):
        access_level = {"admin": 3, "tech": 2, "user": 1}
        if role not in access_level.keys():
            raise ValueError(f"{role} is and invalid role.")
        self.role = role
        self.access_level = access_level.get("role")


UserSchema = pydantic_model_creator(User)
