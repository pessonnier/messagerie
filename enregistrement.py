import subprocess as sp
import os
import RPi.GPIO as gpio

bin=os.environ['MESSBIN']
picam=sp.Popen([bin+'/picam', '--alsadev', 'hw:1,0'], stdout=sp.PIPE)

gpio.setmode(gpio.BCM)
gpio.setup(18,gpio.IN) # btt vert

def enr():
  sp.call(['touch', bin+'/hooks/start_record'])

def stop()
  r=sp.check_output(['touch', bin+'/hooks/stop_record'])
