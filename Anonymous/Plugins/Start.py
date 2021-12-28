import asyncio
import time
from sys import version as pyver
from typing import Dict, List, Union

import psutil
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InputMediaPhoto, Message)

from Anonymous import ASSID, BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Anonymous import boottime as bot_start_time
from Anonymous import db
from Anonymous.Core.PyTgCalls import Anonymous
from Anonymous.Database import (add_nonadmin_chat, add_served_chat,
                            blacklisted_chats, get_assistant, get_authuser,
                            get_authuser_names, is_nonadmin_chat,
                            is_served_chat, remove_active_chat,
                            remove_nonadmin_chat, save_assistant)
from Anonymous.Decorators.admins import ActualAdminCB
from Anonymous.Decorators.permission import PermissionCheck
from Anonymous.Inline import (custommarkup, dashmarkup, setting_markup,
                          start_pannel, usermarkup, volmarkup)
from Anonymous.Utilities.ping import get_readable_time

welcome_group = 2

__MODULE__ = "Essentials"
__HELP__ = """


/start 
» sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.

/help 
» ɢᴇᴛ ᴄᴏᴍᴍᴀɴᴅs ʜᴇʟᴘᴇʀ ᴍᴇɴᴜ​.

"""


@app.on_message(filters.new_chat_members, group=welcome_group)
async def welcome(_, message: Message):
    chat_id = message.chat.id
    if await is_served_chat(chat_id):
        pass
    else:
        await add_served_chat(chat_id)
    if chat_id in await blacklisted_chats():
        await message.reply_text(
            f"ꜰᴜ*ᴋ, ʏᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ[{message.chat.title}] ʜᴀs ʙᴇᴇɴ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ !\n\nᴀsᴋ ᴀɴʏ sᴜᴅᴏ ᴜsᴇʀ ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ʏᴏᴜʀ ᴄʜᴀᴛ"
        )
        await app.leave_chat(chat_id)
    for member in message.new_chat_members:
        try:
            if member.id in OWNER_ID:
                return await message.reply_text(
                    f"{MUSIC_BOT_NAME}'s ᴏᴡɴᴇʀ[{member.mention}] ʜᴀs ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ."
                )
            if member.id in SUDOERS:
                return await message.reply_text(
                    f"ᴀ ᴍᴇᴍʙᴇʀ ᴏꜰ {MUSIC_BOT_NAME}'s sᴜᴅᴏ ᴜsᴇʀ[{member.mention}] ʜᴀs ᴊᴜsᴛ ᴊᴏɪɴᴇᴅ ʏᴏᴜʀ ᴄʜᴀᴛ."
                )
            if member.id == ASSID:
                await remove_active_chat(chat_id)
            if member.id == BOT_ID:
                out = start_pannel()
                await message.reply_text(
                    f"ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ {MUSIC_BOT_NAME}\n\nᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴀs ᴀᴅᴍɪɴɪsᴛʀᴀᴛᴏʀ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏᴛʜᴇʀᴡɪsᴇ ɪ ᴡɪʟʟ ɴᴏᴛ ꜰᴜɴᴄᴛɪᴏɴ ᴘʀᴏᴘᴇʀʟʏ.",
                    reply_markup=InlineKeyboardMarkup(out[1]),
                )
                return
        except:
            return


@app.on_message(filters.command(["help", "start"]) & filters.group)
@PermissionCheck
async def useradd(_, message: Message):
    out = start_pannel()
    await asyncio.gather(
        message.delete(),
        message.reply_text(
            f"ᴛʜᴀɴᴋs ꜰᴏʀ ʜᴀᴠɪɴɢ ᴍᴇ ɪɴ {message.chat.title}.\n{MUSIC_BOT_NAME} ɪs ᴀʟɪᴠᴇ.\n\nꜰᴏʀ ᴀɴʏ ᴀssɪsᴛᴀɴᴄᴇ ᴏʀ ʜᴇʟᴘ, ᴄʜᴇᴄᴋᴏᴜᴛ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ.",
            reply_markup=InlineKeyboardMarkup(out[1]),
        ),
    )


@app.on_callback_query(filters.regex("okaybhai"))
async def okaybhai(_, CallbackQuery):
    await CallbackQuery.answer("Going Back ...")
    out = start_pannel()
    await CallbackQuery.edit_message_text(
        text=f"ᴛʜᴀɴᴋs ꜰᴏʀ ʜᴀᴠɪɴɢ ᴍᴇ ɪɴ {CallbackQuery.message.chat.title}.\n{MUSIC_BOT_NAME}ɪs ᴀʟɪᴠᴇ.\n\nꜰᴏʀ ᴀɴʏ ᴀssɪsᴛᴀɴᴄᴇ ᴏʀ ʜᴇʟᴘ, ᴄʜᴇᴄᴋᴏᴜᴛ ᴏᴜʀ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ.",
        reply_markup=InlineKeyboardMarkup(out[1]),
    )


@app.on_callback_query(filters.regex("settingm"))
async def settingm(_, CallbackQuery):
    await CallbackQuery.answer("Bot Settings ...")
    text, buttons = setting_markup()
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    _check = await get_assistant(c_id, "assistant")
    if not _check:
        assis = {
            "volume": 100,
        }
        await save_assistant(c_id, "assistant", assis)
        volume = 100
    else:
        volume = _check["volume"]
    await CallbackQuery.edit_message_text(
        text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ​:** {volume}%",
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("EVE"))
@ActualAdminCB
async def EVE(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer("ᴄʜᴀɴɢᴇs sᴀᴠᴇᴅ")
        await add_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nᴀᴅᴍɪɴs ᴄᴏᴍᴍᴀɴᴅs ᴍᴏᴅᴇ ᴛᴏ **ᴇᴠᴇʀʏᴏɴᴇ**\n\nɴᴏᴡ ᴀɴʏᴏɴᴇ ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ sᴋɪᴘ, ᴘᴀᴜsᴇ, ʀᴇsᴜᴍᴇ, sᴛᴏᴘ ᴍᴜsɪᴄ.\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ​ @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        await CallbackQuery.answer(
            "ᴄᴏᴍᴍᴀɴᴅs ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ᴛᴏ ᴇᴠᴇʀʏᴏɴᴇ", show_alert=True
        )


@app.on_callback_query(filters.regex("AMS"))
@ActualAdminCB
async def AMS(_, CallbackQuery):
    checking = CallbackQuery.from_user.username
    text, buttons = usermarkup()
    chat_id = CallbackQuery.message.chat.id
    is_non_admin = await is_nonadmin_chat(chat_id)
    if not is_non_admin:
        await CallbackQuery.answer(
            "ᴄᴏᴍᴍᴀɴᴅs ᴍᴏᴅᴇ ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ᴛᴏ ᴀᴅᴍɪɴs ᴏɴʟʏ", show_alert=True
        )
    else:
        await CallbackQuery.answer("Changes Saved")
        await remove_nonadmin_chat(chat_id)
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\nsᴇᴛ ᴄᴏᴍᴍᴀɴᴅs ᴍᴏᴅᴇ ᴛᴏ **ᴀᴅᴍɪɴs**\n\nɴᴏᴡ ᴏɴʟʏ ᴀᴅᴍɪɴs ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ᴄᴀɴ sᴋɪᴘ, ᴘᴀᴜsᴇ, ʀᴇsᴜᴍᴇ, sᴛᴏᴘ ᴍᴜsɪᴄ.\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ​ @{checking}",
            reply_markup=InlineKeyboardMarkup(buttons),
        )


@app.on_callback_query(
    filters.regex(
        pattern=r"^(AQ|AV|AU|Dashboard|HV|LV|MV|HV|VAM|Custommarkup|PTEN|MTEN|PTF|MTF|PFZ|MFZ|USERLIST|UPT|CPT|RAT|DIT)$"
    )
)
async def start_markup_check(_, CallbackQuery):
    command = CallbackQuery.matches[0].group(1)
    c_title = CallbackQuery.message.chat.title
    c_id = CallbackQuery.message.chat.id
    chat_id = CallbackQuery.message.chat.id
    if command == "AQ":
        await CallbackQuery.answer("ᴀʟʀᴇᴀᴅʏ ɪɴ ʙᴇsᴛ ǫᴜᴀʟɪᴛʏ", show_alert=True)
    if command == "AV":
        await CallbackQuery.answer("ʙᴏᴛ sᴇᴛᴛɪɴɢs")
        text, buttons = volmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "AU":
        await CallbackQuery.answer("ʙᴏᴛ sᴇᴛᴛɪɴɢs")
        text, buttons = usermarkup()
        is_non_admin = await is_nonadmin_chat(chat_id)
        if not is_non_admin:
            current = "ᴀᴅᴍɪɴs ᴏɴʟʏ​"
        else:
            current = "ᴇᴠᴇʀʏᴏɴᴇ"
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴡʜᴏ ᴄᴀɴ ᴜsᴇ ᴍᴇ {MUSIC_BOT_NAME}:- **{current}**\n\n**⁉️ ᴡʜᴀᴛ ɪs ᴛʜɪs?**\n\n**👥 ᴇᴠᴇʀʏᴏɴᴇ :-**ᴀɴʏᴏɴᴇ ᴄᴀɴ ᴜsᴇ {MUSIC_BOT_NAME}'s ᴄᴏᴍᴍᴀɴᴅs(sᴋɪᴘ,ᴘᴀᴜsᴇ,ʀᴇsᴜᴍᴇ,ᴇ.ᴛ.ᴄ.) ᴘʀᴇsᴇɴᴛ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ.\n\n**🙍 ᴀᴅᴍɪɴ ᴏɴʟʏ :-**  ᴏɴʟʏ ᴛʜᴇ ᴀᴅᴍɪɴs ᴀᴜᴛʜᴏʀɪsᴇᴅ ᴜsᴇʀs ᴄᴀɴ ᴜsᴇ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴏꜰ​ {MUSIC_BOT_NAME}.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Dashboard":
        await CallbackQuery.answer("ᴅᴀsʜʙᴏᴀʀᴅ​")
        text, buttons = dashmarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n\nᴄʜᴇᴄᴋ {MUSIC_BOT_NAME}'s sʏsᴛᴇᴍ sᴛᴀᴛs ɪɴ ᴛʜᴇ ᴅᴀsʜʙᴏᴀʀᴅ ʜᴇʀᴇ! ᴋᴇᴇᴘ ᴏɴ ᴄʜᴇᴄᴋɪɴɢ sᴜᴘᴘᴏʀᴛ ᴄʜᴀɴɴᴇʟ​.",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "Custommarkup":
        await CallbackQuery.answer("ʙᴏᴛ sᴇᴛᴛɪɴɢs")
        text, buttons = custommarkup()
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "LV":
        assis = {
            "volume": 25,
        }
        volume = 25
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MV":
        assis = {
            "volume": 50,
        }
        volume = 50
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "HV":
        assis = {
            "volume": 100,
        }
        volume = 100
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "VAM":
        assis = {
            "volume": 200,
        }
        volume = 200
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = volmarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTEN":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 10
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MTF":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 25
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "PFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume + 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "MFZ":
        _check = await get_assistant(c_id, "assistant")
        volume = _check["volume"]
        volume = volume - 50
        if int(volume) > 200:
            volume = 200
        if int(volume) < 10:
            volume = 10
        assis = {
            "volume": volume,
        }
        try:
            await Anonymous.pytgcalls.change_volume_call(c_id, volume)
            await CallbackQuery.answer("sᴇᴛᴛɪɴɢ ᴀᴜᴅɪᴏ ᴄʜᴀɴɢᴇs!")
        except:
            return await CallbackQuery.answer("ɴᴏ ᴀᴄᴛɪᴠᴇ ɢʀᴏᴜᴘ ᴄᴀʟʟ​!")
        await save_assistant(c_id, "assistant", assis)
        text, buttons = custommarkup()
        await CallbackQuery.edit_message_text(
            text=f"{text}\n\n**ɢʀᴏᴜᴘ:** {c_title}\n**ɢʀᴏᴜᴘ ɪᴅ:** {c_id}\n**ᴠᴏʟᴜᴍᴇ ʟᴇᴠᴇʟ:** {volume}%\n**ᴀᴜᴅɪᴏ ǫᴜᴀʟɪᴛʏ:** Default Best",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    if command == "USERLIST":
        await CallbackQuery.answer("ᴀᴜᴛʜ ᴜsᴇʀs!")
        text, buttons = usermarkup()
        _playlist = await get_authuser_names(CallbackQuery.message.chat.id)
        if not _playlist:
            return await CallbackQuery.edit_message_text(
                text=f"{text}\n\nɴᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ\n\nʏᴏᴜ ᴄᴀɴ ᴀʟʟᴏᴡ ᴀɴʏ ɴᴏɴ-ᴀᴅᴍɪɴ ᴛᴏ ᴜsᴇ ᴍʏ ᴀᴅᴍɪɴ ᴄᴏᴍᴍᴀɴᴅs ʙʏ /auth ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ʙʏ ᴜsɪɴɢ​ /unauth",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        else:
            j = 0
            await CallbackQuery.edit_message_text(
                "ꜰᴇᴛᴄʜɪɴɢ ᴀᴜᴛʜᴏʀɪsᴇᴅ ᴜsᴇʀs! ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ...​"
            )
            msg = f"**ᴀᴜᴛʜᴏʀɪsᴇᴅ ᴜsᴇʀs ʟɪsᴛ​[AUL]:**\n\n"
            for note in _playlist:
                _note = await get_authuser(
                    CallbackQuery.message.chat.id, note
                )
                user_id = _note["auth_user_id"]
                user_name = _note["auth_name"]
                admin_id = _note["admin_id"]
                admin_name = _note["admin_name"]
                try:
                    user = await app.get_users(user_id)
                    user = user.first_name
                    j += 1
                except Exception:
                    continue
                msg += f"{j}➤ {user}[`{user_id}`]\n"
                msg += f"    » ᴀᴅᴅᴇᴅ ʙʏ:- {admin_name}[`{admin_id}`]\n\n"
            await CallbackQuery.edit_message_text(
                msg, reply_markup=InlineKeyboardMarkup(buttons)
            )
    if command == "UPT":
        bot_uptimee = int(time.time() - bot_start_time)
        Uptimeee = f"{get_readable_time((bot_uptimee))}"
        await CallbackQuery.answer(
            f"ʙᴏᴛ's ᴜᴘᴛɪᴍᴇ: {Uptimeee}", show_alert=True
        )
    if command == "CPT":
        cpue = psutil.cpu_percent(interval=0.5)
        await CallbackQuery.answer(
            f"ʙᴏᴛ's ᴄᴘᴜ ᴜsᴀɢᴇ: {cpue}%", show_alert=True
        )
    if command == "RAT":
        meme = psutil.virtual_memory().percent
        await CallbackQuery.answer(
            f"ʙᴏᴛ's ᴍᴇᴍᴏʀʏ ᴜsᴀɢᴇ: {meme}%", show_alert=True
        )
    if command == "DIT":
        diske = psutil.disk_usage("/").percent
        await CallbackQuery.answer(
            f"ᴀɴᴏɴʏᴍᴏᴜs ᴅɪsᴋ ᴜsᴀɢᴇ​: {diske}%", show_alert=True
        )
