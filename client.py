import asyncio
import functools
import os
import subprocess
import traceback

from pyrogram import Client, filters

bot = Client(":memory:", bot_token=bot_token, api_id=api_id, api_hash=api_hash)
user = Client(SESSION if SESSION else "vcbot", api_id=api_id, api_hash=api_hash)
