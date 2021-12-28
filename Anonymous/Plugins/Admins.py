import asyncio
import os
import random
from asyncio import QueueEmpty

from config import get_queue
from pyrogram import filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, KeyboardButton, Message,
                            ReplyKeyboardMarkup, ReplyKeyboardRemove)
from pytgcalls import StreamType
from pytgcalls.types.input_stream import InputAudioStream, InputStream

from Anonymous import BOT_USERNAME, MUSIC_BOT_NAME, app, db_mem
from Anonymous.Core.PyTgCalls import Queues, Anonymous
from Anonymous.Core.PyTgCalls.Converter import convert
from Anonymous.Core.PyTgCalls.Downloader import download
from Anonymous.Database import (is_active_chat, is_music_playing, music_off,
                            music_on, remove_active_chat)
from Anonymous.Decorators.admins import AdminRightsCheck
from Anonymous.Decorators.checker import checker, checkerCB
from Anonymous.Inline import audio_markup, primary_markup
from Anonymous.Utilities.changers import time_to_seconds
from Anonymous.Utilities.chat import specialfont_to_normal
from Anonymous.Utilities.theme import check_theme
from Anonymous.Utilities.thumbnails import gen_thumb
from Anonymous.Utilities.timer import start_timer
from Anonymous.Utilities.youtube import get_yt_info_id

loop = asyncio.get_event_loop()


__MODULE__ = "Voice Chat"
__HELP__ = """


/pause
- ᴘᴀᴜsᴇ ᴛʜᴇ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʙᴀʙʏ.

/resume
- ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴘᴀᴜsᴇᴅ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʙᴀʙʏ.

/skip
- sᴋɪᴘ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʙᴀʙʏ.

/end or /stop
- sᴛᴏᴘ ᴛʜᴇ ᴘʟᴀʏᴏᴜᴛ ʙᴀʙʏ.

/queue
- ᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ ʟɪsᴛ ʙᴀʙʏ.


**Note:**
ᴏɴʟʏ ꜰᴏʀ sᴜᴅᴏ ᴜsᴇʀs ʙᴀʙʏ

/activevc
- ᴄʜᴇᴄᴋ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴏɴ ʙᴏᴛ ʙᴀʙʏ.

"""


@app.on_message(
    filters.command(["pause", "skip", "resume", "stop", "end"])
    & filters.group
)
@AdminRightsCheck
@checker
async def admins(_, message: Message):
    global get_queue
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ! ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏꜰ ᴄᴏᴍᴍᴀɴᴅ ʙᴀʙʏ.")
    if not await is_active_chat(message.chat.id):
        return await message.reply_text("ɴᴏᴛʜɪɴɢ ɪs ᴘʟᴀʏɪɴɢ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʙᴀʙʏ.")
    chat_id = message.chat.id
    if message.command[0][1] == "a":
        if not await is_music_playing(message.chat.id):
            return await message.reply_text("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ ʙᴀʙʏ.")
        await music_off(chat_id)
        await Anonymous.pytgcalls.pause_stream(chat_id)
        await message.reply_text(
            f"ðŸŽ§ ᴠᴏɪᴄᴇᴄʜᴀᴛ ᴘᴀᴜsᴇᴅ ʙʏ {message.from_user.mention} ʙᴀʙʏ!"
        )
    if message.command[0][1] == "e":
        if await is_music_playing(message.chat.id):
            return await message.reply_text("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘʟᴀʏɪɴɢ ʙᴀʙʏ.")
        await music_on(chat_id)
        await Anonymous.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text(
            f"ðŸŽ§ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʀᴇsᴜᴍᴇᴅ ʙʏ {message.from_user.mention} ʙᴀʙʏ!"
        )
    if message.command[0][1] == "t" or message.command[0][1] == "n":
        try:
            Queues.clear(message.chat.id)
        except QueueEmpty:
            pass
        await remove_active_chat(chat_id)
        await Anonymous.pytgcalls.leave_group_call(message.chat.id)
        await message.reply_text(
            f"ðŸŽ§ ᴠᴏɪᴄᴇᴄʜᴀᴛ ᴇɴᴅ/sᴛᴏᴘᴘᴇᴅ ʙʏ  {message.from_user.mention} ʙᴀʙʏ!"
        )
    if message.command[0][1] == "k":
        Queues.task_done(chat_id)
        if Queues.is_empty(chat_id):
            await remove_active_chat(chat_id)
            await message.reply_text(
                "No more music in __Queue__ \n\nʟᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʙᴀʙʏ."
            )
            await Anonymous.pytgcalls.leave_group_call(message.chat.id)
            return
        else:
            videoid = Queues.get(chat_id)["file"]
            got_queue = get_queue.get(chat_id)
            if got_queue:
                got_queue.pop(0)
            finxx = f"{videoid[0]}{videoid[1]}{videoid[2]}"
            aud = 0
            if str(finxx) != "raw":
                mystic = await message.reply_text(
                    f"**{MUSIC_BOT_NAME} ᴘʟᴀʏʟɪsᴛ ꜰᴜɴᴄᴛɪᴏɴ**\n\n__ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴍᴜsɪᴄ ꜰʀᴏᴍ ᴘʟᴀʏʟɪsᴛ ʙᴀʙʏ....__"
                )
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                ) = get_yt_info_id(videoid)
                await mystic.edit(
                    f"**{MUSIC_BOT_NAME} ᴅᴏᴡɴʟᴏᴀᴅᴇʀ**\n\n**ᴛɪᴛʟᴇ:** {title[:50]}\n\n0% â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“â–“ 100%"
                )
                downloaded_file = await loop.run_in_executor(
                    None, download, videoid, mystic, title
                )
                raw_path = await convert(downloaded_file)
                await Anonymous.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            raw_path,
                        ),
                    ),
                )
                theme = await check_theme(chat_id)
                chat_title = await specialfont_to_normal(message.chat.title)
                thumb = await gen_thumb(
                    thumbnail, title, message.from_user.id, theme, chat_title
                )
                buttons = primary_markup(
                    videoid, message.from_user.id, duration_min, duration_min
                )
                await mystic.delete()
                mention = db_mem[videoid]["username"]
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=(
                        f"<b>__sᴋɪᴘᴘᴇᴅ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʙᴀʙʏ__</b>\n\nðŸŽ¥<b>__sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ:__ </b>[{title[:25]}](https://www.youtube.com/watch?v={videoid}) ʙᴀʙʏ\nâ³<b>__ᴅᴜʀᴀᴛɪᴏɴ:__</b> {duration_min} Mins\nðŸ‘¤**__ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:__** {mention} ʙᴀʙʏ"
                    ),
                )
                os.remove(thumb)
            else:
                await Anonymous.pytgcalls.change_stream(
                    chat_id,
                    InputStream(
                        InputAudioStream(
                            videoid,
                        ),
                    ),
                )
                afk = videoid
                title = db_mem[videoid]["title"]
                duration_min = db_mem[videoid]["duration"]
                duration_sec = int(time_to_seconds(duration_min))
                mention = db_mem[videoid]["username"]
                videoid = db_mem[videoid]["videoid"]
                if str(videoid) == "smex1":
                    buttons = buttons = audio_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                    thumb = "Utils/Telegram.JPEG"
                    aud = 1
                else:
                    _path_ = _path_ = (
                        (str(afk))
                        .replace("_", "", 1)
                        .replace("/", "", 1)
                        .replace(".", "", 1)
                    )
                    thumb = f"cache/{_path_}final.png"
                    buttons = primary_markup(
                        videoid,
                        message.from_user.id,
                        duration_min,
                        duration_min,
                    )
                final_output = await message.reply_photo(
                    photo=thumb,
                    reply_markup=InlineKeyboardMarkup(buttons),
                    caption=f"<b>__sᴋɪᴘᴘᴇᴅ ᴠᴏɪᴄᴇᴄʜᴀᴛ ʙᴀʙʏ__</b>\n\nðŸŽ¥<b>__sᴛᴀʀᴛᴇᴅ ᴘʟᴀʏɪɴɢ:__</b> {title} ʙᴀʙʏ \nâ³<b>__ᴅᴜʀᴀᴛɪᴏɴ__:__</b> {duration_min} \nðŸ‘¤<b>__ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:__ </b> {mention} ʙᴀʙʏ",
                )
            await start_timer(
                videoid,
                duration_min,
                duration_sec,
                final_output,
                message.chat.id,
                message.from_user.id,
                aud,
            )
