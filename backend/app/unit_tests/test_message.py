from services.client import create_client
from services.message import get_recent_messages, get_recent_messages_chronological, log_message


def test_log_and_get_recent(db_session):
    c = create_client(db_session, messenger_psid="psid_m1")

    log_message(db_session, client_id=c.id, direction="in", content="hello")
    log_message(db_session, client_id=c.id, direction="out", content="hi")

    recent = get_recent_messages(db_session, client_id=c.id, limit=10)
    assert len(recent) == 2
    assert recent[0].content == "hi"      # newest first
    assert recent[1].content == "hello"


def test_recent_chronological(db_session):
    c = create_client(db_session, messenger_psid="psid_m2")

    log_message(db_session, client_id=c.id, direction="in", content="1")
    log_message(db_session, client_id=c.id, direction="out", content="2")

    msgs = get_recent_messages_chronological(db_session, client_id=c.id, limit=10)
    assert [m.content for m in msgs] == ["1", "2"]
