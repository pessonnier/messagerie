import RPi.GPIO as GPIO
import time

# les GPIO
BTTROUGE_GPIO=23 # P4 resistance fil bleu
BTTVERT_GPIO=24 # P5 resistance fil marron
RIEN_GPIO_25 = 0 # résevé pour l'écran voir /boot/config.txt irq=25
MOUVEMENT_GPIO=17 # P0 fil violet
RIEN_GPIO_04 = 0 # P7
HORIZONTAL_GPIO=18 # P1 fil gris vers moteur
VERTICAL_GPIO=27 # P2 fil blanc vers moteur
RIEN_GPIO_22 = 0 # P3 fil violet

# calibration
HINIT = 5.4
HMIN = 1.8
HMAX = 9.2
VINIT = 5
VMIN = 4.6
VMAX = 7

def init():
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BTTROUGE_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(BTTVERT_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  GPIO.setup(MOUVEMENT_GPIO, GPIO.IN)
  GPIO.setup(HORIZONTAL_GPIO, GPIO.OUT)
  GPIO.setup(VERTICAL_GPIO, GPIO.OUT)
  h = GPIO.PWM(HORIZONTAL_GPIO, 50) 
  v = GPIO.PWM(VERTICAL_GPIO, 50)
  h.start(HINIT) # 1.8 à 9.2
  v.start(VINIT) # 4.6 à 7
  return h, v

def arretmoteur():
  h.stop()
  v.stop()

def centrer(location):
  pass
  
import identification as id

def rechercheHorizontale(h, identifieur):
  def mesure():
    posh = i*(HMAX-HMIN)/8+HMIN
    print(posh)
    h.ChangeDutyCycle(posh)
    #time.sleep(1)
    return identifieur()
  h0 = 0
  for t in range(0,3):
    for i in range(h0,9): # np.arange(1.8, 9.2, 0.4)+0.1: # 0.925
      l = mesure() 
      if l != []:
        return l
    h0 = 1
    for i in range(7,-1,-1):
      l = mesure() 
      if l != []:
        return l
  h.ChangeDutyCycle(HINIT)

def test():
  face_lec, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces = id.precapture()
  # visagesCodes = initReco()
  print('boucle reco')
  for i in range(100):
    print(face_lec())


def test2():
  h, v = init()
  face_lec, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces = id.precapture()
  print('boucle reco')
  for i in range(10):
    print(rechercheHorizontale(h,face_lec))

if __name__ == "__main__":
  test2()
