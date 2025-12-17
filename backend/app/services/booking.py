from __future__ import annotations

from sqlalchemy.orm import Session

from dbmodels.booking import Booking


VALID_STATUSES = {"pending", "confirmed", "cancelled"}


def create_booking(
    db: Session,
    client_id: int,
    trip_id: int,
    passengers_count: int = 1,
    contact_phone: str | None = None,
    notes: str | None = None,
) -> Booking:
    """
    Create a booking for a client on a trip.

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.
        trip_id: Internal trip id.
        passengers_count: Number of passengers/seats for this booking.
        contact_phone: Optional phone for this booking (can differ from client phone).
        notes: Optional free text (names, requirements, etc).

    Returns:
        The created Booking (refreshed from DB).

    Raises:
        ValueError: if passengers_count <= 0.
    """
    if passengers_count <= 0:
        raise ValueError("passengers_count must be > 0")

    booking = Booking(
        client_id=client_id,
        trip_id=trip_id,
        status="pending",
        passengers_count=passengers_count,
        contact_phone=contact_phone,
        notes=notes,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_booking_by_id(db: Session, booking_id: int) -> Booking | None:
    """
    Fetch a booking by primary key.

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.

    Returns:
        Booking if found, otherwise None.
    """
    return db.query(Booking).filter(Booking.id == booking_id).first()


def list_bookings(
    db: Session,
    limit: int = 50,
    offset: int = 0,
) -> list[Booking]:
    """
    List bookings with pagination.

    Args:
        db: SQLAlchemy session.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of bookings.
    """
    return db.query(Booking).order_by(Booking.id.desc()).offset(offset).limit(limit).all()


def list_bookings_by_client(
    db: Session,
    client_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Booking]:
    """
    List bookings for a specific client.

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of client bookings.
    """
    return (
        db.query(Booking)
        .filter(Booking.client_id == client_id)
        .order_by(Booking.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def list_bookings_by_trip(
    db: Session,
    trip_id: int,
    limit: int = 50,
    offset: int = 0,
) -> list[Booking]:
    """
    List bookings for a specific trip.

    Args:
        db: SQLAlchemy session.
        trip_id: Internal trip id.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of trip bookings.
    """
    return (
        db.query(Booking)
        .filter(Booking.trip_id == trip_id)
        .order_by(Booking.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def update_booking(
    db: Session,
    booking_id: int,
    *,
    passengers_count: int | None = None,
    contact_phone: str | None = None,
    notes: str | None = None,
) -> Booking | None:
    """
    Partially update non-status booking fields.

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.
        passengers_count: New passengers count (optional).
        contact_phone: New contact phone (optional).
        notes: New notes (optional).

    Returns:
        Updated Booking if found, otherwise None.

    Raises:
        ValueError: if passengers_count is provided and <= 0.
    """
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None

    if passengers_count is not None:
        if passengers_count <= 0:
            raise ValueError("passengers_count must be > 0")
        booking.passengers_count = passengers_count

    if contact_phone is not None:
        booking.contact_phone = contact_phone

    if notes is not None:
        booking.notes = notes

    db.commit()
    db.refresh(booking)
    return booking


def set_booking_status(db: Session, booking_id: int, status: str) -> Booking | None:
    """
    Set booking status.

    Status values:
        pending | confirmed | cancelled

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.
        status: New status.

    Returns:
        Updated Booking if found, otherwise None.

    Raises:
        ValueError: if status is not one of the valid statuses.
    """
    if status not in VALID_STATUSES:
        raise ValueError(f"invalid status: {status}")

    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return None

    booking.status = status
    db.commit()
    db.refresh(booking)
    return booking


def confirm_booking(db: Session, booking_id: int) -> Booking | None:
    """
    Mark a booking as confirmed.

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.

    Returns:
        Updated Booking if found, otherwise None.
    """
    return set_booking_status(db, booking_id, "confirmed")


def cancel_booking(db: Session, booking_id: int) -> Booking | None:
    """
    Mark a booking as cancelled.

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.

    Returns:
        Updated Booking if found, otherwise None.
    """
    return set_booking_status(db, booking_id, "cancelled")


def delete_booking(db: Session, booking_id: int) -> bool:
    """
    Permanently delete a booking.

    Args:
        db: SQLAlchemy session.
        booking_id: Booking id.

    Returns:
        True if deleted, False if not found.
    """
    booking = get_booking_by_id(db, booking_id)
    if not booking:
        return False
    db.delete(booking)
    db.commit()
    return True
