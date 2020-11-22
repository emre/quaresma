import asyncio
import aiohttp
from discord.ext import commands

from .db import Database
import uuid

HIVE_RPC_NODE = "https://hived.emre.sh"
RABONA_API_BASE = "https://api.rabona.io"


def build_request_body(method, params):
    return {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": str(uuid.uuid4())
    }


class CustomClient(commands.Bot):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = kwargs.get("config")
        self.db = Database()

    @asyncio.coroutine
    def on_ready(self):
        for server in self.guilds:
            print(f'Running on {server.name}')

    def say_error(self, error, ctx):
        return ctx.send(f":exclamation: {error}")

    def say_success(self, message, ctx):
        return ctx.send(f":thumbsup: {message}")

    async def _hive_request(self, api_call, params):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    HIVE_RPC_NODE,
                    json=build_request_body(api_call, params)) as r:
                return await r.json()

    async def username_is_valid(self, username):
        async with aiohttp.ClientSession() as session:
            r = await self._hive_request(
                "condenser_api.get_accounts", [[username], ])
            if len(r.get("result", [])) == 0:
                return False

            async with aiohttp.ClientSession() as session_rabona:
                r = await session.get(
                    f"{RABONA_API_BASE}/userinfo?user={username}")
                if isinstance(await r.json(), list):
                    # if the username is invalid, rabona api returns an
                    # empty list.
                    return False

        return True

    @property
    def running_on(self):
        return list(self.servers)[0]
