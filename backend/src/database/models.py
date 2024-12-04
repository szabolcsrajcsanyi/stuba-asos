import uuid

from sqlalchemy import Column, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.db import Base, engine

class Users(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    # Relationships
    tickets_selling = relationship('Ticket', back_populates='seller', foreign_keys='Ticket.seller_id')
    tickets_buying = relationship('Ticket', back_populates='buyer', foreign_keys='Ticket.buyer_id')


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Foreign Keys
    buyer_id = Column(UUID, ForeignKey('users.id'), nullable=True)
    seller_id = Column(UUID, ForeignKey('users.id'), nullable=False)

    # Relationships
    buyer = relationship('Users', back_populates='tickets_buying', foreign_keys=[buyer_id])
    seller = relationship('Users', back_populates='tickets_selling', foreign_keys=[seller_id])

Base.metadata.create_all(engine)