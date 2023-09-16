import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import func


def expire_time(days=31):
    now = datetime.datetime.utcnow()
    date = now + datetime.timedelta(days=+days)
    return date.strftime('%Y-%m-%d %H:%M:%S')


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    uuid: Mapped[str] = mapped_column(nullable=False, unique=True)
    protocol: Mapped[str] = mapped_column(nullable=False)
    protocol_detail: Mapped[str] = mapped_column(nullable=False)
    download: Mapped[int] = mapped_column(default=0)
    upload: Mapped[int] = mapped_column(default=0)
    traffic: Mapped[int] = mapped_column(default=0)
    tel_costumer_id: Mapped[int] = mapped_column(default=None, nullable=True)
    active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    expire: Mapped[datetime.datetime] = mapped_column(server_default=expire_time())
