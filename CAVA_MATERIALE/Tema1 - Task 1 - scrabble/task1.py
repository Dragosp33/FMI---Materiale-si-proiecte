import cv2
import numpy as np
import os

dictionar = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'X',
             'Z', 'joker']
dict_puncte = {'A': 1, 'B': 8, 'C': 1, 'D': 2, 'E': 1, 'F': 8, 'G': 9, 'H': 10,
               'I': 1, 'J': 10, 'L': 1, 'M': 4, 'N': 1, 'O': 1, 'P': 2,
               'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 8, 'X': 10, 'Z': 10, 'joker': 0}

def show_image(title,image):
    image=cv2.resize(image,(0,0),fx=0.19,fy=0.19)

    cv2.imshow(title,image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#functie care ia doar patratele de joc (15X15):
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

    cnt = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(cnt)


    img2 = img[y:y + h, x:x + w]
    return img2, cnt


def get_casute(img, matrix, antrenare_litere = False):
    #matrix):
    contur, cnt = get_contour(img)
    show_image("contur",contur)
    height = contur.shape[0]
    width = contur.shape[1]

    gray_contur = cv2.cvtColor(contur, cv2.COLOR_BGR2GRAY)
    g_contur = cv2.GaussianBlur(gray_contur, (3, 3), 0)
    _, thresh = cv2.threshold(g_contur, 180, 255, cv2.THRESH_BINARY)
    height_small = height//15
    width_small = width//15

    #print(height_small, width_small)

    #litera_curenta = 0
    pozitii = []
    for i in range (1, 16):
        for j in range(1, 16):
            patch = thresh[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            patch_orig = contur[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            Medie_patch = np.mean(patch)
            if Medie_patch > 100:
                if matrix[i-1][j-1] == '_':
                    matrix[i-1][j-1] = 'X'
                    #print(matrix)
                    pozitii.append(str(i)+chr(65+j-1))
    print(pozitii)
    return matrix, pozitii

def scrie_rezultate_task1(folder_rezultate, folder_poze):
    for i in range(1,6):
        matrix = matrix = [['_' for i in range(0,15)] for x in range(0,15)]
        print(matrix)
        for turn in range(1,21):
            k = str(turn)
            if turn < 10:
                k = "0"+str(turn)
            filename_rezultat = folder_rezultate+"\\"+str(i)+"_"+k+".txt"
            fisier_poze = folder_poze+"\\"+str(i)+"_"+k+".jpg"
            poza = cv2.imread(fisier_poze)
            matrix, pozitii = get_casute(poza, matrix)
            f=open(filename_rezultat, 'w')
            for l in pozitii:
                f.write(l)
                f.write("\n")




scrie_rezultate_task1("344_Polifronie_Dragos_solutii_task1", "evaluare2")






