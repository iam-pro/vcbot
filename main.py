import traceback, ffmpeg
import asyncio
from pytgcalls import PyTgCalls, StreamType, idle
from pytgcalls.types import Update
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream import InputStream
from client import *
from multiprocessing import Process
from funcs import *

ydl_opts = {"format": "bestaudio"}
ydl = youtube_dl.YoutubeDL(ydl_opts)
vc = PyTgCalls(user)
#vc.start()
queue = []

def check_value(data, val):
    if len(data) > 0:
      for item in data:
          if val in item.values():
              print("sdasd Yes")
              return item["is_playing"]
          else:
              print("sex")
              return False
    else:
      print(len(data))
      print("Nooooooooo")
      return False

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
        await m.reply_text(f"{vc.active_calls}\n\n{QUEUE}", quote=True)

    except Exception as e:
        print(traceback.print_exc())
        await m.reply(e)

@bot.on_message(filters.command("skip"))
async def skipvc(_, m):
    mssg = await m.reply_text("Skipped current song!")
    song, pos, from_user = get_from_queue(m.chat.id)
    ytdetails = await get_yt_dict(song)
    info_dict = download(ytdetails["id"], m.chat.id)
    title = info_dict["title"]
    duration = info_dict["duration"]
    transcode(f"input{m.chat.id}.webm", m.chat.id)
    await vc.change_stream(m.chat.id, InputStream(InputAudioStream(f"input{m.chat.id}.raw"),),)
    QUEUE[m.chat.id].pop(pos)
    await bot.send_document(m.chat.id, f"https://i.ytimg.com/vi/{ytdetails['id']}/hq720.jpg", caption=f"Playing {title}\nDuration: {duration}")
    await asyncio.sleep(duration + 5)
    os.remove(f"input{m.chat.id}.raw")

@bot.on_message(filters.command("play"))
async def playvc(_, m):
    text = m.text.split(" ", 1)
    print(AuthUsers)
    if str(m.from_user.id) not in AuthUsers:
        return
    _check = check_value(json.loads(vc.active_calls.__str__()), m.chat.id)
    print(_check)
    if _check == False:
        ytdetails = await get_yt_dict(text[1])
        chat_id = m.chat.id
        info_dict = download(ytdetails["id"], chat_id)
        title = info_dict["title"]
        thumb = info_dict["thumbnails"][1]["url"]
        duration = info_dict["duration"]
        dl = download(info_dict["webpage_url"], chat_id)
        transcode(f"input{chat_id}.webm", chat_id)
        msg = f"Playing {title} !"
        await vc.join_group_call(
            m.chat.id,
            InputStream(
                InputAudioStream(
                    f"input{chat_id}.raw",
                ),
            ),
            stream_type=StreamType().local_stream
        )
        await m.reply(msg)
    elif _check == True:
        print(m.chat.id, text[1], m.from_user.id)
        add_to_queue(m.chat.id, text[1], m.from_user.id)
        await m.reply("added to queue")

@vc.on_stream_end()
async def streamhandler(vc: PyTgCalls, update: Update):
    song, pos, from_user = get_from_queue(update.chat_id)
    ytdetails = await get_yt_dict(song)
    info_dict = download(ytdetails["id"], update.chat_id)
    title = info_dict["title"]
    thumb = info_dict["thumbnails"][1]["url"]
    duration = info_dict["duration"]
    transcode(f"input{update.chat_id}.webm", update.chat_id)
    msg = f"Playing {title} !"
    await vc.change_stream(update.chat_id, InputStream(InputAudioStream(f"input{update.chat_id}.raw"),),)
    QUEUE[update.chat_id].pop(pos)
    msgg = await bot.send_message(update.chat_id, f"Playing {song}")
    await asyncio.sleep(duration + 5)
    await msgg.delete()

bot.start()
vc.start()
idle()
