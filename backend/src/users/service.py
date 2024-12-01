import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Users, Ticket
from src.users.schemas import RequestRegisterUser, UserInDB, User, TicketToPurchase


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
    print('user neexistuje')
    db_user = Users(
        first_name=request_user.firstname,
        last_name=request_user.lastname,
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
        firstname=db_user.first_name,
        lastname=db_user.last_name,
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
            firstname=user.first_name,
            lastname=user.last_name,
            email=user.email,
            disabled=user.disabled,
            hashed_password=user.password_hash
        )
    return None

def ticket_buy(db: Session, request_ticket: TicketToPurchase, current_user:User):
    ticket = db.query(Ticket).filter(Ticket.id == request_ticket.id).first()
    if ticket:
        if ticket.buyer_id:
            return {"error": "Ticket is already purchased"}
        ticket.buyer_id = current_user.id
        db.commit()
        db.refresh(ticket)

    return {"message": "Ticket successfully purchased", "ticket_id": ticket.id}
