from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_db
from services.message import (
    log_message,
    get_recent_messages,
    get_recent_messages_chronological,
)

router = APIRouter(prefix="/messages", tags=["messages"])


class MessageCreate(BaseModel):
    client_id: int | None
    direction: str  # "in" | "out"
    content: str | None


@router.post("")
def log_message_route(payload: MessageCreate, db: Session = Depends(get_db)):
    if payload.direction not in {"in", "out"}:
        raise HTTPException(status_code=400, detail="direction must be 'in' or 'out'")
    return log_message(db=db, **payload.model_dump())


@router.get("/recent/{client_id}")
def get_recent_messages_route(
    client_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
):
    return get_recent_messages(db=db, client_id=client_id, limit=limit)


@router.get("/recent/{client_id}/chronological")
def get_recent_messages_chronological_route(
    client_id: int,
    db: Session = Depends(get_db),
    limit: int = Query(default=20, ge=1, le=100),
):
    return get_recent_messages_chronological(db=db, client_id=client_id, limit=limit)
