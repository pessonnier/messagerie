print ('import')
import face_recognition
import picamera
import numpy as np
import conf
import os

def initCamera():
  print('camera')
  camera = picamera.PiCamera()
  camera.resolution = (conf.CAMERA_CAPTURE_X,conf.CAMERA_CAPTURE_Y)
  camera.start_preview()
  output = np.empty((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X, 3), dtype=np.uint8)
  ima = np.zeros((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X,3), dtype=np.uint8)
  over = camera.add_overlay(ima.tobytes(), layer=3, alpha=64)
  return camera, output, ima, over

def initReco():
  print('chargement')
  #moi=face_recognition.load_image_file('media/matete1.jpg')
  #karine=face_recognition.load_image_file('media/karine1.jpg')
  #emoi=face_recognition.face_encodings(moi)[0]
  #ekarine=face_recognition.face_encodings(karine)[0]
  visages = [ face_recognition.load_image_file(os.path.join(conf.PHOTOSDIR,f)) for f in os.listdir(conf.PHOTOSDIR) if f.endswith('jpg')]
  visagesCodes = [ face_recognition.face_encodings(v)[0] for v in visages ]
  return visagesCodes

def precapture():
  camera, output, ima, over = initCamera()
  visagesCodes = initReco()
  face_locations = lambda :
    camera.capture(output, format="rgb")
    return face_recognition.face_locations(output)
  face_encodings = lambda loc:
    return face_recognition.face_encodings(output, loc)
  face_le = lambda :
    loc = face_locations()
    return face_recognition.face_encodings(output, loc), loc
  compare_faces = lambda face_encodings:
    matchs = [ False ] * len(visagesCodes)
    for face_encoding in face_encodings:
      #agrege tous les fichiers identifiés dans matchs
      matchs = [ matchs[i] | m for i, m in enumerate(face_recognition.compare_faces(visagesCodes, face_encoding)) ]
    imatchs = [ i for i, m in enumerate(matchs) if m]
    return match, imatch
  face_lec = lambda :
    return compare_faces (face_le ()[0])[1]
  return face_lec, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces

def dessineCadre(over):
  #ajout des cadres
  ima = np.zeros((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X,3), dtype=np.uint8)
  for i,(top, right, bottom, left) in enumerate(face_locations):
    ima[top, left:right, :] = 0xff
    ima[bottom, left:right, :] = 0xff
    ima[top:bottom, left, :] = 0xff
    ima[top:bottom, right, :] = 0xff
  over.update(ima.tobytes())

def rechercheVisage(camera, output, ima, over, visagesCodes):
  print('recherche')
  face_locations = []
  face_encodings = []
  while True:
    camera.capture(output, format="rgb")
    face_locations = face_recognition.face_locations(output)
    #print("Found {} faces in image.".format(len(face_locations)))

    #ajout des cadres
    ima = np.zeros((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X,3), dtype=np.uint8)
    for i,(top, right, bottom, left) in enumerate(face_locations):
      ima[top, left:right, :] = 0xff
      ima[bottom, left:right, :] = 0xff
      ima[top:bottom, left, :] = 0xff
      ima[top:bottom, right, :] = 0xff
    over.update(ima.tobytes())

    # identification des visages
    if len(face_locations)>0:
      #top, right, bottom, left = face_locations[0]
      #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
      face_encodings = face_recognition.face_encodings(output, face_locations)
      matchs = [ False ] * len(visagesCodes)
      for face_encoding in face_encodings:
        #agrege tous les fichiers identifiés dans matchs
        matchs = [ matchs[i] | m for i, m in enumerate(face_recognition.compare_faces(visagesCodes, face_encoding)) ]
      imatchs = [ i for i, m in enumerate(matchs) if m]

      # dessine un carre vert si un visage est reconu
      if len(imatchs)>0:
        ima[10:30, 10:30, 1] = 200
        over.update(ima.tobytes())
      else:
        ima[10:30, 10:30, 0] = 200
        over.update(ima.tobytes())
      for i in imatchs:
        print('trouvé ' + str(i))

def test():
  camera, output, ima, over = initCamera()
  visagesCodes = initReco()
  rechercheVisage(camera, output, ima, over, visagesCodes) 

def test2():
  f=precapture()
  for i in range(10):
    print(f[0]())
  
  
  
