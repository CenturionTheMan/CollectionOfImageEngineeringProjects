import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt


def plot(data, title, rows, columns, index):
    plt.subplot(rows, columns, index)
    plt.imshow(data)
    plt.gray()
    plt.axis('off')
    plt.title(title)
    plt.tight_layout(pad=0.1, w_pad=0.5, h_pad=0.1)


def YCbCrToRGB(Y, Cb, Cr):
    imageYCrCb = np.zeros((Y.shape[0], Y.shape[1], 3), dtype=np.uint8)
    for x in range(Y.shape[0]):
        for y in range(Y.shape[1]):
            imageYCrCb[x][y][0] = Y[x][y]
            imageYCrCb[x][y][1] = Cr[x][y]
            imageYCrCb[x][y][2] = Cb[x][y]
    inverse_conversion = cv.cvtColor(imageYCrCb, cv.COLOR_YCrCb2RGB)
    return inverse_conversion


def RGBtoYCbCr(image):
    mul_matrix = np.array([[0.229, 0.587, 0.114],
                           [0.500, -0.418, -0.082],
                           [-0.168, -0.331, 0.500]])

    add_vector = np.array([0, 128, 128]).transpose()

    Y = np.zeros((image.shape[0], image.shape[1]))
    Cr = np.zeros((image.shape[0], image.shape[1]))
    Cb = np.zeros((image.shape[0], image.shape[1]))
    # imageYCrCb = np.zeros(image.shape, dtype=np.uint8)

    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            rgb = image[x][y]
            YCrCb = add_vector + np.dot(mul_matrix, rgb)
            YCrCb = np.clip(YCrCb, 0, 255)
            Y[x][y] = YCrCb[0]
            Cr[x][y] = YCrCb[1]
            Cb[x][y] = YCrCb[2]
            #imageYCrCb[x][y] = YCrCb
    return Y, Cb, Cr

