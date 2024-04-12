import os.path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from scipy import ndimage
import cv2 as cv

image = None


def plot(data, title, rows, columns, index):
    plt.subplot(rows, columns, index)
    plt.imshow(data)
    plt.gray()
    plt.axis('off')
    plt.title(title)
    plt.tight_layout(pad=0.1, w_pad=0.5, h_pad=0.1)


# high pass filter
def exercise1():
    global image
    plot(image, 'Base image', 1, 2, 1)

    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])

    highpass_3x3 = cv.filter2D(src=image, ddepth=-1, kernel=kernel)
    plot(highpass_3x3, 'High Pass Filter (zad 1)', 1, 2, 2)
    plt.show()


def exercise2():
    data = np.array(image, dtype=float) / 255.0
    plot(data, 'Base image', 1, 2, 1)

    matrix = np.array([[0.393, 0.769, 0.189],
                       [0.349, 0.689, 0.168],
                       [0.272, 0.534, 0.131]])

    converted_data = np.zeros(data.shape)
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            rgb = data[x][y]
            new_val = np.dot(matrix, rgb)
            converted_data[x][y] = new_val
    converted_data = np.clip(converted_data, 0, 1.0)
    plot(converted_data, 'sepia (zad 2)', 1, 2, 2)
    plt.show()


def exercise3():
    global image
    mul_matrix = np.array([[0.229,  0.587,  0.114],
                          [0.500, -0.418, -0.082],
                          [-0.168, -0.331, 0.500]])

    add_vector = np.array([0, 128, 128]).transpose()

    Y = np.zeros((image.shape[0], image.shape[1]))
    Cr = np.zeros((image.shape[0], image.shape[1]))
    Cb = np.zeros((image.shape[0], image.shape[1]))
    imageYCrCb = np.zeros(image.shape, dtype=np.uint8)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            rgb = image[x][y]
            YCrCb = add_vector + np.dot(mul_matrix, rgb)
            YCrCb = np.clip(YCrCb, 0, 255)
            Y[x][y] = YCrCb[0]
            Cr[x][y] = YCrCb[1]
            Cb[x][y] = YCrCb[2]
            imageYCrCb[x][y] = YCrCb

    inverse_conversion = cv.cvtColor(imageYCrCb, cv.COLOR_YCrCb2RGB)
    plot(image, 'Base image', 2, 3, 1)
    plot(Y, 'Składowa: Y', 2, 3, 2)
    plot(Cr, 'Składowa: Cr', 2, 3, 3)
    plot(Cb, 'Składowa: Cb', 2, 3, 4)
    plot(inverse_conversion, 'YCbCr -> RGB', 2, 3, 5)
    plt.show()


def exercise4():
    mul_matrix = np.array([[0.229, 0.587, 0.114],
                           [0.500, -0.418, -0.082],
                           [-0.168, -0.331, 0.500]])

    add_vector = np.array([0, 128, 128]).transpose()

    Y = np.zeros((image.shape[0], image.shape[1]))
    Cr = np.zeros((image.shape[0], image.shape[1]))
    Cb = np.zeros((image.shape[0], image.shape[1]))
    imageYCrCb = np.zeros(image.shape, dtype=np.uint8)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            rgb = image[x][y]
            YCrCb = add_vector + np.dot(mul_matrix, rgb)
            YCrCb = np.clip(YCrCb, 0, 255)
            Y[x][y] = YCrCb[0]
            Cr[x][y] = YCrCb[1]
            Cb[x][y] = YCrCb[2]
            imageYCrCb[x][y] = YCrCb


if __name__ == '__main__':
    path = './image3.jpg'
    while not os.path.isfile(path):
        print(f'Nie znaleziono pliku {path}!')
        path = input('Wskaz sciezke do pliku: ')
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    user_input = ''
    while input != '':
        print('[0] - Wyjscie')
        print('[1] - Zadanie 1')
        print('[2] - Zadanie 2')
        print('[3] - Zadanie 3')
        print('[4] - Wybierz sciezke do zdjecia (bazowo zdjecie: image3.jpg)')
        user_input = input('Wybierz opcje: ')
        user_input = user_input.replace(' ', '').replace('\n', ' ')
        if user_input == '0':
            break
        elif user_input == '1':
            print('Ładuje zadanie 1 ...')
            exercise1()
        elif user_input == '2':
            print('Ładuje zadanie 2 ...')
            exercise2()
        elif user_input == '3':
            print('Ładuje zadanie 3 ...')
            exercise3()
        elif user_input == '4':
            path = input('Podaj sciezke: ')
            if os.path.isfile(path):
                image = cv.imread(path)
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            else:
                print('Plik nie istnieje!')
        else:
            print('Nie rozpoznano opcji')
        print('\n')
