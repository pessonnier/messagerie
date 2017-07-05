import time
import subprocess as sp
import RPi.GPIO as GPIO
import os

import identification as id
import pied
import upload
import bluetooth as bt
import enregistrement as enr
import conf

# les états
INIT = 1
VEILLE = 9
ECOUTE = 2
RECHERCHE = 3
CENTRER = 4
AUTORISE = 10
ENREGISTREMENT = 5
UPLOAD = 6
PLAY = 7
ETEINDRE = 8

etat = INIT

# les transitions
BTTROUGE = 1
BTTROUGE_OFF = 101
BTTVERT = 2
BTTVERT_OFF = 102
MOUVEMENT = 3
MOUVEMENT_OFF = 103
TOUCH = 4
TOUCH_OFF = 104
PROCESSTERMINATED = 5

# fonctions communes
def attente(trs, process = None):
  ev=[]
  while ev == []:
    ev=[]
    time.sleep(0.05)
    bttrouge = GPIO.input(pied.BTTROUGE_GPIO)
    if (bttrouge == 0) and (BTTROUGE in trs):
      ev.append(BTTROUGE)
    if (bttrouge == 1) and (BTTROUGE_OFF in trs):
      ev.append(BTTROUGE_OFF)
    bttvert = GPIO.input(pied.BTTVERT_GPIO)
    if (bttvert == 0) and (BTTVERT in trs):
      ev.append(BTTVERT)
    if (bttvert == 1) and (BTTVERT_OFF in trs):
      ev.append(BTTVERT_OFF)
    mouvement = GPIO.input(pied.MOUVEMENT_GPIO)
    if (mouvement == 1) and (MOUVEMENT in trs):
      ev.append(MOUVEMENT)
    if (mouvement == 0) and (MOUVEMENT_OFF in trs):
      ev.append(MOUVEMENT_OFF)
    if (PROCESSTERMINATED in trs) and (process is not None) and (process.poll() is not None):
      ev.append(PROCESSTERMINATED)
  return ev

# XXX à charger depuis un fichier de conf
# XXX ajouter rien.sh
actions = {0 : "caid.sh", 1 : "rien.sh", 2 : "caid.sh", 3 : "rien.sh"}
def lancescript(idt):
  commande = actions[idt]
  print ('commande ' + os.path.join(conf.ACTIONDIR, commande))
  p=sp.Popen(["/bin/bash", os.path.join(conf.ACTIONDIR, commande)])
  return p
  
# les états
def init():
  print('init')
  # les périfériques
  pied.init()
  # Bluetooth
  bt.connectDefault()
  # passage à l'étape suivante
  global etat
  etat=ECOUTE

def veille():
  print('veille')
  bt.deconnect()
  pied.arretmoteur()
  r = []
  while r == []:
    print('lachez ce boutton rouge')
    r = attente([BTTROUGE_OFF])
  r = []
  while r == []:
    print('lachez ce boutton vert')
    r = attente([BTTVERT_OFF])
  r = []
  while r == []:
    r = attente([BTTVERT, BTTROUGE])
  global etat
  if r[0] == BTTVERT:
    # XXX indiquer que la detection commencera dans 10s
    time.sleep(10)
    etat = INIT
  if r[0] == BTTROUGE:
    etat = ETEINDRE
  
def ecoute():
  print('écoute')
  r = []
  while r == []:
    r=attente([MOUVEMENT])
  global etat
  etat = RECHERCHE

camera = None
processEnFond = None

def rechercheVisage():
  print('recherche')
  global etat, camera, processEnFond
  h, v = pied.init()
  face_lec, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces = id.precapture()
  for i in range(4):
    imatch = pied.rechercheHorizontale(h,face_lec) 
    if imatch != []:
      camera.stop_preview()
      for identifiant, loc in imatch:
        processEnFond = lancescript(identifiant)
      etat = CENTRER
      return imatch
  etat = VEILLE
  return []

def centrer(loc):
  print('centrer')
  pied.centrer(loc)
  global etat
  etat = AUTORISE

# les actions possible une fois identifié
def autorise():
  print('autorise')
  print('choix PLAY ENR')
  global etat
  r = []
  while r == []:
    r = attente([BTTROUGE,BTTVERT])
  processEnFond.kill()
  camera.close()
  if r[0] == BTTROUGE:
    etat = PLAY
  if r[0] == BTTVERT:
    etat = ENREGISTREMENT

def commandePlayVideo(video):
  return [ 'omxplayer', '-o', 'alsa:pulse', os.path.join(conf.MEDIADIR, video)]

def play():
  print('play')
  global etat
  # bt.connectDefault()
  def pardate (x, y):
    return os.stat(os.path.join(conf.MEDIADIR, x)).st_ctime < os.stat(os.path.join(conf.MEDIADIR, y)).st_ctime
  # la playliste est constituée des fichiers du répertoire MEDIADIR qui ne sont pas des miniatures
  playliste = [ f for f in os.listdir(conf.MEDIADIR).sort(pardate) if (not f.endswith('jpg')) and (os.path.isfile(os.path.join(conf.MEDIADIR, f))) ]
  print(playliste)
  pos = 0
  while pos < len(playliste):
    video = playliste[pos]
    p = sp.Popen(commandePlayVideo(video))
    r = []
    while r == []:
      print('lachez ce boutton rouge')
      r = attente([BTTROUGE_OFF])
    r = []
    while r == []:
      print('lachez ce boutton vert')
      r = attente([BTTVERT_OFF])
    r = []
    while r == []:
      r = attente([BTTROUGE, BTTVERT, PROCESSTERMINATED], process = p)
    if (BTTROUGE in r) and (BTTVERT in r):
      etat = VEILLE
      return
    if r[0] == BTTVERT: # video suivante
      p.kill()
      pos += 1
    if r[0] == BTTROUGE: # video précédente
      p.kill()
      pos -= 1
    if r[0] == PROCESSTERMINATED:
      pos += 1
  etat = VEILLE

def enregistrement():
  print('enregistrement')
  global etat
  camera.close()
  picam, pcmess, fich = enr.pcenr()
  r = []
  while r == []:
    r = attente([BTTVERT_OFF])
  enr.pcstop()
  enr.pcquit(picam)
  print('fichier enregistré : '+fich)
  
  # étape upload
  idvideo = upload.upload(fich)
  print('vidéo uploadée id : ' + idvideo)
  
  # aprés enregistrment
  r = []
  while r == []:
    r = attente([BTTROUGE,BTTVERT])
  if r[0] == BTTROUGE:
    etat = VEILLE
  if r[0] == BTTVERT:
    etat = ENREGISTREMENT

def eteindre():
  sp.call('sudo shutdown', shell = True)

#etats = {
#  INIT : init,
#  VEILLE : veille,
#  ECOUTE : ecoute,
#  RECHERCHE : rechercheVisage, # comment récupérer le résultat ?
#  CENTRER : centrer, # comment faire pour lui passer un paramètre ?
#  AUTORISE : autorise,
#  ENREGISTREMENT : enregistrement,
#  UPLOAD : upload,
#  PLAY : play,
#  ETEINDRE : eteindre }

def work():
  global etat # util ?
  while True:
    print('etat : ' + str(etat))
    if etat == INIT:
      init()
    elif etat == VEILLE:
      veille()
    elif etat == ECOUTE:
      ecoute()
    elif etat == RECHERCHE:
      imatch = rechercheVisage()
    elif etat == CENTRER:
      centrer(imatch[0][1]) # la localisation du premier visage
    elif etat == AUTORISE:
      autorise()
    elif etat == ENREGISTREMENT:
      enregistrement()
    elif etat == UPLOAD:
      upload()
    elif etat == PLAY:
      play()
    elif etat == ETEINDRE: # XXX transition à trouver
      eteindre()

def main():
  work()

if __name__ == '__main__':
  main()
