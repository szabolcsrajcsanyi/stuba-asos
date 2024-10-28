from typing import Annotated
from datetime import timedelta

from fastapi import Depends,  HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.auth.schemas import Token
from src.auth.utils import authenticate_user, create_access_token
from src.config import settings
from src.database.db import get_db


router = APIRouter(prefix="/auth", tags=["users"])


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
    ,
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.AUTH_JWT_EXP)
    access_token = create_access_token(
        data={"sub": user.email, "firstname": user.firstname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")