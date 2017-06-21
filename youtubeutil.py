import httplib2
import os
import sys
import conf

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

# variables à personnaliser pour chaques déploiements
CONFDIR = conf.CONFDIR 
PLAYLISTID = conf.PLAYLISTID 
OAUTH2PATH = conf.OAUTH2PATH
CLIENT_SECRETS_FILE = conf.CLIENT_SECRETS_FILE

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"


args = argparser.parse_args()

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(
    CLIENT_SECRETS_FILE,
    scope=YOUTUBE_SCOPE,
    message='pas identifie avec '+CLIENT_SECRETS_FILE)
  storage = Storage(OAUTH2PATH)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

