from fastapi import Depends
from fastapi import HTTPException, status
from services.security import SecurityService
from services.repositories.usersRepo import UserRepository
from dependencies.security import get_security_service
from dependencies.repositories import get_user_repo
from dependencies.slots import get_slot_owner
from models.users import UserBase


async def get_current_user(
        token: str,
        user_repo: UserRepository = Depends(get_user_repo),
        security: SecurityService = Depends(get_security_service),
        ) -> UserBase:
    """ Получение текущего пользователя по access токену. """
    payload = security.validate_token(token)
    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                         "Token is not valid or expired")
    try:
        uid = payload["sub"]
    except KeyError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                             "Token is not valid") 

    user = await user_repo.get_user(int(uid))
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                             "User not found")
    return user


async def get_admin(
        user: UserBase = Depends(get_current_user)
        ) -> UserBase | None:
    """ Проверка наличия прав администратора у пользователя. """
    if not user.is_admin:
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                             "Insufficient permissions. Admin rights are required")
    return user


async def get_admin_or_owner(
        owner_id: int | None = Depends(get_slot_owner),
        user: UserBase = Depends(get_current_user)
        ) -> UserBase | None:
    """ Проверка наличия прав администратора у пользователя. """
    if owner_id is None:
        return user
    if not (user.is_admin or user.id == owner_id):
        raise HTTPException(status.HTTP_403_FORBIDDEN, 
                             "Insufficient permissions. Admin rights or slot ownership are required")
    return user