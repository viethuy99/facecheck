import numpy as np
import cv2
from sklearn.preprocessing import Normalizer
import json



def get_embedding(model, img):
    img = img.astype('float32')
    mean, std = img.mean(), img.std()
    img = (img - mean) / std
    img = np.expand_dims(img, axis=0)
    # print(img.shape)
    res = model.predict(img)
    return res[0]


def recognize(face,model_predict,model_embedding):
    face = np.array(face)
    face = cv2.resize(face, (160, 160))
    face_embedding = get_embedding(model_embedding, face)
    face_embedding = np.expand_dims(face_embedding, axis=0)
    transformer = Normalizer(norm='l2').fit(face_embedding)
    face_embedding = transformer.transform(face_embedding)
    res = model_predict.predict(face_embedding)
    return res

def get_data_member(fileName):
    file_json = open(fileName)
    data_json = json.load(file_json)

    classes = data_json["name"]
    class_name = data_json["id"]

    numberPerson = len(classes)

    file_json.close()
    return classes, class_name, numberPerson
