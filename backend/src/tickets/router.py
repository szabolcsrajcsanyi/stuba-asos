from typing import List, Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.users.schemas import User
from src.tickets.schemas import RequestSellTicket, TicketResponse
from src.database.db import get_db
from src.tickets.service import ticket_create

from src.auth.dependencies import get_current_active_user

router = APIRouter(prefix="/tickets", tags=["tickets"])

@router.post("/sell", status_code=status.HTTP_201_CREATED, response_model=TicketResponse)
def create_ticket(request_ticket: RequestSellTicket, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    return ticket_create(db=db, request_ticket=request_ticket, seller_id=current_user.id)