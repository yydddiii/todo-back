from fastapi import FastAPI

from contextlib import asynccontextmanager

from database import create_tables

from router.tasks import router as tasks_router
from router.users import router as users_router
from router.categories import router as categoies_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("start")
    await create_tables()
    print("create table")
    yield
    print("close")


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)

app.include_router(users_router)

app.include_router(categoies_router)
