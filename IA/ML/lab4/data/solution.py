import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn import svm

def normalize_data(train, test, type=None):
    scaler = None
    if type == 'standard':
        scaler = preprocessing.StandardScaler()
    elif type == 'minmax':
        scaler = preprocessing.MinMaxScaler()
    elif type == 'l1':
        scaler = preprocessing.Normalizer(norm='l1')
    elif type == 'l2':
        scaler = preprocessing.Normalizer(norm='l2')
    if scaler is not None:
        #scaler.fit(train)
        scaled_train = scaler.transform(train)
        #scaler.fit(test)
        scaled_test = scaler.transform(test)
        return scaled_train, scaled_test
    else:
        print("nu s-a realizat nicio normalizare")
        return train, test


class bag_of_words:

    def __init__(self):
        self.words = []
        self.vocabulary_length = 0

    def build_bow(self, train_data):
        for document in train_data:
            for word in document:
                if word not in self.words:
                    self.words.append(word)

        self.vocabulary_length = len(self.words)
        self.words = np.array(self.words)

    def get_features(self, test_data):
        features = np.zeros((len(test_data), self.vocabulary_length))
        for document_idx, document in enumerate(test_data):
            for word in document:
                if word in self.words:
                    features[document_idx][np.where(self.words == word)[0][0]] += 1
        return features


training_data = np.load('training_sentences.npy', allow_pickle=True)
training_labels = np.load('training_labels.npy', allow_pickle=True)

test_data = np.load('test_sentences.npy', allow_pickle=True)
test_labels = np.load('test_labels.npy', allow_pickle=True)


bow_model = bag_of_words()
bow_model.build_bow(training_data)

train_features = bow_model.get_features(training_data)
test_features = bow_model.get_features(test_data)

scaled_train, scaled_test = normalize_data(train_features, test_features, type='l2')


trainer = svm.SVC(C=1, kernel='linear')
trainer.fit(scaled_train, training_labels)
#predicted_labels = trainer.predict(scaled_test)
print(trainer.score(scaled_test, test_labels))
