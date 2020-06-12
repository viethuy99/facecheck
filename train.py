from numpy import load
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer
from sklearn.svm import SVC
import pickle
import os
import numpy as np

X_train=[]
Y_train=[]

for fileName in os.listdir('./data_embedded/'):
    data = load('./data_embedded/'+fileName)
    print(fileName)

    x_train, y_train = data['arr_0'], data['arr_1']
    transformer = Normalizer(norm='l2').fit(x_train)
    x_train = transformer.transform(x_train)

    for i in range(len(x_train)):
        X_train.append(x_train[i])
    for i in range(len(y_train)):
        print(y_train[i])
        Y_train.append(y_train[i])


if __name__ == '__main__':

    kernels=["sigmoid","poly","rbf","linear"]
    kernel=kernels[3]
    model = SVC(kernel=kernel, probability=True)
    model.fit(X_train, Y_train)


    yhat_train = model.predict(X_train)
    # score
    score_train = accuracy_score(Y_train, yhat_train)
    Y_train=np.array(Y_train)
    print(Y_train)
    print(yhat_train)
    print(type(Y_train))
    print(type(yhat_train))
    # summarize
    print('Accuracy: train={}'.format(score_train*100))
    filename="./model/final_model.sav"
    pickle.dump(model, open(filename, 'wb'))

