from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from services.repositories.roomsRepo import RoomRepository, SlotRepository
from services.repositories.usersRepo import UserRepository
from core.db import get_db


def get_room_repo(db: AsyncSession = Depends(get_db)) -> RoomRepository:
    repository = RoomRepository(db)
    return repository


def get_slot_repo(db: AsyncSession = Depends(get_db)) -> SlotRepository:
    repository = SlotRepository(db)
    return repository


def get_user_repo(db: AsyncSession = Depends(get_db)) -> UserRepository:
    repository = UserRepository(db)
    return repository