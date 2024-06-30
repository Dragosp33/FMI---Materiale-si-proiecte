import cv2
import numpy as np
import os


def get_contour(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(img, (3, 3), 0)
    edges = cv2.Canny(blur, 120, 300, apertureSize=3)
    kernel = np.ones((3, 3), np.uint8)
    dilation = cv2.dilate(edges, kernel, iterations=2)
    contours, hierarchy = cv2.findContours(
        dilation,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)

    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)


    img2 = img[y:y + h, x:x + w]
    return img2, cnt


def get_casute(img, antrenare_litere = False):
    #matrix):
    contur, cnt = get_contour(img)
    height = contur.shape[0]
    width = contur.shape[1]

    grey_contur = cv2.cvtColor(contur, cv2.COLOR_BGR2GRAY)
    g_contur = cv2.GaussianBlur(grey_contur, (3, 3), 0)
    _, thresh = cv2.threshold(g_contur, 180, 255, cv2.THRESH_BINARY)
    height_small = height // 15
    width_small = width // 15

    for i in range (1, 16):
        for j in range(1, 16):
            patch = thresh[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            patch_orig = contur[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            Medie_patch = np.mean(patch)
            if Medie_patch > 100:
                clasificare(patch_orig)





img = cv2.imread("data\\litere_antrenate\\litera_A.jpg")
x, cnt = get_contour(img)
cv2.imshow("imagine", x)
cv2.waitKey(0)
cv2.destroyAllWindows()