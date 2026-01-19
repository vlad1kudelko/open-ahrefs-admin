from pydantic import BaseModel


class Rlink(BaseModel):
    url: str
    status: int
    title: str | None
    redirect_urls: list[str]
    referer: str
    task: str
