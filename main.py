import traceback, ffmpeg
import asyncio
from pytgcalls import PyTgCalls, PyLogs, StreamType
from pyrogram import idle
from client import *
from multiprocessing import Process
from funcs import *

ydl_opts = {"format": "bestaudio"}
ydl = youtube_dl.YoutubeDL(ydl_opts)
vc = PyTgCalls(user, log_mode=PyLogs.ultra_verbose)
queue = []

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
    try:
        await m.reply_text(f"{vc.active_calls}", quote=True)

    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)

@bot.on_message(filters.command("play"))
async def playvc(_, m):
    text = m.text.split(" ", 1)
#    if m.from_user.id not in AuthUsers:
#        return
    if m.chat.id in vc.active_calls.keys():
        ytdetails = await get_yt_dict(text[1])
        chat_id = m.chat.id
        info_dict = download(ytdetails["id"], chat_id)
        title = info_dict["title"]
        thumb = info_dict["thumbnails"][1]["url"]
        duration = info_dict["duration"]
        dl = download(info_dict["webpage_url"], chat_id)
        transcode(f"input{chat_id}.webm", chat_id)
        msg = f"Playing {title} !"
        vc.join_group_call(
            m.chat.id,
            f"input{chat_id}.raw",
        )
        await m.reply(msg)
    else:
        add_to_queue(m.chat.id, text[1], m.from_user.id)

@vc.on_stream_end()
async def streamhandler(chat_id: int):
    chat, song, from_user = get_from_queue(chat_id)
    ytdetails = await get_yt_dict(song)
    info_dict = download(ytdetails["id"], chat)
    title = info_dict["title"]
    thumb = info_dict["thumbnails"][1]["url"]
    duration = info_dict["duration"]
    transcode(f"input{chat}.webm", chat)
    msg = f"Playing {title} !"
    vc.change_stream(chat, f"input{chat}.raw")
    QUEUE[chat_id].pop(pos)
    msgg = await bot.send_message(f"Playing {song}")
    if not QUEUE[chat]:
        QUEUE.pop(chat)
    await asyncio.sleep(duration + 5)
    await msgg.delete()

bot.start()
p = Process(target=idle).start()
vc.run()
