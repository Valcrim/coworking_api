from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from services.repositories.roomsRepo import RoomRepository, SlotRepository
from schemas.rooms import SlotSchema
from dependencies.repositories import get_room_repo, get_slot_repo
from dependencies.types import AdminUser

router = APIRouter(prefix='/rooms', tags=['rooms'])

@router.get('/')
async def get_rooms(repo: RoomRepository = Depends(get_room_repo)):
    """ Получение списка всех комнат с их слотами. """
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
    """ Получение информации о комнате с ее слотами. """
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