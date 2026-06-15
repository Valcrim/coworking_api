from pydantic_settings import BaseSettings, SettingsConfigDict

class JWTSettings(BaseSettings):
    SECRET_KEY: str 
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    model_config = SettingsConfigDict(env_file=".env", extra='allow')


settings = JWTSettings()