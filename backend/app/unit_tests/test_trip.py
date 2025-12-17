from datetime import datetime, timedelta

from services.trip import (
    create_trip,
    decrement_trip_seats,
    get_trip_by_id,
    search_trips,
    set_trip_active,
    update_trip,
)


def test_create_and_get_trip(db_session):
    t = create_trip(db_session, title="Tunis → Paris", origin="Tunis", destination="Paris", available_seats=10)
    got = get_trip_by_id(db_session, t.id)
    assert got is not None
    assert got.title == "Tunis → Paris"
    assert got.available_seats == 10


def test_search_trips_filters(db_session):
    now = datetime.utcnow()
    create_trip(db_session, title="A", origin="Tunis", destination="Paris", departure_time=now, price=100, available_seats=5)
    create_trip(db_session, title="B", origin="Tunis", destination="Rome", departure_time=now + timedelta(days=1), price=200, available_seats=1)

    res = search_trips(db_session, origin="Tunis", destination="Paris", max_price=150, min_seats=2)
    assert len(res) == 1
    assert res[0].destination == "Paris"


def test_update_and_deactivate(db_session):
    t = create_trip(db_session, title="X", origin="Tunis", destination="Paris", available_seats=3)
    updated = update_trip(db_session, t.id, title="Y")
    assert updated is not None
    assert updated.title == "Y"

    deactivated = set_trip_active(db_session, t.id, False)
    assert deactivated is not None
    assert deactivated.is_active is False


def test_decrement_seats(db_session):
    t = create_trip(db_session, title="Seats", origin="Tunis", destination="Paris", available_seats=2)
    t2 = decrement_trip_seats(db_session, t.id, seats=1)
    assert t2 is not None
    assert t2.available_seats == 1
