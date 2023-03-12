from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from RaiChu.config import (
    ASSISTANT_NAME,
    BOT_NAME,
    BOT_USERNAME,
    GROUP_SUPPORT,
    OWNER_NAME,
    UPDATES_CHANNEL,
)
from Process.filters import other_filters2
from time import time
from Process.filters import command
from datetime import datetime
from Process.decorators import authorized_users_only


@Client.on_message(other_filters2)
async def start(_, message: Message):
        await message.reply_photo(
        photo=f"https://te.legra.ph/file/33792e73e6fb56533f770.jpg",
        caption=f"""━━━━━━━━━━━━━━━━━━━━━━━━
🥀 𝐇𝐞𝐥𝐥𝐨, 𝐈 𝐀𝐦 𝐀𝐧 📀 𝐀𝐝𝐯𝐚𝐧𝐜𝐞𝐝 𝐀𝐧𝐝
𝐒𝐮𝐩𝐞𝐫𝐟𝐚𝐬𝐭 𝐕𝐂 𝐏𝐥𝐚𝐲𝐞𝐫 » 𝐅𝐨𝐫 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦
𝐂𝐡𝐚𝐧𝐧𝐞𝐥 𝐀𝐧𝐝 𝐆𝐫𝐨𝐮𝐩𝐬 ✨ ...

┏━━━━━━━━━━━━━━━━━━━┓
┣★ 𝐎𝐰𝐧𝐞𝐫'𝐱𝐃 : @THE_VIP_BOY
┣★ 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 » : @VIP_CREATORS
┣★ 𝐒𝐮𝐩𝐩𝐨𝐫𝐭 » : @TG_FRIENDSS
┗━━━━━━━━━━━━━━━━━━━┛

💐 𝐅𝐞𝐞𝐥 𝐅𝐫𝐞𝐞 𝐓𝐨 🕊️ 𝐀𝐝𝐝 𝐌𝐞 𝐢𝐧 𝐘𝐨𝐮𝐫
𝐆𝐫𝐨𝐮𝐩, 🌺 𝐀𝐧𝐝 𝐄𝐧𝐣𝐨𝐲 ❥︎ 𝐒𝐮𝐩𝐞𝐫 𝐇𝐢𝐠𝐡
𝐐𝐮𝐚𝐥𝐢𝐭𝐲 𝐀𝐮𝐝𝐢𝐨 𝐀𝐧𝐝 𝐕𝐢𝐝𝐞𝐨 🌷 ...

📡 𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐲: [𝐕𝐈𝐏 𝐁𝐎𝐘](https://t.me/the_vip_boy) 💞 ...
━━━━━━━━━━━━━━━━━━━━━━━━
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [                   
                    InlineKeyboardButton(
                        "🌷𝐀𝐝𝐝 𝐌𝐞 𝐌𝐨𝐢 𝐋𝐮𝐯🌷", url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
                    ),
                ],
                [
                    InlineKeyboardButton(
                       "🍁𝐆𝐑𝐎𝐔𝐏🍁", url=f"https://t.me/VIP_CREATORS"
                    ),
                    InlineKeyboardButton(
                       "🥀𝐎𝐅𝐅𝐈𝐂𝐄🥀", url=f"https://t.me/TG_FRIENDSS"
                    )
                ],[
                    InlineKeyboardButton(
                        "★ 𝐎𝐰𝐧𝐞𝐫'𝐱𝐃 ★",
                        url=f"https://t.me/THE_VIP_BOY",
                    ),
                    InlineKeyboardButton(
                        "🌱𝐒𝐨𝐮𝐫𝐜𝐞🌱",
                        url=f"https://github.com/THE-VIP-BOY-OP/VIP-MUSIC",
                    )
                ]
            ]
        ),
     disable_web_page_preview=True
    )


@Client.on_message(command(["repo", "source"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://telegra.ph/file/53299d9b822f47eff93f4.jpg",
        caption=f"""🍒𝐇𝐞𝐫𝐞 𝐈𝐬 𝐓𝐡𝐞 𝐒𝐨𝐮𝐫𝐜𝐞 𝐂𝐨𝐝𝐞 𝐅𝐨𝐫𝐤 𝐀𝐧𝐝 𝐆𝐢𝐯𝐞 𝐒𝐭𝐚𝐫𝐬✨""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌹𝐇𝐄𝐑𝐎𝐊𝐔 𝐌𝐔𝐒𝐈𝐂🌹", url=f"https://github.com/THE-VIP-BOY-OP/VIP-MUSIC")
                ]
            ]
        ),
    )


@Client.on_message(command(["owner"]) & filters.group & ~filters.edited)
async def help(client: Client, message: Message):
    await message.reply_photo(
        photo=f"https://te.legra.ph/file/2ff2dab0dd5953e674c79.jpg",
        caption=f"""🍁𝐂𝐋𝐈𝐂𝐊🥰𝐁𝐄𝐋𝐎𝐖💝𝐁𝐔𝐓𝐓𝐎𝐍✨𝐓𝐎🙊𝐃𝐌❤️𝐎𝐖𝐍𝐄𝐑🍁""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🌹 𝐕𝐈𝐏 𝐁𝐎𝐘 🌹", url=f"https://t.me/THE_VIP_BOY")
                ]
            ]
        ),
    )
