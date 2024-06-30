import numpy as np
import matplotlib.pyplot as plt

class knn_classifier:
    def __init__(self, train_images, train_labels):
        self.train_images = train_images
        self.train_labels = train_labels

    def classify_image(self, test_image, num_neighbors = 3, metric = 'L2'):
        if metric == 'L1':
            distance = np.sum(abs(self.train_images - test_image), axis = 1)
        elif metric == 'L2':
            distance = np.sqrt(np.sum((self.train_images - test_image) ** 2, axis= 1))
        else:
            return 'error'

        sort_idx = np.argsort(distance)
        sort_idx = sort_idx[:num_neighbors]

        nearest_label = self.train_labels[sort_idx]
        histc = np.bincount(nearest_label)
        histc = np.argmax(histc)
        return histc

    def classify_images(self, test_images, num_neighbors = 3, metric = 'L2'):
        num_img = len(test_images)
        predict = np.zeros(num_img)
        for x in range(len(test_images)):
            if(x % 50 == 0):
                print("classify items...{}%...".format(x / num_img * 100))
            predict[x] = self.classify_image(test_images[:x], num_neighbors, metric)

        return predict

    def accuracy(self, y_true, y_pred):
        return (y_true == y_pred).mean()















