from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.users.schemas import RequestRegisterUser, User
from src.database.db import get_db
from src.users.service import (
    users_get_all,
    user_create
)

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    return users_get_all(db=db)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request_user: RequestRegisterUser, db: Session = Depends(get_db)):
    return user_create(db=db, request_user=request_user)