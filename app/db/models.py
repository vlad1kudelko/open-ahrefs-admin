from db.engine import engine
from sqlalchemy.orm import DeclarativeBase, Mapped


class Base(DeclarativeBase):
    pass


class Link(Base):
    url: Mapped[str]


Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
