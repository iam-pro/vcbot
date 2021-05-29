import traceback, ffmpeg
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

@bot.on_message(filters.command("joinvc"))
async def joinvc(_, m):
    try:
        await m.reply_text(f"{vc.active_calls}", quote=True)

    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)

@bot.on_message(filters.command("play"))
async def playvc(_, m):
    if not m.from_user.id == 1303895686:
        return
    text = m.text.split(" ", 1)
    ytdetails = await get_yt_dict(text[1])
    chat_id = m.chat.id
    info_dict = download(ytdetails["id"], chat_id)
    title = info_dict["title"]
    thumb = info_dict["thumbnails"][1]["url"]
    duration = info_dict["duration"]
    transcode(f"input{chat_id}.webm", chat_id)
    msg = f"Playing {title} !"
    vc.join_group_call(
        m.chat.id,
        f"input{chat_id}.raw",
    )
    await m.reply(msg)

bot.start()
p = Process(target=idle).start()
vc.run()
