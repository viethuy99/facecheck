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

NAME = "Huy"
CREATE_NEW_MEMBER = 1


file_json = open("Name_with_Id.json")

data_json = json.load(file_json)
classes = data_json["name"]
numberPerson = len(classes)
file_json.close()


# if NAME in classes:
#     CREATE_NEW_MEMBER = 0
if CREATE_NEW_MEMBER == 1:
    if not os.path.exists('./img_save/'+NAME):
        os.makedirs('./img_save/'+NAME)
    if NAME in data_json["name"].keys():
        print("name exist!")
    else:
        print(data_json["name"][NAME])
        data_json["name"][NAME] = str(numberPerson)
        data_json["id"][str(numberPerson)] = NAME
        with open('Name_with_Id.json', 'w') as f:
            json.dump(data_json, f)

if __name__ == '__main__':

    numFrame = 0
    numFrameNull = 0
    dir = "./img_noise/"+NAME+"/"
    for filename in os.listdir(dir):
        img = cv2.imread(dir+filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # neu khong detect duoc face thi khong ve bbox
        if len(faces) == 0:
            continue
        # chon bbox to nhat lam mat
        center = [0, 0, 0, 0]
        for (x, y, w, h) in faces:
            if(center[2]*center[3] < w*h):
                center = [x, y, w, h]
        x, y, w, h = center
        img_name = './img_save/'+NAME+'/'+str(numFrame)+'.jpg'
        print(NAME+" "+str(numFrame))
        cv2.imwrite(img_name, img[y:y+h, x:x+w])
        numFrame += 1