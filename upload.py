# d'après
# https://stackoverflow.com/questions/21228815/adding-youtube-video-to-playlist-using-python
# https://github.com/youtube/api-samples/blob/master/python/upload_video.py

import httplib2
import os
import sys

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

httplib2.RETRIES = 1

PLAYLISTID='PLA9Pn-3QZQ4uexuT6Gg_SZjk2IOFeOMjZ'
OAUTH2FILE='/home/pi/prog/pmessagerie/RW-oauth2.json'
CLIENT_SECRETS_FILE = "/home/pi/prog/pmessagerie/client_secrets.json"

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"

def get_authenticated_service():
  flow = flow_from_clientsecrets(
    CLIENT_SECRETS_FILE, 
    scope=YOUTUBE_SCOPE,
    message='pas identifie avec '+CLIENT_SECRETS_FILE)
  storage = Storage(OAUTH2FILE)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run(flow, storage)

  return build(
    YOUTUBE_API_SERVICE_NAME, 
    YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))


def add_video_to_playlist(youtube,videoID,playlistID):
  add_video_request=youtube.playlistItems().insert(
  part="snippet",
  body={
    'snippet': {
      'playlistId': playlistID, 
      'resourceId': {
        'kind': 'youtube#video',
        'videoId': videoID
      }
      #'position': 0
    }
  }
   ).execute()

def initialize_upload(youtube, file, title, category=22, description='rien', tags=[], diffusion='unlisted'):
  body=dict(
    snippet=dict(
      title=title,
      description=description,
      tags=tags,
      categoryId=category
    ),
    status=dict(
      privacyStatus=diffusion
    )
  )

  # Call the API's videos.insert method to create and upload the video.
  insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(file, chunksize=-1, resumable=True)
  )

  return resumable_upload(insert_request)

# This method implements an exponential backoff strategy to resume a
# failed upload.
def resumable_upload(insert_request):
  response = None
  error = None
  retry = 0
  while response is None:
    try:
      print ("Uploading file...")
      status, response = insert_request.next_chunk()
      if response is not None:
        if 'id' in response:
          print ("Video id '%s' was successfully uploaded." % response['id'])
        else:
          exit("The upload failed with an unexpected response: %s" % response)
    except (HttpError) as e:
      if e.resp.status in RETRIABLE_STATUS_CODES:
        error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                             e.content)
      else:
        raise
    except (RETRIABLE_EXCEPTIONS) as e:
      error = "A retriable error occurred: %s" % e

    if error is not None:
      print (error)
      retry += 1
      if retry > MAX_RETRIES:
        exit("No longer attempting to retry.")

      max_sleep = 2 ** retry
      sleep_seconds = random.random() * max_sleep
      print ("Sleeping %f seconds and then retrying..." % sleep_seconds)
      time.sleep(sleep_seconds)
  return response

def upload(file):
  youtube = get_authenticated_service()
  response = initialize_upload(youtube,
    file=file,
    title=file.split('/')[-1].split('.')[0],
    description='',
    tags=[],
    diffusion='unlisted',
    category=22)
  add_video_to_playlist(youtube,response['id'],PLAYLISTID)

# obtenir l'id de la playliste
# a faire

if __name__ == '__main__':
  youtube = get_authenticated_service()
  response = initialize_upload(youtube,
    file='/home/pi/prog/messagerie/rec/archive/2017-06-08_00-03-27.ts',
    title='t4',
    description='description',
    tags=['k1','k2'],
    diffusion='unlisted',
    category=22)
  add_video_to_playlist(youtube,response['id'],PLAYLISTID)

