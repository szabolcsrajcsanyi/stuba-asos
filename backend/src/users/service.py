import bcrypt
from uuid import UUID

from sqlalchemy.orm import Session

from src.database.models import Users
from src.users.schemas import RegisterUser, UserInDB


def users_get_all(db: Session):
    return db.query(Users).all()

def user_create(db: Session, post: RegisterUser):
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

def get_user_by_name(db: Session, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)