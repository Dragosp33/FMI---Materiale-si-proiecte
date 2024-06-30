import cv2
import numpy as np


def show_image(title,image):
    image=cv2.resize(image,(0,0),fx=0.19,fy=0.19)

    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


img = cv2.cvtColor(cv2.imread("data\\imagini_auxiliare\\template_5.jpg"), cv2.COLOR_BGR2GRAY)
img_m_blur = cv2.medianBlur(img, 5)
show_image("initial blur", img_m_blur)
img_g_blur = cv2.GaussianBlur(img, (0, 0), 5)
show_image("initial blur", img_g_blur)
thresh1 = cv2.Canny(img_m_blur, 60, 120)
thresh2 = cv2.Canny(img_g_blur, 10, 300)
#show_image("median blur", thresh1)
#show_image("gausian blur", thresh2)
"""th3 = cv2.adaptiveThreshold(img_m_blur, 127, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                           cv2.THRESH_BINARY, 11, 2)"""
ret, thresh = cv2.threshold(img_m_blur, 190, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                       cv2.CHAIN_APPROX_SIMPLE)
color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
img = cv2.drawContours(color, contours, -1, (0,255,0), 2)
show_image("??",img)




