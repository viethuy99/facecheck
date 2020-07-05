import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"]="0"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import cv2
from keras.models import load_model
from Processing import get_embedding
from Processing import get_data_member

# load the model
model = load_model('./pretrain_model/facenet_keras.h5')

classes, class_name, numberPerson = get_data_member("Name_with_Id.json")

# config
name = "Huy"
embedded_data = name+".npz"

if __name__ == '__main__':

    # save image to faces
    faces=[]
    labels=[]
    id=classes[name]
    dir = "./img_save/"+name+"/"
    for filename in os.listdir(dir):
        image = cv2.imread(dir+filename)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (160, 160))
        face_array = np.asarray(image)
        faces.append(face_array)
        labels.append(int(id))
    faces=np.array(faces)
    print(faces.shape)

    # embedding
    x_train=[]

    for face in faces:
        x=get_embedding(model,face)
        x_train.append(x)
    x_train=np.array(x_train)
    y_train = np.array(labels)
    print(y_train)
    print(x_train.shape)
    print(y_train.shape)

    # save model
    np.savez_compressed('./data_embedded/'+embedded_data,
                    x_train, y_train)
    print("Done!")
