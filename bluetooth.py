import subprocess as sp
from queue import Queue, Empty
from threading import Thread
import time

def enqueue_output(out, queue):
  for line in iter(out.readline, b''):
    print('>'+line.decode()+'<')
    queue.put(line)
  out.close()

def attend(mess, txt, timeout = 0):
  try:
    while True:
      if timeout == 0:
        l=mess.get_nowait().decode()
      else:
        print('get')
        l=mess.get(block=True, timeout=timeout).decode()
        print(l)
      if l.find(txt) != -1:
        break
      print('while')
  except Empty:
    return False
  else:
    return True

def commande(coms):
  with sp.Popen(['/usr/bin/bluetoothctl'], stdin=sp.PIPE, stdout=sp.PIPE) as btproc:
    btmess = Queue()
    btthread = Thread(target=enqueue_output, args=(btproc.stdout, btmess))
    btthread.daemon = True
    btthread.start()
    time.sleep(0.1)
    for com, txt in coms:
      print(com) 
      btproc.stdin.write((com+'\n').encode())
      print('write ok') 
      if txt != '':
        if not attend(btmess, txt, timeout=1):
          return False
  return True

def inter():
  btproc = sp.Popen(['/usr/bin/bluetoothctl'], stdin=sp.PIPE, stdout=sp.PIPE)
  btmess = Queue()
  btthread = Thread(target=enqueue_output, args=(btproc.stdout, btmess))
  btthread.daemon = True
  btthread.start()
  time.sleep(0.1)
  return btproc.stdin

def connect_bug(id='30:21:95:5C:A8:A8'):
  commande([['connect '+id, 'Connection successful']])

def disconnect_bug(id='30:21:95:5C:A8:A8'):
  commande([['disconnect '+id, 'Successful disconnected']])

def connect(id='30:21:95:5C:A8:A8'):
  sp.call('echo "connect ' + id + '\nexit\n" | /usr/bin/bluetoothctl', shell = True)

def disconnect(id='30:21:95:5C:A8:A8'):
  sp.call('echo "disconnect ' + id + '\nexit\n" | /usr/bin/bluetoothctl', shell = True)

if __name__ == '__main__':
  connect()
