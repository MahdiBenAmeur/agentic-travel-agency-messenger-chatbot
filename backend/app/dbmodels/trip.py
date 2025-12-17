from sqlalchemy import Column, Integer, Text, TIMESTAMP, Numeric, Boolean, func
from .base import Base


class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True)
    title = Column(Text, nullable=False)

    origin = Column(Text, nullable=False)
    destination = Column(Text, nullable=False)

    departure_time = Column(TIMESTAMP)
    arrival_time = Column(TIMESTAMP)

    price = Column(Numeric)
    available_seats = Column(Integer)

    is_active = Column(Boolean, server_default="true")
    created_at = Column(TIMESTAMP, server_default=func.now())
