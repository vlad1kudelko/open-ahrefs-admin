from contextlib import asynccontextmanager

from admin.views import LinkAdmin, TaskAdmin
from db.engine import engine
from fastapi import FastAPI
from sqladmin import Admin

#  from config.settings import settings
#  from redis import Redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)
admin = Admin(app, engine)

admin.add_view(TaskAdmin)
admin.add_view(LinkAdmin)

#  rds = Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0)
