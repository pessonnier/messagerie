import time
import subprocess as sp
import RPi.GPIO as GPIO
import os
import pickle
import threading

# XXX image d'acceuil

import identification as id
import pied
import upload
import bluetooth as bt
import enregistrement as enr
import conf
import telecharger

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
def attente(trs, process = None, bloquant = True):
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
    if not bloquant:
      break
  return ev

# XXX à charger depuis un fichier de conf
actions = {0 : "caid.sh", 1 : "rien.sh", 2 : "rien.sh", 3 : "rien.sh", 4 : "caid.sh", 5 : "rien.sh"}
def lancescript(idt):
  commande = actions[idt]
  print ('commande ' + os.path.join(conf.ACTIONDIR, commande))
  p=sp.Popen(["/bin/bash", os.path.join(conf.ACTIONDIR, commande)], stdin = sp.PIPE)
  return p

def fichierRecent():
  return playlisteParDate()[0]

def memoriserFichier(fich):
  with open(os.path.join(conf.CONFDIR, 'dernierevideo.dmp'), 'wb') as f:
    pickle.dump(fich, f)

def memoriserFichierRecent():
  fich = fichierRecent()
  memoriserFichier(fich)

# XXX utiliser 
def nouveauFichier():
  memo = pickle.load(os.path.join(conf.CONFDIR, 'dernierevideo.dmp'))
  dernier = fichierRecent()
  return memo != dernier

def chargerVideosVues():
  try:
    return pickle.load(os.path.join(conf.CONFDIR, 'videosVues.dmp'))
  except :
    print ('nouveau fichier de videos vues')
    return {}

def sauverVideosVues(videosVues):
  with open(os.path.join(conf.CONFDIR, 'videosVues.dmp'), 'wb') as f:
    pickle.dump(videosVues, f)

def fusionnerVideosVues(vues, liste):
  for l in liste:
    if vues.get(l, 'yapas') == 'yapas':
      vues[l]=False
  return vues

# XXX utiliser
def afficherVideosVues(videosVues):
  for f, t in videosVues.items():
    if t:
      etoile = '*'
    else:
      etoile = '-'
    print (f[:20].ljust(20)+etoile)

h = None
v = None
centrerPied = None
arretMoteur = None

# les états
def init():
  print('init')
  # les périfériques
  global h, v, centrerPied, arretMoteur
  h, v, arretMoteur, centrerPied = pied.init()
  # Bluetooth
  bt.connectDefault()
  # operations sur le system
  sp.call('/bin/bash '+ os.path.join(os.getcwd(),'system.sh'), shell = True)
  # mise a jour du projet git
  sp.Popen(['/bin/bash', os.path.join(os.getcwd(),'miseajour.sh')])
  # passage à l'étape suivante
  global etat
  etat=ECOUTE

def veille():
  print('veille')
  # bt.disconnect()
  global centrerPied, arretMoteur
  centrerPied()
  arretMoteur()
  global camera
  camera.close()
  # telechargement de la playliste
  t = threading.Thread(target = telecharger.telecharger)
  t.daemon = True
  t.start()
  if attente([BTTROUGE_OFF], bloquant = False) == []:
    print('lachez ce boutton rouge')
    attente([BTTROUGE_OFF])
  if attente([BTTVERT_OFF], bloquant = False) == []:
    print('lachez ce boutton vert')
    attente([BTTVERT_OFF])
  # XXX ajouter un timeout
  r = attente([BTTVERT, BTTROUGE])
  global etat
  if r[0] == BTTVERT:
    etat = INIT
  if r[0] == BTTROUGE:
    etat = ETEINDRE

# XXX signaler qu'un message est en attente
def ecoute():
  print('écoute')
  attente([MOUVEMENT])
  global etat
  etat = RECHERCHE
  # etat = ENREGISTREMENT # XXX

camera = None
processEnFond = None

def rechercheVisage():
  print('recherche')
  global etat, camera, processEnFond, h, v, centrerPied, arretMoteur
  # h, v, arretMoteur, centrerPied = pied.init()
  face_lec, captureur, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces = id.precapture()
  def arretDetection(): # le btt rouge interromp la recherche et passe en lecture
    return attente([BTTROUGE], bloquant = False) != []
  imatch = pied.rechercheHorizontale(h, face_lec, captureur, arretDetection)
  if imatch != []:
    camera.close()
    centrerPied()
    arretMoteur()
    bt.connectDefault()
    for identifiant, loc in imatch:
      processEnFond = lancescript(identifiant)
    etat = CENTRER
    return imatch
  elif arretDetection():
    camera.close()
    centrerPied()
    arretMoteur()
    etat = PLAY
    attente([BTTROUGE_OFF])
  else:
    etat = VEILLE
  return []

def centrer(loc):
  print('centrer')
  pied.viser(loc) # ne fait rien
  global etat
  etat = AUTORISE

# les actions possibles une fois identifié
def autorise():
  print('autorise')
  print('choix PLAY ENR')
  global etat, processEnFond, camera
  r = attente([BTTROUGE,BTTVERT])
  if r[0] == BTTROUGE:
    arreter(processEnFond, force = True)
    etat = PLAY
    attente([BTTROUGE_OFF])
  if r[0] == BTTVERT:
    arreter(processEnFond, force = True)
    etat = ENREGISTREMENT

def commandePlayVideo(video):
  return [ 'omxplayer', '-o', 'alsa:pulse', os.path.join(conf.MEDIADIR, video)]

def playlisteParDate():
  def pardate (x):
    return - os.stat(os.path.join(conf.MEDIADIR, x)).st_ctime
  # la playliste est constituée des fichiers du répertoire MEDIADIR qui ne sont pas des miniatures
  return [ f for f in sorted(os.listdir(conf.MEDIADIR), key = pardate) if (not f.endswith('jpg')) and (os.path.isfile(os.path.join(conf.MEDIADIR, f))) ]

def arreter(p, force = False):
  if p is None:
    print('rien a arreter')
    return
  try:
    p.stdin.write(b'q')
    p.stdin.flush()
  except :
    print('echec de l envoi de message')
  cpt = 0
  while (p.poll() is None) and (cpt < 10):
    time.sleep(0.1)
    cpt += 1
  if p.poll() is None:
    print("ERR : omxplayer ne d'arrete pas")
    p.terminate()
    sp.Popen(['killall', 'omxplayer.bin'])
  if force:
    sp.Popen(['killall', 'omxplayer.bin'])
    # XXX ajouter un killtree

# XXX differentier les fichiers lu
def play():
  print('play')
  global etat
  bt.connectDefault()
  playliste = playlisteParDate()
  memoriserFichier(playliste[0])
  videosVues = fusionnerVideosVues(chargerVideosVues(), playliste)
  print(playliste)
  print(videosVues)
  pos = 0
  while pos < len(playliste):
    video = playliste[pos]
    p = sp.Popen(commandePlayVideo(video), stdin = sp.PIPE)
    r = attente([BTTROUGE, BTTVERT, PROCESSTERMINATED], process = p)
    if (BTTROUGE in r) and (BTTVERT in r):
      arreter(p)
      etat = VEILLE
      return
    if r[0] == BTTVERT: # video suivante
      arreter(p)
      pos += 1
    if r[0] == BTTROUGE: # video précédente
      arreter(p)
      pos -= 1
      if pos < 0:
        pos = 0
    if r[0] == PROCESSTERMINATED:
      pos += 1
      videosVues[video] = True
      sauverVideosVues(videosVues)
  etat = VEILLE

def enregistrement():
  print('enregistrement')
  global etat
  # relacher le btt vert de la transition
  if attente([BTTVERT], bloquant = False) != []:
    print('lachez le boutton vert puis rapuyez pour enregistrer')
  attente([BTTVERT_OFF])
  #
  # enregistrement
  #
  # visualise la camera pour le cadrage
  picam=sp.Popen([conf.PICAMDIR+'/picam', '-p', '--autoex', '--rotation', '90', '--alsadev', 'hw:1,0', '--statedir', conf.PICAMSTATE, '--hooksdir', conf.PICAMHOOKS], stdout=sp.PIPE)
  # sp.call('/bin/bash -c echo "text=Veille     Enregistrer" > ' + os.path.join(conf.PICAMHOOKS, 'subtitle'))
  with open(os.path.join(conf.PICAMHOOKS, 'subtitle'), 'w') as f:
    f.write('text=Veille     Enregistrer')
  r = attente([BTTVERT, BTTROUGE])
  if r == [BTTROUGE]:
    etat = VEILLE
    enr.pcquit(picam)
    return

  fich=''
  while attente([BTTVERT_OFF], bloquant = False) == []:
    sp.call(['touch', conf.PICAMHOOKS+'/start_record'])
    time.sleep(0.2)

  enr.pcstop()
  # enr.pcquit(picam)
  try:
    while True:
      l = picam.stdout.readline().decode()
      if not l.startswith('x'):
        print(l)
      if l.startswith('disk'):
        fich = ' '.join(l.split(' ')[4:]).strip()
        break
      if l == '':
        break
  except:
    print('fin de fichier')
  if fich == '':
    print('échec de l\'enregistrement') # log
  print('fichier enregistré : '+fich)
  if fich == '':
    print('echec on recommence')
    return
  
  # étape upload
  # XXX indiquer upload
  try:
    idvideo = upload.upload(fich)
    print('vidéo uploadée id : ' + str(idvideo))
  except (ServerNotFoundError):
    print ('la vidéo n\'est pas envoyée. pas de connexion réseau')
  enr.pcquit(picam) # arret du processus de capture décalé pour lui laisser le temps de finaliser le fichier
  
  # aprés enregistrment
  r = attente([BTTROUGE,BTTVERT])
  if r[0] == BTTROUGE:
    etat = VEILLE
  if r[0] == BTTVERT:
    etat = ENREGISTREMENT

def eteindre():
  sp.call('sudo halt', shell = True)

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
    elif etat == ETEINDRE:
      eteindre()

def main():
  work()

if __name__ == '__main__':
  main()
