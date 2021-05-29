import traceback

from pytgcalls import GroupCall
from client import bot, user
vc = GroupCall(
    client=user,
    input_filename="input.raw",
    play_on_repeat=True,
    enable_logs_to_console=False,
)

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
