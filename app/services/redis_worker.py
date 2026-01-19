import asyncio
from contextlib import asynccontextmanager

from config.settings import settings
from fastapi import APIRouter, FastAPI
from redis import asyncio as aioredis

redis_client = aioredis.from_url(
    f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}", decode_responses=True
)
router = APIRouter()

KEY_INPUT = "crawler:start_urls"
KEY_OUTPUT = "crawler:items"


@router.get("/addurl")
async def router_addurl(url: str):
    await redis_client.lpush(KEY_INPUT, url)
    return "ok"


@asynccontextmanager
async def lifespan(app: FastAPI):
    task_redis = asyncio.create_task(redis_to_pg())
    yield
    task_redis.cancel()


async def redis_to_pg():
    pass
