import youtube_dl, json
from client import QUEUE

ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

def add_to_queue(chat_id, song_name, from_user):
    try:
        n = sorted(list(QUEUE[int(chat_id)].keys()))
        play_at = n[-1] + 1
    except BaseException:
        play_at = 1
    if QUEUE.get(int(chat_id)):
        QUEUE[int(chat_id)].update(
            {
                play_at: {
                    "title": song_name,
                    "from_user": from_user,
                }
            }
        )
    else:
        QUEUE.update(
            {
                int(chat_id): {
                    play_at: {
                        "title": song_name,
                        "from_user": from_user,
                    }
                }
            }
        )
    return QUEUE[int(chat_id)]

def get_from_queue(chat_id):
    play_this = list(QUEUE[int(chat_id)].keys())[0]
    info = QUEUE[int(chat_id)][play_this]
    title = info["title"]
    from_user = info["from_user"]
    return title, play_this, from_user

async def get_yt_dict(query):
  omk = ydl.extract_info(f"ytsearch:{query}", False)
  yt = omk["entries"][0]
  return yt
