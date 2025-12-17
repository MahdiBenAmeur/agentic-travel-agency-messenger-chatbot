from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.database import get_db
from services.booking import (
    cancel_booking,
    confirm_booking,
    create_booking,
    delete_booking,
    get_booking_by_id,
    list_bookings,
    list_bookings_by_client,
    list_bookings_by_trip,
    update_booking,
)

router = APIRouter(prefix="/bookings", tags=["bookings"])


class BookingCreate(BaseModel):
    client_id: int
    trip_id: int
    passengers_count: int = Field(default=1, ge=1)
    contact_phone: str | None = None
    notes: str | None = None


class BookingUpdate(BaseModel):
    passengers_count: int | None = Field(default=None, ge=1)
    contact_phone: str | None = None
    notes: str | None = None


@router.post("")
def create_booking_route(payload: BookingCreate, db: Session = Depends(get_db)):
    try:
        return create_booking(db=db, **payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{booking_id}")
def get_booking_route(booking_id: int, db: Session = Depends(get_db)):
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="booking not found")
    return booking


@router.get("")
def list_bookings_route(
    db: Session = Depends(get_db),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    client_id: int | None = Query(default=None),
    trip_id: int | None = Query(default=None),
):
    if client_id is not None and trip_id is not None:
        raise HTTPException(status_code=400, detail="use either client_id or trip_id, not both")

    if client_id is not None:
        return list_bookings_by_client(db=db, client_id=client_id, limit=limit, offset=offset)

    if trip_id is not None:
        return list_bookings_by_trip(db=db, trip_id=trip_id, limit=limit, offset=offset)

    return list_bookings(db=db, limit=limit, offset=offset)


@router.patch("/{booking_id}")
def update_booking_route(booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db)):
    try:
        updated = update_booking(db=db, booking_id=booking_id, **payload.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated:
        raise HTTPException(status_code=404, detail="booking not found")
    return updated


@router.post("/{booking_id}/confirm")
def confirm_booking_route(booking_id: int, db: Session = Depends(get_db)):
    try:
        updated = confirm_booking(db=db, booking_id=booking_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated:
        raise HTTPException(status_code=404, detail="booking not found")
    return updated


@router.post("/{booking_id}/cancel")
def cancel_booking_route(booking_id: int, db: Session = Depends(get_db)):
    updated = cancel_booking(db=db, booking_id=booking_id)
    if not updated:
        raise HTTPException(status_code=404, detail="booking not found")
    return updated


@router.delete("/{booking_id}")
def delete_booking_route(booking_id: int, db: Session = Depends(get_db)):
    ok = delete_booking(db=db, booking_id=booking_id)
    if not ok:
        raise HTTPException(status_code=404, detail="booking not found")
    return {"deleted": True}
