from services.client import (
    create_client,
    get_client_by_psid,
    get_or_create_client,
    update_client,
)


def test_create_and_get_by_psid(db_session):
    c = create_client(db_session, messenger_psid="psid_1", name="Mahdi")
    got = get_client_by_psid(db_session, "psid_1")
    assert got is not None
    assert got.id == c.id
    assert got.name == "Mahdi"


def test_get_or_create(db_session):
    c1 = get_or_create_client(db_session, messenger_psid="psid_2", name="A")
    c2 = get_or_create_client(db_session, messenger_psid="psid_2", name="B")
    assert c1.id == c2.id
    assert c2.name == "A"  # name shouldn't change on second call


def test_update_client_optional_fields(db_session):
    c = create_client(db_session, messenger_psid="psid_3")
    updated = update_client(
        db_session,
        c.id,
        name="NewName",
        phone_number="123",
        national_id="CIN123",
    )
    assert updated is not None
    assert updated.name == "NewName"
    assert updated.phone_number == "123"
    assert updated.national_id == "CIN123"
