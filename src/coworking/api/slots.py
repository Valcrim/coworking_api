from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from services.repositories.roomsRepo import SlotRepository
from dependencies.repositories import get_slot_repo
from dependencies.types import OwnerOrAdmin, AdminUser


router = APIRouter(prefix='/slots', tags=['slots'])


@router.patch('/{slot_id}', tags=['slots', 'booking'])
async def update_slot(
        user: OwnerOrAdmin,
        slot_id: int, 
        repo: SlotRepository = Depends(get_slot_repo)
        ):
    """ 
    Бронирование и снятие брони со слота.

    Метод защищен.
    Снять бронь может только владелец брони или администратор.
    Свободные слот может забронировать любой пользователь.
    """
    slot = await repo.get_slot(slot_id)
    if not slot:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                             "Slot with this id does not exist")
    
    if slot.booked_by is None:
        booked_by = user.id
    else:
        booked_by = None
    slot = await repo.book_slot(slot_id, booked_by)
    return slot


@router.delete("/{slot_id}")
async def delete_slot(
        user: AdminUser,
        slot_id: int,
        repo: SlotRepository = Depends(get_slot_repo)
        ):
    """ 
    Удаление слота.
    Метод защищен. Доступно только администраторам.
    """
    slot = await repo.get_slot(slot_id)
    if not slot: 
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                             f"Slot with this id is does not exist")
    if await repo.delete_slot(slot_id):
        return {"detail": "Slot deleted successfully"}
    else:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, 
                             "Failed to delete the slot")