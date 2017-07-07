print ('import')
import face_recognition
import picamera
import numpy as np
import conf
import os
import pickle

def initCamera():
  print('camera')
  print(conf.CAMERA_CAPTURE_Y)
  print(conf.CAMERA_CAPTURE_X)
  camera = picamera.PiCamera()
  camera.rotation = 90 # XXX faire une variable
  camera.resolution = (conf.CAMERA_CAPTURE_X,conf.CAMERA_CAPTURE_Y)
  camera.start_preview()
  output = np.empty((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X, 3), dtype=np.uint8)
  ima = np.zeros((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X,3), dtype=np.uint8)
  over = camera.add_overlay(ima.tobytes(), layer=3, alpha=64)
  return camera, output, ima, over

def initFace():
  # encode les visages et les sérialises
  print('encodage')
  visages = [ face_recognition.load_image_file(os.path.join(conf.PHOTOSDIR,f)) for f in os.listdir(conf.PHOTOSDIR) if f.endswith('jpg')]
  visagesCodes = [ face_recognition.face_encodings(v)[0] for v in visages ]
  visagesCodesDump = open(os.path.join(conf.PHOTOSDIR,'visagesCodes.fre'), 'wb')
  pickle.dump(visagesCodes, visagesCodesDump)

def initReco():
  # charge les encodage des photos sérialisés
  print('chargement')
  visagesCodesDump = open(os.path.join(conf.PHOTOSDIR,'visagesCodes.fre'), 'rb')
  visagesCodes = pickle.load(visagesCodesDump)
  print('return chargement')
  return visagesCodes

def precapture(cadre = True):
  camera, output, ima, over = initCamera()
  visagesCodes = initReco()
  def face_locations ():
    camera.capture(output, format="rgb")
    return face_recognition.face_locations(output)
  def face_encodings (loc):
    return face_recognition.face_encodings(output, loc)
  def face_le ():
    loc = face_locations()
    if cadre:
      dessineCadre(over, loc)
    return face_recognition.face_encodings(output, loc), loc
  def compare_faces (face_encodings, loc):
    xmatchs = [ (False, (0,0,0,0)) ] * len(visagesCodes)
    for locnum, face_encoding in enumerate(face_encodings):
      #agrege tous les fichiers identifies dans matchs
      xmatchs = [ (xmatchs[i][0] | m, loc[locnum]) for i, m in enumerate(face_recognition.compare_faces(visagesCodes, face_encoding)) ]
    imatchs = [ (i, loc) for i, (m, loc) in enumerate(xmatchs) if m]
    return xmatchs, imatchs # imatch contient des couples identifiant visualisé / position
  def face_lec ():
    face_encodings, loc = face_le ()
    return compare_faces (face_encodings, loc)[1] # ne retourne que le imatch
  return face_lec, camera, output, ima, over, visagesCodes, face_locations, face_encodings, compare_faces

def dessineCadre(over, face_locations, carreVert = False):
  #ajout des cadres
  ima = np.zeros((conf.CAMERA_CAPTURE_Y,conf.CAMERA_CAPTURE_X,3), dtype=np.uint8)
  for i,(top, right, bottom, left) in enumerate(face_locations):
    if right == conf.CAMERA_CAPTURE_X:
      right = conf.CAMERA_CAPTURE_X -1
    if bottom == conf.CAMERA_CAPTURE_Y:
      bottom = conf.CAMERA_CAPTURE_Y -1
    ima[top, left:right, :] = 0xff
    ima[bottom, left:right, :] = 0xff
    ima[top:bottom, left, :] = 0xff
    ima[top:bottom, right, :] = 0xff
  if carreVert:
    ima[10:30, 10:30, 1] = 200
  #over.update(ima.tobytes()) # XXX

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
  print('id test2')
  f=precapture()
  for i in range(10):
    print(f[0]())

def creeVisageEncode():
  initFace()
  print(initReco())

if __name__ == "__main__":
  test()
