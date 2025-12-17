from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, func
from .base import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)

    client_id = Column(Integer, ForeignKey("clients.id", ondelete="SET NULL"))
    direction = Column(Text, nullable=False)  # in|out
    content = Column(Text)

    created_at = Column(TIMESTAMP, server_default=func.now())
