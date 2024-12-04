from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Ticket
from src.tickets.schemas import RequestSellTicket, TicketResponse
from typing import List

def ticket_create(db: Session, request_ticket: RequestSellTicket, seller_id: str):

    db_ticket = Ticket(
        name=request_ticket.name,
        description=request_ticket.description,
        date=request_ticket.date,
        category=request_ticket.category,
        price=request_ticket.price,
        seller_id=seller_id
    )

    try:
        db.add(db_ticket)
        db.commit()
        db.refresh(db_ticket)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Error occurred creating ticket'
        )

    return TicketResponse(
        id=db_ticket.id,
        name=db_ticket.name,
        description=db_ticket.description,
        date=db_ticket.date,
        category=db_ticket.category,
        price=db_ticket.price,
        seller_id=db_ticket.seller_id
    )

def my_tickets(db: Session, seller_id: str):
    tickets = db.query(Ticket).filter(Ticket.seller_id == seller_id).all()
    if not tickets:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tickets found for the current user.",
        )

    return [TicketResponse.model_validate(ticket) for ticket in tickets]


def update_ticket(db: Session, ticket_id: str, request_ticket: RequestSellTicket, current_user):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.seller_id == current_user.id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found or you do not have permission to update it.",
        )

    ticket.name = request_ticket.name
    ticket.description = request_ticket.description
    ticket.date = request_ticket.date
    ticket.category = request_ticket.category
    ticket.price = request_ticket.price

    db.commit()
    db.refresh(ticket)
    return TicketResponse.model_validate(ticket)


def delete_ticket(db: Session, ticket_id: str, current_user):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id, Ticket.seller_id == current_user.id).first()
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found or you do not have permission to delete it.",
        )

    db.delete(ticket)
    db.commit()