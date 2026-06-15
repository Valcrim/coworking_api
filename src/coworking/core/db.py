from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from core.db_config import settings
from models.base import Base
from typing import AsyncGenerator
from datetime import datetime, time, timezone
from services.repositories.roomsRepo import RoomRepository, SlotRepository
from services.repositories.usersRepo import UserRepository
 
async_engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL,
    pool_size=10,
    max_overflow=5,
    echo=True
    )

async_session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine, 
    autocommit=False,
    autoflush=False,
    expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def _fill_db_with_defalut_data():    
    rooms_count = 3
    days = [datetime(day=i, month=6, year=2026) for i in range(1,8)]
    default_slots = [
        {"start": time(hour=9),  "end": time(hour=10, minute=30)},
        {"start": time(hour=11), "end": time(hour=12, minute=30)},
        {"start": time(hour=14), "end": time(hour=14, minute=45)},
        {"start": time(hour=15), "end": time(hour=15, minute=45)},
        {"start": time(hour=16), "end": time(hour=17, minute=30)},
        {"start": time(hour=18), "end": time(hour=20)},
    ]
    users = [ 
        {"username": "admin", "password": "superpass", "is_admin": True},
        {"username": "Vasya", "password": "qwerty", "is_admin": False},
    ]

    async with async_session() as db:
        room_repo = RoomRepository(db)
        slot_repo = SlotRepository(db)
        user_repo = UserRepository(db)
        for i in range(1, rooms_count+1):
            await room_repo.create_room()
            for day in days:
                for slot in default_slots:
                    await slot_repo.create_slot(i, day, slot["start"], slot["end"])
        for user in users:
            await user_repo.create_user(user["username"], user["password"], user['is_admin'])


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    await _fill_db_with_defalut_data()