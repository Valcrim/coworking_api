from sqlalchemy.orm import Mapped, mapped_column
from models.base import Base

class UserBase(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    is_admin: Mapped[bool] = mapped_column(default=False)