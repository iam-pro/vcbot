import youtube_dl, json
from youtube_search import YoutubeSearch

ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

async def get_yt_dict(query):
  omk = YoutubeSearch(query, max_results=1).to_json()
  yt = json.loads(omk)["videos"][0]
  return yt
