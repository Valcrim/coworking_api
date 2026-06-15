from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from services.repositories.roomsRepo import SlotRepository
from schemas.rooms import BookingSchema
from dependencies.repositories import get_slot_repo
from dependencies.types import OwnerOrAdmin

router = APIRouter(prefix='/booking', tags=['booking'])


@router.patch('/slots/{slot_id}')
async def update_slot(
        user: OwnerOrAdmin,
        slot_id: int, 
        repo: SlotRepository = Depends(get_slot_repo)
        ):
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