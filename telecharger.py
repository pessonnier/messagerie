import youtubeutil as y
import youtube_dl
import os
import conf
import requests as r
import re

# XXX utiliser nextPageToken voir https://developers.google.com/youtube/v3/docs/playlistItems/list
def telecharger():
  youtube=y.get_authenticated_service(y.args)
  liste = youtube.playlistItems().list(playlistId=conf.PLAYLISTID, maxResults=25, part='snippet,contentDetails').execute()
  print(liste)
  # toute la playliste
  for item in liste['items']:
    videoId = item['snippet']['resourceId']['videoId']
    print(item['snippet']['title'])
    titre = re.sub('[&\"\'\(\`\\@\)\{\},;:\?\./!\*<>’]', '', item['snippet']['title'])
    vignette = item['snippet']['thumbnails']['default']['url']
    print('DL : ' + videoId + ' ' + titre)
    with youtube_dl.YoutubeDL({'outtmpl':os.path.join(conf.MEDIADIR,titre)}) as ydl:
      ydl.download(['http://www.youtube.com/watch?v='+videoId])
    req = r.get(vignette)
    nomimage = titre + '.jpg'
    if os.path.exists(os.path.join(conf.MEDIADIR, nomimage)):
      print('l image '+nomimage+' existe déjà')
      continue 
    with open(os.path.join(conf.MEDIADIR, nomimage), 'wb') as image:
      for bl in req.iter_content(chunk_size=1024):
        image.write(bl)

if __name__ == '__main__':
  telecharger()
