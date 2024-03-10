import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from scipy import ndimage


image = Image.open('catImage.png')


def plot(data, title, rows, columns, index):
    plt.subplot(rows, columns, index)
    plt.imshow(data)
    plt.gray()
    plt.axis('off')
    plt.title(title)


# high pass filter
def exercise1():
    data = np.array(image, dtype=float) / 255.0
    plot(data, 'Base image', 1, 2, 1)

    kernel = np.array([[-1, -1, -1],
                       [-1, 8, -1],
                       [-1, -1, -1]])
    kernel = np.dstack([kernel, kernel, kernel])

    highpass_3x3 = ndimage.convolve(data, kernel)
    highpass_3x3 = np.clip(highpass_3x3, 0, 1)
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
    converted_data = np.clip(converted_data, 0, 1)
    plot(converted_data, 'sepia (zad 2)', 1, 2, 2)
    plt.show()


def exercise3():
    data = np.array(image, dtype=int)

    mul_matrix = np.array([[0.229,  0.587,  0.114],
                          [0.500, -0.418, -0.082],
                          [-0.168, -0.331, 0.500]])
    inverse_mul_matrix = np.array([[1.000, 0.000, 1.403],
                                   [1.000, -0.344, -0.714],
                                   [1.000, 1.773, 0.000]])
    add_vector = np.array([0, 128, 128]).transpose()

    Y = np.zeros((data.shape[0], data.shape[1]))
    Cr = np.zeros((data.shape[0], data.shape[1]))
    Cb = np.zeros((data.shape[0], data.shape[1]))
    inverse_conversion = np.zeros(data.shape)
    for x in range(data.shape[0]):
        for y in range(data.shape[1]):
            rgb = data[x][y]
            YCrCb = add_vector + np.dot(mul_matrix, rgb)
            Y[x][y] = YCrCb[0]
            Cr[x][y] = YCrCb[1]
            Cb[x][y] = YCrCb[2]
            inverse_conversion[x][y] = np.dot(inverse_mul_matrix, (YCrCb.transpose() - add_vector))

    inverse_conversion = np.clip(inverse_conversion, 0, 255)/255.0

    plot(data, 'Base image', 3, 2, 1)
    plot(Y, 'Składowa: Y', 3, 2, 2)
    plot(Cr, 'Składowa: Cr', 3, 2, 3)
    plot(Cb, 'Składowa: Cb', 3, 2, 4)
    plot(inverse_conversion, 'YCbCr -> RGB', 3, 2, 5)
    plt.show()


if __name__ == '__main__':
    #exercise1()
    #exercise2()
    exercise3()