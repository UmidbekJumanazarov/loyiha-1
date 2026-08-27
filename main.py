from contextlib import asynccontextmanager

from fastapi import FastAPI

from order_service.api.router import router as orders_router
from order_service.infrastructure.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="E-Commerce Buyurtmalarni Boshqarish API", lifespan=lifespan)

app.include_router(orders_router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}