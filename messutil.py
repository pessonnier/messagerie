import picamera
import time
import subprocess as os

def photo():
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    camera.start_preview()
    #camera.annotate_text = 'Hello world!'
    time.sleep(2)
    n=input()
    # Take a picture including the annotation
    camera.capture('visage'+n+'.jpg')

def getCPUtemperature():
    res = os.check_output(['vcgencmd', 'measure_temp']).decode()
    return(res.replace("temp=","").replace("'C\n",""))

from pkg_resources import require
def picameraVersion():
  return require('picamera')[0].version
