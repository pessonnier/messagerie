import youtubeutil as y
import youtube_dl
import os
import conf

PLAYLISTID = conf.PLAYLISTID
MEDIADIR = conf.MEDIADIR

youtube=y.get_authenticated_service(y.args)
liste = youtube.playlistItems().list(playlistId=PLAYLISTID, part='snippet,contentDetails').execute()

for item in liste['items']:
  videoId = item['snippet']['resourceId']['videoId']
  titre = item['snippet']['title']
  print('DL : ' + videoId + ' ' + titre)
  with youtube_dl.YoutubeDL({'outtmpl':os.path.join(MEDIADIR,titre)}) as ydl:
    ydl.download(['http://www.youtube.com/watch?v='+videoId])
