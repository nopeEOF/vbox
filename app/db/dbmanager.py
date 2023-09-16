import json
from app.utils.stats import UsersUsage
from app.db import database
from app.v2ray.v2call import VMessUser
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.tables import Users
from collections.abc import AsyncIterator
from sqlalchemy import select, update
from v2client.v2ray import stats
from app.utils import stats as mystats
from typing import List


async def get_user(email: str) -> Users | bool:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        query = select(Users).where(Users.email == email)
        result = await session.execute(query)
        if user := result.scalars().first():
            return user
        else:
            return False


async def get_session():
    async_iterator: AsyncIterator[AsyncSession] = database.session()
    return await anext(async_iterator)


async def db_add_vmess_user(user: VMessUser) -> mystats.Detail:
    if not await get_user(email=user.email):
        async_session: AsyncSession = await get_session()
        protocol_detail = str(json.dumps(vars(user)))
        async with async_session.__call__() as session:
            async with session.begin():
                session.add(Users(
                    email=user.email,
                    uuid=user.userUuid,
                    active=True,
                    protocol="vmess",
                    protocol_detail=protocol_detail
                ))
        return mystats.Detail(flag=True, status="user added in db")
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_add_vless_user(email: str):
    pass


async def db_add_trojan_user():
    pass


async def db_remove_user(email: str) -> mystats.Detail:
    if user := await get_user(email=email):
        async_session: AsyncSession = await get_session()
        async with async_session.__call__() as session:
            await session.delete(user)
            await session.commit()
            return mystats.Detail(flag=True, status="user removed in db")
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_update_activity(email: str, active: bool) -> mystats.Detail:
    if user := await get_user(email=email):
        async_session: AsyncSession = await get_session()
        async with async_session.__call__() as session:
            user.active = active
            # user_dict = vars(user)
            # user_dict.pop("_sa_instance_state")
            # query = update(Users).values(user_dict).where(Users.id == user.id)
            query = update(Users).values({"active": active}).where(Users.id == user.id)
            await session.execute(query)
            await session.commit()
            return mystats.Detail(flag=True, status=user)
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_user_usage(email: str) -> mystats.Detail:
    if user := await get_user(email=email):
        return mystats.Detail(flag=True, status=stats.UsageResponse(user.download, user.upload))
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_users_usage() -> mystats.Detail:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        query = select(Users).order_by(Users.id)
        result = await session.execute(query)
        if users := result.scalars().all():
            list_user_usage = list()
            for user in users:
                list_user_usage.append(
                    UsersUsage(email=user.email, upload=int(user.upload), download=int(user.download))
                )
            return mystats.Detail(flag=True, status=list_user_usage)
        else:
            return mystats.Detail(flag=False, status="user not found in db")


async def db_update_user_usage(email: str, download: int, upload: int) -> mystats.Detail:
    if user := await get_user(email=email):
        async_session: AsyncSession = await get_session()
        async with async_session.__call__() as session:
            user.download += download
            user.upload += upload
            query = update(Users).values(
                {
                    "download": user.download,
                    "upload": user.upload
                }
            ).where(Users.email == user.email)
            await session.execute(query)
            await session.commit()
            print(f"download: {download}. upload: {upload}. user: {user}")
            return mystats.Detail(flag=True, status=user)
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_set_user_usage(email: str, upload: int = 0, download: int = 0, traffic: int = 0):
    if user := await get_user(email=email):
        async_session: AsyncSession = await get_session()
        async with async_session.__call__() as session:
            query = update(Users).values(
                {
                    "download": download,
                    "upload": upload,
                    "traffic": traffic
                }
            ).where(Users.email == user.email)
            await session.execute(query)
            await session.commit()
            return mystats.Detail(flag=True, status="traffic success set")
    else:
        return mystats.Detail(flag=False, status="user not found in db")


async def db_update_users_usage(users: List[dict]):
    # not working
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        await session.execute(
            update(Users),
            [{"id": 1, "download": Users.__table__.c.download + 1, "upload": +43984}]
        )
        await session.commit()


async def get_all_users() -> mystats.Detail:
    async_session: AsyncSession = await get_session()
    async with async_session.__call__() as session:
        query = select(Users)
        result = await session.execute(query)
        if users := result.scalars().all():
            return mystats.Detail(flag=True, status=users)
        else:
            return mystats.Detail(flag=False, status="users list is empty from db")


def db_traffic_all():
    pass
