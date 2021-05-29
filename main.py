import traceback, ffmpeg
from pytgcalls import PyTgCalls, PyLogs, StreamType
from pyrogram import idle
from client import *
from multiprocessing import Process
from funcs import *

ydl_opts = {"format": "bestaudio"}
ydl = youtube_dl.YoutubeDL(ydl_opts)
vc = PyTgCalls(user, log_mode=PyLogs.verbose)

def transcode(filename: str, chat_id: str):
    ffmpeg.input(filename).output(
        f"input{chat_id}.raw",
        format="s16le",
        acodec="pcm_s16le",
        ac=2,
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

@bot.on_message(filters.regex("joinvc"))
async def joinvc(_, m):
    try:
        if m.chat.id in vc.active_calls:
            try:
                await m.reply_text("Already in Voice Chat!", quote=True)
            except:
                await bot.send_message(m.chat.id, "Already in Voice Chat!")
            return
        await vc.join_group_call(m.chat.id, f"input{m.chat.id}.raw", 48000, vc.get_cache_peer(), StreamType().local_stream,)
        await m.reply_text("Joined The Voice Chat!", quote=True)

    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)

@bot.on_message(filters.regex("play"))
async def playvc(_, m):
    text = m.text.split(None, 2)[1:]
    ytdetails = await get_yt_dict(text[1])
    info_dict = download(ytdetails["id"], m.chat.id)
    title = info_dict["title"]
    thumb = info_dict["thumbnails"][1]["url"]
    duration = info_dict["duration"]
    transcode(f"input{m.chat.id}.webm", m.chat.id)
    vc = vc.join_group_call(
        m.chat.id,
        "input{m.chat.id}.raw",
        48000,
        vc.get_cache_peer(),
        StreamType().local_stream,
    )
    if not vc.is_connected:
        vc.join_group_call(
            m.chat.id,
            "input{m.chat.id}.raw",
            48000,
            vc.get_cache_peer(),
            StreamType().local_stream,
        )
    msg = f"Playing {title} !"
    await m.reply(msg)

p = Process(target=bot.run).start()
p2 = Process(target=vc.run).start()
