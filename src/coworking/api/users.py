from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from services.repositories.usersRepo import UserRepository
from services.repositories.roomsRepo import SlotRepository
from dependencies.types import CurrentUser
from dependencies.repositories import get_user_repo, get_slot_repo


router = APIRouter(tags=['users'])

@router.get('/users')
async def get_users(
        repo: UserRepository = Depends(get_user_repo)
        ):
    """ Получение списка всех пользователей. """
    users = await repo.get_users()
    return users

@router.get('/users/{user_id}')
async def get_user(
        user_id: int,
        repo: UserRepository = Depends(get_user_repo)
        ):
    """ Получение информации о пользователе. """
    user = await repo.get_user(user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            "User with this id does not exist")
    return user

@router.get('/me')
async def get_current_user(
        user: CurrentUser
        ):
    """ Получение информации о текущем пользователе. """
    return user

@router.get('/users/{user_id}/slots', tags=['slots'])
async def get_user_slots(
    user_id: int,
    repo: SlotRepository = Depends(get_slot_repo)
    ):
    """ Получение списка всех слотов, забронированных пользователем. """
    slots = await repo.get_user_slots(user_id)
    return slots


@router.get('/me/slots', tags=['slots'])
async def get_current_user_slots(
        user: CurrentUser,
        repo: SlotRepository = Depends(get_slot_repo)
        ):
    """ Получение списка всех слотов, забронированных текущим пользователем. """
    slots = await repo.get_user_slots(user.id)
    return slots
