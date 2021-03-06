# Messagerie
échange de messages vidéos entre boites abonnées

# configuration initiale

# installation
sur la base d'une rasbian jessie

### variables
dans .profile :
```
export PICAMDIR=~/pmessagerie
export MESSAGERIEMEDIADIR=~/pmessagerie/media
export PLAYLISTID="XXX"
export MESSAGERIECONFDIR=~/pmessagerie
export MESSAGERIESECRETFILE="MrPlume_secrets.json"
export OAUTH2FILE="RW.oauth2.json"
```

### caméra
activation
- `sudo raspi-config`
- aller dans 5 Interfacing Options
split de la mémoire
 - tests à 16mo
 - tests à 64mo
doc
 - picamera : http://picamera.readthedocs.io/en/release-1.13/quickstart.html

eteindre la led, `disable_camera_led=1` dans `/boot/config.txt`


### upload youtube voir https://developers.google.com/youtube/v3/guides/uploading_a_video
 - `sudo pip3 install --upgrade google-api-python-client` ou sans `sudo` dans un virtualenv
```
Installing collected packages: httplib2, pyasn1, rsa, pyasn1-modules, oauth2client, uritemplate, google-api-python-client
Successfully installed google-api-python-client-1.6.2 httplib2-0.10.3 oauth2client-4.1.1 pyasn1-0.2.3 pyasn1-modules-0.0.9 rsa-3.4.2 uritemplate-3.0.0
```
 - exemples youtube https://github.com/youtube/api-samples/tree/master/python
 - autre api https://github.com/google/google-api-python-client/tree/master/samples
 - creation d'un identifiant d'application dans la console google
 - creation du fichier client_secrets.json
 - clone des demo d'utilisation de l'api youtube : `git clone https://github.com/youtube/api-samples.git`

### picam :
- source : https://github.com/iizukanao/picam
- https://github.com/iizukanao/picam/blob/master/INSTALL.md
- `apt-get install flex bison automake gperf libtool patch texinfo ncurses-dev help2man`
- `sudo apt-get install netcat`
- test `raspistill -v -t 9999999`
- test `raspivid -t 999999 -w 640 -h 480`
- test en mode text : `mplayer -xy 800`
- streaming
```
nc -l 5001 | mplayer -fps 31 -cache 1024 -
raspivid -t 999999 -o - | nc 192.168.1.20 5001
```

### ecran :
- doc : http://www.waveshare.com/wiki/5inch_HDMI_LCD
sudo apt-get install xserver-xorg-input-evdev
sudo cp -rf /usr/share/X11/xorg.conf.d/10-evdev.conf /usr/share/X11/xorg.conf.d/45-evdev.conf
http://www.waveshare.com/w/upload/3/37/Xinput-calibrator_0.7.5-1_armhf.zip
sudo dpkg -i -B xinput-calibrator_0.7.5-1_armhf.deb 
xinput-calibrator --device 6
copie dans /usr/share/X11/xorg.conf.d/99-calibration.conf

### audio bluetooth
doc de configuration initiale : http://youness.net/raspberry-pi/bluetooth-headset-raspberry-pi-3-ad2p-only

après redémarage il suffit de démarer le demon audio `pulseaudio --start` et d'apairer avec le bouton BT de l'enceinte

pour lire 
`paplay -d bluez_sink.30_21_95_5C_A8_A8 /home/pi/prog/pmessagerie/h2g2.ogg/h2g2.ogg`
pour enregistrer depuis le micro usb :
`parecord -r -d alsa_input.usb-0c76_USB_Headphone_Set-00-Set.analog-mono -v boo.wav`
- pour que pulseaudio diffuse par défaut vers le BT : `pacmd set-default-sink bluez_sink.30_21_95_5C_A8_A8`
- pour que omxplayer utilise pulseaudio : `omxplayer -o alsa:pulse Videos/aze.mp4`

#### ne marche pas
ajout de `default-sink = bluez_sink.30_21_95_5C_A8_A8` dans `/etc/pulse/client.conf`

création de `/lib/systemd/system/pulseaudio.service` contenant
```
[Unit]
Description=PulseAudio Daemon

[Install]
WantedBy=multi-user.target

[Service]
Type=simple
PrivateTmp=true
ExecStart=/usr/bin/pulseaudio –system –realtime 
```
installation du service `sudo systemctl --system enable pulseaudio.service`

démarage du service `sudo systemctl --system start pulseaudio.service`

echec aves l'ajout de `sudo -u pi /usr/bin/pulseaudio --start` dans `/etc/rc.local`, connection ok mais la carte bluez n'est plus vue par `pactl`

#### commandes utiles
- pulseaudio --start
- pacmd set-default-sink bluez_sink.30_21_95_5C_A8_A8
- pactl list cards short
- bluetoothctl

### opencv3 :
- http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
- https://github.com/opencv/opencv/releases/tag/3.2.0
- https://github.com/opencv/opencv_contrib/releases/tag/3.2.0

### partage samba
- doc : http://www.framboise314.fr/partager-un-repertoire-sous-jessie-avec-samba/
- modif de `/etc/samba/smb.conf`
```
[SalleCafe]
comment = La salle café
path = /home/pi/pmessagerie/media # comme MESSAGERIEMEDIADIR
writable = yes
guest ok = yes
guest only = yes
create mode = 0777
directory mode = 0777
share modes = yes
```
- chargement de la conf `sudo systemctl restart smbd.service`
- accès depuis un autre poste avec `smb://192.XXX/sallecafe`

### pygame
pour peut-être gérer les evenements du touchscreen
```
sudo apt-get install python3-pygame`
sudo apt-get install libsdl-dev libsdl-image1.2-dev libsdl-mixer1.2-dev libsdl-ttf2.0-dev 
sudo apt-get install libsmpeg-dev libportmidi-dev libavformat-dev libswscale-dev
sudo apt-get install python3-dev python3-numpy
workon XXX
pip install pygame

Collecting pygame
  Using cached pygame-1.9.3.tar.gz
Building wheels for collected packages: pygame
  Running setup.py bdist_wheel for pygame ... done
  Stored in directory: /home/pi/.cache/pip/wheels/3b/24/0d/fef366d21bb01ac20148018a3bb3090193cdd64df596e092e1
Successfully built pygame
Installing collected packages: pygame
Successfully installed pygame-1.9.3
```

tslib = libts-0.0-0 
`sudo apt-get install evtest tslib libts-bin`

calibration : `sudo TSLIB_TSDEVICE=/dev/input/event1 ts_calibrate`
```
xres = 800, yres = 480
Took 7 samples...
Top left : X =  371 Y =  529
Took 6 samples...
Top right : X = 3689 Y =  561
Took 7 samples...
Bot right : X = 3697 Y = 3483
Took 7 samples...
Bot left : X =  391 Y = 3519
Took 10 samples...
Center : X = 2055 Y = 2017
-29.244141 0.211346 -0.001004
-20.026306 0.000076 0.128534
Calibration constants: -1916544 13850 -65 -1312444 5 8423 65536 
```

test : `sudo TSLIB_TSDEVICE=/dev/input/event1 ts_test`

### tas :
- `sudo apt-get install youtube-dl mplayer2 fbi`
- `sudo pip3 install GPIO`
- `pip3 install youtube-dl`
- `sudo apt-get install samba samba-common-bin`
- `pip install requests` voir http://docs.python-requests.org/en/latest/user/quickstart/

### reconaissance faciale
- projet qui encapsule dlib : https://github.com/ageitgey/face_recognition
- projet dlib : https://github.com/davisking/dlib
```
sudo python3 setup.py install
...
Extracting dlib-19.4.99-py3.4-linux-armv7l.egg to /usr/local/lib/python3.4/dist-packages
Adding dlib 19.4.99 to easy-install.pth file

Installed /usr/local/lib/python3.4/dist-packages/dlib-19.4.99-py3.4-linux-armv7l.egg
Processing dependencies for dlib==19.4.99
Finished processing dependencies for dlib==19.4.99
```
- doc install dlib pour rpi : https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

# technique
https://docs.python.org/3.4/tutorial/introduction.html

![26 broches](http://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/images/10000201000002110000012646FC1CA4.png)
![40 broches](http://deusyss.developpez.com/tutoriels/RaspberryPi/PythonEtLeGpio/images/10000201000002B4000001268CC8D3D9.png)

### console
la console google developers se trouve `https://console.developers.google.com/apis/dashboard`

### T°
vérifier la température du CPU
```
vcgencmd measure_temp
```

### flux video
client de test :
- si besoin ouverture de ports sur le client `sudo ufw allow proto udp from 192.168.1.0/24 to any port 5678`
- ecoute du client : `nc -l 5678 | mplayer - -cache 1024`
- emission : `./picam --alsadev hw:1,0 --tcpout tcp://192.168.1.20:5678`

### uploader une video sur la playlist
```
from upload import upload
upload('/home/pi/prog/messagerie/rec/archive/2017-06-07_23-59-19.ts')
```

### configurer pour youtube
- la chaine
- la playliste
- ajouter l'API youtube
- créer un client_secrets.json XXX
- permettre / configurer auth2

### tester la caméra
```
from time import sleep
from picamera import PiCamera
camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
```

### lire une video
- `sudo SDL_VIDEODRIVER=fbcon SDL_FBDEV=/dev/fb0 mplayer -vo sdl  Videos/aze.mp4`
- `omxplayer -o hdmi Videos/aze.mp4`
- sur une enceinte bluetooth : `omxplayer -o alsa:pulse Videos/aze.mp4`

### playlists
- doc : https://developers.google.com/youtube/v3/docs/playlists/list
- la première video d'une playliste
```
youtube.playlistItems().list(playlistId="XXX", part='snippet,contentDetails').execute()['items'][0]['snippet']['resourceId']['videoId']
```

### tester le toucscreen
#### tentative avec pygame
ne retourne pas de bonnes coordonnées
```
sudo /home/pi/.virtualenvs/cv/bin/python3
ou
sudo SDL_MOUSEDRV=TSLIB SDL_MOUSEDEV=/dev/input/event1 TSLIB_TSDEVICE=/dev/input/event1 /home/pi/.virtualenvs/cv/bin/python3

import pygame
from pygame.locals import *
import os
os.putenv('SDL_MOUSEDRV', 'TSLIB')
os.putenv('TSLIB_TSDEVICE', '/dev/input/event1')
os.putenv('SDL_MOUSEDEV', '/dev/input/event1')
os.putenv('SDL_FBDEV', '/dev/fb0')
pygame.init()
lcd = pygame.display.set_mode((800, 480))
#pygame.event.get()

while True:
  for ev in pygame.event.get():
    if ev.type is MOUSEBUTTONDOWN:
      print(ev)
      print(pygame.mouse.get_pos())
```
#### tentative avec evdev
pip install evdev

# spec
- enregistrer son + video
- uploader sur une playliste
- reconnaissance faciale
- sortie audio
- 
- bouton enregistrer
- activer les servomoteurs
- jouer la playliste
- déclancher une action pour un visage préci
- plaque
- alimentation
- bouton eteindre
- projet pour les actions personnalisées
- reconnaître un nouveau visage
- mise à jour
- personnaliser une action par visage

## seq
- faire pivoter en identifiant

# notes
identification github : https://gist.github.com/ageitgey/1ac8dbe8572f3f533df6269dab35df65

pendant `apt-get upgrade`
```
--- /etc/lightdm/lightdm.conf   2016-09-23 05:52:37.980007612 +0200
+++ /etc/lightdm/lightdm.conf.dpkg-new  2016-10-13 14:03:14.000000000 +0200
@@ -96,7 +96,7 @@
 #xdmcp-key=
 #unity-compositor-command=unity-system-compositor
 #unity-compositor-timeout=60
-greeter-session=pi-greeter
+#greeter-session=example-gtk-gnome
 greeter-hide-users=false
 #greeter-allow-guest=true
 #greeter-show-manual-login=false
```

au premier upload
```
pi@pi3:~/prog/mess/api-samples/python $ python upload_video.py --file="/home/pi/Videos/SiaChandelier.mp4" --title="je danse bien" --privacyStatus="private" --noauth_local_webserver
/usr/local/lib/python2.7/dist-packages/oauth2client/_helpers.py:255: UserWarning: Cannot access upload_video.py-oauth2.json: No such file or directory
  warnings.warn(_MISSING_FILE_MESSAGE.format(filename))

Go to the following link in your browser:

    https://accounts.google.com/o/oauth2/auth?scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fyoutube.upload&redirect_uri=urn%3Aietf%3Awg%3Aoauth%3A2.0%3Aoob&response_type=code&client_id=933051813395-51bu05fbdfl4671vtu6degibtqei34b9.apps.googleusercontent.com&access_type=offline

Enter verification code: 4/moOjOiXKZq768TZY5bGuX634-lW36oPaVhyZDpL7qdM
Authentication successful.
Uploading file...
An HTTP error 403 occurred:
{
 "error": {
  "errors": [
   {
    "domain": "usageLimits",
    "reason": "accessNotConfigured",
    "message": "Project 933051813395 is not found and cannot be used for API calls. If it is recently created, enable YouTube Data API by visiting https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=933051813395 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry.",
    "extendedHelp": "https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=933051813395"
   }
  ],
  "code": 403,
  "message": "Project 933051813395 is not found and cannot be used for API calls. If it is recently created, enable YouTube Data API by visiting https://console.developers.google.com/apis/api/youtube.googleapis.com/overview?project=933051813395 then retry. If you enabled this API recently, wait a few minutes for the action to propagate to our systems and retry."
 }
}
```

il faut 
- qu'un compte youtube autorise l'application
- activer l'api youtube data dans la console de dev google

2nd tentative ok :
```
pi@pi3:~/prog/mess/api-samples/python $ python upload_video.py --file="/home/pi/Videos/SiaChandelier.mp4" --title="je danse bien" --privacyStatus="private" --noauth_local_webserver
Uploading file...
Video id 'ZyEKXv-qrvY' was successfully uploaded.
```

# evolution
- voir Using MJPG-Streamer dans http://www.akeric.com/blog/?p=2437

# références
le logo provient de http://www.i2clipart.com/

le code utilisant l'API youtube est insprié de :
- https://stackoverflow.com/questions/21228815/adding-youtube-video-to-playlist-using-python
- https://github.com/youtube/api-samples/blob/master/python/upload_video.py

la reconnaissance de visage provient des exemples https://github.com/ageitgey/face_recognition/tree/master/examples 

## test ipython
install initiale
```
mkvirtualenv ipython -p python3
workon ipython
pip3 install ipython jupyter numpy matplotlib
jupyter notebook --generate-config
```
ajout d'un mot de passe (celui de l'OS)
```
jupyter notebook password
[NotebookPasswordApp] Wrote hashed password to /home/pi/.jupyter/jupyter_notebook_config.json
```
ouverture aux clients distants, ajout de `c.NotebookApp.ip = '*'`dans `/home/pi/.jupyter/jupyter_notebook_config.py`

la console est accessible dans le navigateur http://192.168.1.28:8888/

## test kera + TF + Theano
```
workon cv
sudo pip3 install keras # inclu Theano
...
Successfully installed keras theano pyyaml numpy scipy
Cleaning up...
```
err, le même sans le su
```
...
Successfully built keras theano pyyaml scipy
Installing collected packages: scipy, six, theano, pyyaml, keras
Successfully installed keras-2.0.4 pyyaml-3.12 scipy-0.19.0 six-1.10.0 theano-0.9.0
```

pas possible d'installer TF avec `sudo pip3 install --upgrade tensorflow` donc utilisation de la doc https://github.com/samjabrahams/tensorflow-on-raspberry-pi/#installing-from-pip
```
wget https://github.com/samjabrahams/tensorflow-on-raspberry-pi/releases/download/v1.1.0/tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
pip3 install tensorflow-1.1.0-cp34-cp34m-linux_armv7l.whl
...
Successfully built protobuf
Installing collected packages: six, protobuf, werkzeug, tensorflow
Successfully installed protobuf-3.3.0 six-1.10.0 tensorflow-1.1.0 werkzeug-0.12.2
```

choisir entre Theano et Tensorflow
XXX
