import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
from keras.models import load_model
import pickle
import numpy as np
from sklearn.preprocessing import Normalizer
from Processing import get_embedding
from Processing import recognize
from Processing import get_data_member
import time

print("Load library done!")

# Config

MULTIPLE_PERSON=0
classes, class_name, numberPerson = get_data_member("Name_with_Id.json")

# Load model
model_embedding = load_model('./pretrain_model/facenet_keras.h5')
print("Load model embedding done!")

model_predict = pickle.load(open('./model/final_model.sav', 'rb'))
print("Load model predict done!")

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
print("Load model detect done!")

if __name__ == '__main__':

    cap = cv2.VideoCapture(0)

    numFrame = 0
    numFrameNull = 0
    counter = 0
    start_time = time.time()
    fps = 0

    while True:
        # doc anh tu camera
        ret, img = cap.read()
        img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        numFrame += 1
        counter += 1
        if (time.time() - start_time) >= 0.5 :
            fps = int(counter / (time.time() - start_time))
            counter = 0
            start_time = time.time()
        # neu khong detect duoc face thi khong ve bbox
        if len(faces) == 0:
            if numFrameNull%10==0:
                print('No face !')
            # nhan phim 'q' de thoat
            cv2.putText(img, "FPS: " + str(fps), (10, 30),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0))
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            numFrameNull+=1
            continue

        # nhan phim 'q' de thoat
        cv2.putText(img, "FPS: " + str(fps), (10, 30),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0))

        res=[]
        if MULTIPLE_PERSON==0:
            # detect 1 nguoi
            center = [0, 0, 0, 0]
            for (x, y, w, h) in faces:
                if(center[2]*center[3] < w*h):
                    center = [x, y, w, h]
            x, y, w, h = center
            face = img[y:y+h, x:x+w, :]
            id = recognize(face, model_predict, model_embedding)[0]
            res.append(id)
            # ve bbox trong anh va show anh
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # ghi ten
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, class_name[str(id)],
                        (x, y), font, 1, (255, 255, 255))
        else:
            # detect nhieu nguoi
            for (x, y, w, h) in faces:
                face = img[y:y+h, x:x+w, :]
                id = recognize(face, model_predict, model_embedding)[0]
                res.append(id)
                # ve bbox trong anh va show anh
                cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img, class_name[str(id)],
                            (x, y), font, 1, (255, 255, 255))
        cv2.imshow('img', img)
        framePerImage = 10

        if numFrame % framePerImage == 0:
            num = numFrame/framePerImage
            num = int(num)
            print("Frame {} with {} persons:".format(numFrame,len(res)))
            for i in res:
                print(class_name[str(i)])

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
