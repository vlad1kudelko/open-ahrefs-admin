from contextlib import asynccontextmanager

from db.engine import engine
from db.models import Link
from fastapi import FastAPI
from sqladmin import Admin, ModelView

#  from config.settings import settings
#  from redis import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


class LinkAdmin(ModelView, model=Link):
    column_list = [
        Link.url,
        Link.created_at,
    ]


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)

admin.add_view(LinkAdmin)

#  rds = Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0)
