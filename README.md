# Messagerie
échange de messages vidéos entre boites abonnées

# configuration initiale

# installation
sur la base d'une rasbian jessie

activation de la caméra
- `sudo raspi-config`
- aller dans 5 Interfacing Options

upload youtube voir https://developers.google.com/youtube/v3/guides/uploading_a_video
 - `sudo pip3 install --upgrade google-api-python-client`
 - exemples youtube https://github.com/youtube/api-samples/tree/master/python
 - autre api https://github.com/google/google-api-python-client/tree/master/samples
 - creation d'un identifiant d'application dans la console google
 - creation du fichier client_secrets.json
 - clone des demo d'utilisation de l'api youtube : `git clone https://github.com/youtube/api-samples.git`

picam :
- https://github.com/iizukanao/picam/blob/master/INSTALL.md
- `apt-get install flex bison automake gperf libtool patch texinfo ncurses-dev help2man`
- `sudo apt-get install netcat`

client de test :
- si besoin ouverture de ports sur le client `sudo ufw allow proto udp from 192.168.1.0/24 to any port 5678`
- ecoute du client : `nc -l 5678 | mplayer - -cache 1024`
- emission : `./picam --alsadev hw:1,0 --tcpout tcp://192.168.1.20:5678`

opencv3 :
- http://www.pyimagesearch.com/2016/04/18/install-guide-raspberry-pi-3-raspbian-jessie-opencv-3/
- https://github.com/opencv/opencv/releases/tag/3.2.0
- https://github.com/opencv/opencv_contrib/releases/tag/3.2.0

tas :
-`sudo apt-get install youtube-dl mplayer2 fbi`
-`sudo pip3 install GPIO`

reconaissance faciale
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


# spec

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

