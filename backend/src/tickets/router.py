from typing import List, Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.users.schemas import User
from src.tickets.schemas import RequestSellTicket, TicketResponse, TicketToPurchase
from src.database.db import get_db


from src.tickets.service import ticket_create, my_tickets, update_ticket, delete_ticket, tickets_get_all, ticket_buy

from src.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/sell", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def create_ticket(request_ticket: RequestSellTicket, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return ticket_create(db=db, request_ticket=request_ticket, seller_id=current_user.id)


@router.post("/buy", status_code=status.HTTP_200_OK, response_model=TicketResponse)
def buy_ticket(request_ticket: TicketToPurchase, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
     return ticket_buy(db=db, request_ticket=request_ticket, buyer_id=current_user.id)

@router.get("/alltickets", status_code=status.HTTP_200_OK, response_model=List[TicketResponse])
def get_all_tickets(db: Session = Depends(get_db)):
    return tickets_get_all(db=db)


@router.get("/my-tickets", status_code=status.HTTP_200_OK, response_model=List[TicketResponse])
def get_my_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve all tickets for the current user.
    """
    return my_tickets(db=db, seller_id=current_user.id)

@router.put("/my-tickets/{ticket_id}", status_code=status.HTTP_200_OK, response_model=TicketResponse)
def update_ticket_by_id(
    ticket_id: str,
    request_ticket: RequestSellTicket,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Update a ticket by its ID.
    """
    return update_ticket(db=db, ticket_id=ticket_id, request_ticket=request_ticket, current_user=current_user)


@router.delete("/my-tickets/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ticket_by_id(
    ticket_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Delete a ticket by its ID.
    """
    delete_ticket(db=db, ticket_id=ticket_id, current_user=current_user)
    return