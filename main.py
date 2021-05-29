import traceback, ffmpeg
from pytgcalls import GroupCall
from pyrogram import idle
from client import *
from funcs import *


ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)
vc = GroupCall(
    client=user,
    input_filename=f"input.raw",
    play_on_repeat=False,
    enable_logs_to_console=True,
)
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

@bot.on_message(filters.command("joinvc") & filters.user(AuthUsers))
async def joinvc(_, m):
    try:

        if vc.is_connected:
            try:
                await m.reply_text("Already in Voice Chat!", quote=True)
            except:
                await bot.send_message(m.chat.id, "Already in Voice Chat!")
            return
        await vc.start(m.chat.id)
        await m.reply_text("Joined The Voice Chat!", quote=True)

    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)

@bot.on_message(filters.command("play") & filters.user(AuthUsers))
async def playvc(_, m):
    text = message.text.split(None, 2)[1:]
    ytdetails = await get_yt_dict(text[1])
    info_dict = download(ytdetails["id"], m.chat.id)
    title = info_dict["title"]
    thumb = info_dict["thumbnails"][1]["url"]
    duration = info_dict["duration"]
    transcode(f"input{m.chat.id}.webm", m.chat.id)
    vc = GroupCall(
        client=user,
        input_filename=f"input{m.chat.id}.raw",
        play_on_repeat=False,
        enable_logs_to_console=False,
    )
    if not vc.is_connected:
        await vc.start(m.chat.id)
    msg = f"Playing {title} !"
    await m.reply(msg)

bot.start()
user.start()
idle()
