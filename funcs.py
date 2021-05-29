import youtube_dl
from youtubesearchpython.__future__ import VideosSearch

ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

async def get_yt_id(query):
  omk = VideosSearch("faded", limit=1)
  omk = await omk.next()
  ytid = omk["result"][0]["id"]
  return ytid
