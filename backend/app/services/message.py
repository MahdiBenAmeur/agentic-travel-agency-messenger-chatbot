from sqlalchemy.orm import Session
from dbmodels.message import Message


def log_message(
    db: Session,
    *,
    client_id: int | None,
    direction: str,
    content: str | None,
) -> Message:
    """
    Log a message (incoming or outgoing).

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id (can be None).
        direction: "in" or "out".
        content: Message text.

    Returns:
        Created Message.
    """
    msg = Message(
        client_id=client_id,
        direction=direction,
        content=content,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def get_recent_messages(
    db: Session,
    *,
    client_id: int,
    limit: int = 20,
) -> list[Message]:
    """
    Get recent conversation history for a client
    (both user and bot messages).

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.
        limit: Number of latest messages to fetch.

    Returns:
        List of messages ordered from newest to oldest.
    """
    return (
        db.query(Message)
        .filter(Message.client_id == client_id)
        .order_by(Message.id.desc())
        .limit(limit)
        .all()
    )
def get_recent_messages_chronological(
    db: Session,
    *,
    client_id: int,
    limit: int = 20,
) -> list[Message]:
    """
    Get recent messages ordered from oldest to newest (better for building context).
    """
    msgs = (
        db.query(Message)
        .filter(Message.client_id == client_id)
        .order_by(Message.id.desc())
        .limit(limit)
        .all()
    )
    return list(reversed(msgs))
