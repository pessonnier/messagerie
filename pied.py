import RPi.GPIO as GPIO
import time

# les GPIO
BTTROUGE_GPIO=23
BTTVERT_GPIO=24
MOUVEMENT_GPIO=17
HORIZONTAL_GPIO=18
VERTICAL_GPIO=27

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BTTROUGE_OFF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTTVERT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(MOUVEMENT_GPIO, GPIO.IN)
  GPIO.setup(HORIZONTAL_GPIO, GPIO.OUT)
  GPIO.setup(VERTICAL_GPIO, GPIO.OUT)
  h = GPIO.PWM(HORIZONTAL_GPIO, 50) 
  v = GPIO.PWM(VERTICAL_GPIO, 50)
  h.start(5.4) # 1.8 à 9.2
  v.start(5) # 4.6 à 7

def centrer(location):
  pass

def rechercheHorizontale(identifieur):
  pass
