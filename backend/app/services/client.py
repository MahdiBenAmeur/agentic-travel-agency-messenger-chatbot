from __future__ import annotations

from sqlalchemy.orm import Session

from dbmodels.client import Client


def get_client_by_id(db: Session, client_id: int) -> Client | None:
    """
    Fetch a client by internal primary key.

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.

    Returns:
        Client if found, otherwise None.
    """
    return db.query(Client).filter(Client.id == client_id).first()


def get_client_by_psid(db: Session, messenger_psid: str) -> Client | None:
    """
    Fetch a client by Messenger PSID.

    PSID = Page-Scoped ID (unique per user per Facebook page).

    Args:
        db: SQLAlchemy session.
        messenger_psid: Messenger PSID.

    Returns:
        Client if found, otherwise None.
    """
    return db.query(Client).filter(Client.messenger_psid == messenger_psid).first()


def create_client(
    db: Session,
    messenger_psid: str,
    name: str | None = None,
    phone_number: str | None = None,
    national_id: str | None = None,
) -> Client:
    """
    Create a new client row.

    Args:
        db: SQLAlchemy session.
        messenger_psid: Messenger PSID (must be unique).
        name: Optional display name.
        phone_number: Optional phone number.
        national_id: Optional national ID / passport / CIN.

    Returns:
        The created Client (refreshed from DB).
    """
    client = Client(
        messenger_psid=messenger_psid,
        name=name,
        phone_number=phone_number,
        national_id=national_id,
    )
    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_or_create_client(
    db: Session,
    messenger_psid: str,
    name: str | None = None,
) -> Client:
    """
    Fetch client by PSID or create a new one if it doesn't exist.

    Args:
        db: SQLAlchemy session.
        messenger_psid: Messenger PSID.
        name: Optional name used only when creating a new client.

    Returns:
        Existing or newly created Client.
    """
    existing = get_client_by_psid(db, messenger_psid)
    if existing:
        return existing
    return create_client(db, messenger_psid=messenger_psid, name=name)


def update_client(
    db: Session,
    client_id: int,
    *,
    name: str | None = None,
    phone_number: str | None = None,
    national_id: str | None = None,
    messenger_psid: str | None = None,
) -> Client | None:
    """
    Partially update a client row (only provided fields are changed).

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.
        name: New name (optional).
        phone_number: New phone number (optional).
        national_id: New national ID (optional).
        messenger_psid: New PSID (optional, should be rare).

    Returns:
        Updated Client if found, otherwise None.
    """
    client = get_client_by_id(db, client_id)
    if not client:
        return None

    if name is not None:
        client.name = name
    if phone_number is not None:
        client.phone_number = phone_number
    if national_id is not None:
        client.national_id = national_id
    if messenger_psid is not None:
        client.messenger_psid = messenger_psid

    db.commit()
    db.refresh(client)
    return client


def list_clients(db: Session, limit: int = 50, offset: int = 0) -> list[Client]:
    """
    List clients with pagination.

    Args:
        db: SQLAlchemy session.
        limit: Max number of rows.
        offset: Rows to skip.

    Returns:
        List of clients.
    """
    return db.query(Client).order_by(Client.id.desc()).offset(offset).limit(limit).all()


def delete_client(db: Session, client_id: int) -> bool:
    """
    Permanently delete a client row.

    Note:
        Because other tables reference clients (bookings/messages),
        ON DELETE is set to SET NULL in those tables, so deletion is possible.

    Args:
        db: SQLAlchemy session.
        client_id: Internal client id.

    Returns:
        True if deleted, False if not found.
    """
    client = get_client_by_id(db, client_id)
    if not client:
        return False
    db.delete(client)
    db.commit()
    return True
