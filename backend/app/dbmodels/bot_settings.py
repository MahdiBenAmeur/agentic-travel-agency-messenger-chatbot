from sqlalchemy import Column, Integer, Boolean, TIMESTAMP, func
from .base import Base


class BotSettings(Base):
    __tablename__ = "bot_settings"

    id = Column(Integer, primary_key=True)
    is_enabled = Column(Boolean, server_default="true")
    updated_at = Column(TIMESTAMP, server_default=func.now())
