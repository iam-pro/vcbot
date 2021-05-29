import youtube_dl
from youtubesearchpython.__future__ import VideosSearch

ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

async def get_yt_dict(query):
  omk = VideosSearch(query, limit=1)
  omk = await omk.next()
  yt = omk["result"][0]
  return yt
