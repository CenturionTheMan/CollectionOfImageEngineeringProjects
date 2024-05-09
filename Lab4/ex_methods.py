from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
import binascii
import cv2 as cv
import math
from io import BytesIO

def encode_as_binary_array(msg):
    """Encode a message as a binary string."""
    msg = msg.encode("utf-8")
    msg = msg.hex()
    msg = [msg[i:i + 2] for i in range(0, len(msg), 2)]
    msg = [ "{:08b}".format(int(el, base=16)) for el in msg]
    return "".join(msg)


def decode_from_binary_array(array):
    """Decode a binary string to utf8."""
    array = [array[i: i +8] for i in range(0, len(array), 8)]
    if len(array[-1]) != 8:
        array[-1] = array[-1] + "0" * (8 - len(array[-1]))
    array = [ "{:02x}".format(int(el, 2)) for el in array]
    array = "".join(array)
    result = binascii.unhexlify(array)
    return result.decode("utf-8", errors="replace")


def load_image(path, to_rgb=True, pad=False):
    """Load an image.

    If pad is set then pad an image to multiple of 8 pixels.
    """
    image = cv.imread(path)
    print(image is not None)
    if to_rgb:
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    if pad:
        y_pad = 8 - (image.shape[0] % 8)
        x_pad = 8 - (image.shape[1] % 8)
        image = np.pad(
            image, ((0, y_pad), (0, x_pad), (0, 0)), mode='constant')
    return image


def save_image(path, image):
    """Save an image."""
    plt.imsave(path, image)


def clamp(n, minn, maxn):
    """Clamp the n value to be in range (minn, maxn)."""
    return max(min(maxn, n), minn)


def hide_message(image, message, nbits=1, spos=0):
    """Hide a message in an image (LSB).

    nbits: number of least significant bits
    """


    nbits = clamp(nbits, 1, 8)
    shape = image.shape
    image = np.copy(image).flatten()
    # do pos niech bedzie bez zmian
    image_start = image[:spos]
    # dodajemy napis po pos
    image = image[spos:]

    if len(message) > len(image) * nbits + spos:
        raise ValueError("Message is to long :(")

    chunks = [message[i:i + nbits] for i in range(0, len(message), nbits)]
    for i, chunk in enumerate(chunks):
        byte = "{:08b}".format(image[i])
        new_byte = byte[:-nbits] + chunk
        image[i] = int(new_byte, 2)
    #laczenie poczatku z zmienionym fragmentem
    image = np.concatenate((image_start, image ), axis=None)
    return image.reshape(shape)


def reveal_message(image, nbits=1, length=0, spos=0):
    """Reveal the hidden message.

    nbits: number of least significant bits
    length: length of the message in bits.
    """

    nbits = clamp(nbits, 1, 8)
    image = np.copy(image).flatten()[spos:]
    length_in_pixels = math.ceil(length / nbits)
    if len(image) < length_in_pixels or length_in_pixels <= 0:
        length_in_pixels = len(image)

    message = ""
    i = 0
    while i < length_in_pixels:
        byte = "{:08b}".format(image[i])
        message += byte[-nbits:]
        i += 1

    mod = length % -nbits
    if mod != 0:
        message = message[:mod]
    return message


def hide_image(image, image_to_hide_path, nbits=1):
    with open(image_to_hide_path, "rb") as file:
        secret_img = file.read()

    secret_img = secret_img.hex()
    secret_img = [secret_img[i:i + 2] for i in range(0, len(secret_img), 2)]
    secret_img = ["{:08b}".format(int(el, base=16)) for el in secret_img]
    secret_img = "".join(secret_img)
    return hide_message(image, secret_img, nbits), len(secret_img)


def reveal_image(image, lenght, nbits=1):
    # pobranie obrazu w postaci napisu z obrazu
    message = reveal_message(image, length=lenght, nbits=nbits)
    # przedstawienie danych w postaci tablicy bajtow w postaci bitow
    message = [message[i:i + 8] for i in range(0, len(message), 8)]
    # konwersja na liczbe
    message = [int(element, 2) for element in message]

    # Stworzenie bajtow z liczb
    message = bytes(message)

    # Create an image object from bytes
    img = Image.open(BytesIO(message))
    return img


def reveal_message_eoi(image, nbits=1):
    """Reveal the hidden message.

    nbits: number of least significant bits
    length: length of the message in bits.
    """

    nbits = clamp(nbits, 1, 8)
    image = np.copy(image).flatten()

    # kodowanie eoi
    jpg_eoi = bin(255)[2:].zfill(8) + bin(217)[2:].zfill(0)

    print(jpg_eoi)
    message = ""
    i = 0
    while True:
        byte = "{:08b}".format(image[i])
        message += byte[-nbits:]
        # rozpatrujemy czy znalezlismy stopke jpg'a jak tak to konczymy
        if message.endswith(jpg_eoi) or message.endswith(png_eoi):
            break
        i += 1

    mod = i % -nbits
    if mod != 0:
        message = message[:mod]
    return message


def reveal_image_eof(image, nbits=1):
    # pobranie obrazu w postaci napizu z obrazu
    message = reveal_message_eoi(image, nbits=nbits)
    # przedstawienie danych w postaci tablicy bajtow w postaci bitow
    message = [message[i:i + 8] for i in range(0, len(message), 8)]
    # konwersja na liczbe
    message = [int(element, 2) for element in message]
    # Stworzenie bajtow z liczb
    message = bytes(message)
    # Create an image object from bytes
    img = Image.open(BytesIO(message))
    return img
