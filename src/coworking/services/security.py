from fastapi import Depends
from fastapi import HTTPException, status
from models import UserBase
from services.repositories.usersRepo import UserRepository
from dependencies.repositories import get_user_repo
from datetime import timedelta, datetime, timezone
from core.jwt_config import settings
from jose import jwt, JWTError
from typing import Literal
from datetime import datetime, timezone

tkn_type = Literal["access", "refresh"]

class SecurityService:
    async def authenticate(login: str, password: str, repo: UserRepository = Depends(get_user_repo)):
        return await repo.authenticate(login, password)
    
    def authorize(self, token) -> UserBase:
        pass

    def _create_token(self, data: dict, tkn_type: tkn_type, timedelta: timedelta) -> str:
        iat = datetime.now(timezone.utc)
        payload = {"iat": iat, 
                  "exp": iat + timedelta,
                  "type": tkn_type}
        payload.update(data)
        token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
        return token
    
    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, "access", timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, "refresh", timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))

    def decode_token(self, token: str) -> dict | None:
        try:
            return jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except JWTError:
            return None

    def is_token_expired(self, token: str) -> bool:
        payload = self.decode_token(token)
        if payload is None:
            return True
        
        exp = payload.get("exp")
        if exp is None:
            return True
        
        now = datetime.now(timezone.utc).timestamp() # Перевод datetime в число секунд с 1970 года
        return exp < now
        

    def validate_token(self, token: str) -> dict | None:
        if self.is_token_expired(token):
            return None
        return self.decode_token(token)