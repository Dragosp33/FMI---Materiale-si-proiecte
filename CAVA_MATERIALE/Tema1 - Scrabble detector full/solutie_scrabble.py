import cv2
import numpy as np
import os

dictionar = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'V', 'X',
             'Z', 'joker']
dict_puncte = {'A': 1, 'B': 8, 'C': 1, 'D': 2, 'E': 1, 'F': 8, 'G': 9, 'H': 10,
               'I': 1, 'J': 10, 'L': 1, 'M': 4, 'N': 1, 'O': 1, 'P': 2,
               'R': 1, 'S': 1, 'T': 1, 'U': 1, 'V': 8, 'X': 10, 'Z': 10, 'joker': 0}


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



def get_contour_litera(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (5, 5), 0)
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


def clasifica_litera(img):
    maxim = -np.inf
    h, w = img.shape[0], img.shape[1]
    litera = 'k'
    for i in range(0, len(dictionar)):
        template = cv2.imread("data\\litere_antrenate\\"+dictionar[i]+".jpg")
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        template = cv2.resize(template, (w, h))
        res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
        if res > maxim:
            maxim = res
            litera = dictionar[i]
    return litera


def get_casute(img, matrix, antrenare_litere = False):
    #matrix):
    contur, cnt = get_contour(img)
    height = contur.shape[0]
    width = contur.shape[1]

    gray_contur = cv2.cvtColor(contur, cv2.COLOR_BGR2GRAY)
    g_contur = cv2.GaussianBlur(gray_contur, (3, 3), 0)
    _, thresh = cv2.threshold(g_contur, 180, 255, cv2.THRESH_BINARY)
    height_small = height//15
    width_small = width//15

    #print(height_small, width_small)

    litera_curenta = 0
    for i in range (1, 16):
        for j in range(1, 16):
            patch = thresh[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            patch_orig = contur[height_small*(i-1):height_small*i, width_small*(j-1):width_small*j]
            Medie_patch = np.mean(patch)
            if Medie_patch > 100:
                if antrenare_litere == True:
                    patch2, _ = get_contour_litera(patch_orig)
                    cv2.imwrite("data\\litere_antrenate\\"+dictionar[litera_curenta]+".jpg", patch2)
                    litera_curenta+=1
                else:
                    print(i, j)
                    if matrix[i-1][j-1] == '_':

                        contur2, _ = get_contour_litera(patch_orig)
                        contur2 = cv2.cvtColor(contur2, cv2.COLOR_BGR2GRAY)

                        litera_recunoscuta = clasifica_litera(contur2)
                        print(litera_recunoscuta)

                        matrix[i-1][j-1] = litera_recunoscuta
    for coloana in matrix:
        print(coloana)


                    #print(i, j)
                    #print(litera_recunoscuta)


matrix = [['_' for i in range(0,15)] for x in range(0,15)]
print(len(matrix))

img = cv2.imread("data\\evaluare\\fake_test\\2_01.jpg")
get_casute(img, matrix)

for game in range(1, 6):
    matrix = [['_' for i in range(0,15)]*15]
    for turn in range(1, 21):

        name_turn = str(turn)
        if (turn < 10):
            name_turn = '0' + str(turn)

        #filename_predicted = predictions_path_root + str(game) + '_' + name_turn + '.txt'
        #filename_gt = gt_path_root + str(game) + '_' + name_turn + '.txt'





