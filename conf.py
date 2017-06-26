import os

PICAMDIR = os.environ["PICAMDIR"]
PICAMSTATE = os.path.join(PICAMDIR, 'state')
PICAMHOOKS = os.path.join(PICAMDIR, 'hooks')

MEDIADIR = os.environ["MESSAGERIEMEDIADIR"]
PHOTOSDIR = os.path.join(MEDIADIR, 'photo')

PLAYLISTID = os.environ["PLAYLISTID"]
CONFDIR = os.environ["MESSAGERIECONFDIR"]
SECRETFILE = os.environ["MESSAGERIESECRETFILE"]
OAUTH2FILE = os.environ["OAUTH2FILE"]

OAUTH2PATH = os.path.join(CONFDIR,OAUTH2FILE)
CLIENT_SECRETS_FILE = os.path.join(CONFDIR, SECRETFILE) 

