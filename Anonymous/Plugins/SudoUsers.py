import asyncio
import os
import shutil
import subprocess
from sys import version as pyver

from config import OWNER_ID
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from Anonymous import BOT_ID, MUSIC_BOT_NAME, OWNER_ID, SUDOERS, app
from Anonymous.Database import (add_gban_user, add_off, add_on, add_sudo,
                            get_active_chats, get_served_chats, get_sudoers,
                            is_gbanned_user, remove_active_chat,
                            remove_gban_user, remove_served_chat, remove_sudo)

__MODULE__ = "SudoUsers"
__HELP__ = """


**Note:**
ᴏɴʟʏ ꜰᴏʀ sᴜᴅᴏ ᴜsᴇʀs


/sudolist 
» ᴄʜᴇᴄᴋ ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀ ʟɪsᴛ ᴏꜰ ʙᴏᴛ

/addsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ]
» ᴛᴏ ᴀᴅᴅ ᴀ ᴜsᴇʀ ɪɴ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀs

/delsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ]
» ᴛᴏ ʀᴇᴍᴏᴠᴇ ᴀ ᴜsᴇʀ ꜰʀᴏᴍ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀs

/restart 
» ʀᴇsᴛᴀʀᴛ ʙᴏᴛ [ᴀʟʟ ᴅᴏᴡɴʟᴏᴀᴅs, ᴄᴀᴄʜᴇ, ʀᴀᴡ ꜰɪʟᴇs ᴡɪʟʟ ʙᴇ ᴄʟᴇᴀʀᴇᴅ ᴛᴏᴏ]

/maintenance [ᴇɴᴀʙʟᴇ / ᴅɪsᴀʙʟᴇ]
» ᴡʜᴇɴ ᴇɴᴀʙʟᴇᴅ ʙᴏᴛ ɢᴏᴇs ᴜɴᴅᴇʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ. ɴᴏ ᴏɴᴇ ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɴᴏᴡ!​

/update 
» ꜰᴇᴛᴄʜ ᴜᴘᴅᴀᴛᴇs ꜰʀᴏᴍ sᴇʀᴠᴇʀ

/clean
» ᴄʟᴇᴀɴ ᴛᴇᴍᴘ ꜰɪʟᴇs ᴀɴᴅ ʟᴏɢs
"""
# Add Sudo Users!


@app.on_message(filters.command("addsudo") & filters.user(OWNER_ID))
async def useradd(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                f"{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ."
            )
        added = await add_sudo(user.id)
        if added:
            await message.reply_text(
                f"ᴀᴅᴅᴇᴅ **{user.mention}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs."
            )
            os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")
        else:
            await message.reply_text("Failed")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            f"{message.reply_to_message.from_user.mention} is already a sudo user."
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        await message.reply_text(
            f"ᴀᴅᴅᴇᴅ **{message.reply_to_message.from_user.mention}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs"
        )
        os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")
    else:
        await message.reply_text("Failed")
    return


@app.on_message(filters.command("delsudo") & filters.user(OWNER_ID))
async def userdel(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ."
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id not in SUDOERS:
            return await message.reply_text(f"ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ʙᴏᴛ's sᴜᴅᴏ.")
        removed = await remove_sudo(user.id)
        if removed:
            await message.reply_text(
                f"ʀᴇᴍᴏᴠᴇᴅ **{user.mention}** ꜰʀᴏᴍ {MUSIC_BOT_NAME}'s sᴜᴅᴏ."
            )
            return os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")
        await message.reply_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    if user_id not in SUDOERS:
        return await message.reply_text(
            f"ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ {MUSIC_BOT_NAME}'s sᴜᴅᴏ."
        )
    removed = await remove_sudo(user_id)
    if removed:
        await message.reply_text(
            f"ʀᴇᴍᴏᴠᴇᴅ **{mention}** ꜰʀᴏᴍ {MUSIC_BOT_NAME}'s sᴜᴅᴏ."
        )
        return os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")
    await message.reply_text(f"sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ.")


@app.on_message(filters.command("sudolist"))
async def sudoers_list(_, message: Message):
    sudoers = await get_sudoers()
    text = "💔<u> **ᴏᴡɴᴇʀ​:**</u>\n"
    sex = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            sex += 1
        except Exception:
            continue
        text += f"{sex}➤ {user}\n"
    smex = 0
    for count, user_id in enumerate(sudoers, 1):
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n🖤<u> **sᴜᴅᴏ ᴜsᴇʀs:**</u>\n"
                sex += 1
                text += f"{sex}➤ {user}\n"
            except Exception:
                continue
    if not text:
        await message.reply_text("ɴᴏ sᴜᴅᴏ ᴜsᴇʀs")
    else:
        await message.reply_text(text)


# Restart Anonymous


@app.on_message(filters.command("restart") & filters.user(SUDOERS))
async def theme_func(_, message):
    A = "downloads"
    B = "raw_files"
    C = "cache"
    shutil.rmtree(A)
    shutil.rmtree(B)
    shutil.rmtree(C)
    await asyncio.sleep(2)
    os.mkdir(A)
    os.mkdir(B)
    os.mkdir(C)
    served_chats = []
    try:
        chats = await get_active_chats()
        for chat in chats:
            served_chats.append(int(chat["chat_id"]))
    except Exception as e:
        pass
    for x in served_chats:
        try:
            await app.send_message(
                x,
                f"{MUSIC_BOT_NAME} ʜᴀs ᴊᴜsᴛ ʀᴇsᴛᴀʀᴛᴇᴅ ʜᴇʀsᴇʟꜰ. sᴏʀʀʏ ꜰᴏʀ ᴛʜᴇ ɪssᴜᴇs.\n\nsᴛᴀʀᴛ ᴘʟᴀʏɪɴɢ ᴀꜰᴛᴇʀ 10-15 sᴇᴄᴏɴᴅs ᴀɢᴀɪɴ.​",
            )
            await remove_active_chat(x)
        except Exception:
            pass
    x = await message.reply_text(f"ʀᴇsᴛᴀʀᴛɪɴɢ {MUSIC_BOT_NAME}")
    os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")


## Maintenance Anonymous


@app.on_message(filters.command("maintenance") & filters.user(SUDOERS))
async def maintenance(_, message):
    usage = "**ᴜsᴀɢᴇ:**\n/Anonymous [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ​]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        user_id = 1
        await add_on(user_id)
        await message.reply_text("ᴇɴᴀʙʟᴇᴅ ꜰᴏʀ ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ")
    elif state == "disable":
        user_id = 1
        await add_off(user_id)
        await message.reply_text("ᴍᴀɪɴᴛᴇɴᴀɴᴄᴇ ᴍᴏᴅᴇ ᴅɪsᴀʙʟᴇᴅ​")
    else:
        await message.reply_text(usage)


## Gban Module


@app.on_message(filters.command("gban") & filters.user(SUDOERS))
async def ban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) < 2:
            await message.reply_text("**ᴜsᴀɢᴇ:**\n/gban [ᴜsᴇʀɴᴀᴍᴇ|ᴜsᴇʀ_ɪᴅ​]")
            return
        user = message.text.split(None, 2)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        if user.id == from_user.id:
            return await message.reply_text(
                "ᴡʜᴀᴛ ᴛʜᴇ ꜰᴜ*ᴋ, ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢʙᴀɴ ʏᴏᴜʀsᴇʟꜰ​😂!"
            )
        elif user.id == BOT_ID:
            await message.reply_text("sʜᴏᴜʟᴅ ɪ ʙʟᴏᴄᴋ ᴍʏsᴇʟꜰ, ʟᴍᴀᴏ​!")
        elif user.id in SUDOERS:
            await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʟᴏᴄᴋ ᴀ sᴜᴅᴏ ᴜsᴇʀ, ᴀʀᴇ ʏᴏᴜ ᴍᴀᴅ ?​")
        else:
            await add_gban_user(user.id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {user.mention}**\n\nᴇxᴘᴇᴄᴛᴇᴅ ᴛɪᴍᴇ​ : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user.id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {MUSIC_BOT_NAME}**__

**ᴏʀɪɢɪɴ:** {message.chat.title} [`{message.chat.id}`]
**sᴜᴅᴏ ᴜsᴇʀ:** {from_user.mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ:** {user.mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ:** `{user.id}`
**ᴄʜᴀᴛs:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
        return
    from_user_id = message.from_user.id
    from_user_mention = message.from_user.mention
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("ᴡʜᴀᴛ ᴛʜᴇ ꜰᴜ*ᴋ, ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʟᴏᴄᴋ ʏᴏᴜʀsᴇʟꜰ​")
    elif user_id == BOT_ID:
        await message.reply_text("sʜᴏᴜʟᴅ ɪ ʙʟᴏᴄᴋ ᴍʏsᴇʟꜰ, ʟᴍᴀᴏ​!")
    elif user_id in sudoers:
        await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʙʟᴏᴄᴋ ᴀ sᴜᴅᴏ ᴜsᴇʀ, ᴀʀᴇ ʏᴏᴜ ᴍᴀᴅ ?​")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if is_gbanned:
            await message.reply_text("ᴀʟʀᴇᴀᴅʏ ɢʙᴀɴɴᴇᴅ​")
        else:
            await add_gban_user(user_id)
            served_chats = []
            chats = await get_served_chats()
            for chat in chats:
                served_chats.append(int(chat["chat_id"]))
            m = await message.reply_text(
                f"**ɪɴɪᴛɪᴀʟɪᴢɪɴɢ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {mention}**\n\nᴇxᴘᴇᴄᴛᴇᴅ ᴛɪᴍᴇ​ : {len(served_chats)}"
            )
            number_of_chats = 0
            for sex in served_chats:
                try:
                    await app.kick_chat_member(sex, user_id)
                    number_of_chats += 1
                    await asyncio.sleep(1)
                except FloodWait as e:
                    await asyncio.sleep(int(e.x))
                except Exception:
                    pass
            ban_text = f"""
__**ɴᴇᴡ ɢʟᴏʙᴀʟ ʙᴀɴ ᴏɴ {MUSIC_BOT_NAME}**__

**ᴏʀɪɢɪɴ:** {message.chat.title} [`{message.chat.id}`]
**sᴜᴅᴏ ᴜsᴇʀ:** {from_user_mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ:** {mention}
**ʙᴀɴɴᴇᴅ ᴜsᴇʀ ɪᴅ:** `{user_id}`
**ᴄʜᴀᴛs:** {number_of_chats}"""
            try:
                await m.delete()
            except Exception:
                pass
            await message.reply_text(
                f"{ban_text}",
                disable_web_page_preview=True,
            )
            return


@app.on_message(filters.command("ungban") & filters.user(SUDOERS))
async def unban_globally(_, message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            await message.reply_text(
                "**ᴜsᴀɢᴇ:**\n/ungban [ᴜsᴇʀɴᴀᴍᴇ|ᴜsᴇʀ_ɪᴅ​]"
            )
            return
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        from_user = message.from_user
        sudoers = await get_sudoers()
        if user.id == from_user.id:
            await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴʙʟᴏᴄᴋ ʏᴏᴜʀsᴇʟꜰ?")
        elif user.id == BOT_ID:
            await message.reply_text("sʜᴏᴜʟᴅ ɪ ᴜɴʙʟᴏᴄᴋ ᴍʏsᴇʟꜰ? ʙᴜᴛ ɪ'ᴍ ɴᴏᴛ ʙʟᴏᴄᴋᴇᴅ")
        elif user.id in sudoers:
            await message.reply_text("sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ'ᴛ ʙᴇ ʙʟᴏᴄᴋᴇᴅ/ᴜɴʙʟᴏᴄᴋᴇᴅ.")
        else:
            is_gbanned = await is_gbanned_user(user.id)
            if not is_gbanned:
                await message.reply_text("ʜᴇ's ᴀʟʀᴇᴀᴅʏ ꜰʀᴇᴇ, ᴡʜʏ ʙᴜʟʟʏ ʜɪᴍ ᴜɴᴄʟᴇ ?")
            else:
                await remove_gban_user(user.id)
                await message.reply_text(f"ᴜɴɢʙᴀɴɴᴇᴅ!")
        return
    from_user_id = message.from_user.id
    user_id = message.reply_to_message.from_user.id
    mention = message.reply_to_message.from_user.mention
    sudoers = await get_sudoers()
    if user_id == from_user_id:
        await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜɴʙʟᴏᴄᴋ ʏᴏᴜʀsᴇʟꜰ?")
    elif user_id == BOT_ID:
        await message.reply_text(
            "sʜᴏᴜʟᴅ ɪ ᴜɴʙʟᴏᴄᴋ ᴍʏsᴇʟꜰ? ʙᴜᴛ ɪ'ᴍ ɴᴏᴛ ʙʟᴏᴄᴋᴇᴅ."
        )
    elif user_id in sudoers:
        await message.reply_text("sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ'ᴛ ʙᴇ ʙʟᴏᴄᴋᴇᴅ/ᴜɴʙʟᴏᴄᴋᴇᴅ.")
    else:
        is_gbanned = await is_gbanned_user(user_id)
        if not is_gbanned:
            await message.reply_text("ʜᴇ's ᴀʟʀᴇᴀᴅʏ ꜰʀᴇᴇ, ᴡʜʏ ʙᴜʟʟʏ ʜɪᴍ ᴜɴᴄʟᴇ?")
        else:
            await remove_gban_user(user_id)
            await message.reply_text(f"ᴜɴɢʙᴀɴɴᴇᴅ!")


chat_watcher_group = 5


@app.on_message(group=chat_watcher_group)
async def chat_watcher_func(_, message):
    try:
        userid = message.from_user.id
    except Exception:
        return
    checking = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    if await is_gbanned_user(userid):
        try:
            await message.chat.kick_member(userid)
        except Exception:
            return
        await message.reply_text(
            f"{checking} ɪs ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ʙʏ sᴜᴅᴏ ᴜsᴇʀs ᴀɴᴅ ʜᴀs ʙᴇᴇɴ ᴋɪᴄᴋᴇᴅ ᴏᴜᴛ ᴏꜰ ᴛʜᴇ ᴄʜᴀᴛ.\n\n**ᴘᴏssɪʙʟᴇ ʀᴇᴀsᴏɴ:** ᴘᴏᴛᴇɴᴛɪᴀʟ sᴘᴀᴍᴍᴇʀ ᴀɴᴅ ᴀʙᴜsᴇʀ​."
        )


## UPDATE


@app.on_message(filters.command("update") & filters.user(SUDOERS))
async def update(_, message):
    m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
    if str(m[0]) != "A":
        x = await message.reply_text("ꜰᴏᴜɴᴅ ᴜᴘᴅᴀᴛᴇs ! ᴘᴜsʜɪɴɢ ɴᴏᴡ.")
        return os.system(f"kill -9 {os.getpid()} && python3 -m Anonymous")
    else:
        await message.reply_text("ᴀʟʀᴇᴀᴅʏ ᴜᴘᴅᴀᴛᴇᴅ​!")


# Broadcast Message


@app.on_message(filters.command("broadcast_pin") & filters.user(SUDOERS))
async def broadcast_message_pin_silent(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent}  ᴄʜᴀᴛs ᴡɪᴛʜ {pin} ᴘɪɴs.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴍᴇssᴀɢᴇ]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent} ᴄʜᴀᴛs ᴡɪᴛʜ {pin} ᴘɪɴs.**"
    )


@app.on_message(filters.command("broadcast_pin_loud") & filters.user(SUDOERS))
async def broadcast_message_pin_loud(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=False)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent}  ᴄʜᴀᴛs ᴡɪᴛʜ {pin} ᴘɪɴs.**"
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴍᴇssᴀɢᴇ]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            try:
                await m.pin(disable_notification=False)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent} ᴄʜᴀᴛs ᴡɪᴛʜ {pin} ᴘɪɴs.**"
    )


@app.on_message(filters.command("broadcast") & filters.user(SUDOERS))
async def broadcast(_, message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await app.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent} ᴄʜᴀᴛs.**")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**Usage**:\n/broadcast [ᴍᴇssᴀɢᴇ] ᴏʀ [ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ ᴍᴇssᴀɢᴇ]"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await app.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ {sent} ᴄʜᴀᴛs.**")


# Clean


@app.on_message(filters.command("clean") & filters.user(SUDOERS))
async def clean(_, message):
    dir = "downloads"
    dir1 = "cache"
    shutil.rmtree(dir)
    shutil.rmtree(dir1)
    os.mkdir(dir)
    os.mkdir(dir1)
    await message.reply_text("sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴄʟᴇᴀɴᴇᴅ ᴀʟʟ **ᴛᴇᴍᴘ** ᴅɪʀ(s)!")
