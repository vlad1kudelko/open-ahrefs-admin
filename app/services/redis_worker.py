import asyncio
from contextlib import asynccontextmanager

import redis.asyncio as redis
from config.settings import settings
from db.engine import async_session_factory, get_session
from db.models import Link, Task
from fastapi import APIRouter, Depends, FastAPI
from schemas.rlink import Rlink
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

redis_client = redis.Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT))
router = APIRouter()

KEY_INPUT = "crawler:start_urls"
KEY_OUTPUT = "crawler:items"


@router.get("/clearall")
async def router_clearall(db: AsyncSession = Depends(get_session)):
    await redis_client.delete("crawler:start_urls")
    await redis_client.delete("crawler:dupefilter")
    await redis_client.delete("crawler:requests")
    await redis_client.delete("crawler:items")
    await db.execute(delete(Link))
    await db.execute(delete(Task))
    await db.commit()
    return "ok"


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
    while True:
        redis_str = await redis_client.rpop(KEY_OUTPUT)
        if redis_str:
            rlink = Rlink.model_validate_json(redis_str)
            async with async_session_factory() as session:
                stmt = select(Task).where(Task.name == rlink.task)
                result = await session.execute(stmt)
                task = result.scalar_one_or_none()
                if not task:
                    task = Task(name=rlink.task)
                    session.add(task)
                    await session.flush()
                link = Link(
                    url=rlink.url,
                    status=rlink.status,
                    title=rlink.title,
                    redirect_urls=rlink.redirect_urls,
                    referer=rlink.referer,
                    task_id=task.task_id,
                )
                session.add(link)
                await session.commit()
        await asyncio.sleep(0.1)
