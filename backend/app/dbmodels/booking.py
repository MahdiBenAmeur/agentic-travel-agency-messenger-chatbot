from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from .base import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id", ondelete="SET NULL"))
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="SET NULL"))

    status = Column(Text, server_default="pending")  # pending|confirmed|cancelled

    passengers_count = Column(Integer, server_default="1")
    contact_phone = Column(Text)
    notes = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
