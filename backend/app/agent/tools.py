from __future__ import annotations

from datetime import datetime
from typing import Any

from langchain_core.tools import tool

from core.database import SessionLocal
from services.trip import (
    get_trip_by_id,
    list_trips,
    search_trips,
)
from services.client import (
    get_client_by_psid,
)


@tool
def tool_list_trips(include_inactive: bool = False, limit: int = 20, offset: int = 0) -> list[dict]:
    """
    List trips with pagination.
    Returns a list of dicts (JSON-serializable).
    """
    db = SessionLocal()
    try:
        trips = list_trips(db=db, include_inactive=include_inactive, limit=limit, offset=offset)
        return [
            {
                "id": t.id,
                "title": t.title,
                "origin": t.origin,
                "destination": t.destination,
                "departure_time": t.departure_time.isoformat() if t.departure_time else None,
                "arrival_time": t.arrival_time.isoformat() if t.arrival_time else None,
                "price": float(t.price) if t.price is not None else None,
                "available_seats": t.available_seats,
                "is_active": bool(t.is_active),
            }
            for t in trips
        ]
    finally:
        db.close()


@tool
def tool_search_trips(
    origin: str | None = None,
    destination: str | None = None,
    depart_from: str | None = None,
    depart_to: str | None = None,
    max_price: float | None = None,
    min_seats: int | None = None,
    include_inactive: bool = False,
    limit: int = 20,
    offset: int = 0,
) -> list[dict]:
    """
    Search trips using filters.

    depart_from/depart_to are ISO datetime strings.
    Returns a list of dicts (JSON-serializable).
    """
    db = SessionLocal()
    try:
        df = datetime.fromisoformat(depart_from) if depart_from else None
        dt = datetime.fromisoformat(depart_to) if depart_to else None

        trips = search_trips(
            db=db,
            origin=origin,
            destination=destination,
            depart_from=df,
            depart_to=dt,
            max_price=max_price,
            min_seats=min_seats,
            include_inactive=include_inactive,
            limit=limit,
            offset=offset,
        )

        return [
            {
                "id": t.id,
                "title": t.title,
                "origin": t.origin,
                "destination": t.destination,
                "departure_time": t.departure_time.isoformat() if t.departure_time else None,
                "arrival_time": t.arrival_time.isoformat() if t.arrival_time else None,
                "price": float(t.price) if t.price is not None else None,
                "available_seats": t.available_seats,
                "is_active": bool(t.is_active),
            }
            for t in trips
        ]
    finally:
        db.close()


@tool
def tool_get_trip(trip_id: int) -> dict | None:
    """
    Get a trip by id. Returns dict or None.
    """
    db = SessionLocal()
    try:
        t = get_trip_by_id(db=db, trip_id=trip_id)
        if not t:
            return None
        return {
            "id": t.id,
            "title": t.title,
            "origin": t.origin,
            "destination": t.destination,
            "departure_time": t.departure_time.isoformat() if t.departure_time else None,
            "arrival_time": t.arrival_time.isoformat() if t.arrival_time else None,
            "price": float(t.price) if t.price is not None else None,
            "available_seats": t.available_seats,
            "is_active": bool(t.is_active),
        }
    finally:
        db.close()


@tool
def tool_get_client_profile(messenger_psid: str) -> dict | None:
    """
    Fetch client by Messenger PSID. Returns dict or None.
    """
    db = SessionLocal()
    try:
        c = get_client_by_psid(db=db, messenger_psid=messenger_psid)
        if not c:
            return None
        return {
            "id": c.id,
            "messenger_psid": c.messenger_psid,
            "name": c.name,
            "phone_number": c.phone_number,
            "national_id": c.national_id,
        }
    finally:
        db.close()
from services.booking import create_booking, confirm_booking, cancel_booking
from services.client import update_client


@tool
def tool_create_booking(
    client_id: int,
    trip_id: int,
    passengers_count: int = 1,
    contact_phone: str | None = None,
    notes: str | None = None,
) -> dict:
    """
    Create a booking (status = pending).

    Returns:
        Booking as JSON-serializable dict.
    """
    db = SessionLocal()
    try:
        b = create_booking(
            db=db,
            client_id=client_id,
            trip_id=trip_id,
            passengers_count=passengers_count,
            contact_phone=contact_phone,
            notes=notes,
        )
        return {
            "id": b.id,
            "client_id": b.client_id,
            "trip_id": b.trip_id,
            "status": b.status,
            "passengers_count": b.passengers_count,
            "contact_phone": b.contact_phone,
            "notes": b.notes,
        }
    finally:
        db.close()


@tool
def tool_confirm_booking(booking_id: int) -> dict | None:
    """
    Confirm a booking and decrement trip seats accordingly.

    Returns:
        Updated booking dict, or None if not found.
    """
    db = SessionLocal()
    try:
        b = confirm_booking(db=db, booking_id=booking_id)
        if not b:
            return None
        return {
            "id": b.id,
            "client_id": b.client_id,
            "trip_id": b.trip_id,
            "status": b.status,
            "passengers_count": b.passengers_count,
            "contact_phone": b.contact_phone,
            "notes": b.notes,
        }
    finally:
        db.close()


@tool
def tool_cancel_booking(booking_id: int) -> dict | None:
    """
    Cancel a booking.

    Returns:
        Updated booking dict, or None if not found.
    """
    db = SessionLocal()
    try:
        b = cancel_booking(db=db, booking_id=booking_id)
        if not b:
            return None
        return {
            "id": b.id,
            "client_id": b.client_id,
            "trip_id": b.trip_id,
            "status": b.status,
            "passengers_count": b.passengers_count,
            "contact_phone": b.contact_phone,
            "notes": b.notes,
        }
    finally:
        db.close()


@tool
def tool_update_client_profile(
    client_id: int,
    name: str | None = None,
    phone_number: str | None = None,
    national_id: str | None = None,
) -> dict | None:
    """
    Update a client's profile fields.

    Returns:
        Updated client dict, or None if not found.
    """
    db = SessionLocal()
    try:
        c = update_client(
            db=db,
            client_id=client_id,
            name=name,
            phone_number=phone_number,
            national_id=national_id,
        )
        if not c:
            return None
        return {
            "id": c.id,
            "messenger_psid": c.messenger_psid,
            "name": c.name,
            "phone_number": c.phone_number,
            "national_id": c.national_id,
        }
    finally:
        db.close()
        
TOOLS = [
    tool_search_trips,
    tool_list_trips,
    tool_get_trip,
    tool_get_client_profile,
    tool_create_booking,
    tool_confirm_booking,
    tool_cancel_booking,
    tool_update_client_profile,
]
