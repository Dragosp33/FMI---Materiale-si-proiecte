import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread("butterfly.jpeg")
cv.imshow("Fluture galben",img)
cv.waitKey(0)
cv.destroyAllWindows()

img = cv.imread("butterfly.jpeg",cv.IMREAD_GRAYSCALE)
cv.imshow("Fluture gray",img)
cv.waitKey(0)
cv.destroyAllWindows()

H, W = img.shape
print(H,W)

img = cv.resize(img,(100, 100))
H, W = img.shape
print(H,W)
cv.imshow("Fluture gray redimensionat",img)
cv.waitKey(0)
cv.destroyAllWindows()

img = cv.resize(cv.cvtColor(cv.imread("football.jpg"), cv.COLOR_BGR2GRAY), (100, 100));

cv.imshow("Football",img)
cv.waitKey(0)
cv.destroyAllWindows()

#a
v=img.flatten()
x=np.sort(v)
print(x)
plt.plot(np.arange(len(x)),x)
plt.show()

#b
A=img[50:,50:].copy()
cv.imshow("A",A)
cv.waitKey(0)
cv.destroyAllWindows()

#c
t=np.median(x)
print(t)

#d
B=img.copy()
B[B<t]=0
B[B>=t]=255
cv.imshow("B",B)
cv.waitKey(0)
cv.destroyAllWindows()

#e
i_mediu=img.mean()
print(i_mediu)
C=img-i_mediu
C[C<0]=0
C=np.uint8(C)
cv.imshow("C",C)
cv.waitKey(0)
cv.destroyAllWindows()

#f
i_min=img.min()
print(i_min)
l,c=np.where(img==i_min)
print(l,c)

#1.7
#imagine de culoare medie
import os
dir_path='colectiiImagini\\colectiiImagini\\set2\\'
files=os.listdir(dir_path)
color_images=[]
gray_images=[]
for image_name in files:
    path=dir_path+image_name
    img=cv.imread(path)
    img_gray=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    color_images.append(img)
    gray_images.append(img_gray)
color_images=np.array(color_images)
print(color_images.shape)
gray_images=np.array(gray_images)
print(gray_images.shape)
mean_color_image=np.uint8(np.mean(color_images,axis=0)) #imagine medie de culoare
cv.imshow("mean_color_image",mean_color_image)
cv.waitKey(0)
cv.destroyAllWindows()
mean_gray_image=np.uint8(np.mean(gray_images,axis=0)) #imagine medie de intensitate 
cv.imshow("mean_gray_image",mean_gray_image)
cv.waitKey(0)
cv.destroyAllWindows()
#calcularea matricei X unde fiecare element este deviatia standard a intensitatii

X=np.uint8(np.std(gray_images,axis=0))
cv.imshow("X",X)
cv.waitKey(0)
cv.destroyAllWindows()

#1.8
img=cv.imread('butterfly.jpeg')
ws=20
img_crop=img[250:250+ws,250:250+ws,:].copy()
nw=5000
H,W,_=img.shape
y=np.random.randint(0,H-ws,size=(nw))
x=np.random.randint(0,W-ws,size=(nw))
print(len(y))
dist=np.zeros(nw)
for i in range(nw):
    patch=img[y[i]:y[i]+ws,x[i]:x[i]+ws,:].copy()
    dist[i]=np.sqrt(np.sum((np.float64(patch)-np.float64(img_crop))**2))
index=np.argmin(dist)
print(index)
print(dist.min())
print(dist[index])
img_noua=img.copy()
img_noua[250:250+ws,250:250+ws,:]=img[y[index]:y[index]+ws,x[index]:x[index]+ws,:].copy()
cv.imshow("img_noua",img_noua)
cv.waitKey(0)
cv.destroyAllWindows()