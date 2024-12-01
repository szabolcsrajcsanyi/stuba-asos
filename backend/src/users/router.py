from typing import List, Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.users.schemas import RequestRegisterUser, User
from src.database.db import get_db
from src.users.service import (
    users_get_all,
    user_create,
    user_delete
)

from src.auth.dependencies import get_current_active_user


router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    return users_get_all(db=db)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request_user: RequestRegisterUser, db: Session = Depends(get_db)):
    return user_create(db=db, request_user=request_user)


@router.delete("/me", status_code=status.HTTP_200_OK)
def delete_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return user_delete(db=db, current_user=current_user)

@router.post("/buyticket", status_code=status.HTTP_200_OK, response_model=List[User])
def buy_ticket(db: Session = Depends(get_db)):
     pass