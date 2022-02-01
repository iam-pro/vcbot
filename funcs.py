import yt_dlp, json, re
from client import QUEUE

ydl_opts = {"format": "bestaudio", "no-playlist": True, "geo-bypass": True}
ydl = yt_dlp.YoutubeDL(ydl_opts)

def add_to_queue(chat_id, song_name, from_user):
    try:
        n = sorted(list(QUEUE[int(chat_id)].keys()))
        play_at = n[-1] + 1
    except BaseException:
        play_at = 1
    if QUEUE.get(int(chat_id)):
        QUEUE[int(chat_id)].append(
            [
                {
                    "title": song_name,
                    "from_user": from_user,
                }
            ]
        )
    else:
        QUEUE.update(
            {
                int(chat_id): [
                    {
                        "title": song_name,
                        "from_user": from_user,
                    }
                ]
            }
        )
    return QUEUE[int(chat_id)]

def get_from_queue(chat_id):
    try:
        info = QUEUE[int(chat_id)][0]
    except IndexError:
        return
    title = info["title"]
    from_user = info["from_user"]
    return title, from_user

async def get_yt_dict(query):
    if re.search("youtu", query):
        omk = ydl.extract_info(f"{query}", download=False)
        return omk
    omk = ydl.extract_info(f"ytsearch:{query}", download=False)
    yt = omk["entries"][0]
    return yt
