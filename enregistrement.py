# utilise https://github.com/iizukanao/picam
import subprocess as sp
import picamera
import os
#import RPi.GPIO as gpio
import time
from queue import Queue, Empty
from threading import Thread
import conf

#gpio.setmode(gpio.BCM)
#gpio.setup(18,gpio.IN) # btt vert

PICAMDIR = conf.PICAMDIR
PICAMSTATE = conf.PICAMSTATE
PICAMHOOKS = conf.PICAMHOOKS

# trouvé sur https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
def enqueue_output(out, queue):
  for line in iter(out.readline, b''):
    print('>lecture : '+line.decode())
    queue.put(line)
  out.close()

def pcinit():
  camera = picamera.PiCamera()
  camera.rotation = 90
  camera.resolution = (conf.CAMERA_MAX_X, conf.CAMERA_MAX_Y)
  camera.start_preview()
  return camera

def pcexe():
  picam=sp.Popen([PICAMDIR+'/picam', '-p', '--autoex', '--rotation', '90', '--alsadev', 'hw:1,0', '--statedir', PICAMSTATE, '--hooksdir', PICAMHOOKS], stdout=sp.PIPE)
  return picam

def pcstop():
  print(PICAMHOOKS+'/stop_record')
  sp.call(['touch', PICAMHOOKS+'/stop_record'])

def pcconnout(picam):
  picammess = Queue()
  picammessthread = Thread(target=enqueue_output, args=(picam.stdout, picammess))
  picammessthread.daemon = True
  picammessthread.start()
  return picammess

def pcstart(picammess):
  fich=''
  timeout=10
  while timeout>0:
    timeout-=1
    sp.call(['touch', PICAMHOOKS+'/start_record'])
    time.sleep(0.5)
    try:
      l=picammess.get(timeout=0.1).decode()
      if l.startswith('disk'):
        fich = ' '.join(l.split(' ')[4:]).strip()
        break
    except Empty:
      print('attente enr')
  if fich == '':
    print('échec de l\'enregistrement') # log
  return fich

def pcenr():
  picam=pcexe()
  picammess=pcconnout(picam)
  fich=pcstart(picammess)
  return picam, picammess,fich

def pcquit(picam):
  #picam.terminate()
  #if not picam.stdout.closed:
  #  picam.stdout.close()
  picam.kill()


def test():
  camera = pcinit()
  time.sleep(5)
  camera.close()
  time.sleep(0.5)
  picam,pcmess,fich=pcenr()
  time.sleep(5)
  pcstop()
  pcquit(picam)
  print('fichier enregistré : '+fich)

if __name__ == '__main__':
  test()
