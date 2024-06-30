import cv2
import numpy as np
import os

def read_images(folder):
    filenames = os.listdir(folder)
    paths = (os.path.join(folder, filename) for filename in filenames)
    imgs = (cv2.imread(path) for path in paths)
    return [img for img in imgs if img is not None]


def show_image(title,image):
    image=cv2.resize(image,(0,0),fx=0.19,fy=0.19)

    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_contour(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 0)
    edges = cv2.Canny(blur, 120, 300, apertureSize=3)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(
        dilation,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    #print(contours[0])
    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)
    print(x, y, w, h)
    #cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)

    img2 = img[y:y + h, x:x + w]
    return img2, cnt

"""

img = cv2.imread("data\\evaluare\\fake_test\\2_04.jpg")
contururi, cnt = get_contour(img)
dimensiuni = contururi.shape
print(dimensiuni)
show_image("result", contururi)
inaltime = 2130
latime = 1950
show_image("taiat:", contururi[:2130, :1950])
cv2.imshow("1 bucata:", contururi[0:(2130//15)*5, 0:(1950//15)*5])
cv2.waitKey(0)
cv2.destroyAllWindows()
"""


"""
img = cv2.imread("data\\imagini_auxiliare\\litere_2.jpg")
contururi, cnt = get_contour(img)
A = contururi[(2130//15)*3:(2130//15)*4, 1950//15*3:(1950//15)*4]
cv2.imshow("1 bucata:", A)
cv2.waitKey(0)
cv2.destroyAllWindows()
img_grey = cv2.cvtColor(contururi, cv2.COLOR_BGR2GRAY)
img_template= cv2.cvtColor(A,cv2.COLOR_BGR2GRAY)
w, h = img_template.shape[::-1]



"""





