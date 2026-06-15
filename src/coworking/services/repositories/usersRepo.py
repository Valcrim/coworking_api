from services.repositories.baseRepo import BaseRepository
from models.users import UserBase
from sqlalchemy import select
import hashlib

class UserRepository(BaseRepository[UserBase]):
    """ Репозиторий для работы с моделью пользователя в БД. """
    model = UserBase

    async def create_user(self, username, password, is_admin=False) -> UserBase:
        hashed_password = self._hash(password)
        return await self._create(username=username, password=hashed_password, is_admin=is_admin)

    async def get_users(self) -> list[UserBase]:
        return await self._get_all()

    async def get_user(self, id) -> UserBase | None:
        return await self._get(id)

    async def get_user_by_username(self, username: str) -> UserBase | None:
        query = select(self.model).where(self.model.username == username)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user

    def _hash(self, string: str):
        h = hashlib.sha256()
        h.update(string.encode())
        return h.hexdigest()

    async def authenticate(self, login, password) -> UserBase | None:
        user = await self.get_user_by_username(login)
        hashed_password = self._hash(password)

        if user and user.password == hashed_password:
            return user
        return None
