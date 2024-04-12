import os.path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from scipy import ndimage
import cv2 as cv
from helpers import *
import struct
import zlib

image = None


# 1, 2 - zalegle
def exercise1():
    global image

    sampling_const = 2

    plot(image, 'Bazowy obraz', 2, 3, 1)
    Y, Cb, Cr = RGBtoYCbCr(image)

    imageYCbCrToRGB = YCbCrToRGB(Y, Cb, Cr)

    Cb_down = Cb[::sampling_const, ::sampling_const]
    Cr_down = Cr[::sampling_const, ::sampling_const]

    Cb_up = np.repeat(Cb_down, sampling_const, axis=0)
    Cb_up = np.repeat(Cb_up, sampling_const, axis=1)

    Cr_up = np.repeat(Cr_down, sampling_const, axis=0)
    Cr_up = np.repeat(Cr_up, sampling_const, axis=1)

    image_post_send_rgb = YCbCrToRGB(Y, Cb_up, Cr_up)

    plot(image_post_send_rgb, 'YCbCR -> RGB (po wysłaniu)', 2, 3, 2)

    plot(Y, 'Składowa Y', 2, 3, 3)
    plot(Cb_up, 'Składowa Cb (po wysłaniu)', 2, 3, 4)
    plot(Cr_up, 'Składowa Cr (po wysłaniu)', 2, 3, 5)

    mse_RGB_YCbCr = np.mean((np.array(image, dtype=int) - np.array(imageYCbCrToRGB, dtype=int)) ** 2)
    mse_post_send = np.mean((np.array(image, dtype=int) - np.array(image_post_send_rgb, dtype=int)) ** 2)


    print(f"Błąd średniokwadratowy pomiędzy oryginalnym obrazem a obrazem po konwersji YCbRc -> RGB: "
          f"{round(mse_RGB_YCbCr, 2)}")
    print(f"Błąd średniokwadratowy pomiędzy oryginalnym a przesłanym obrazem:                        "
          f"{round(mse_post_send, 2)}")
    plt.show()


def ppm(img, p3path, p6path):
    # P3
    if p3path is not None:
        text_p3 = f"P3\n" \
                  f"{img.shape[1]} {img.shape[0]}\n" \
                  f"255\n"
        for rgb in img.reshape(-1, 3):
            text_p3 += f"{rgb[0]} {rgb[1]} {rgb[2]}\n"
        f = open(p3path, "w")
        f.write(text_p3)
        f.close()

    if p6path is not None:
        f = open(p6path, "wb")
        f.write(bytearray(f'P6\n'
                          f'{img.shape[1]} {img.shape[0]}\n'
                          f'255\n', 'ascii'))
        f.write(img.flatten().tobytes())
        f.close()


# zad 1
def exercise2():
    img = np.array([[[255, 0, 0], [0, 0, 255], [0, 255, 0]],
                    [[255, 255, 0], [0, 255, 0], [0, 0, 255]],
                    [[0, 0, 255], [255, 0, 255], [255, 0, 0]]], dtype=np.uint8)

    ppm(img, "./P3_szkic.ppm", "./P6_szkic.ppm")
    ppm(image, "./P3_obraz.ppm", "./P6_obraz.ppm")
    print("Zapisano obrazy...")

    plot(img, 'Oryginalny szkic', 2, 3, 4)
    plot(cv.cvtColor(cv.imread("./P3_szkic.ppm"), cv.COLOR_BGR2RGB), 'Plik P3 - szkic', 2, 3, 5)
    plot(cv.cvtColor(cv.imread("./P6_szkic.ppm"), cv.COLOR_BGR2RGB), 'Plik P6 - szkic', 2, 3, 6)

    plot(image, 'Oryginalny obraz', 2, 3, 1)
    plot(cv.cvtColor(cv.imread("./P3_obraz.ppm"), cv.COLOR_BGR2RGB), 'Plik P3 - obraz', 2, 3, 2)
    plot(cv.cvtColor(cv.imread("./P6_obraz.ppm"), cv.COLOR_BGR2RGB), 'Plik P6 - obraz', 2, 3, 3)

    print(f"Rozmiar pliku P3_szkic: {os.path.getsize('./P3_szkic.ppm')} B")
    print(f"Rozmiar pliku P6_szkic: {os.path.getsize('./P6_szkic.ppm')} B")

    print(f"Rozmiar pliku P3_obraz: {round((os.path.getsize('./P3_obraz.ppm') / 1024.0/ 1024.0),2)} MB")
    print(f"Rozmiar pliku P6_obraz: {round((os.path.getsize('./P6_obraz.ppm') /1024.0/1024.0),2)} MB")

    plt.show()


def create_spectrum(width):
    spectrum = []
    line = []
    pixel = np.array([0, 0, 0])

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, 0, 1]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, 1, 0]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, 0, -1]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [1, 0, 0]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, -1, 0]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, 0, 1]

    for x in range(255):
        line.append(pixel.copy())
        pixel += [0, 1, 0]

    for x in range(width):
        spectrum.append(line)
    return np.array(spectrum, dtype=np.uint8)


def exercise3():
    print("Tworzę spektra barw...")
    width = 1000
    spectrum = create_spectrum(width)

    spectrum2 = []
    line2 = []
    pixel2 = np.array([0, 0, 0], dtype=float)

    for x in range(255 * 7):
        line2.append(np.round(pixel2.copy() * 255.0, 0))
        pixel2 += 1/(255 * 7)

    for x in range(width):
        spectrum2.append(line2)
    spectrum2 = np.array(spectrum2, dtype=np.uint8)

    print("Zapisuję do plików ppm...")
    ppm(np.array(spectrum, dtype=np.uint8), 'spectrum1P3.ppm', None)
    ppm(np.array(spectrum2, dtype=np.uint8), 'spectrum2P3.ppm', None)

    print("Odczytuję z plików...")
    plot(cv.cvtColor(cv.imread("spectrum1P3.ppm"), cv.COLOR_BGR2RGB), '(plik P3) spektrum', 2, 1, 1)
    plot(cv.cvtColor(cv.imread("spectrum2P3.ppm"), cv.COLOR_BGR2RGB), '(plik P3) spektrum 1-8', 2, 1, 2)

    plt.show()


def exercise4():
    #
    # Image data
    #
    img = create_spectrum(1000)

    #
    # Construct signature
    #
    png_file_signature = b'\x89PNG\x0D\x0A\x1A\x0A'

    #
    # Construct header
    #
    header_id = b'IHDR'
    #                 |  wysokosc     |   szerokosc|bpp|RGB|DEF|filter|Interlance
    header_content = b'\x00\x00\x06\xf9\x00\x00\x03\xe8\x08\x02\x00\x00\x00'
    header_size = struct.pack('!I', len(header_content))
    header_crc = struct.pack('!I', zlib.crc32(header_id + header_content))
    png_file_header = header_size + header_id + header_content + header_crc

    #
    # Construct data
    #
    data_id = b'IDAT'  # TODO: implement
    data_content = zlib.compress(b''.join([b'\x00' + bytes(row) for row in img]))
    data_size = struct.pack('!I', len(data_content))  # TODO: implement
    data_crc = struct.pack('!I', zlib.crc32(data_id + data_content))
    png_file_data = data_size + data_id + data_content + data_crc

    #
    # Consruct end
    #
    end_id = b'IEND'
    end_content = b''
    end_size = struct.pack('!I', len(end_content))
    end_crc = struct.pack('!I', zlib.crc32(end_id + end_content))
    png_file_end = end_size + end_id + end_content + end_crc

    #
    # Save the PNG image as a binary file
    #
    with open('png_file.png', 'wb') as fh:
        fh.write(png_file_signature)
        fh.write(png_file_header)
        fh.write(png_file_data)
        fh.write(png_file_end)

    print("Zapisano obraz pod nazwą: png_file.png")
    plot(cv.cvtColor(cv.imread('png_file.png'), cv.COLOR_BGR2RGB), 'obraz PNG', 1, 1, 1)
    plt.show()


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
        print('[1] - Zadanie 1 i 2 (4 i 5 z poprzednich zajęć)')
        print('[2] - Zadanie 1 (aktualne)')
        print('[3] - Zadanie 2 (aktualne)')
        print('[4] - Zadanie 3 (aktualne)')
        print('[5] - Wybierz sciezke do zdjecia (bazowo zdjecie: image3.jpg)')
        user_input = input('Wybierz opcje: ')
        user_input = user_input.replace(' ', '').replace('\n', ' ')
        if user_input == '0':
            break
        elif user_input == '1':
            print('Ładuje zadanie ...')
            exercise1()
        elif user_input == '2':
            print('Ładuje zadanie ...')
            exercise2()
        elif user_input == '3':
            print('Ładuje zadanie ...')
            exercise3()
        elif user_input == '4':
            print('Ładuje zadanie ...')
            exercise4()
        elif user_input == '5':
            path = input('Podaj sciezke: ')
            if os.path.isfile(path):
                image = cv.imread(path)
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
            else:
                print('Plik nie istnieje!')
        else:
            print('Nie rozpoznano opcji')
        print('\n')
