from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class BaseRepository[ModelType]():
    """
    Базовый репозиторий для работы с БД.
    Реализует базовые CRUD операции для модели ModelType.
    """
    model: type[ModelType]

    def __init__(self, async_session: AsyncSession):
        self.session = async_session

    def __call__(self): # Позволяет использовать репозиторий как зависимость в FastAPI
        return self

    async def _create(self, **data: dict | None) -> ModelType:
        obj = self.model(**(data or {}))
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def _get_all(self) -> list[ModelType]:
        objs = await self.session.execute(select(self.model))
        return objs.scalars().all()
    
    async def _get(self, id: int) -> ModelType:
        obj = await self.session.get(self.model, id)
        return obj
    
    async def _delete(self, id: int) -> bool:
        obj = await self.session.get(self.model, id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False