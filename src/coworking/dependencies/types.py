from fastapi import Depends
from dependencies.auth import get_current_user,  get_admin, get_admin_or_owner
from typing import Annotated
from models.users import UserBase

CurrentUser = Annotated[UserBase, Depends(get_current_user)]
AdminUser = Annotated[UserBase, Depends(get_admin)]
OwnerOrAdmin = Annotated[UserBase, Depends(get_admin_or_owner)]