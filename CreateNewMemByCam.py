import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"  
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import cv2
import json

# Load the cascade
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Config
# Muon them nguoi thi sua CREATE_NEW_MEMBER thanh 1 va sua NAME thanh ten nguoi do

NAME = "Phuc"
CREATE_NEW_MEMBER = 1

file_json = open("Name_with_Id.json")

data_json = json.load(file_json)
classes = data_json["name"]
numberPerson=len(classes)
file_json.close()

if NAME in classes:
    CREATE_NEW_MEMBER = 0
if CREATE_NEW_MEMBER == 1:
    if not os.path.exists('./img_save/'+NAME):
        os.makedirs('./img_save/'+NAME)
    data_json["name"][NAME] = str(numberPerson)
    data_json["id"][str(numberPerson)] = NAME
    with open('Name_with_Id.json', 'w') as f:
        json.dump(data_json, f)

if __name__ == '__main__':

    
    cap = cv2.VideoCapture(0)

    numFrame = 0
    numFrameNull = 0 

    while True:
        ret,img=cap.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)
        
        if len(faces) == 0:
            if numFrameNull % 10 == 0:
                print('No face !')
            cv2.putText(img, "Press Q to out... ", (10, 30),
                        cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0))
            cv2.imshow('img', img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            numFrameNull += 1
            continue
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        # chon bbox to nhat lam mat
        center=[0,0,0,0]
        for (x, y, w, h) in faces:
            if(center[2]*center[3]<w*h):
                center=[x,y,w,h]
        x,y,w,h=center
        
        imgPerFrame=10
        if numFrame % imgPerFrame == 0:
            num = numFrame/imgPerFrame
            num=int(num)
            print(num)
            # # ghi class va anh ra file
            if CREATE_NEW_MEMBER==1:
    
                img_name = './img_save/'+NAME+'/'+str(num)+'.jpg'
                print(NAME)
                cv2.imwrite(img_name, img[y:y+h, x:x+w])

        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(img, "Press Q to out... ", (10, 30),
                    cv2.FONT_HERSHEY_TRIPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow('img', img)
        
        if cv2.waitKey(1) & 0xFF==ord('q'):
            break

        numFrame += 1

    cap.release()
    cv2.destroyAllWindows()
