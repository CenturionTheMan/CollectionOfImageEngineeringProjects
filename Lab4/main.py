import math

import ex_methods as ex
import custom_helpers as custom
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np

image = None


def zad1():
    message = input("Podaj tekst do ukrycia: ")
    binary = ex.encode_as_binary_array(message)
    new_image = ex.hide_message(image, binary)
    if new_image is not None:
        print("Wiadomość zakodowana pomyślnie")
        image_path = input("Podaj ścieżke do zapisania obrazu (z rozszerzeniem):")
        ex.save_image(image_path, new_image)
        custom.plot(new_image, "Obraz z zakodowaną wiadomością", 1, 1, 1)
        plt.show()

        retrieved_binary = ex.reveal_message(new_image, 1, len(binary))
        decoded_bin = ex.decode_from_binary_array(retrieved_binary)
        print(f"Wiadomość po odkodowaniu z obrazu:\n{decoded_bin}")


def zad2():
    message_len = math.ceil(len(np.copy(image).flatten()) * 0.095)
    message = ex.encode_as_binary_array("#" * message_len)

    images = [ex.hide_message(image, message, x, spos=0) for x in range(1, 9)]
    mses = [custom.mse(image, x, 2) for x in images]
    X = [x for x in range(1, 9)]

    for index, img in enumerate(images):
        custom.plot(img, f"Obraz dla nbits={index + 1}", 2, 4, index + 1)
    plt.show()

    custom.create_single_dot_line_plt(X, mses, x_axis_name="Wartości nbits", y_axis_name="MSE",
                                      title="Wartości MSE w zależności od nbits")

def zad3():
    message = input("Podaj wiadomość do zakodowania: ")
    start_pos = input("Podaj pozycję od której ma być kodowana wiadomość (liczba naturalna):")
    try:
        start_pos = int(start_pos)
    except:
        print("Błędna wartość pozycji startowej!")
        return
    message = ex.encode_as_binary_array(message)
    coded_img = ex.hide_message(image, message, nbits=1, spos=start_pos)
    if coded_img is not None:
        print("Wiadomość zakodowana pomyślnie")
        image_path = input("Podaj lokalną ścieżke do zapisana obrazu (z rozszerzeniem):")
        ex.save_image(image_path, coded_img)
        custom.plot(coded_img, f"Obraz z zakodowaną wiadomością od pozycji: {start_pos}", 1, 1, 1)
        plt.show()
        retrieved_binary = ex.reveal_message(coded_img, 1, len(message), spos=start_pos)
        decoded_bin = ex.decode_from_binary_array(retrieved_binary)
        print(f"Wiadomość po odkodowaniu z obrazu:\n{decoded_bin}")


def zad4():
    to_hide_image_path = input("Podaj sciezkę do pliku, który ma zostać ukryty: ")
    while not os.path.isfile(to_hide_image_path):
        print(f'Nie znaleziono pliku {to_hide_image_path}!')
        to_hide_image_path = input('Podaj sciezkę do pliku, który ma zostać ukryty: ')
    print(f"Znaleziono plik {to_hide_image_path}")

    nbits = input("Podaj liczbe najmłodszych bitów do użycia do zakodowania obrazka (liczba naturalna): ")
    try:
        nbits = int(nbits)
    except:
        print("Błędna wartość nbit!")
        return

    coded_image, hidden_image_len = ex.hide_image(image, to_hide_image_path, nbits)
    secret_image = ex.reveal_image(coded_image, hidden_image_len, nbits)

    custom.plot(coded_image, "Oryginalny obraz\nz zakodowanym ukrytym obrazem", 1, 2, 1)
    custom.plot(secret_image, "Ukryty obraz po odkodowaniu", 1, 2, 2)
    plt.show()


def zad5():
    to_hide_image_path = input("Podaj sciezkę do pliku, który ma zostać ukryty: ")
    while not os.path.isfile(to_hide_image_path):
        print(f'Nie znaleziono pliku {to_hide_image_path}!')
        to_hide_image_path = input('Podaj sciezkę do pliku, który ma zostać ukryty: ')
    print(f"Znaleziono plik {to_hide_image_path}")

    coded_image, hidden_image_len = ex.hide_image(image, to_hide_image_path, 1)
    secret_image = ex.reveal_image_eof(coded_image, hidden_image_len)

    custom.plot(coded_image, "Oryginalny obraz\nz zakodowanym ukrytym obrazem", 1, 2, 1)
    custom.plot(secret_image, "Ukryty obraz po odkodowaniu", 1, 2, 2)
    plt.show()


if __name__ == '__main__':
    path = './image3.jpg'
    while not os.path.isfile(path):
        print(f'Nie znaleziono pliku {path}!')
        path = input('Wskaz sciezke do pliku: ')
    image = ex.load_image(path)
    user_input = ''
    while True:
        print('[0] - Wyjscie')
        print('[1] - Zadanie 1')
        print('[2] - Zadanie 2')
        print('[3] - Zadanie 3')
        print('[4] - Zadanie 4')
        print('[5] - Zadanie 5')
        print(f'[6] - Wybierz sciezke do zdjecia (wybrane zdjecie: {path})')
        user_input = input('Wybierz opcje: ')
        user_input = user_input.replace(' ', '').replace('\n', ' ')
        if user_input == '0':
            break
        elif user_input == '1':
            print('Ładuje zadanie ...')
            zad1()
        elif user_input == '2':
            print('Ładuje zadanie ...')
            zad2()
        elif user_input == '3':
            print('Ładuje zadanie ...')
            zad3()
        elif user_input == '4':
            print('Ładuje zadanie ...')
            zad4()
        elif user_input == '5':
            print('Ładuje zadanie ...')
            zad5()
        elif user_input == '6':
            path = input('Podaj sciezke: ')
            if os.path.isfile(path):
                image = cv2.imread(path)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                print('Plik nie istnieje!')
        else:
            print('Nie rozpoznano opcji')
        print('\n')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
