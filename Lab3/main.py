import os.path

import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv2
import helpers as help


image = None


def exercise1():
    global image
    image_data = np.copy(image)
    width = image_data.shape[1]
    height = image_data.shape[0]
    xxxx = image_data.shape[2]

    # 1. Convert RGB to YCbCr
    image_data = cv2.cvtColor(image_data, cv2.COLOR_RGB2YCrCb)

    # 2. Downsampling on Cb and Cr channels
    CR_0, CB_0, Y = help.downsample(image_data, sample_rate=1)
    CR_2, CB_2, Y = help.downsample(image_data, sample_rate=2)
    CR_4, CB_4, Y = help.downsample(image_data, sample_rate=4)

    # 3. Produce 8x8 blocks
    #blocks = (width * height) // 64
    y_blocks = help.get_8x8_blocks_from_list(Y)

    CR_0_blocks, CB_0_blocks = help.get_8x8_blocks_from_list(CR_0), help.get_8x8_blocks_from_list(CB_0)
    CR_2_blocks, CB_2_blocks = help.get_8x8_blocks_from_list(CR_2), help.get_8x8_blocks_from_list(CB_2)
    CR_4_blocks, CB_4_blocks = help.get_8x8_blocks_from_list(CR_4), help.get_8x8_blocks_from_list(CB_4)

    # 4. Calculate DCT on each block
    y_blocks = [help.dct2(x) for x in y_blocks]
    CR_2_blocks, CB_2_blocks = [help.dct2(x) for x in CR_2_blocks], [help.dct2(x) for x in CB_2_blocks]

    # 5. Divide each block by quantisation matrix
    y_blocks = [np.round(block / help.QY()) for block in y_blocks]
    CR_2_blocks, CB_2_blocks = [np.round(block / help.QC()) for block in CR_2_blocks], [np.round(block / help.QC()) for block in CB_2_blocks]

    # 6. Round values in each block to integers
    y_blocks = np.array(y_blocks, dtype=int)
    CR_2_blocks, CB_2_blocks = np.array(CR_2_blocks, dtype=int), np.array(CB_2_blocks, dtype=int)


    # 7. Zig-zag
    Y_zig_zag_blocks = np.asarray([help.zig_zag(y_blocks[x]) for x in range(len(y_blocks))])

    CR_0_zig_zag_blocks = np.asarray([help.zig_zag(CR_0_blocks[x]) for x in range(len(CR_0_blocks))])
    CB_0_zig_zag_blocks = np.asarray([help.zig_zag(CB_0_blocks[x]) for x in range(len(CB_0_blocks))])

    CR_2_zig_zag_blocks = np.asarray([help.zig_zag(CR_2_blocks[x]) for x in range(len(CR_2_blocks))])
    CB_2_zig_zag_blocks = np.asarray([help.zig_zag(CB_2_blocks[x]) for x in range(len(CB_2_blocks))])

    CR_4_zig_zag_blocks = np.asarray([help.zig_zag(CR_4_blocks[x]) for x in range(len(CR_4_blocks))])
    CB_4_zig_zag_blocks = np.asarray([help.zig_zag(CB_4_blocks[x]) for x in range(len(CB_4_blocks))])

    # 8. Flatten, concatenate, compress and calculate the size -- how many bytes?
    compress_0 = help.compress(Y_zig_zag_blocks, CR_0_zig_zag_blocks, CB_0_zig_zag_blocks)
    compress_2 = help.compress(Y_zig_zag_blocks, CR_2_zig_zag_blocks, CB_2_zig_zag_blocks)
    compress_4 = help.compress(Y_zig_zag_blocks, CR_4_zig_zag_blocks, CB_4_zig_zag_blocks)

    #with open('image_zad4_rate1.jpg', 'wb') as fh:
    #    fh.write(compress_0)
    #with open('image_zad4_rate2.jpg', 'wb') as fh:
    #    fh.write(compress_2)
    #with open('image_zad4_rate4.jpg', 'wb') as fh:
    #    fh.write(compress_4)

    print(f"Dlugosc bez probkowania: {round(len(str(compress_0)) / 1024, 2)} KB")
    print(f"Dlugosc z probkowaniem co 2. element: {round(len(str(compress_2)) / 1024, 2)} KB")
    print(f"Dlugosc z probkowaniem co 4. element: {round(len(str(compress_4)) / 1024, 2)} KB")

    # 5'. Reverse division by quantisation matrix -- multiply
    y_blocks = [np.round(block * help.QY()) for block in y_blocks]
    CR_2_blocks, CB_2_blocks = [np.round(block * help.QC()) for block in CR_2_blocks], [np.round(block * help.QC()) for block in CB_2_blocks]

    # 4'. Reverse DCT and round
    y_blocks = [help.idct2(x) for x in y_blocks]
    CR_2_blocks, CB_2_blocks = [help.idct2(x) for x in CR_2_blocks], [help.idct2(x) for x in CB_2_blocks]

    # 3'. Combine 8x8 blocks to original image
    Y = help.reconstruct_image_from_blocks(y_blocks, height, width)
    CR_0 = help.reconstruct_image_from_blocks(CR_0_blocks, CR_0.shape[0], CR_0.shape[1])
    CB_0 = help.reconstruct_image_from_blocks(CB_0_blocks, CB_0.shape[0], CB_0.shape[1])
    CR_2 = help.reconstruct_image_from_blocks(CR_2_blocks, CR_2.shape[0], CR_2.shape[1])
    CB_2 = help.reconstruct_image_from_blocks(CB_2_blocks, CB_2.shape[0], CB_2.shape[1])
    CR_4 = help.reconstruct_image_from_blocks(CR_4_blocks, CR_4.shape[0], CR_4.shape[1])
    CB_4 = help.reconstruct_image_from_blocks(CB_4_blocks, CB_4.shape[0], CB_4.shape[1])

    # 2'. Upsampling on Cb and Cr channels
    CR_0, CB_0 = help.upsample(CR_0, 1), help.upsample(CB_0, 1)
    CR_0, CB_0 = help.adjust_size((CR_0, CB_0), Y)
    CR_2, CB_2 = help.upsample(CR_2, 2), help.upsample(CB_2, 2)
    CR_2, CB_2 = help.adjust_size((CR_2, CB_2), Y)
    CR_4, CB_4 = help.upsample(CR_4, 4), help.upsample(CB_4, 4)
    CR_4, CB_4 = help.adjust_size((CR_4, CB_4), Y)

    # 1'. Convert YCbCr to RGB
    image_0 = cv2.cvtColor(np.stack((Y.astype(np.uint8), CR_0.astype(np.uint8), CB_0.astype(np.uint8)), axis=-1), cv2.COLOR_YCrCb2RGB)
    image_2 = cv2.cvtColor(np.stack((Y.astype(np.uint8), CR_2.astype(np.uint8), CB_2.astype(np.uint8)), axis=-1), cv2.COLOR_YCrCb2RGB)
    image_4 = cv2.cvtColor(np.stack((Y.astype(np.uint8), CR_4.astype(np.uint8), CB_4.astype(np.uint8)), axis=-1), cv2.COLOR_YCrCb2RGB)

    help.plot(image, "Oryginalny obraz (png)", 2, 2, 1)
    help.plot(image_0, "Obraz bez próbkowania, \npo kompresi i dekompresji", 2, 2, 2)
    help.plot(image_2, "Obraz z próbkowaniem co 2. element, \npo kompresi i dekompresji", 2, 2, 3)
    help.plot(image_4, "Obraz z próbkowaniem co 4. element, \npo kompresi i dekompresji", 2, 2, 4)
    plt.show()

# zad 1
def exercise2():
    pass


if __name__ == '__main__':
    path = './png_file.png'
    while not os.path.isfile(path):
        print(f'Nie znaleziono pliku {path}!')
        path = input('Wskaz sciezke do pliku: ')
    image = cv2.imread(path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    exercise1()
    input()
    user_input = ''
    while True:
        print('[0] - Wyjscie')
        print('[1] - Zajęcia 2 > Zadanie 4')
        print('[2] - Zajęcia 2 > Zadanie 5')
        print(f'[3] - Wybierz sciezke do zdjecia (wybrane zdjecie: {path})')
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
            path = input('Podaj sciezke: ')
            if os.path.isfile(path):
                image = cv2.imread(path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                print('Plik nie istnieje!')
        else:
            print('Nie rozpoznano opcji')
        print('\n')
