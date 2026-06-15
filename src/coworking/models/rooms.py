from typing import Optional
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from datetime import datetime, time

class SlotBase(Base):
    __tablename__ = 'slots'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime] = mapped_column(nullable=False)
    start: Mapped[time] = mapped_column(nullable=False)
    end: Mapped[time] = mapped_column(nullable=False)
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id"), nullable=False)
    booked_by: Mapped[Optional[int]] = mapped_column(default=None)
    room = relationship("RoomBase", back_populates="slots") 

class RoomBase(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    slots = relationship("SlotBase", back_populates="room", cascade="all, delete-orphan")