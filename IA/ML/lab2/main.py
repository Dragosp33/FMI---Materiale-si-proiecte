from sklearn.naive_bayes import MultinomialNB
import numpy as np
import math
import pdb

import matplotlib.pyplot as plt

"""
ex1:


train_data = [(160, 'F'), (165, 'F'), (155, 'F'), (172, 'F'), (175, 'B'), (180, 'B'), (188, 'B'), (190, 'B')]


x_train = []
y_labels = []
for i in train_data:
    x_train.append(i[0])
    y_labels.append(i[1])
y_train = np.array(y_labels)
x_train = np.array(x_train)
x_train = x_train.reshape(-1,1)

print(x_train, y_train)
bins = np.linspace(start=150, stop=190, num=5)

corespond = np.digitize(x_train, bins)
print(corespond)

x_test = np.array([[150]])

x_test.reshape(1,-1)
x_test = np.digitize(x_test, bins)
print(x_test)
nb = MultinomialNB()
nb = nb.fit(corespond, y_train)
p = nb.predict(x_test)
print(p)
#test_labels = np.array(['F', 'B'])
#sc = nb.score(x_test, test_labels)
print(sc)
"""

#Ex2:
train_images = np.loadtxt("data/train_images.txt")
train_labels = np.loadtxt("data/train_labels.txt", int)
test_images = np.loadtxt("data/test_images.txt")
test_labels = np.loadtxt("data/test_labels.txt", int)

def value_to_bins(x, num_bins):
    x = np.digitize(x, num_bins)
    return x - 1

num_bins = 5
bins = np.linspace(0, 255, num=num_bins)
x_train = value_to_bins(train_images, bins)
x_test = value_to_bins(test_images, bins)

#print(x_train)

""" Ex 3: """
def show_score(x_train, y_train, x_test, y_test):
    clf = MultinomialNB()
    clf.fit(x_train, y_train)
    print("accuracy: ", clf.score(x_test, y_test))

#show_score(x_train, train_labels, x_test, test_labels)
""" 
#Ex4: 
num_bins = [3, 5, 7, 9, 11]
for x in num_bins:
    bins = np.linspace(0, 255, num=x)
    x_train = value_to_bins(train_images, bins)
    x_test = value_to_bins(test_images, bins)
    show_score(x_train, train_labels, x_test, test_labels)

"""

"""Ex5: """
num_bins = 5
bins = np.linspace(0, 255, num=num_bins)
x_train = value_to_bins(train_images, bins)
x_test = value_to_bins(test_images, bins)

clf = MultinomialNB()
clf.fit(x_train, train_labels)
predicted_labels = clf.predict(x_test)
misclasified_indices = np.where(predicted_labels != test_labels)[0]

""" 
for i in range(20):
    image = train_images[misclasified_indices[i], :] # prima imagine
    image = np.reshape(image, (28, 28))
    plt.imshow(image.astype(np.uint8), cmap='gray')
    plt.title('Aceasta imagine a fost clasificata ca %d.' % predicted_labels[misclasified_indices[i]])
    plt.show()
"""
"""Ex 6: """


def confusion_matrix(y_true, y_pred):
    num_classes = max(y_true.max(), y_pred.max()) + 1
    conf_matrix = np.zeros((num_classes, num_classes))

    for i in range(len(y_true)):
        conf_matrix[int(y_true[i]), int(y_pred[i])] += 1
    return conf_matrix


print(confusion_matrix(test_labels, predicted_labels))