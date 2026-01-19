from admin.router import router as admin_router
from fastapi import FastAPI
from services.redis_worker import lifespan
from services.redis_worker import router as redis_router

app = FastAPI(lifespan=lifespan)
app.include_router(admin_router, prefix="/admin")
app.include_router(redis_router, prefix="/redis")
