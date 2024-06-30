import numpy as np
from skimage import io


# citire imagini si salvarea lor sub np.array; calcularea sumei pixelilor pt fiecare imagine si afisarea maximului

fisier = "images\\car_"
sum = 0
x = np.zeros(9)
images = np.zeros([9, 400, 600])
for i in range(0,9):
    filepath = fisier + str(i) + ".npy"
    image = np.load(filepath)

    #print(image)
    images[i] = image
    sum = np.sum(image)

    x[i] = sum



# media imaginilor :

mean = np.mean(images, axis=0)
io.imshow(mean.astype(np.uint8))
io.show()

# calcularea deviatiei standard:

std = np.std(images)
print(std)

#normalizare imaginilor: Scade imagine medie si imparte rezultat la deviatie standard

for i in images:
    x = i - mean
    x = x/std
    io.imshow(x.astype(np.uint8))
    io.show()




