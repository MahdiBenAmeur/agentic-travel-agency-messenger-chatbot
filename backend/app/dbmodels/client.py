from sqlalchemy import Column, Integer, Text, TIMESTAMP, func
from .base import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    messenger_psid = Column(Text, unique=True, nullable=False)

    name = Column(Text)
    phone_number = Column(Text)
    national_id = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
