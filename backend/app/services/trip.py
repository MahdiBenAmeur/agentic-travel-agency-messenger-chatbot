from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy.orm import Session

from dbmodels.trip import Trip


def create_trip(
    db: Session,
    title: str,
    origin: str,
    destination: str,
    departure_time: datetime | None = None,
    arrival_time: datetime | None = None,
    price: float | None = None,
    available_seats: int | None = None,
    is_active: bool = True,
) -> Trip:
    """
    Create a new trip (travel service offer) row.

    Args:
        db: SQLAlchemy session.
        title: Human-readable offer title (e.g., "Tunis → Paris").
        origin: Starting city/airport.
        destination: Destination city/airport.
        departure_time: Departure datetime (optional).
        arrival_time: Arrival datetime (optional).
        price: Price (optional).
        available_seats: Remaining seats (optional).
        is_active: Whether this offer is visible/usable.

    Returns:
        The created Trip instance (refreshed from DB).
    """
    trip = Trip(
        title=title,
        origin=origin,
        destination=destination,
        departure_time=departure_time,
        arrival_time=arrival_time,
        price=price,
        available_seats=available_seats,
        is_active=is_active,
    )
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


def get_trip_by_id(db: Session, trip_id: int) -> Trip | None:
    """
    Fetch a single trip by its primary key.

    Args:
        db: SQLAlchemy session.
        trip_id: Trip ID.

    Returns:
        Trip if found, otherwise None.
    """
    return db.query(Trip).filter(Trip.id == trip_id).first()


def list_trips(
    db: Session,
    include_inactive: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[Trip]:
    """
    List trips with pagination.

    Args:
        db: SQLAlchemy session.
        include_inactive: If True, include inactive offers.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of trips.
    """
    q = db.query(Trip)
    if not include_inactive:
        q = q.filter(Trip.is_active == True)  # noqa: E712
    return q.order_by(Trip.id.desc()).offset(offset).limit(limit).all()


def search_trips(
    db: Session,
    origin: str | None = None,
    destination: str | None = None,
    depart_from: datetime | None = None,
    depart_to: datetime | None = None,
    max_price: float | None = None,
    min_seats: int | None = None,
    include_inactive: bool = False,
    limit: int = 50,
    offset: int = 0,
) -> list[Trip]:
    """
    Search trips using common travel filters.

    Notes:
        - Uses exact match for origin/destination (no fuzzy search).
        - depart_from/depart_to filter on Trip.departure_time (if present).

    Args:
        db: SQLAlchemy session.
        origin: Filter by origin.
        destination: Filter by destination.
        depart_from: Departure time lower bound (inclusive).
        depart_to: Departure time upper bound (inclusive).
        max_price: Only trips with price <= max_price (if price not null).
        min_seats: Only trips with available_seats >= min_seats (if seats not null).
        include_inactive: If True, include inactive offers.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of matching trips.
    """
    q = db.query(Trip)

    if not include_inactive:
        q = q.filter(Trip.is_active == True)  # noqa: E712

    if origin:
        q = q.filter(Trip.origin == origin)
    if destination:
        q = q.filter(Trip.destination == destination)

    if depart_from is not None:
        q = q.filter(Trip.departure_time >= depart_from)
    if depart_to is not None:
        q = q.filter(Trip.departure_time <= depart_to)

    if max_price is not None:
        q = q.filter(Trip.price.isnot(None)).filter(Trip.price <= max_price)

    if min_seats is not None:
        q = q.filter(Trip.available_seats.isnot(None)).filter(Trip.available_seats >= min_seats)

    return q.order_by(Trip.id.desc()).offset(offset).limit(limit).all()


def update_trip(
    db: Session,
    trip_id: int,
    *,
    title: str | None = None,
    origin: str | None = None,
    destination: str | None = None,
    departure_time: datetime | None = None,
    arrival_time: datetime | None = None,
    price: float | None = None,
    available_seats: int | None = None,
    is_active: bool | None = None,
) -> Trip | None:
    """
    Partially update a trip (only provided fields are changed).

    Args:
        db: SQLAlchemy session.
        trip_id: Trip ID.
        title/origin/destination/departure_time/arrival_time/price/available_seats/is_active:
            Fields to update. If a field is None, it is not changed.

    Returns:
        Updated Trip if found, otherwise None.
    """
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        return None

    if title is not None:
        trip.title = title
    if origin is not None:
        trip.origin = origin
    if destination is not None:
        trip.destination = destination
    if departure_time is not None:
        trip.departure_time = departure_time
    if arrival_time is not None:
        trip.arrival_time = arrival_time
    if price is not None:
        trip.price = price
    if available_seats is not None:
        trip.available_seats = available_seats
    if is_active is not None:
        trip.is_active = is_active

    db.commit()
    db.refresh(trip)
    return trip


def set_trip_active(db: Session, trip_id: int, is_active: bool) -> Trip | None:
    """
    Activate/deactivate a trip without deleting it.

    Args:
        db: SQLAlchemy session.
        trip_id: Trip ID.
        is_active: True to activate, False to deactivate.

    Returns:
        Updated Trip if found, otherwise None.
    """
    return update_trip(db, trip_id, is_active=is_active)


def decrement_trip_seats(db: Session, trip_id: int, seats: int = 1) -> Trip | None:
    """
    Decrease available seats for a trip.

    Important:
        - If available_seats is NULL, this function will do nothing and return the trip.
        - If available_seats would go below 0, it raises ValueError.

    Args:
        db: SQLAlchemy session.
        trip_id: Trip ID.
        seats: Number of seats to decrement.

    Returns:
        Updated Trip if found, otherwise None.

    Raises:
        ValueError: if seats <= 0 or not enough seats available.
    """
    if seats <= 0:
        raise ValueError("seats must be > 0")

    trip = get_trip_by_id(db, trip_id)
    if not trip:
        return None

    if trip.available_seats is None:
        return trip

    if trip.available_seats - seats < 0:
        raise ValueError("not enough available seats")

    trip.available_seats = trip.available_seats - seats
    db.commit()
    db.refresh(trip)
    return trip


def delete_trip(db: Session, trip_id: int) -> bool:
    """
    Permanently delete a trip row.

    Note:
        In many systems you would prefer deactivation instead of deletion.

    Args:
        db: SQLAlchemy session.
        trip_id: Trip ID.

    Returns:
        True if deleted, False if not found.
    """
    trip = get_trip_by_id(db, trip_id)
    if not trip:
        return False
    db.delete(trip)
    db.commit()
    return True
