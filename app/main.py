from contextlib import asynccontextmanager

from config.settings import settings
from fastapi import FastAPI
from redis import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
rds = Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0)
