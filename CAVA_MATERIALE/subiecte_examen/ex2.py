import numpy as np
import cv2
import os

from skimage.feature import hog
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score





img_size = (64, 128)
train_data = []
test_data = []
train_labels = []
test_labels = []

def show_image(title,image, fx=0.1, fy=0.1):
    image=cv2.resize(image,(0,0),fx=fx,fy=fy)
    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

fisier_train = 'CAVA-2023-Lucrare2-Subiect/data/ex2/antrenare/'

imagini = ['001.jpg', '002.jpg', '003.jpg', '004.jpg','005.jpg', '006.jpg','007.jpg', '008.jpg', '009.jpg', '010.jpg',]
THRESHOLD = 100
def get_contour(img2):
    img2 = cv2.imread(img2)
    show_image("sss", img2)
    img = img2.copy()
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(grey, (5, 5), 0)
    edges = cv2.Canny(blur, 200, 400, apertureSize=3)
    #show_image("canny", edges)
    kernel = np.ones((5, 5), np.uint8)
    #kernel2 = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations=3)
    erosion = cv2.erode(dilation, kernel, iterations=3)
    #show_image("erode",erosion)
    contours, hierarchy = cv2.findContours(
        erosion,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img, contours, -1, (0, 255, 0), 20)
    show_image("contururi", img)

    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)

    #img_cropped = img[x:x+h, y:y+w]
    #show_image("chenar", img_cropped)
    width = 810
    height = 810
    img2 = img[y:y + h, x:x + w]
    puzzle = np.array([[x, y], [x + w, y], [x + w, y + h], [x, y + h]], dtype="float32")
    destination_of_puzzle = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv2.getPerspectiveTransform(puzzle, destination_of_puzzle)
    result = cv2.warpPerspective(img, M, (width, height))
    show_image("rezultat", result, 0.5, 0.5)
    return result, cnt


#get_contour(fisier_train + '003.jpg')

lines_horizontal=[]
for i in range(0,811,81):
    l=[]
    l.append((0,i))
    l.append((809,i))
    lines_horizontal.append(l)

lines_vertical=[]
for i in range(0,811,81):
    l=[]
    l.append((i,0))
    l.append((i,809))
    lines_vertical.append(l)


litere = {'A' : 0, 'B' : 1, 'C' : 2, 'D' : 3, 'E' : 4, 'F': 5, 'G' : 6, 'H' : 7, 'I': 8, 'J': 9}


def get_data_from_image(fisier_train, nume_imagine):
    result, cnt = get_contour(fisier_train + nume_imagine)
    show_image("cnt", result, 0.5, 0.5)
    fisier_txt = fisier_train + "ground-truth/" + nume_imagine[:-3] + "txt"
    print(fisier_txt)
    pozitii = []
    valori = []
    patch = result.copy()
    with open(fisier_txt, 'r') as f:
        s = f.readline().strip(" ").split()
        while len(s) > 0:
            print(s)

            pozitii.append(s[0])
            valori.append(s[1])
            s = f.readline().strip().split()

    for i in  range(len(pozitii)):
        coloana = int(litere[pozitii[i][1]])
        linie = int(pozitii[i][0]) -1
        print(coloana)
        print(coloana*81, (coloana+1)*81)

        patch2 = patch[linie*81:(linie+1)*81, coloana*81:(coloana+1)*81]
        show_image('patch ', patch2)

        train_data.append(patch2)
        train_labels.append(valori[i])


#pentru antrenare
for x in imagini:
    get_data_from_image(fisier_train, x)



model = LogisticRegression(solver='liblinear')
model.fit(train_data, train_labels)


def test_data_from_image(fisier_test, nume_imagine):
    result, cnt = get_contour(fisier_train + nume_imagine)
    show_image("cnt", result, 0.5, 0.5)
    fisier_txt = fisier_train + "ground-truth/" + nume_imagine[:-3] + "txt"
    print(fisier_txt)
    pozitii = []
    valori = []
    patch = result.copy()
    testare1 = []
    with open(fisier_txt, 'r') as f:
        s = f.readline().strip(" ").split()
        for i in range(0, int(s[0])):
            pozitii.append(s[0])
            s = f.readline().strip().split()

    for i in  range(len(pozitii)):
        coloana = int(litere[pozitii[i][1]])
        linie = int(pozitii[i][0]) -1
        print(coloana)
        print(coloana*81, (coloana+1)*81)

        patch2 = patch[linie*81:(linie+1)*81, coloana*81:(coloana+1)*81]
        show_image('patch ', patch2)

        testare1.append(patch2)
    testare1 = np.array(testare1)
    model.predict(testare1)










test_features = np.array(test_features)
train_features = np.array(train_features)


fisier_test = "nume_fisier_test"

for x in imagini_test:
    get_data_from_image(fisier_test, x)





"""

def get_features(img2):
    img = img2.copy()
    img = cv2.resize(img, img_size)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    features = hog(img, pixels_per_cell=(6, 6),
               cells_per_block=(2, 2), feature_vector=True)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    img = img.reshape(-1)  # Flatten the image
    train_features.append(features)

"""