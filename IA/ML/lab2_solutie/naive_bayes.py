import pdb
import numpy as np
import math
import pdb
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt 
         
# load data          
train_images = np.loadtxt('data/train_images.txt')
train_labels = np.loadtxt('data/train_labels.txt', 'int')
test_images = np.loadtxt('data/test_images.txt')
test_labels = np.loadtxt('data/test_labels.txt', 'int') 
   
image = train_images[0, :] # prima imagine
image = np.reshape(image, (28, 28)) 
plt.imshow(image.astype(np.uint8), cmap='gray')  
plt.show()
  

### ---- 2 ----
def values_to_bins(x, bins): 
    x = np.digitize(x, bins)    
    return x - 1  

num_bins = 5
bins = np.linspace(0, 255, num=num_bins)  
x_train = values_to_bins(train_images, bins) 
x_test = values_to_bins(test_images, bins)  

### ---- 3 ----
clf = MultinomialNB()
clf.fit(x_train, train_labels)
print('accuracy =', clf.score(x_test, test_labels))
 
### ---- 4 ---- 
for num_bins in range(3, 12, 2):
    bins = np.linspace(0, 255, num=num_bins)  
    x_train = values_to_bins(train_images, bins) 
    x_test = values_to_bins(test_images, bins)  
 
    clf = MultinomialNB()
    clf.fit(x_train, train_labels)
    print('accuracy for num_bins=%d is %f' % (num_bins, clf.score(x_test, test_labels)))

### ---- 5 ----     
num_bins = 5
bins = np.linspace(0, 255, num=num_bins)  
x_train = values_to_bins(train_images, bins) 
x_test = values_to_bins(test_images, bins)  


clf = MultinomialNB()
clf.fit(x_train, train_labels)
predicted_labels = clf.predict(x_test)

misclasified_indices = np.where(predicted_labels != test_labels)[0] 

for i in range(20):
    image = train_images[misclasified_indices[i], :] # prima imagine
    image = np.reshape(image, (28, 28)) 
    plt.imshow(image.astype(np.uint8), cmap='gray')  
    plt.title('Aceasta imagine a fost clasificata ca %d.' % predicted_labels[misclasified_indices[i]])
    plt.show()
      
### ---- 6 ----           
def confusion_matrix(y_true, y_pred): 
    num_classes = max(y_true.max(), y_pred.max()) + 1
    conf_matrix = np.zeros((num_classes, num_classes)) 
    
    for i in range(len(y_true)): 
        conf_matrix[int(y_true[i]), int(y_pred[i])] +=1
    return conf_matrix

print(confusion_matrix(test_labels, predicted_labels))