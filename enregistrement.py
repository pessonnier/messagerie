import subprocess as sp
import os
#import RPi.GPIO as gpio
import time
from queue import Queue, Empty
from threading  import Thread

#gpio.setmode(gpio.BCM)
#gpio.setup(18,gpio.IN) # btt vert

global picamdir, picamstate, picamhooks

# trouvé sur https://stackoverflow.com/questions/375427/non-blocking-read-on-a-subprocess-pipe-in-python
def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def pcinit():
  global picamdir, picamstate, picamhooks
  picamdir=os.environ['PICAMDIR']
  if picamdir.endswith('/'):
    picamdir=picamdir[:-1]
  
  picamstate=picamdir+'/state'
  picamhooks=picamdir+'/hooks'

def pcenr():
  picam=sp.Popen([picamdir+'/picam', '--alsadev', 'hw:1,0', '--statedir', picamstate, '--hooksdir', picamhooks], stdout=sp.PIPE)
  print(picam)
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
  picam.terminate()
  #if not picam.stdout.closed:
  #  picam.stdout.close()
  #picam.kill()

pcinit()
picam=pcenr()
pcmess=pcconnout(picam)
pcout(pcmess)
time.sleep(5)
pcstop()
pcout(pcmess)
#print(pcfich(picam))
pcquit(picam)
print(picam.stdout.readlines())
