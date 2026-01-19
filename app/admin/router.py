from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/links", response_class=HTMLResponse)
def router_links(request: Request):
    return templates.TemplateResponse(
        "links/list.html", {"request": request, "hello": "world"}
    )
