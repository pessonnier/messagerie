import httplib2
import os
import sys

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow, argparser

# variables à personnaliser pour chaques déploiements
CONFDIR = '/home/pi/prog/pmessagerie/'
PLAYLISTID = 'PL19vuSI02yWn7h0wBa8T6FOMwiqwadB97' # salle c
fé privée
# 'PLA9Pn-3QZQ4uexuT6Gg_SZjk2IOFeOMjZ' zazezy unlisted
OAUTH2FILE = CONFDIR+'RW_sallecafe.oauth2.json'
CLIENT_SECRETS_FILE = CONFDIR+'breuille.client_secrets.json

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
YOUTUBE_SCOPE = "https://www.googleapis.com/auth/youtube"


args = argparser.parse_args()

def get_authenticated_service(args):
  flow = flow_from_clientsecrets(
    CLIENT_SECRETS_FILE,
    scope=YOUTUBE_SCOPE,
    message='pas identifie avec '+CLIENT_SECRETS_FILE)
  storage = Storage(OAUTH2FILE)
  credentials = storage.get()

  if credentials is None or credentials.invalid:
    credentials = run_flow(flow, storage, args)

  return build(
    YOUTUBE_API_SERVICE_NAME,
    YOUTUBE_API_VERSION,
    http=credentials.authorize(httplib2.Http()))

