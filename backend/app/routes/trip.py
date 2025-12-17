from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from core.database import get_db
from services.trip import (
    create_trip,
    decrement_trip_seats,
    delete_trip,
    get_trip_by_id,
    list_trips,
    search_trips,
    set_trip_active,
    update_trip,
)

router = APIRouter(prefix="/trips", tags=["trips"])


class TripCreate(BaseModel):
    title: str
    origin: str
    destination: str
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    price: float | None = None
    available_seats: int | None = None
    is_active: bool = True


class TripUpdate(BaseModel):
    title: str | None = None
    origin: str | None = None
    destination: str | None = None
    departure_time: datetime | None = None
    arrival_time: datetime | None = None
    price: float | None = None
    available_seats: int | None = None
    is_active: bool | None = None


class TripActiveUpdate(BaseModel):
    is_active: bool


class TripDecrementSeats(BaseModel):
    seats: int = Field(default=1, ge=1)


@router.post("")
def create_trip_route(payload: TripCreate, db: Session = Depends(get_db)):
    try:
        return create_trip(db=db, **payload.model_dump())
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{trip_id}")
def get_trip_route(trip_id: int, db: Session = Depends(get_db)):
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="trip not found")
    return trip


@router.get("")
def list_or_search_trips_route(
    db: Session = Depends(get_db),
    include_inactive: bool = Query(default=False),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    origin: str | None = Query(default=None),
    destination: str | None = Query(default=None),
    depart_from: datetime | None = Query(default=None),
    depart_to: datetime | None = Query(default=None),
    max_price: float | None = Query(default=None, ge=0),
    min_seats: int | None = Query(default=None, ge=0),
):
    any_filter = any(
        x is not None
        for x in [origin, destination, depart_from, depart_to, max_price, min_seats]
    )

    if any_filter:
        return search_trips(
            db=db,
            origin=origin,
            destination=destination,
            depart_from=depart_from,
            depart_to=depart_to,
            max_price=max_price,
            min_seats=min_seats,
            include_inactive=include_inactive,
            limit=limit,
            offset=offset,
        )

    return list_trips(
        db=db,
        include_inactive=include_inactive,
        limit=limit,
        offset=offset,
    )


@router.patch("/{trip_id}")
def update_trip_route(trip_id: int, payload: TripUpdate, db: Session = Depends(get_db)):
    updated = update_trip(db=db, trip_id=trip_id, **payload.model_dump(exclude_none=True))
    if not updated:
        raise HTTPException(status_code=404, detail="trip not found")
    return updated


@router.patch("/{trip_id}/active")
def set_trip_active_route(trip_id: int, payload: TripActiveUpdate, db: Session = Depends(get_db)):
    updated = set_trip_active(db=db, trip_id=trip_id, is_active=payload.is_active)
    if not updated:
        raise HTTPException(status_code=404, detail="trip not found")
    return updated


@router.post("/{trip_id}/decrement-seats")
def decrement_trip_seats_route(trip_id: int, payload: TripDecrementSeats, db: Session = Depends(get_db)):
    try:
        updated = decrement_trip_seats(db=db, trip_id=trip_id, seats=payload.seats)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not updated:
        raise HTTPException(status_code=404, detail="trip not found")
    return updated


@router.delete("/{trip_id}")
def delete_trip_route(trip_id: int, db: Session = Depends(get_db)):
    ok = delete_trip(db=db, trip_id=trip_id)
    if not ok:
        raise HTTPException(status_code=404, detail="trip not found")
    return {"deleted": True}
