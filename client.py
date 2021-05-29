import asyncio
import functools
import os
import subprocess
import traceback

SESSION = os.getenv("SESSION")
api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
bot_token = os.getenv("bot_token")
AuthUsers = list(os.getenv("AuthUsers"))

from pyrogram import Client, filters

bot = Client(":memory:", bot_token=bot_token, api_id=api_id, api_hash=api_hash)
user = Client(SESSION if SESSION else "vcbot", api_id=api_id, api_hash=api_hash)
