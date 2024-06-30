import numpy as np
import os
import cv2
from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

folder = 'CAVA-2023-Lucrare2-Subiect/data/ex1'


img_size = (64, 128)
train_data = []
test_data = []
train_labels = np.concatenate((np.ones(100), np.zeros(100)))
test_labels = np.concatenate((np.ones(25), np.zeros(25)))
train_features = []
test_features = []
for i, file in enumerate(os.listdir(folder)):
    img_path = os.path.join(folder, file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, img_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    features = hog(img, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), feature_vector=True)
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = img.reshape(-1)  # Flatten the image
    img = img / 225.0
    if i % 125 < 100:
        train_data.append(img)
        train_features.append(features)

    else:
        test_features.append(features)
        test_data.append(img)
        print(file)
""" print(img)
    img = img.reshape(64, 128)
    print(img.shape)
    features = hog(img, pixels_per_cell=(6, 6),
                   cells_per_block=(2, 2), feature_vector=True)
"""


test_features = np.array(test_features)
train_features = np.array(train_features)

#model = LogisticRegression(max_iter=200)
model = LogisticRegression(solver='liblinear')
model.fit(train_features, train_labels)

# Make predictions on the testing data
pred_labels = model.predict(test_features)
print("predictions::: ")
print(pred_labels)

acc = accuracy_score(test_labels, pred_labels)
prec = precision_score(test_labels, pred_labels)
rec = recall_score(test_labels, pred_labels)
f1 = f1_score(test_labels, pred_labels)
print("Accuracy: {:.3f}, Precision: {:.3f}, Recall: {:.3f}, F1 score: {:.3f}".format(acc, prec, rec, f1))



"""


for i, file in enumerate(os.listdir(folder)):

    img_path = os.path.join(folder, file)
    img = cv2.imread(img_path)
    img = cv2.resize(img, img_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    features = hog(img, pixels_per_cell=(6, 6),
                   cells_per_block=(2, 2), feature_vector=True)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = img.reshape(-1)  # Flatten the image
    if i % 60 < 45:
        train_data.append(img)
        train_features.append(features)

    else:
        test_features.append(features)
        test_data.append(img)

test_features = np.array(test_features)
train_features = np.array(train_features)

model = LogisticRegression()
model.fit(train_data, train_labels)

# Make predictions on the testing data
pred_labels = model.predict(test_data)
print(pred_labels)

acc = accuracy_score(test_labels, pred_labels)
prec = precision_score(test_labels, pred_labels)
rec = recall_score(test_labels, pred_labels)
f1 = f1_score(test_labels, pred_labels)"""
#print("Accuracy: {:.3f}, Precision: {:.3f}, Recall: {:.3f}, F1 score: {:.3f}".format(acc, prec, rec, f1))