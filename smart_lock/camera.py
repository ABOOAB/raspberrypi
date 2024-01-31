import cv2
import os

import numpy
from controller import Door

door = Door()


class Camera:
    def __init__(self):
        self.active = False
        self.camera = cv2.VideoCapture(0)

    def activate(self):
        if not self.active:
            print("Camera is on ...")
            self.active = True
            
            path_to_training_images = 'data/at'
            training_image_size = (200, 200)
            names, training_images, training_labels = self.read_images(
                path_to_training_images, training_image_size)

            model = cv2.face.LBPHFaceRecognizer_create()

            model.train(training_images, training_labels)

            face_cascade = face_cascade = cv2.CascadeClassifier(
                './cascades/haarcascade_frontalface_default.xml')

            while cv2.waitKey(1) == -1:
                success, frame = self.camera.read()
                if success:
                    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
                    for (x, y, w, h) in faces:
                        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        roi_gray = gray[x:x+w, y:y+h]
                        if roi_gray.size == 0:
                            # The ROI is empty. Maybe the face is at the image edge.
                            # Skip it.
                            continue
                        roi_gray = cv2.resize(roi_gray, training_image_size)
                        label, confidence = model.predict(roi_gray)
                        if confidence >= 80.00:
                            print("match ... open the door.")
                            door.open()
                        text = '%s, confidence=%.2f' % (names[label], confidence)
                        cv2.putText(frame, text, (x, y - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    cv2.imshow('Face Recognition', frame)

            # Release the camera and destroy OpenCV windows
            self.deactivate()

    def deactivate(self):
        if self.active:
            print("Camera is in sleep mode ...")
            self.active = False

            # Release the camera
            self.camera.release()
            cv2.destroyAllWindows()
            
    def read_images(self, path, image_size):
        names = []
        training_images, training_labels = [], []
        label = 0
        for dirname, subdirnames, filenames in os.walk(path):
            for subdirname in subdirnames:
                names.append(subdirname)
                subject_path = os.path.join(dirname, subdirname)
                for filename in os.listdir(subject_path):
                    img = cv2.imread(os.path.join(subject_path, filename),
                                     cv2.IMREAD_GRAYSCALE)
                    if img is None:
                        # The file cannot be loaded as an image.
                        # Skip it.
                        continue
                    img = cv2.resize(img, image_size)
                    training_images.append(img)
                    training_labels.append(label)
                label += 1
        training_images = numpy.asarray(training_images, numpy.uint8)
        training_labels = numpy.asarray(training_labels, numpy.int32)
        return names, training_images, training_labels


