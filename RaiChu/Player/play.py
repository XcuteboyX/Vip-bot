Pimport io
from os import path
from typing import Callable
from asyncio.queues import QueueEmpty
import os
import random
import re
import youtube_dl
import youtube_dl
import aiofiles
import aiohttp
from RaiChu.converter import convert
import ffmpeg
import requests
from Process.fonts import CHAT_TITLE
from PIL import Image, ImageDraw, ImageFont
from RaiChu.config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2, IMG_5
from Process.filters import command, other_filters
from Process.queues import QUEUE, add_to_queue
from Process.main import call_py, aman as user
from Process.utils import bash
from Process.main import bot as Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream.quality import MediumQualityVideo
from pytgcalls.types.input_stream import AudioImagePiped, AudioVideoPiped
from youtubesearchpython import VideosSearch
from Process.design.thumbnail import play_thumb, queue_thumb
from RaiChu.inline import stream_markup, audio_markup

def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1).result()
        data = search["result"][0]
        songname = data["title"]
        url = data["link"]
        duration = data["duration"]
        thumbnail = f"https://i.ytimg.com/vi/{data['id']}/hqdefault.jpg"
        videoid = data["id"]
        return [songname, url, duration, thumbnail, videoid]
    except Exception as e:
        print(e)
        return 0


async def ytdl(format: str, link: str):
    stdout, stderr = await bash(f'yt-dlp --geo-bypass -g -f "[height<=?720][width<=?1280]" {link}')
    if stdout:
        return 1, stdout.split("\n")[0]
    return 0, stderr

chat_id = None
DISABLED_GROUPS = []
useer = "NaN"
ACTV_CALLS = []

    
@Client.on_message(command(["play", "cplay", "mukku", "tg", "vip", "kittu", "p", "vplay", f"play@{BOT_USERNAME}"]) & other_filters)
async def play(c: Client, m: Message):
    await m.delete()
    replied = m.reply_to_message
    chat_id = m.chat.id
    user_id = m.from_user.id
    buttons = audio_markup(user_id)
    if m.sender_chat:
        return await m.reply_text("You're an __Anonymous__ Admin !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"Error:\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 𝗧𝗼 𝘂𝘀𝗲 𝗺𝗲, 𝗜 𝗻𝗲𝗲𝗱 𝘁𝗼 𝗯𝗲 𝗮𝗻 **𝐀𝐝𝐦𝐢𝐧𝐢𝐬𝐭𝐫𝐚𝐭𝐨𝐫😌** 𝘄𝗶𝘁𝗵 𝘁𝗵𝗲 𝗳𝗼𝗹𝗹𝗼𝘄𝗶𝗻𝗴 **𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧𝐬🥀**:\n\n» ❌ 𝙳𝚎𝚕𝚎𝚝𝚎 𝙼𝚎𝚜𝚜𝚊𝚐𝚎𝚜🍁\n» ❌ __Add users__\n» ❌ 𝙼𝚊𝚗𝚊𝚐𝚎 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝🍁\n\n🥀𝗗𝗮𝘁𝗮 𝗜𝘀 𝗔𝘂𝘁𝗼𝗺𝗮𝘁𝗶𝗰 𝗥𝗲𝗹𝗼𝗮𝗱 𝗔𝗳𝘁𝗲𝗿 𝗣𝗿𝗼𝗺𝗼𝘁𝗲 𝗠𝗲🥀"
        )
        return
    if not a.can_manage_voice_chats: 
        await m.reply_text(
            "𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻🥺:" + "\n\n» ❌ 𝙼𝚊𝚗𝚊𝚐𝚎 𝚅𝚒𝚍𝚎𝚘 𝙲𝚑𝚊𝚝🍁"
        )
        return
    if not a.can_delete_messages:
        await m.reply_text(
            "𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻🥺:" + "\n\n» ❌ 𝙳𝚎𝚕𝚎𝚝𝚎 𝙼𝚎𝚜𝚜𝚊𝚐𝚎𝚜🍁"
        )
        return
    if not a.can_invite_users:
        await m.reply_text("𝗠𝗶𝘀𝘀𝗶𝗻𝗴 𝗥𝗲𝗾𝘂𝗶𝗿𝗲𝗱 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗶𝗼𝗻🥺:" + "\n\n» ❌ 𝙰𝚍𝚍 𝚄𝚜𝚎𝚛𝚜🍁")
        return
    try:
        ubot = (await user.get_me()).id
        b = await c.get_chat_member(chat_id, ubot)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **𝐈𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 𝐈𝐧 𝐓𝐡𝐢𝐬 𝐆𝐫𝐨𝐮𝐩** {m.chat.title}\n\n» ** 𝐔𝐧𝐛𝐚𝐧  𝐓𝐡𝐞  𝐔𝐬𝐞𝐫𝐛𝐨𝐭  𝐅𝐢𝐫𝐬𝐭  𝐈𝐟  𝐘𝐨𝐮  𝐖𝐚𝐧𝐭  𝐓𝐨  𝐔𝐬𝐞  𝐓𝐡𝐢𝐬  𝐁𝐨𝐭.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐉𝐨𝐢𝐧**\n\n**𝐑𝐞𝐚𝐬𝐨𝐧**: `{e}`")
                return
        else:
            try:
                invitelink = await c.export_chat_invite_link(
                    m.chat.id
                )
                if invitelink.startswith("https://t.me/+"):
                    invitelink = invitelink.replace(
                        "https://t.me/+", "https://t.me/joinchat/"
                    )
                await user.join_chat(invitelink)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐉𝐨𝐢𝐧**\n\n**𝐑𝐞𝐚𝐬𝐨𝐧**: `{e}`"
                )
    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐀𝐮𝐝𝐢𝐨...🥲**")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else: 
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"**🥳𝐀𝐝𝐝𝐞𝐝 𝐎𝐧 𝐋𝐢𝐧𝐞 »** `{pos}`\n\n**💞𝐒𝐨𝐧𝐠 𝐈𝐧𝐟𝐨: ** [{songname}]({link}) | `𝐌𝐮𝐬𝐢𝐜`\n\n**🌷𝐂𝐡𝐚𝐭 𝐈𝐝: ** `{chat_id}`\n\n**✨𝐏𝐥𝐚𝐲𝐞𝐝 𝐁𝐲: ** {m.from_user.mention()}",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
            else:
             try:
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"**✨𝐍𝐚𝐦𝐞: ** [{songname}]({link})\n\n**🌷𝐂𝐡𝐚𝐭 𝐈𝐝: ** `{chat_id}`\n\n**🎉𝐒𝐭𝐚𝐭𝐮𝐬: ** `𝐏𝐥𝐚𝐲𝐢𝐧𝐠`\n\n**✨𝐏𝐥𝐚𝐲𝐞𝐝 𝐁𝐲: ** {requester}\n\n**🙂𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐓𝐲𝐩𝐞: ** `𝐌𝐮𝐬𝐢𝐜`",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫  𝗘𝗿𝗿𝗼𝗿:\n\n» {e}")
        
    else:
        if len(m.command) < 2:
         await m.reply_photo(
                     photo=f"{IMG_5}",
                    caption="**🌹𝐓𝐘𝐏𝐄= /play 🤖 𝐆𝐢𝐯𝐞 🙃 𝐒𝐨𝐦𝐞 💿 𝐐𝐮𝐞𝐫𝐲 😍 \n💞 𝐓𝐨 🔊 𝐏𝐥𝐚𝐲 🥀 𝐒𝐨𝐧𝐠 🌷...**",
                      reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("❅ 𝐆𝐑𝐎𝐔𝐏 ❅", url=f"https://t.me/TG_FRIENDSS"),
                            InlineKeyboardButton("✧ 𝐎𝐅𝐅𝐈𝐂𝐄 ✧", url=f"https://t.me/VIP_CREATORS")
                        ]
                    ]
                )
            )
        else:
            suhu = await m.reply_text(
        f"⚡"
    )
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("💬 **𝐍𝐨 𝐑𝐞𝐬𝐮𝐥𝐭𝐬 𝐅𝐨𝐮𝐧𝐝.\n 🍁𝐓𝐲𝐩𝐞 𝐀𝐠𝐚𝐢𝐧 𝐖𝐢𝐭𝐡 𝐂𝐨𝐫𝐫𝐞𝐜𝐭 𝐒𝐨𝐧𝐠 𝐍𝐚𝐦𝐞🥀.**")
            else:
                songname = search[0]
                title = search[0]
                url = search[1]
                duration = search[2]
                thumbnail = search[3]
                userid = m.from_user.id
                gcname = m.chat.title
                videoid = search[4]
                dlurl = f"https://www.youtubepp.com/watch?v={videoid}"
                info = f"https://t.me/{BOT_USERNAME}?start=info_{videoid}"
                keyboard = stream_markup(user_id, dlurl)
                playimg = await play_thumb(videoid)
                queueimg = await queue_thumb(videoid)
                await suhu.edit(
                            f"🌹𝐋𝐨𝐚𝐝𝐢𝐧𝐠...😘"
                        )
                format = "bestaudio"
                abhi, ytlink = await ytdl(format, url)
                if abhi == 0:
                    await suhu.edit(f"💬 yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=queueimg,
                            caption=f"🥳𝐀𝐝𝐝𝐞𝐝 𝐎𝐧 𝐋𝐢𝐧𝐞> {pos}\n\n✨𝐏𝐥𝐚𝐲𝐞𝐝 𝐁𝐲: {requester}\n\n💞𝐒𝐨𝐧𝐠 𝐈𝐧𝐟𝐨: [🥀𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞🥀]({info})",
                            reply_markup=InlineKeyboardMarkup(keyboard),
                        )
                    else:
                        try:
                            await suhu.edit(
                            f"❣️𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐖𝐚𝐢𝐭 𝐁𝐚𝐛𝐲😁"
                        )
                            await call_py.join_group_call(

                                chat_id,

                                AudioImagePiped(

                                          ytlink,

                                          playimg,

                               video_parameters=MediumQualityVideo(),

                            ),

                               stream_type=StreamType().local_stream,

                            )

                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)

                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=playimg,
                                caption=f"🎉𝐒𝐭𝐚𝐫𝐭𝐞𝐝 𝐏𝐥𝐲𝐢𝐧𝐠 𝐔𝐫 𝐂𝐮𝐭𝐞 𝐌𝐮𝐬𝐢𝐜😍\n\n✨𝐏𝐥𝐚𝐲𝐞𝐝 𝐁𝐲: {requester}\n\n💞𝐒𝐨𝐧𝐠 𝐈𝐧𝐟𝐨: [🥀𝐂𝐥𝐢𝐜𝐤 𝐇𝐞𝐫𝐞🥀]({info})",
                                reply_markup=InlineKeyboardMarkup(keyboard),
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"💬 𝐄𝐫𝐫𝐨𝐫: `{ep}`")
