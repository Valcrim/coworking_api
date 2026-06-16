from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException, status
from schemas.users import UserSchema, CredentialsSchema
from services.repositories.usersRepo import UserRepository
from services.security import SecurityService
from dependencies.repositories import get_user_repo
from dependencies.security import get_security_service

router = APIRouter(prefix="/auth", tags=['auth'])


@router.post('/register')
async def register(
        data: UserSchema, 
        repo: UserRepository = Depends(get_user_repo)
        ):
    """ Регистрация нового пользователя. """
    user = await repo.get_user_by_username(data.username)
    if user is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, 
                             "User with this username already exists")
    
    user = await repo.create_user(data.username, data.password, data.is_admin)
    return user

@router.post('/login')
async def login(
        data: CredentialsSchema, 
        repo: UserRepository = Depends(get_user_repo),
        security: SecurityService = Depends(get_security_service)
        ):
    """ 
    Первичная аутентификация пользователя и выдача JWT токенов.
    
    Метод принимает логин и пароль, проверяет их и при успешной аутентификации 
    возвращает пару токенов: access и refresh. 
    
    Access токен используется для доступа к защищенным ресурсам
    Refresh токен используется для получения нового access токена после его истечения.
    """
    user = await repo.authenticate(data.login, data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Incorrect username or password")
    
    access_token = security.create_access_token({"sub": str(user.id)})
    refresh_token = security.create_refresh_token({"sub": str(user.id)})
    return { 
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post('/refresh')
async def refresh_access_token(
        refresh_token: str,
        security: SecurityService = Depends(get_security_service)
        ):
    """ Получение нового access токена по refresh токену."""
    payload = security.validate_token(refresh_token)
    if payload is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Token is not valid or expired")
    try:
        tkn_type = payload["type"]
        uid = payload["sub"]
    except KeyError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Token is not valid")
    
    if tkn_type != "refresh":
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            "Token is not a refresh token")
    
    new_access_token = security.create_access_token({"sub": uid})
    return {"access_token": new_access_token}