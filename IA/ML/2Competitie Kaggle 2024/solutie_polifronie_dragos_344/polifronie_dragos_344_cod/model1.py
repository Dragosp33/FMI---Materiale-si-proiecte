import glob
import cv2
import multiprocessing
import numpy as np
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
import tensorflow as tf
import csv


images_list = sorted(glob.glob(r'/kaggle/input/unibuc-brain-ad/data/data/*.png'))




def load_image(image_path):
    return cv2.imread(image_path)


try:
    cpus = multiprocessing.cpu_count()
except NotImplementedError:
    cpus = 2  # arbitrary default

pool = multiprocessing.Pool(processes=cpus)
images = pool.map(load_image, images_list)


def read_labels(file_name):
  f = open(file_name)
  f.readline()
  vector = []
  while True:
    x = f.readline().strip(" ")
    #print(x)
    if x == '':
      return vector
      break
    else:
      x = x.split(",")
      vector.append(int(x[1]))

train_labels = read_labels("/kaggle/input/unibuc-brain-ad/data/train_labels.txt")
validation_labels = read_labels("/kaggle/input/unibuc-brain-ad/data/validation_labels.txt")






def normalize_data(train_data, test_data, type='standard'):
    scaler = None
    if type == 'standard':
        scaler = preprocessing.StandardScaler()
        if scaler is not None:
          scaler.fit(train_data)
          scaled_train_data = scaler.transform(train_data)
          scaled_test_data = scaler.transform(test_data)
          return (scaled_train_data, scaled_test_data)
    else:
        print("No scaling was performed. Raw data is returned.")
        return (train_data, test_data)


train_data = np.array(images[:15000]).reshape(15000, 3*224*224)
x_train, x_test, y_train, y_test = train_test_split(train_data, train_labels, train_size = .10)

test_data = np.array(images[17000:]).reshape(5149, 3*224*224)

scaled_train, scaled_test = normalize_data(x_train, test_data, type='standard')

from sklearn.neural_network import MLPClassifier
mlp = MLPClassifier(hidden_layer_sizes=(200, 200, 200), activation='relu', solver='adam',
alpha = 0.0001, batch_size='auto', learning_rate='constant', learning_rate_init=0.001,
power_t=0.5, max_iter = 200, shuffle = True, random_state = None, tol=0.0001,verbose=False,
momentum=0.9, early_stopping = False, validation_fraction = 0.1, n_iter_no_change=10)


#1st version: 0.27 acc - early stop = false, layers = 200, 200, 200

mlp.fit(scaled_train, y_train)
#print("Test set score: %f" % mlp.score(scaled_validation, validation_labels))

predicted_labels = mlp.predict(scaled_test)



file2 = '/kaggle/working/submission_1_poifronie_dragos.csv'
fields = ['id', 'values']
with open(file2, 'w', newline='') as file:
  writer = csv.writer(file)
  row1=['id','class']
  writer.writerow(row1)
  for y in range(len(predicted_labels)):
    j = 17001+y
    row = [str('0' + str(j)), predicted_labels[y]]
    writer.writerow(row)






