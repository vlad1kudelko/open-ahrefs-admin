import asyncio
from contextlib import asynccontextmanager

import redis.asyncio as redis
from config.settings import settings
from db.engine import async_session_factory, get_session
from db.models import Link, Task
from fastapi import APIRouter, Depends, FastAPI, Form
from fastapi.responses import RedirectResponse
from schemas.rlink import Rlink
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

redis_client = redis.Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT))
router = APIRouter()

KEY_INPUT = "crawler:start_urls"
KEY_OUTPUT = "crawler:items"


@router.post("/clearall")
async def router_clearall(db: AsyncSession = Depends(get_session)):
    await redis_client.delete("crawler:start_urls")
    await redis_client.delete("crawler:bloomfilter")
    await redis_client.delete("crawler:requests")
    await redis_client.delete("crawler:items")
    await db.execute(delete(Link))
    await db.execute(delete(Task))
    await db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.post("/addurl")
async def router_addurl(url: str = Form()):
    await redis_client.lpush(KEY_INPUT, url)
    return RedirectResponse(url="/", status_code=303)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task_redis = asyncio.create_task(redis_to_pg())
    yield
    task_redis.cancel()


async def redis_to_pg():
    while True:
        items = []
        try:
            for _ in range(100):
                item = await redis_client.rpop(KEY_OUTPUT)
                if not item:
                    break
                items.append(item)
        except Exception:
            print("Redis не отвечает, ожидание...")
            await asyncio.sleep(1)
            continue
        if not items:
            await asyncio.sleep(1)
            continue
        rlinks = [Rlink.model_validate_json(i) for i in items]
        async with async_session_factory() as session:
            task_names = list(set(r.task for r in rlinks))
            stmt = select(Task).where(Task.name.in_(task_names))
            result = await session.execute(stmt)
            existing_tasks = {t.name: t for t in result.scalars().all()}
            for name in task_names:
                if name not in existing_tasks:
                    new_task = Task(name=name)
                    session.add(new_task)
                    existing_tasks[name] = new_task
            if session.new:
                await session.flush()
            links_to_add = [
                Link(
                    url=r.url,
                    status=r.status,
                    title=r.title,
                    redirect_urls=r.redirect_urls,
                    referer=r.referer,
                    task_id=existing_tasks[r.task].task_id,
                )
                for r in rlinks
            ]
            session.add_all(links_to_add)
            await session.commit()
        print(f"Обработано записей: {len(items)}")
        await asyncio.sleep(0.1)
