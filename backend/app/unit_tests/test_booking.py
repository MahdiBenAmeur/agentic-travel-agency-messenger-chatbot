import pytest

from services.booking import (
    cancel_booking,
    confirm_booking,
    create_booking,
    list_bookings_by_client,
)
from services.client import create_client
from services.trip import create_trip


def test_create_booking_and_list_by_client(db_session):
    c = create_client(db_session, messenger_psid="psid_b1")
    t = create_trip(db_session, title="Trip", origin="Tunis", destination="Paris", available_seats=10)

    b = create_booking(db_session, client_id=c.id, trip_id=t.id, passengers_count=2, contact_phone="999", notes="note")
    assert b.status == "pending"
    assert b.passengers_count == 2

    lst = list_bookings_by_client(db_session, c.id)
    assert len(lst) == 1
    assert lst[0].id == b.id


def test_confirm_and_cancel_booking(db_session):
    c = create_client(db_session, messenger_psid="psid_b2")
    t = create_trip(db_session, title="Trip2", origin="Tunis", destination="Rome", available_seats=10)

    b = create_booking(db_session, client_id=c.id, trip_id=t.id)
    b2 = confirm_booking(db_session, b.id)
    assert b2 is not None
    assert b2.status == "confirmed"

    b3 = cancel_booking(db_session, b.id)
    assert b3 is not None
    assert b3.status == "cancelled"


def test_invalid_passengers_count(db_session):
    c = create_client(db_session, messenger_psid="psid_b3")
    t = create_trip(db_session, title="Trip3", origin="Tunis", destination="Paris", available_seats=10)

    with pytest.raises(ValueError):
        create_booking(db_session, client_id=c.id, trip_id=t.id, passengers_count=0)
