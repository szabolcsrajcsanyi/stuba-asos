from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db


router = APIRouter()


@router.get("/status", status_code=status.HTTP_200_OK)
def get_status(db: Session = Depends(get_db)):
    return {
        "status": "ok",
        "db": "connected"
    }
