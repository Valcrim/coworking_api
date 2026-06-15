from pydantic import BaseModel
from datetime import datetime, time
from typing import List, Optional

class SlotSchema(BaseModel):
    id: int
    room_id: int
    date: datetime
    start: time
    end: time
    booked_by: Optional[int] = None

class BookingSchema(BaseModel):
    booked_by: int | None

class RoomSchema(BaseModel):
    id: int
    slots: List[SlotSchema]