import numpy as np
import pdb
import matplotlib.pyplot as plt
from skimage import io
import sklearn.metrics as sm


class knn_classifier:

    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels

    def classify_image(self, test_image, num_neighbors = 3, metric = 'l2'):
        if metric == 'l1':
            dist = np.sum(abs(self.train_images - test_image), axis=1)
        elif metric == 'l2':
            dist = np.sqrt(np.sum((self.train_images - test_image)**2, axis = 1))
        else:
            print("error")
        #print("distante: ", dist)
        sort_index = np.argsort(dist)
        #print("sort_index: ")
        sort_index = sort_index[:num_neighbors]
        #print(sort_index)
        nearest_label = self.train_labels[sort_index]
        #print("cel mai apropiat label: ", nearest_label)
        histc = np.bincount(nearest_label)
        return np.argmax(histc)

    def classify_images(self, test_images, num_neighbors = 3, metric = 'l2'):
        num_test = test_images.shape[0]
        predicted_labels = np.zeros(num_test, int)
        for i in range(num_test):
            if(i % 50 == 0):
                print('processing {}%...'.format(i / num_test * 100))
            predicted_labels[i] = self.classify_image(test_images[i, :], num_neighbors = num_neighbors, metric = metric)

        return predicted_labels

    def accuracy_score(self, y_true, y_pred):
        return (y_true==y_pred).mean()


train_images = np.loadtxt('data/train_images.txt')
train_labels = np.loadtxt('data/train_labels.txt', 'int')




classifier = knn_classifier(train_images, train_labels)

test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int')
# 1, 2, 3
predicted_labels = classifier.classify_images(test_images, 3, metric = 'l2')
accuracy = classifier.accuracy_score(test_labels, predicted_labels)
print('the classifier accuracy using l2 distance and 3 neighbors is ', accuracy)




""" 4 : 
#A):

neighbors = [3, 5, 7, 9, 11]
accuracy = np.zeros((len(neighbors)))
for i in range(len(neighbors)):
    predicted_labels = classifier.classify_images(test_images, neighbors[i], metric='l2')
    accuracy[i] = classifier.accuracy_score(test_labels, predicted_labels)

np.savetxt('acuratete_l2.txt', accuracy)
# Ploteaza punctele
plt.plot(neighbors, accuracy)
plt.xlabel('number of neighbors')
plt.ylabel('accuracy')

# Afiseaza figura
plt.show()"""