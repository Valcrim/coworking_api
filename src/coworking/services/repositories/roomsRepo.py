from services.repositories.baseRepo import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from models.rooms import RoomBase, SlotBase
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import datetime, time

class RoomRepository(BaseRepository[RoomBase]):
    """ Репозиторий для работы с моделью комнаты в БД. """
    model = RoomBase

    async def create_room(self) -> RoomBase:
        return await self._create()

    async def get_rooms(self) -> list[RoomBase]:        
        rooms = await self._get_all()
        return rooms
    
    async def get_rooms_with_slots(self) -> list[RoomBase]:        
        query = select(self.model).options(selectinload(self.model.slots))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_room(self, id: int) -> RoomBase:
        return await self._get(id)

    async def get_room_with_slots(self, id: int) -> RoomBase:
        query = select(self.model
                ).where(self.model.id == id
                ).options(selectinload(self.model.slots))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def delete_room(self, id: int):
        return await self._delete(id)


class SlotRepository(BaseRepository[SlotBase]):
    """ Репозиторий для работы с моделью слотов в БД. """
    model = SlotBase

    async def create_slot(self, room_id: int, date: datetime, 
                          start: time, end: time) -> SlotBase:
        return await self._create(room_id=room_id, date=date, start=start, end=end)

    async def get_slots(self, room_id: int) -> list[SlotBase]:
        slots = await self.session.get(self.model, room_id)
        return slots
        
    async def get_slot(self, id: int) -> SlotBase:
        return await self._get(id)
    
    async def delete_slot(self, id: int) -> bool:
        return await self._delete(id)

    async def book_slot(self, slot_id: int, user_id: int) -> SlotBase:
        slot = await self.session.get(self.model, slot_id)
        slot.booked_by = user_id
        self.session.add(slot)
        await self.session.commit()
        return slot


