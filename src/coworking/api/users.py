from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from schemas.users import UserSchema, CredentialsSchema
from services.repositories.usersRepo import UserRepository
from services.security import SecurityService
from dependencies.repositories import get_user_repo
from dependencies.security import get_security_service

router = APIRouter(tags=['users'])

@router.get('/users')
async def get_users(
        repo: UserRepository = Depends(get_user_repo)
        ):
    users = await repo.get_users()
    return users