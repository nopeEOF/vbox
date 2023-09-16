import asyncio
from app.utils import v2_match_db
from app.readconfig import get_config


class Service:
    def __init__(self):
        self.refreshTime = get_config()["service"]["refresh_time"]

    @staticmethod
    async def first_run():
        await v2_match_db.read_users_db_add_v2ray()

    async def refresh_v2_in_db(self, first_run: bool):
        if first_run:
            await self.first_run()
        while True:
            await v2_match_db.users_usage()
            await v2_match_db.check_activity_users()
            await asyncio.sleep(self.refreshTime)
