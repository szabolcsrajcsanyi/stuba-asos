import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Users, Ticket
from src.users.schemas import RequestRegisterUser, UserInDB, User


def users_get_all(db: Session):
    return db.query(Users).all()

def user_create(db: Session, request_user: RequestRegisterUser):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(request_user.password.encode('utf-8'), salt)

    existing_user = get_user_by_email(db=db, email=request_user.email)

    if existing_user:
        # Raise an HTTP 400 error if the email already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered"
        )
    db_user = Users(
        firstname=request_user.firstname,
        lastname=request_user.lastname,
        email=request_user.email,
        password_hash=password_hash.decode('utf-8')
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()  # Rollback in case of any other unique constraint violations
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An error occurred while creating the user. Please try again."
        )

    return User(
        id=db_user.id,
        firstname=db_user.firstname,
        lastname=db_user.lastname,
        email=db_user.email,
        disabled=db_user.disabled
    )


def user_delete(db: Session, current_user: User):
    user = db.query(Users).filter(Users.id == current_user.id).first()
    if user:
        db.delete(user)
        db.commit()
        return "User deleted successfully"
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


def get_user_by_email(db: Session, email: str):
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return UserInDB(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            disabled=user.disabled,
            hashed_password=user.password_hash
        )
    return None
