import os.path

import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import helpers as help


image = None


def worker(sample_rate, size_console_text, qf):
    global image
    image_data = np.copy(image)
    width = image_data.shape[1]
    height = image_data.shape[0]

    # 1. Convert RGB to YCbCr
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2YCrCb)

    # 2. Downsampling on Cb and Cr channels
    CR_2, CB_2, Y = help.downsample(image_data, sample_rate=sample_rate)

    # 3. Produce 8x8 blocks
    # blocks = (width * height) // 64
    y_blocks = help.get_8x8_blocks_from_list(Y)

    CR_2_blocks, CB_2_blocks = help.get_8x8_blocks_from_list(CR_2), help.get_8x8_blocks_from_list(CB_2)

    # 4. Calculate DCT on each block
    y_blocks = [help.dct2(x) for x in y_blocks]
    CR_2_blocks, CB_2_blocks = [help.dct2(x) for x in CR_2_blocks], [help.dct2(x) for x in CB_2_blocks]

    # 5. Divide each block by quantisation matrix
    y_blocks = [np.round(block / help.QY(qf)) for block in y_blocks]
    CR_2_blocks, CB_2_blocks = [np.round(block / help.QC(qf)) for block in CR_2_blocks], [np.round(block / help.QC(qf)) for
                                                                                        block in CB_2_blocks]

    # 6. Round values in each block to integers
    y_blocks = np.array(y_blocks, dtype=int)
    CR_2_blocks, CB_2_blocks = np.array(CR_2_blocks, dtype=int), np.array(CB_2_blocks, dtype=int)

    # 7. Zig-zag
    Y_zig_zag_blocks = np.asarray([help.zig_zag(y_blocks[x]) for x in range(len(y_blocks))])

    CR_2_zig_zag_blocks = np.asarray([help.zig_zag(CR_2_blocks[x]) for x in range(len(CR_2_blocks))])
    CB_2_zig_zag_blocks = np.asarray([help.zig_zag(CB_2_blocks[x]) for x in range(len(CB_2_blocks))])

    # 8. Flatten, concatenate, compress and calculate the size -- how many bytes?
    compress_2 = help.compress(Y_zig_zag_blocks, CR_2_zig_zag_blocks, CB_2_zig_zag_blocks)

    print(f"{size_console_text}: {round(len(str(compress_2)) / 1024, 2)} KB")

    # 5'. Reverse division by quantisation matrix -- multiply
    y_blocks = [np.round(block * help.QY(qf)) for block in y_blocks]
    CR_2_blocks, CB_2_blocks = [np.round(block * help.QC(qf)) for block in CR_2_blocks], [np.round(block * help.QC(qf)) for
                                                                                        block in CB_2_blocks]

    # 4'. Reverse DCT and round
    y_blocks = [help.idct2(x) for x in y_blocks]
    CR_2_blocks, CB_2_blocks = [help.idct2(x) for x in CR_2_blocks], [help.idct2(x) for x in CB_2_blocks]

    # 3'. Combine 8x8 blocks to original image
    Y = help.reconstruct_image_from_blocks(y_blocks, height, width)
    CR_2 = help.reconstruct_image_from_blocks(CR_2_blocks, CR_2.shape[0], CR_2.shape[1])
    CB_2 = help.reconstruct_image_from_blocks(CB_2_blocks, CB_2.shape[0], CB_2.shape[1])

    # 2'. Upsampling on Cb and Cr channels
    CR_2, CB_2 = help.upsample(CR_2, sample_rate), help.upsample(CB_2, sample_rate)
    CR_2, CB_2 = help.adjust_size((CR_2, CB_2), Y)

    # 1'. Convert YCbCr to RGB
    image_2 = cv2.cvtColor(np.stack((Y.astype(np.uint8), CR_2.astype(np.uint8), CB_2.astype(np.uint8)), axis=-1),
                           cv2.COLOR_YCrCb2RGB)
    return image_2


def exercise1():
    image_0 = worker(1, "Rozmiar dla: bez próbkowania, QF=85",85)
    image_1 = worker(2, "Rozmiar dla: próbkowanie co 2, QF=85",85)
    image_2 = worker(4, "Rozmiar dla: próbkowanie co 4, QF=85",85)
    image_3 = worker(2, "Rozmiar dla: próbkowanie co 2, QF=5",5)
    image_4 = worker(2, "Rozmiar dla: próbkowanie co 2, QF=40",40)

    help.plot(image, "Oryginalny obraz (png)", 2, 3, 1)
    help.plot(image_0, "Bez próbkowania | QF=85, \npo kompresi i dekompresji", 2, 3, 2)
    help.plot(image_1, "Z próbkowaniem co 2. element | QF=85, \npo kompresi i dekompresji", 2, 3, 3)
    help.plot(image_2, "Z próbkowaniem co 4. element | QF=85, \npo kompresi i dekompresji", 2, 3, 4)
    help.plot(image_3, "Z próbkowaniem co 2. element | QF=5, \npo kompresi i dekompresji", 2, 3, 5)
    help.plot(image_4, "Z próbkowaniem co 2. element | QF=40, \npo kompresi i dekompresji", 2, 3, 6)

    plt.show()


if __name__ == '__main__':
    path = './png_file.png'
    while not os.path.isfile(path):
        print(f'Nie znaleziono pliku {path}!')
        path = input('Wskaz sciezke do pliku: ')
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    user_input = ''
    while True:
        print('[0] - Wyjscie')
        print('[1] - Zajęcia 2 > Zadanie 4 i 5')
        print(f'[2] - Wybierz sciezke do zdjecia (wybrane zdjecie: {path})')
        user_input = input('Wybierz opcje: ')
        user_input = user_input.replace(' ', '').replace('\n', ' ')
        if user_input == '0':
            break
        elif user_input == '1':
            print('Ładuje zadanie ...')
            exercise1()
        elif user_input == '2':
            path = input('Podaj sciezke: ')
            if os.path.isfile(path):
                image = cv2.imread(path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                print('Plik nie istnieje!')
        else:
            print('Nie rozpoznano opcji')
        print('\n')
