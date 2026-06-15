from pydantic import BaseModel
from pydantic import Field

class UserSchema(BaseModel):
    username: str = Field(min_length=1, max_length=64)
    password: str = Field(min_length=8, max_length=64)
    is_admin: bool = Field(default=False)

class CredentialsSchema(BaseModel):
    login: str = Field()
    password: str = Field()