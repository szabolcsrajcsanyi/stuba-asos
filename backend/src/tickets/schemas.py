from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel

class RequestSellTicket(BaseModel):
    name: str
    description: Optional[str] = None
    date: datetime
    category: str
    price: float

    class Config:
        from_attributes = True

class TicketResponse(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: Optional[str] = None
    date: datetime
    category: str
    price: float
    seller_id: UUID
    buyer_id: Optional[UUID] = None
    
    class Config:
        from_attributes = True