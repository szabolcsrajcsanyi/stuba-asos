import uuid

from sqlalchemy import Column, String, TIMESTAMP, Boolean
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from src.database.db import Base, engine

class Users(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)
    disabled = Column(Boolean, default=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True),
                       default=None, onupdate=func.now())
    

# class Events(Base):
#     __tablename__ = 'events'

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
#     name = Column(String, nullable=False)
#     title = Column(String, nullable=False)
#     description = Column(String, nullable=False)
#     location = Column(String, nullable=False)
#     date = Column(TIMESTAMP(timezone=True), nullable=False)
#     createdAt = Column(TIMESTAMP(timezone=True),
#                        nullable=False, server_default=func.now())
#     updatedAt = Column(TIMESTAMP(timezone=True),
#                        default=None, onupdate=func.now())


Base.metadata.create_all(engine)