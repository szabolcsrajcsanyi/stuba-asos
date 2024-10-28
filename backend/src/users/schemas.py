from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RequestRegisterUser(BaseModel):
    id: Optional[UUID] = None
    firstname: str
    lastname: str
    email: str
    password: str

    class Config:
        from_attributes = True


class User(BaseModel):
    id: Optional[UUID] = None
    firstname: str
    lastname: str
    email: str
    disabled: bool

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str