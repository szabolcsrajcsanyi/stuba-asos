from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class RegisterUser(BaseModel):
    id: Optional[UUID]
    firstname: str
    lastname: str
    email: str
    password: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: Optional[UUID]
    firstname: str
    lastname: str
    email: str

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str