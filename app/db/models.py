from datetime import datetime
from typing import Annotated

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

created_at = Annotated[
    datetime,
    mapped_column(sa.DateTime, server_default=sa.text("TIMEZONE('utc', now())")),
]


class Base(DeclarativeBase):
    metadata = sa.MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Task(Base):
    __tablename__ = "tasks"
    task_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    name: Mapped[str] = mapped_column(sa.Text, unique=True)
    link: Mapped["Link"] = relationship("Link", back_populates="task")


class Link(Base):
    __tablename__ = "links"
    __table_args__ = (
        sa.CheckConstraint(
            "(status >= 100 AND status < 600) OR status = 888 OR status = 999",
            name="status_valid",
        ),
    )
    link_id: Mapped[int] = mapped_column(sa.BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    url: Mapped[str] = mapped_column(sa.Text)
    status: Mapped[int] = mapped_column(sa.Integer)
    title: Mapped[str | None] = mapped_column(sa.Text)
    redirect_urls: Mapped[list[str]] = mapped_column(ARRAY(sa.Text))
    referer: Mapped[str] = mapped_column(sa.Text)
    task_id: Mapped[int] = mapped_column(sa.BigInteger, sa.ForeignKey("tasks.task_id"))
    task: Mapped["Task"] = relationship("Task", back_populates="link")
