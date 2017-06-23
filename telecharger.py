import youtubeutil as y
import youtube_dl
import os
import conf
import requests as r

PLAYLISTID = conf.PLAYLISTID
MEDIADIR = conf.MEDIADIR

youtube=y.get_authenticated_service(y.args)
liste = youtube.playlistItems().list(playlistId=PLAYLISTID, part='snippet,contentDetails').execute()

for item in liste['items']:
  videoId = item['snippet']['resourceId']['videoId']
  titre = item['snippet']['title'].replace('/',' ')
  vignette = item['snippet']['thumbnails']['default']['url']
  print('DL : ' + videoId + ' ' + titre)
  with youtube_dl.YoutubeDL({'outtmpl':os.path.join(MEDIADIR,titre)}) as ydl:
    ydl.download(['http://www.youtube.com/watch?v='+videoId])
  req = r.get(vignette)
  nomimage = titre + '.jpg'
  if os.path.exists(os.path.join(MEDIADIR, nomimage)):
    print('l image '+nomimage+' existe déjà')
    continue 
  with open(os.path.join(MEDIADIR, nomimage), 'wb') as image:
    for bl in req.iter_content(chunk_size=1024):
      image.write(bl)
