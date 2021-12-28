import os

import speedtest
import wget
from pyrogram import Client, filters
from pyrogram.types import Message

from Anonymous import BOT_ID, SUDOERS, app

__MODULE__ = "Speedtest"
__HELP__ = """

/speedtest 
» ᴄʜᴇᴄᴋ sᴇʀᴠᴇʀ ʟᴀᴛᴇɴᴄʏ & sᴘᴇᴇᴅ​.

"""


def bytes(size: float) -> str:
    """humanize size"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


@app.on_message(filters.command("speedtest") & ~filters.edited)
async def statsguwid(_, message):
    m = await message.reply_text("ʀᴜɴɴɪɴɢ sᴘᴇᴇᴅ ᴛᴇsᴛ")
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        m = await m.edit("ʀᴜɴɴɪɴɢ ᴅᴏᴡɴʟᴏᴀᴅ sᴘᴇᴇᴅ ᴛᴇsᴛ")
        test.download()
        m = await m.edit("ʀᴜɴɴɪɴɢ ᴜᴘʟᴏᴀᴅ sᴘᴇᴇᴅ ᴛᴇsᴛ")
        test.upload()
        test.results.share()
        result = test.results.dict()
    except Exception as e:
        return await m.edit(e)
    m = await m.edit("sʜᴀʀɪɴɢ sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs")
    path = wget.download(result["share"])

    output = f"""**sᴘᴇᴇᴅᴛᴇsᴛ ʀᴇsᴜʟᴛs​**
    
<u>**ᴄʟɪᴇɴᴛ:**</u>
**__ɪsᴘ:__** {result['client']['isp']}
**__ᴄᴏᴜɴᴛʀʏ:__** {result['client']['country']}
  
<u>**sᴇʀᴠᴇʀ:**</u>
**__ɴᴀᴍᴇ:__** {result['server']['name']}
**__ᴄᴏᴜɴᴛʀʏ:__** {result['server']['country']}, {result['server']['cc']}
**__sᴘᴏɴsᴏʀ:__** {result['server']['sponsor']}
**__ʟᴀᴛᴇɴᴄʏ:__** {result['server']['latency']}  
**__ᴘɪɴɢ:__** {result['ping']}"""
    msg = await app.send_photo(
        chat_id=message.chat.id, photo=path, caption=output
    )
    os.remove(path)
    await m.delete()
