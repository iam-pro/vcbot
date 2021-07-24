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

async def get_yt_dict(query):
  omk = ydl.extract_info(f"ytsearch:{query}", False)
  yt = omk["entries"][0]
  return yt
