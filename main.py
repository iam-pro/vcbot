import traceback, ffmpeg

from pytgcalls import GroupCall
from client import bot, user
vc = GroupCall(
    client=user,
    input_filename="input.raw",
    play_on_repeat=True,
    enable_logs_to_console=False,
)

def transcode(filename):
    ffmpeg.input(filename).output(
            "input.raw", format='s16le', acodec='pcm_s16le',
            ac=2, ar='48k', loglevel='error').overwrite_output().run() 
    os.remove(filename)
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
    if not vc.is_connected:
        await vc.start(m.chat.id)
    text = message.text.split(None, 2)[1:]
    
    
