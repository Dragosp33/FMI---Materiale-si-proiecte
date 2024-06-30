import numpy as np
import cv2 as cv

def show_image(title,image):
    image=cv.resize(image,(0,0),fx=0.19,fy=0.19)

    cv.imshow(title,image)

def destroy():
    cv.waitKey(0)
    cv.destroyAllWindows()








#print(contours)
def gaseste_contur(img):
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    image_m_blur = cv.medianBlur(image, 3)
    # show_image("medianblur", image_m_blur)
    image_g_blur = cv.GaussianBlur(image_m_blur, (0, 0), 5)
    # show_image("gausianblur", image_g_blur)
    image_sharpened = cv.addWeighted(image_m_blur, 1.2, image_g_blur, -0.8, 0)
    show_image('image_sharpened', image_sharpened)

    _, thresh = cv.threshold(image_sharpened, 50, 255, cv.THRESH_BINARY)

    canny = cv.Canny(image, 50, 255)
    show_image("canny", canny)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv.erode(thresh, kernel)
    show_image('image_thresholded', thresh)
    edges = cv.Canny(thresh, 100, 300)
    show_image('canny with threshold', edges)
    th3 = cv.adaptiveThreshold(image_sharpened, 127, cv.ADAPTIVE_THRESH_GAUSSIAN_C, \
                               cv.THRESH_BINARY, 11, 2)

    show_image('adaptive gausian threshold', th3)
    contours, _ = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_area = 0

    for i in range(len(contours)):
        if (len(contours[i]) > 3):
            print("i: ", i, " ", contours[i])
            possible_top_left = None
            possible_bottom_right = None
            for point in contours[i].squeeze():
                if possible_top_left is None or point[0] + point[1] < possible_top_left[0] + possible_top_left[1]:
                    possible_top_left = point

                if possible_bottom_right is None or point[0] + point[1] > possible_bottom_right[0] + \
                        possible_bottom_right[1]:
                    possible_bottom_right = point

            diff = np.diff(contours[i].squeeze(), axis=1)
            possible_top_right = contours[i].squeeze()[np.argmin(diff)]
            possible_bottom_left = contours[i].squeeze()[np.argmax(diff)]
            if cv.contourArea(np.array([[possible_top_left], [possible_top_right], [possible_bottom_right],
                                        [possible_bottom_left]])) > max_area:
                max_area = cv.contourArea(np.array(
                    [[possible_top_left], [possible_top_right], [possible_bottom_right], [possible_bottom_left]]))
                top_left = possible_top_left
                bottom_right = possible_bottom_right
                top_right = possible_top_right
                bottom_left = possible_bottom_left



    print(top_left, bottom_left, top_right, bottom_right)
    width = 810
    height = 810

    image_copy = cv.cvtColor(image.copy(), cv.COLOR_GRAY2BGR)
    cv.circle(image_copy, tuple(top_left), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(top_right), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(bottom_left), 20, (0, 0, 255), -1)
    cv.circle(image_copy, tuple(bottom_right), 20, (0, 0, 255), -1)
    show_image("detected corners",image_copy)

    puzzle = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")
    destination_of_puzzle = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype="float32")

    M = cv.getPerspectiveTransform(puzzle, destination_of_puzzle)

    result = cv.warpPerspective(image, M, (width, height))
    result = cv.cvtColor(result, cv.COLOR_GRAY2BGR)

    return result

img = cv.imread("data\\imagini_auxiliare\\template_1.jpg")
result = gaseste_contur(img)
show_image("contururi", result)
destroy()