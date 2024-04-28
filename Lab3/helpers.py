import numpy as np
import matplotlib.pyplot as plt
import cv2
from matplotlib import pyplot
import numpy as np
from scipy.fftpack import dct
from scipy.fftpack import idct
import struct
import zlib


def plot(data, title, rows, columns, index):
    plt.subplot(rows, columns, index)
    plt.imshow(data)
    plt.gray()
    plt.axis('off')
    plt.title(title)
    #plt.tight_layout(pad=1, w_pad=0.8, h_pad=0.5)

def dct2(array):
    return dct(dct(array, axis=0, norm='ortho'), axis=1, norm='ortho')


def idct2(array):
    return idct(idct(array, axis=0, norm='ortho'), axis=1, norm='ortho')


#
# Calculate quantisation matrices
#
# Based on: https://www.hdm-stuttgart.de/~maucher/Python/MMCodecs/html/jpegUpToQuant.html
#           #step-3-and-4-discrete-cosinus-transform-and-quantisation
#
_QY = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                   [12, 12, 14, 19, 26, 48, 60, 55],
                   [14, 13, 16, 24, 40, 57, 69, 56],
                   [14, 17, 22, 29, 51, 87, 80, 62],
                   [18, 22, 37, 56, 68, 109, 103, 77],
                   [24, 35, 55, 64, 81, 104, 113, 92],
                   [49, 64, 78, 87, 103, 121, 120, 101],
                   [72, 92, 95, 98, 112, 100, 103, 99]])

_QC = np.array([[17, 18, 24, 47, 99, 99, 99, 99],
                   [18, 21, 26, 66, 99, 99, 99, 99],
                   [24, 26, 56, 99, 99, 99, 99, 99],
                   [47, 66, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99],
                   [99, 99, 99, 99, 99, 99, 99, 99]])

def convert_8x8_to_channel(blocks, width):
    step = int(width / 8)
    rows = []

    for i in range(0, len(blocks), step):
        row_blocks = blocks[i:i + step]
        max_height = max([block.shape[0] for block in row_blocks])
        max_width = max([block.shape[1] for block in row_blocks])

        # Create a list to store padded blocks
        padded_blocks = []

        for block in row_blocks:
            # Pad block to have the same width and height
            pad_height = max_height - block.shape[0]
            pad_width = max_width - block.shape[1]
            padded_block = np.pad(block, ((0, pad_height), (0, pad_width)), 'constant', constant_values=0)
            padded_blocks.append(padded_block)

        # Concatenate padded blocks along axis 1 to form a row
        row = np.concatenate(padded_blocks, axis=1)
        rows.append(row)

    # Concatenate rows along axis 0 to form the channel
    channel = np.concatenate(rows, axis=0)

    return channel

def zig_zag(block_of_image) -> list:
    # setup of helper variables
    n = x = y = 0
    zig_zag_vector = np.zeros(64, dtype=np.uint8)
    # main loop
    while n < 64 :
        #moving left
        while x > -1 and y <8:
            zig_zag_vector[n] = block_of_image[x ,y]
            x-=1
            y+=1
            n+=1
        x+=1
        if y == 8:
            y-=1
            x+=1
        #moving right
        while y > -1 and x <8:
            zig_zag_vector[n] = block_of_image[x, y]
            y-=1
            x+=1
            n+=1
        y+=1
        if x == 8:
            x-=1
            y+=1
    return zig_zag_vector

def get_8x8_blocks_from_list(image_array):
    """
    Extracts 8x8 pixel data from a 2-dimensional image list, padding with zeros if necessary.

    Parameters:
    image_list (list): The 2-dimensional list representing the image.

    Returns:
    list: A list of 8x8 lists containing pixel data.
    """

    height, width = image_array.shape

    pixel_data_list = []

    for i in range(0, height, 8):
        for j in range(0, width, 8):
            # Extract 8x8 pixel data, padding with zeros if necessary
            block = np.zeros((8, 8), dtype=image_array.dtype)
            for x in range(8):
                for y in range(8):
                    if i + x < height and j + y < width:
                        block[x, y] = image_array[i + x, j + y]

            pixel_data_list.append(block)

    return pixel_data_list

def reconstruct_image_from_blocks(blocks, height, width):
    """
    Reconstructs a 2-dimensional numpy array from a list of 8x8 pixel blocks.

    Parameters:
    blocks (list): A list of 8x8 numpy arrays containing pixel data.
    height (int): The height of the original image.
    width (int): The width of the original image.

    Returns:
    numpy.ndarray: A 2-dimensional numpy array representing the reconstructed image.
    """
    # Initialize an empty array to hold the reconstructed image
    reconstructed_image = np.zeros((height, width), dtype=blocks[0].dtype)

    block_idx = 0
    for i in range(0, height, 8):
        for j in range(0, width, 8):
            block = blocks[block_idx]
            for x in range(8):
                for y in range(8):
                    if i + x < height and j + y < width:
                        reconstructed_image[i + x, j + y] = block[x, y]
            block_idx += 1

    # Move to the next block
    block_idx += 1

    return reconstructed_image

def adjust_size(base_params, reference):
    res = []
    for base in base_params:
        if base.shape[1] > reference.shape[1]:
            diff = base.shape[1] - reference.shape[1]
            base = base[:, :-diff]
        res.append(base)
    return tuple(res)

def compress(Y, CR, CB):
    concat = np.concatenate((Y.flatten(), CR.flatten(), CB.flatten()), axis=0)
    compress = zlib.compress(concat)
    return compress

def downsample(image_data, sample_rate=2):
    CR = image_data[0::sample_rate,0::sample_rate,1]
    CB = image_data[0::sample_rate,0::sample_rate,2]
    Y  = image_data[0::,0::,0]
    return CR, CB, Y

def upsample(chanel, sample_rate=2):
    upsample = np.repeat(chanel, sample_rate, axis=0)
    upsample = np.repeat(upsample, sample_rate, axis=1)
    return upsample



def _scale(QF):
    if QF < 50 and QF >= 1:
        scale = np.floor(5000 / QF)
    elif QF < 100:
        scale = 200 - 2 * QF
    else:
        raise ValueError('Quality Factor must be in the range [1..99]')

    scale = scale / 100.0
    return scale


def QY(QF=2):
    return _QY * _scale(QF)


def QC(QF=2):
    return _QC * _scale(QF)

