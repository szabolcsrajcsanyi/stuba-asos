from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.database.models import Ticket
from src.tickets.schemas import RequestSellTicket, TicketResponse, TicketToPurchase

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

def ticket_buy(db: Session, request_ticket: TicketToPurchase, buyer_id: str):
    ticket = db.query(Ticket).filter(Ticket.id == request_ticket.id).first()
    if ticket:
        if ticket.buyer_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Ticket was already bought'
            )
        try:
            ticket.buyer_id = buyer_id
            db.commit()
            db.refresh(ticket)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'Error occurred buying ticket'
            )

    return TicketResponse(
        id=ticket.id,
        name=ticket.name,
        description=ticket.description,
        date=ticket.date,
        category=ticket.category,
        price=ticket.price,
        seller_id=ticket.seller_id,
        buyer_id=ticket.buyer_id
    )
