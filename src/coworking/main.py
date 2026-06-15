from fastapi import FastAPI
from contextlib import asynccontextmanager
import uvicorn
from core.db import init_db
from api.rooms import router as rooms_router
from api.users import router as users_router
from api.booking import router as booking_router
from api.auth import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Начало работы")
    await init_db()
    yield
    print("Завершение работы")

app = FastAPI(lifespan=lifespan)
app.include_router(rooms_router)
app.include_router(users_router)
app.include_router(booking_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
