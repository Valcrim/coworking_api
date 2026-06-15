from fastapi import Depends
from fastapi import HTTPException, status
from dependencies.repositories import get_slot_repo
from services.repositories.roomsRepo import SlotRepository

async def get_slot_owner(
        slot_id: int,
        repo: SlotRepository = Depends(get_slot_repo)
        ) -> int | None:
    slot = await repo.get_slot(slot_id)
    if not slot:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                             "Slot with this id does not exist")
    return slot.booked_by