print ('import')
import face_recognition
import picamera
import numpy as np

print('initialisation')
camera = picamera.PiCamera()
camera.resolution = (320, 240)
camera.start_preview()
output = np.empty((240, 320, 3), dtype=np.uint8)
ima = np.zeros((240,320,3), dtype=np.uint8)
over = camera.add_overlay(ima.tobytes(), layer=3, alpha=64)

print('chargement')
moi=face_recognition.load_image_file('media/matete1.jpg')
karine=face_recognition.load_image_file('media/karine1.jpg')
emoi=face_recognition.face_encodings(moi)[0]
ekarine=face_recognition.face_encodings(karine)[0]
face_locations = []
face_encodings = []

cpt=10
while True:
  if cpt==10:
    cpt=0
    print('capture')
  cpt+=1
  camera.capture(output, format="rgb")
  face_locations = face_recognition.face_locations(output)
  print("Found {} faces in image.".format(len(face_locations)))

  #ajout des cadres
  ima = np.zeros((240,320,3), dtype=np.uint8)
  for i,(top, right, bottom, left) in enumerate(face_locations):
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    ima[top, left:right, :]=0xff
    ima[bottom, left:right, :]=0xff
    ima[top:bottom, left, :] = 0xff
    ima[top:bottom, right, :] = 0xff
  over.update(ima.tobytes())

  if len(face_locations)>0:
    #top, right, bottom, left = face_locations[0]
    #print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))
    face_encodings = face_recognition.face_encodings(output, face_locations)
    for face_encoding in face_encodings:
      # See if the face is a match for the known face(s)
      match = face_recognition.compare_faces([emoi,ekarine], face_encoding)
      if match[0]:
        print('trouvé moi')
      if match[1]:
        print('trouvé karine')
  
