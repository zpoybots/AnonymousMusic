from pyrogram import Client, filters
from pyrogram.types import Message

from Anonymous import SUDOERS, app
from Anonymous.Database import blacklist_chat, blacklisted_chats, whitelist_chat

__MODULE__ = "Blacklist"
__HELP__ = """


/blacklistedchat 
» Cʜᴇᴄᴋ Bʟᴀᴄᴋʟɪsᴛᴇᴅ Cʜᴀᴛs ᴏғ Bᴏᴛ.


**Note:**
» Oɴʟʏ ғᴏʀ Sᴜᴅᴏ Usᴇʀs.


/blacklistchat [CHAT_ID] 
» Bʟᴀᴄᴋʟɪsᴛ ᴀɴʏ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ Mᴜsɪᴄ Bᴏᴛ


/whitelistchat [CHAT_ID] 
» Wʜɪᴛᴇʟɪsᴛ ᴀɴʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ Mᴜsɪᴄ Bᴏᴛ

"""


@app.on_message(filters.command("blacklistchat") & filters.user(SUDOERS))
async def blacklist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/blacklistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("» Cʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        return await message.reply_text(
            "» Cʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ"
        )
    await message.reply_text("» Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢs.")


@app.on_message(filters.command("whitelistchat") & filters.user(SUDOERS))
async def whitelist_chat_func(_, message: Message):
    if len(message.command) != 2:
        return await message.reply_text(
            "**Usage:**\n/whitelistchat [CHAT_ID]"
        )
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("» Cʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text(
            "» Cʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssғᴜʟʟʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ"
        )
    await message.reply_text("» Sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ, ᴄʜᴇᴄᴋ ʟᴏɢs.")


@app.on_message(filters.command("blacklistedchat"))
async def blacklisted_chats_func(_, message: Message):
    text = "**Blacklisted Chats:**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except Exception:
            title = "Private"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("» Nᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs")
    else:
        await message.reply_text(text)
