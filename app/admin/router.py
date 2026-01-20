from db.engine import get_session
from db.models import Link
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/links", response_class=HTMLResponse)
async def router_links(
    request: Request,
    page: int = Query(1, ge=1),
    size: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    # 1. Рассчитываем отступ
    offset_val = (page - 1) * size
    # 2. Получаем данные
    links_query = select(Link).order_by(Link.link_id).offset(offset_val).limit(size)
    result = await db.execute(links_query)
    links = result.scalars().all()
    # 3. Получаем количество строк
    total_query = select(func.count()).select_from(Link)
    total_result = await db.execute(total_query)
    total_count = total_result.scalar()
    # 4. Рассчитываем общее кол-во страниц
    total_pages = (total_count + size - 1) // size
    return templates.TemplateResponse(
        "links/list.html",
        {
            "request": request,
            "links": links,
            "page": page,
            "size": size,
            "total_pages": total_pages,
            "total_count": total_count,
        },
    )
