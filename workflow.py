import time
import subprocess

import identification as id
import pied
import upload
import play
import bluetooth as bt
import conf

# les états
INIT=1
ECOUTE=2
RECHERCHE=3
CENTRER=4
ENREGISTREMENT=5
UPLOAD=6
PLAY=7
ETEINDRE=8

etat = INIT

# les transitions
BTTROUGE=1
BTTROUGE_OFF=101
BTTVERT=2
BTTVERT_OFF=102
MOUVEMENT=3
MOUVEMENT_OFF=103
TOUCH=4
TOUCH_OFF=104

def attente(trs):
  ev=[]
  while ev == []:
    ev=[]
    time.sleep(0.05)
    bttrouge = GPIO.input(BTTROUGE_GPIO)
    if (bttrouge == 0) and (BTTROUGE in trs):
      ev.append(BTTROUGE)
    if (bttrouge == 1) and (BTTROUGE_OFF in trs):
      ev.append(BTTROUGE_OFF)
    bttvert = GPIO.input(BTTVERT_GPIO)
    if (bttvert == 0) and (BTTVERT in trs):
      ev.append(BTTVERT)
    if (bttvert == 1) and (BTTVERT_OFF in trs):
      ev.append(BTTVERT_OFF)
    mouvement = GPIO.input(MOUVEMENT_GPIO)
    if (mouvement == 0) and (MOUVEMENT in trs):
      ev.append(MOUVEMENT)
    if (mouvement == 1) and (MOUVEMENT_OFF in trs):
      ev.append(MOUVEMENT_OFF)
  return ev

def init():
  print('init')
  # les périfériques
  pied.init()
  # Bluetooth
  bt.connect()
  # passage à l'étape suivante
  etat=ECOUTE

def ecoute():
  print('écoute')
  r = []
  while r == []:
    r=attente([MOUVEMENT])
  etat = RECHERCHE

def rechercheVisage():
  print('recherche')
  etat = CENTRER

def centrer():
  print('centrer')
  etat = IDENTIFIER

def identifier():
  print('identifier')
  etat = AUTORISE

# les actions possible une fois identifié
def autorise():
  print('identifier')
  r = []
  while r == []:
    r=attente([BTTROUGE,BTTVERT])
  if r[0] == BTTROUGE:
    etat = PLAY
  if r[0] == BTTVERT:
    etat = ENREGISTREMENT

def work():
  while True:
    print('etat : ' + str(etat))
    if etat == INIT:
      init()
    elif etat == ECOUTE:
      ecoute()
    elif etat == RECHERCHE:
      rechercheVisage()
    elif etat == CENTRER:
      centrer()
    elif etat == IDENTIFIER:
      identifier()
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

main()
