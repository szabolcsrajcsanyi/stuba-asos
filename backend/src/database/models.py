from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from src.database.db import Base, engine

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)

    # Relationships
    tickets_selling = relationship('Ticket', back_populates='seller', foreign_keys='Ticket.seller_id')
    tickets_buying = relationship('Ticket', back_populates='buyer', foreign_keys='Ticket.buyer_id')


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date = Column(DateTime, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Float, nullable=False)

    # Foreign Keys
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    seller_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relationships
    buyer = relationship('Users', back_populates='tickets_buying', foreign_keys=[buyer_id])
    seller = relationship('Users', back_populates='tickets_selling', foreign_keys=[seller_id])

Base.metadata.create_all(engine)