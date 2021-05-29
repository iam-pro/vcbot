import youtube_dl, json

ydl_opts = {"format": "bestaudio", "no-playlist": True}
ydl = youtube_dl.YoutubeDL(ydl_opts)

async def get_yt_dict(query):
  omk = ydl.extract_info(f"ytsearch:{query}", False)
  yt = omk["entries"][0]
  return yt
