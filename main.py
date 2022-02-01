import traceback
import ffmpeg
import re
import asyncio
import datetime
from pytgcalls import PyTgCalls, StreamType, idle
from pytgcalls.types import Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.types.input_stream.quality import HighQualityVideo
from pytgcalls.types.input_stream import InputStream
from pytgcalls.exceptions import AlreadyJoinedError
from client import *
from multiprocessing import Process
from funcs import *

vc = PyTgCalls(user)
# vc.start()
queue = []


async def is_admin(chat_id, user):
    return user in [
        x.user.id
        async for x in bot.iter_chat_members(chat_id, filter="administrators")
        if x.can_manage_voice_chats
    ]


async def yt_stream(query, only_audio=True):
    if only_audio:
        if re.search("youtu", query):
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "-g",
                "-f",
                "bestaudio/best",
                f"{query}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            return stdout.decode().split("\n")[0]
        else:
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "-g",
                "-f",
                # CHANGE THIS BASED ON WHAT YOU WANT
                "best[height<=?720][width<=?1280]",
                f"ytsearch1:{query}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            return stdout.decode().split("\n")[0]
    if re.search("youtu", query):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{query}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        return stdout.decode().split("\n")[0]
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        # CHANGE THIS BASED ON WHAT YOU WANT
        "best[height<=?720][width<=?1280]",
        f"ytsearch1:{query}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    return stdout.decode().split("\n")[0]


def check_value(data, val):
    if len(data) > 0:
        if val in data and data[val] == 1:
            is_playing = True
        else:
            is_playing = False
    else:
        is_playing = False
    return is_playing


def transcode(filename: str, chat_id: int):
    ffmpeg.input(filename).output(
        f"input{chat_id}.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=1,
        ar="48k",
        loglevel="error",
    ).overwrite_output().run()
    os.remove(filename)


def download(idd, chat_id):
    info_dict = ydl.extract_info(idd, download=False)
    audio_file = ydl.prepare_filename(info_dict)
    ydl.process_info(info_dict)
    os.rename(audio_file, f"input{chat_id}.webm")
    return info_dict


@bot.on_message(filters.command("vcs"))
async def joinvc(_, m):
    if str(m.chat.id) not in AuthChats:
        return
    if await is_admin(m.chat.id, m.from_user.id) == False:
        return
    try:
        await m.reply_text(f"{vc._call_holder._calls}\n\n{QUEUE}", quote=True)
    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)


@bot.on_message(filters.command("stop"))
async def joinvc(_, m):
    if str(m.chat.id) not in AuthChats:
        return
    if await is_admin(m.chat.id, m.from_user.id) == False:
        return
    await vc.leave_group_call(m.chat.id)


@bot.on_message(filters.command("skip"))
async def skipvc(_, m):
    if str(m.chat.id) not in AuthChats:
        return
    if await is_admin(m.chat.id, m.from_user.id) == False:
        return
    mssg = await m.reply_text("Skipped current song!")
    song, from_user = get_from_queue(m.chat.id)
    info_dict = ytdetails = await get_yt_dict(song)
    title = info_dict["title"]
    remote = await yt_stream(song)
    xx = datetime.timedelta(seconds=info_dict["duration"])
    if str(xx).startswith("0"):
        duration = str(xx)[2:]
    else:
        duration = str(xx)
    await vc.change_stream(m.chat.id, AudioPiped(remote, HighQualityAudio()))
    QUEUE[m.chat.id].pop(0)
    await bot.send_photo(
        m.chat.id,
        f"https://i.ytimg.com/vi/{ytdetails['id']}/maxresdefault.jpg",
        caption=f"Playing {title}\nDuration: {duration}",
    )


@bot.on_message(filters.command("yt"))
async def ytvc(_, m):
    if str(m.chat.id) not in AuthChats:
        return
    if await is_admin(m.chat.id, m.from_user.id) == False:
        return
    text = m.text.split(" ", 1)
    remote = await yt_stream(text[1], only_audio=False)
    try:
        await vc.join_group_call(
            m.chat.id, AudioVideoPiped(remote, HighQualityAudio(), HighQualityVideo())
        )
    except AlreadyJoinedError:
        _check = check_value(vc._call_holder._calls, m.chat.id)
        if _check == False:
            await vc.change_stream(
                m.chat.id,
                AudioVideoPiped(remote, HighQualityAudio(), HighQualityVideo()),
            )
        else:
            return
    await m.reply_text("accha")


@bot.on_message(filters.command("play"))
async def playvc(_, m):
    text = m.text.split(" ", 1)
    if str(m.chat.id) not in AuthChats:
        return
    if await is_admin(m.chat.id, m.from_user.id) == False:
        return
    _check = check_value(vc._call_holder._calls, m.chat.id)
    print(_check)
    if _check == False:
        ytdetails = await get_yt_dict(text[1])
        chat_id = m.chat.id
        remote = await yt_stream(text[1])
        title = ytdetails["title"]
        #        print(info_dict["thumbnails"])
        #        thumb = info_dict["thumbnails"][1]["url"]
        xx = datetime.timedelta(seconds=ytdetails["duration"])
        if str(xx).startswith("0"):
            duration = str(xx)[2:]
        else:
            duration = str(xx)
        try:
            await vc.join_group_call(m.chat.id, AudioPiped(remote, HighQualityAudio()))
        except AlreadyJoinedError:
            await vc.change_stream(m.chat.id, AudioPiped(remote, HighQualityAudio()))
        await bot.send_photo(
            m.chat.id,
            f"https://i.ytimg.com/vi/{ytdetails['id']}/maxresdefault.jpg",
            caption=f"Playing: `{title}`\nDuration: `{duration}`",
        )
    elif _check == True:
        print(m.chat.id, text[1], m.from_user.id)
        add_to_queue(m.chat.id, text[1], m.from_user.id)
        await m.reply("added to queue")


@vc.on_stream_end()
async def streamhandler(vc: PyTgCalls, update: Update):
    song, from_user = get_from_queue(update.chat_id)
    ytdetails = await get_yt_dict(song)
    remote = await yt_stream(song)
    title = ytdetails["title"]
    thumb = ytdetails["thumbnails"][1]["url"]
    xx = datetime.timedelta(seconds=ytdetails["duration"])
    if str(xx).startswith("0"):
        duration = str(xx)[2:]
    else:
        duration = str(xx)
    msg = f"Playing {title} !"
    await vc.change_stream(update.chat_id, AudioPiped(remote, HighQualityAudio()))
    QUEUE[update.chat_id].pop(0)
    await bot.send_photo(
        update.chat_id,
        f"https://i.ytimg.com/vi/{ytdetails['id']}/maxresdefault.jpg",
        caption=f"Playing: `{title}`\nDuration: `{duration}`",
    )


bot.start()
vc.start()
idle()
