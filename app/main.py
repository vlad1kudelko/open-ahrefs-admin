from fastapi import FastAPI
import uvicorn
from redis import Redis
from config.settings import settings

app = FastAPI()
rds = Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0)

@app.get('/api/redis')
def api_redis():
    return rds.keys('*')

@app.get('/api/test')
def api_test(text: str):
    return {'text': text}
