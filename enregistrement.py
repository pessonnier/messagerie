import subprocess as sp
import os
#import RPi.GPIO as gpio
import time
from queue import Queue, Empty
from threading import Thread

#gpio.setmode(gpio.BCM)
#gpio.setup(18,gpio.IN) # btt vert

global picamdir, picamstate, picamhooks

# trouvé sur https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
def enqueue_output(out, queue):
  for line in iter(out.readline, b''):
    print('>lecture : '+line.decode())
    queue.put(line)
  out.close()

def pcinit():
  global picamdir, picamstate, picamhooks
  picamdir=os.environ['PICAMDIR']
  if picamdir.endswith('/'):
    picamdir=picamdir[:-1]
  
  picamstate=picamdir+'/state'
  picamhooks=picamdir+'/hooks'

def pcexe():
  picam=sp.Popen([picamdir+'/picam', '--alsadev', 'hw:1,0', '--statedir', picamstate, '--hooksdir', picamhooks], stdout=sp.PIPE)
  print(picam)
  return picam

def pcenr0():
  picam=pcexe()
  # envisager bufsize=1, close_fds=ON_POSIX
  print(picamhooks+'/start_record')
  sp.call(['touch', picamhooks+'/start_record'])
  return picam

def pcstop():
  print(picamhooks+'/stop_record')
  sp.call(['touch', picamhooks+'/stop_record'])

def pcconnout(picam):
  picammess = Queue()
  picammessthread = Thread(target=enqueue_output, args=(picam.stdout, picammess))
  picammessthread.daemon = True
  picammessthread.start()
  return picammess

def pcout(picammess):
  try:
    while True:
      #l=picammess.get_nowait().decode()
      l=picammess.get(timeout=0.1).decode()
      print(l)
  except Empty:
    print('fin')

def pcstart(picammess):
  fich=''
  timeout=10
  while timeout>0:
    timeout-=1
    sp.call(['touch', picamhooks+'/start_record'])
    time.sleep(0.5)
    try:
      l=picammess.get(timeout=0.1).decode()
      if l.startswith('disk'):
        fich=l #l.split(' ')[4].strip()
        break
    except Empty:
      print('attente enr')
  return fich

def pcenr():
  picam=pcexe()
  picammess=pcconnout(picam)
  fich=pcstart(picammess)
  return picam, picammess,fich

# le fichier enregistré
def pcfich(picam):
  picammess = Queue()
  print(picam)
  picammessthread = Thread(target=enqueue_output, args=(picam.stdout, picammess))
  picammessthread.daemon = True
  picammessthread.start()
  time.sleep(1)
  try:
    while 1:
      l=picammess.get_nowait().decode()
      # picam.stdout.readline().decode()
      print(l)
      if l.startswith('disk'):
        break
  except Empty:
    print('pas trouvé')
    return ''
  else:
    picam.stdout.close()
    return l.split(' ')[4].strip()

def pcquit(picam):
  #picam.terminate()
  #if not picam.stdout.closed:
  #  picam.stdout.close()
  picam.kill()

pcinit()

def test():
  picam,pcmess,fich=pcenr()
  #pcout(pcmess)
  time.sleep(5)
  pcstop()
  pcout(pcmess)
  #print(pcfich(picam))
  pcquit(picam)
  #print(picam.stdout.readlines())
