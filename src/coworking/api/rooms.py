from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from services.repositories.roomsRepo import RoomRepository, SlotRepository
from services.repositories.usersRepo import UserRepository
from services.security import SecurityService
from schemas.rooms import RoomSchema, SlotSchema, BookingSchema
from models.users import UserBase
from dependencies.repositories import get_room_repo, get_slot_repo, get_user_repo
from dependencies.security import get_security_service
from dependencies.types import CurrentUser, AdminUser, OwnerOrAdmin

router = APIRouter(prefix='/rooms', tags=['rooms'])

@router.get('/')
async def get_rooms(repo: RoomRepository = Depends(get_room_repo)):
    rooms = await repo.get_rooms_with_slots()
    return rooms

@router.post('/')
async def create_room(
        user: AdminUser,
        room_repo: RoomRepository = Depends(get_room_repo)
        ):
    """ 
    Создание новой комнаты.
    Метод защищен. Доступно только администраторам.
    """
    room = await room_repo.create_room()
    return room

@router.get('/{room_id}')
async def get_room(
        room_id: int, 
        repo: RoomRepository = Depends(get_room_repo)
        ):
    room = await repo.get_room_with_slots(room_id)
    if not room: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                             f"Room with this id is does not exist")
    return room

@router.delete('/{room_id}')
async def delete_room(
        user: AdminUser,
        room_id: int, 
        repo: RoomRepository = Depends(get_room_repo)
        ):
    """ 
    Удаление комнаты.
    Метод защищен. Доступно только администраторам.
    """
    room = await repo.get_room(room_id)
    if not room: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                             f"Room with this id is does not exist")
    if await repo.delete_room(room_id):
        return {"detail": "Room deleted successfully"}
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             "Failed to delete the room")

@router.post('/{room_id}/slots')
async def create_slot(
        user: AdminUser,
        room_id: int,
        data: SlotSchema, 
        repo: SlotRepository = Depends(get_slot_repo)
        ):
    """ 
    Создание нового слота для комнаты.
    Метод защищен. Доступно только администраторам.
    """
    slot = await repo.create_slot(room_id, data.start, data.end)
    return slot