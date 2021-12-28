import asyncio
import json
import logging
import platform
import re
import socket
import time
import uuid
from datetime import datetime
from sys import version as pyver

import psutil
from pyrogram import Client
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import Message
from pymongo import MongoClient
from config import MONGO_DB_URI
from Anonymous import (BOT_ID, MUSIC_BOT_NAME, SUDOERS, app, boottime,
                   userbot)
from Anonymous.Database import get_gbans_count, get_served_chats, get_sudoers
from Anonymous.Inline import (stats1, stats2, stats3, stats4, stats5, stats6,
                          stats7)
from Anonymous.Plugins import ALL_MODULES
from Anonymous.Utilities.ping import get_readable_time

__MODULE__ = "Stats"
__HELP__ = """


/stats
» ᴄʜᴇᴄᴋ ᴛʜᴇ sᴛᴀᴛs ᴏꜰ ʙᴏᴛ
» ɢᴇᴛs ᴛʜᴇ sᴛᴀᴛ ᴏꜰ ᴍᴏɴɢᴏᴅʙ , ᴀssɪsᴛᴀɴᴛ, sʏsᴛᴇᴍ ᴇᴛᴄ
"""


async def bot_sys_stats():
    bot_uptime = int(time.time() - boottime)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    stats = f"""
**ᴜᴘᴛɪᴍᴇ:** {get_readable_time((bot_uptime))}
**ᴄᴘᴜ:** {cpu}%
**ʀᴀᴍ:** {mem}%
**ᴅɪsᴋ: **{disk}%"""
    return stats


@app.on_message(filters.command("stats") & ~filters.edited)
async def gstats(_, message):
    start = datetime.now()
    try:
        await message.delete()
    except:
        pass
    uptime = await bot_sys_stats()
    response = await message.reply_photo(
        photo="Utils/Query.jpg", caption="ɢᴇᴛᴛɪɴɢ sᴛᴀᴛs​..."
    )
    end = datetime.now()
    resp = (end - start).microseconds / 1000
    smex = f"""
[•]<u>**ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs​**</u>

ᴘɪɴɢ: `⚡{resp} ms`
{uptime}
    """
    await response.edit_text(smex, reply_markup=stats1)
    return


@app.on_callback_query(
    filters.regex(
        pattern=r"^(sys_stats|sto_stats|bot_stats|Dashboard|mongo_stats|gen_stats|assis_stats|wait_stats)$"
    )
)
async def stats_markup(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    if command == "sys_stats":
        await CallbackQuery.answer("Getting System Stats...", show_alert=True)
        sc = platform.system()
        arch = platform.machine()
        ram = (
            str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
        )
        bot_uptime = int(time.time() - boottime)
        uptime = f"{get_readable_time((bot_uptime))}"
        smex = f"""
[•]<u>**sʏsᴛᴇᴍ sᴛᴀᴛs**</u>

**ᴀɴᴏɴʏᴍᴏᴜs ᴜᴘᴛɪᴍᴇ:** {uptime}
**sʏsᴛᴇᴍ ᴘʀᴏᴄ:** ᴏɴʟɪɴᴇ
**ᴘʟᴀᴛꜰᴏʀᴍ:** {sc}
**ᴀʀᴄʜɪᴛᴇᴄᴛᴜʀᴇ:** {arch}
**ʀᴀᴍ:** {ram}
**ᴘʏᴛʜᴏɴ ᴠᴇʀsɪᴏɴ:** {pyver.split()[0]}
**ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ​:** {pyrover}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats2)
    if command == "sto_stats":
        await CallbackQuery.answer(
            "Getting Storage Stats...", show_alert=True
        )
        hdd = psutil.disk_usage("/")
        total = hdd.total / (1024.0 ** 3)
        total = str(total)
        used = hdd.used / (1024.0 ** 3)
        used = str(used)
        free = hdd.free / (1024.0 ** 3)
        free = str(free)
        smex = f"""
[•]<u>**sᴛᴏʀᴀɢᴇ sᴛᴀᴛs**</u>

**sᴛᴏʀᴀɢᴇ ᴀᴠᴀɪʟ:** {total[:4]} GiB
**sᴛᴏʀᴀɢᴇ ᴜsᴇᴅ:** {used[:4]} GiB
**sᴛᴏʀᴀɢᴇ ʟᴇꜰᴛ​:** {free[:4]} GiB"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats3)
    if command == "bot_stats":
        await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ʙᴏᴛ sᴛᴀᴛs...​", show_alert=True)
        served_chats = []
        chats = await get_served_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
        blocked = await get_gbans_count()
        sudoers = await get_sudoers()
        modules_loaded = len(ALL_MODULES)
        j = 0
        for count, user_id in enumerate(sudoers, 0):
            try:
                user = await app.get_users(user_id)
                j += 1
            except Exception:
                continue
        smex = f"""
[•]<u>**ʙᴏᴛ sᴛᴀᴛs**</u>

**ᴍᴏᴅᴜʟᴇs ʟᴏᴀᴅᴇᴅ:** {modules_loaded}
**ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs:** {blocked}
**sᴜᴅᴏ ᴜsᴇʀs:** {j}
**sᴇʀᴠᴇᴅ ᴄʜᴀᴛs:** {len(served_chats)}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats4)
    if command == "mongo_stats":
        await CallbackQuery.answer(
            "ɢᴇᴛᴛɪɴɢ ᴍᴏɴɢᴏᴅʙ sᴛᴀᴛs​...", show_alert=True
        )
        try:
            pymongo = MongoClient(MONGO_DB_URI)
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴍᴏɴɢᴏᴅʙ sᴛᴀᴛs​", reply_markup=stats5)
        try:
            db = pymongo.Anonymous
        except Exception as e:
            print(e)
            return await CallbackQuery.edit_message_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ɢᴇᴛ ᴍᴏɴɢᴏᴅʙ sᴛᴀᴛs​", reply_markup=stats5)
        call = db.command("dbstats")
        database = call["db"]
        datasize = call["dataSize"] / 1024
        datasize = str(datasize)
        storage = call["storageSize"] / 1024
        objects = call["objects"]
        collections = call["collections"]
        status = db.command("serverStatus")
        query = status["opcounters"]["query"]
        mver = status["version"]
        mongouptime = status["uptime"] / 86400
        mongouptime = str(mongouptime)
        provider = status["repl"]["tags"]["provider"]
        smex = f"""
[•]<u>**ᴍᴏɴɢᴏᴅʙ sᴛᴀᴛs**</u>

**ᴍᴏɴɢᴏ ᴜᴘᴛɪᴍᴇ:** {mongouptime[:4]} Days
**ᴠᴇʀsɪᴏɴ:** {mver}
**ᴅᴀᴛᴀʙᴀsᴇ:** {database}
**ᴘʀᴏᴠɪᴅᴇʀ:** {provider}
**ᴅʙ sɪᴢᴇ:** {datasize[:6]} Mb
**sᴛᴏʀᴀɢᴇ:** {storage} Mb
**ᴄᴏʟʟᴇᴄᴛɪᴏɴs:** {collections}
**ᴋᴇʏs:** {objects}
**ᴛᴏᴛᴀʟ ǫᴜᴇʀɪᴇs:** `{query}`"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats5)
    if command == "assis_stats":
        await CallbackQuery.answer(
            "ɢᴇᴛᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ sᴛᴀᴛs...", show_alert=True
        )
        await CallbackQuery.edit_message_text(
            "ɢᴇᴛᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ sᴛᴀᴛs... ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ​...", reply_markup=stats7
        )
        groups_ub = channels_ub = bots_ub = privates_ub = total_ub = 0
        async for i in userbot.iter_dialogs():
            t = i.chat.type
            total_ub += 1
            if t in ["supergroup", "group"]:
                groups_ub += 1
            elif t == "channel":
                channels_ub += 1
            elif t == "bot":
                bots_ub += 1
            elif t == "private":
                privates_ub += 1

        smex = f"""
[•]<u>ᴀssɪsᴛᴀɴᴛ sᴛᴀᴛs</u>

**ᴅɪᴀʟᴏɢs:** {total_ub}
**ɢʀᴏᴜᴘs:** {groups_ub}
**ᴄʜᴀɴɴᴇʟs:** {channels_ub}
**ʙᴏᴛs:** {bots_ub}
**ᴜsᴇʀs:** {privates_ub}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats6)
    if command == "gen_stats":
        start = datetime.now()
        uptime = await bot_sys_stats()
        await CallbackQuery.answer(
            "ɢᴇᴛᴛɪɴɢ ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs...", show_alert=True
        )
        end = datetime.now()
        resp = (end - start).microseconds / 1000
        smex = f"""
[•]<u>ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs</u>

**ᴘɪɴɢ:** `⚡{resp} ms`
{uptime}"""
        await CallbackQuery.edit_message_text(smex, reply_markup=stats1)
    if command == "wait_stats":
        await CallbackQuery.answer()
