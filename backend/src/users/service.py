import bcrypt
from uuid import UUID

from sqlalchemy.orm import Session

from src.database.models import Users
from src.users.schemas import RequestRegisterUser, UserInDB


def users_get_all(db: Session):
    return db.query(Users).all()

def user_create(db: Session, post: RequestRegisterUser):
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(post.password.encode('utf-8'), salt)
    db_post = Users(
        firstname=post.firstname, 
        lastname=post.lastname, 
        email=post.email, 
        password_hash=password_hash.decode('utf-8')
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_user_by_email(db: Session, email: str):
    user = db.query(Users).filter(Users.email == email).first()
    if user:
        return UserInDB(
            id=user.id,
            firstname=user.firstname,
            lastname=user.lastname,
            email=user.email,
            hashed_password=user.password_hash
        )
    return None