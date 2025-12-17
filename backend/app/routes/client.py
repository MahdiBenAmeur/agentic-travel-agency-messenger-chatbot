from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from core.database import get_db
from services.client import (
    create_client,
    delete_client,
    get_client_by_id,
    get_client_by_psid,
    get_or_create_client,
    list_clients,
    update_client,
)

router = APIRouter(prefix="/clients", tags=["clients"])


class ClientCreate(BaseModel):
    messenger_psid: str
    name: str | None = None
    phone_number: str | None = None
    national_id: str | None = None


class ClientGetOrCreate(BaseModel):
    messenger_psid: str
    name: str | None = None


class ClientUpdate(BaseModel):
    name: str | None = None
    phone_number: str | None = None
    national_id: str | None = None
    messenger_psid: str | None = None


@router.post("")
def create_client_route(payload: ClientCreate, db: Session = Depends(get_db)):
    try:
        return create_client(db=db, **payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/get-or-create")
def get_or_create_client_route(payload: ClientGetOrCreate, db: Session = Depends(get_db)):
    try:
        return get_or_create_client(db=db, **payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{client_id}")
def get_client_route(client_id: int, db: Session = Depends(get_db)):
    client = get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="client not found")
    return client


@router.get("/by-psid/{messenger_psid}")
def get_client_by_psid_route(messenger_psid: str, db: Session = Depends(get_db)):
    client = get_client_by_psid(db, messenger_psid)
    if not client:
        raise HTTPException(status_code=404, detail="client not found")
    return client


@router.get("")
def list_clients_route(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
):
    return list_clients(db=db, limit=limit, offset=offset)


@router.patch("/{client_id}")
def update_client_route(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db)):
    updated = update_client(db=db, client_id=client_id, **payload.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="client not found")
    return updated


@router.delete("/{client_id}")
def delete_client_route(client_id: int, db: Session = Depends(get_db)):
    ok = delete_client(db=db, client_id=client_id)
    if not ok:
        raise HTTPException(status_code=404, detail="client not found")
    return {"deleted": True}
