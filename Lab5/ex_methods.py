import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv


def plot(data, title, rows, columns, index, to_rgb=True):
    plt.subplot(rows, columns, index)
    image = data
    plt.imshow(image)
    plt.gray()
    plt.axis('off')
    plt.title(title)
    plt.tight_layout(pad=1, w_pad=0.8, h_pad=0.5)


def mse(base_image, mod_image, round_dig=2):
    return round(np.square(np.subtract(base_image, mod_image)).mean(), 2)