from typing import Dict, List, Union

from pyrogram import Client, filters

from Anonymous import BOT_USERNAME, MUSIC_BOT_NAME, app, db
from Anonymous.Database import _get_theme, get_theme, save_theme
from Anonymous.Decorators.permission import PermissionCheck

themes = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
    "Random",
]

themes2 = [
    "blue",
    "black",
    "red",
    "green",
    "grey",
    "orange",
    "pink",
    "yellow",
]

__MODULE__ = "Theme"
__HELP__ = """


/settheme
» sᴇᴛ ᴀ ᴛʜᴇᴍᴇ ꜰᴏʀ ᴛʜᴜᴍʙɴᴀɪʟs.

/theme
» ᴄʜᴇᴄᴋ ᴛʜᴇᴍᴇ ꜰᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ​.
"""


@app.on_message(
    filters.command(["settheme", f"settheme@{BOT_USERNAME}"]) & filters.group
)
async def settheme(_, message):
    usage = f"ᴛʜɪs ɪsɴ'ᴛ ᴀ ᴛʜᴇᴍᴇ.\n\ɴsᴇʟᴇᴄᴛ ꜰʀᴏᴍ ᴛʜᴇᴍ\n{' | '.ᴊᴏɪɴ(themes)}\n\nᴜsᴇ 'ʀᴀɴᴅᴏᴍ' ᴛᴏ ɢᴇᴛ ʀᴀɴᴅᴏᴍ ᴄʜᴏɪᴄᴇ ᴏꜰ ᴛʜᴇᴍᴇs​"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    theme = message.text.split(None, 1)[1].strip()
    if theme not in themes:
        return await message.reply_text(usage)
    note = {
        "theme": theme,
    }
    await save_theme(message.chat.id, "theme", note)
    await message.reply_text(f"ᴄʜᴀɴɢᴇᴅ ᴛʜᴜᴍʙɴᴀɪʟ ᴛʜᴇᴍᴇ ᴛᴏ​ {theme}")


@app.on_message(filters.command("theme"))
@PermissionCheck
async def theme_func(_, message):
    await message.delete()
    _note = await get_theme(message.chat.id, "theme")
    if not _note:
        theme = "Random"
    else:
        theme = _note["theme"]
    await message.reply_text(
        f"**{MUSIC_BOT_NAME} ᴛʜᴜᴍʙɴᴀɪʟs ᴛʜᴇᴍᴇ**\n\n**ᴄᴜʀʀᴇɴᴛ ᴛʜᴇᴍᴇ:-** {theme}\n\n**ᴀᴠᴀɪʟᴀʙʟᴇ ᴛʜᴇᴍᴇs:-** {' | '.ᴊᴏɪɴ(themes2)} \n\nᴜsᴇ /settheme ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʜᴇᴍᴇ​."
    )
