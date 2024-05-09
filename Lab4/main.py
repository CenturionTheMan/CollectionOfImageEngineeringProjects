import math

import ex_methods as ex
import custom_helpers as custom
import os
import cv2
import matplotlib.pyplot as plt
import numpy as np


def user_load_image(text="Podaj ścieżkę do obrazu: "):
    path = input(text)
    while not os.path.isfile(path):
        if path == 'm':
            return None
        print(f"Obraz o ścieżce: {path} nie istnieje!")
        print(f"[m] - Powrót do menu")
        path = input(text)
    return ex.load_image(path)


def user_save_image(image, text="Podaj ścieżke do zapisania obrazu (z rozszerzeniem): "):
    image_path = input(text)
    while image_path != 'm':
        try:
            ex.save_image(image_path, image)
            return
        except:
            print("Błędna ścieżka! Nie zapisano zdjęcia...")
            print(f"[m] - Nie zapisuj obrazu")
        image_path = input(text)


def user_get_int(text):
    tmp = input(text)
    while tmp != 'm':
        try:
            tmp_int = int(tmp)
            if tmp_int >= 0:
                return tmp_int
        except ValueError:
            print(f"Wartość musi być liczbą naturalną! Została podana: {tmp}")
            print(f"[m] - Powrót do menu")
        tmp = input(text)
    return None


def zad1(): # sth do not work
    print("Zadanie 1")
    print("[0] - Zakoduj wiadomość")
    print("[1] - Odczytaj wiadomość")
    choice = input("Wybierz opcje: ")
    if choice == '0':
        image = user_load_image()
        if image is None:
            return
        message = input("Podaj tekst do ukrycia: ")
        nbits = user_get_int("Podaj liczbe najmłodszych bitów do użycia do zakodowania obrazka (liczba naturalna): ")
        if nbits is None:
            return

        binary = ex.encode_as_binary_array(message)
        try:
            new_image = ex.hide_message(image, binary, nbits=nbits)
        except ValueError:
            return
        if new_image is not None:
            print(f"Wiadomość zakodowana pomyślnie. Długość: {len(binary)}")
            user_save_image(new_image)
            custom.plot(new_image, "Obraz z zakodowaną wiadomością", 1, 1, 1)
            plt.show()
        else:
            print("Nie udało się zakodować wiadomości, ponieważ jest za długa")
    elif choice == '1':
        image = user_load_image()
        if image is None:
            return
        lengh = user_get_int("Podaj długość wiadomości do odkodowania: ")
        if lengh is None:
            return
        nbits = user_get_int("Podaj liczbe najmłodszych bitów do użycia do zakodowania obrazka (liczba naturalna): ")
        if nbits is None:
            return

        retrieved_binary = ex.reveal_message(image, nbits, lengh)
        decoded_bin = ex.decode_from_binary_array(retrieved_binary)
        print(f"Wiadomość po odkodowaniu z obrazu:\n{decoded_bin}")
    else:
        print(f"Nie rozpoznano opcji: {choice}")


def zad2():
    print("Zadanie 2")
    image = user_load_image()
    if image is None:
        return

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
    print("Zadanie 3")
    print("[0] - Zakoduj wiadomość")
    print("[1] - Odczytaj wiadomość")
    choice = input("Wybierz opcje: ")
    if choice == '0':
        image = user_load_image()
        if image is None:
            return
        start_pos = user_get_int("Podaj pozycję od której ma być kodowana wiadomość (liczba naturalna): ")
        if start_pos is None:
            return
        message = input("Podaj tekst do ukrycia: ")
        nbits = user_get_int("Podaj liczbe najmłodszych bitów do użycia do zakodowania obrazka (liczba naturalna): ")
        if nbits is None:
            return

        binary = ex.encode_as_binary_array(message)
        try:
            new_image = ex.hide_message(image, binary, nbits=nbits, spos=start_pos)
        except ValueError:
            return
        if new_image is not None:
            print(f"Wiadomość zakodowana pomyślnie. Długość: {len(binary)}")
            user_save_image(new_image)
            custom.plot(new_image, "Obraz z zakodowaną wiadomością", 1, 1, 1)
            plt.show()
        else:
            print("Nie udało się zakodować wiadomości, ponieważ jest za długa")
    elif choice == '1':
        image = user_load_image()
        if image is None:
            return
        start_pos = user_get_int("Podaj pozycję od której ma być dekodowana wiadomość (liczba naturalna): ")
        if start_pos is None:
            return
        lengh = user_get_int("Podaj długość wiadomości do odkodowania: ")
        if lengh is None:
            return
        lengh = len(ex.encode_as_binary_array("X" * lengh))
        nbits = user_get_int("Podaj liczbe najmłodszych bitów użytą do zakodowania obrazka (liczba naturalna): ")
        if nbits is None:
            return

        retrieved_binary = ex.reveal_message(image, nbits=nbits, length=lengh, spos=start_pos)
        decoded_bin = ex.decode_from_binary_array(retrieved_binary)
        print(f"Wiadomość po odkodowaniu z obrazu:\n{decoded_bin}")
    else:
        print(f"Nie rozpoznano opcji: {choice}")


def zad4():
    print("Zadanie 4")
    print("[0] - Zakoduj obraz")
    print("[1] - Odczytaj obraz")
    choice = input("Wybierz opcje: ")

    if choice == '0':
        image = user_load_image("Podaj scieżkę do głównego obrazu: ")
        if image is None:
            return

        to_hide_image_path = input('Podaj sciezkę do pliku, który ma zostać ukryty: ')
        while not os.path.isfile(to_hide_image_path):
            print(f'Nie znaleziono pliku {to_hide_image_path}!')
            to_hide_image_path = input('Podaj sciezkę do pliku, który ma zostać ukryty: ')
        print(f"Znaleziono plik {to_hide_image_path}")

        nbits = user_get_int("Podaj liczbe najmłodszych bitów do użycia do zakodowania obrazka (liczba naturalna): ")
        if nbits is None:
            return

        try:
            coded_image, hidden_image_len = ex.hide_image(image, to_hide_image_path, nbits)
        except ValueError:
            return
        print(f"Zakodowano obraz. Jego długość to: {hidden_image_len}")
        user_save_image(coded_image)
        custom.plot(coded_image, "Oryginalny obraz\nz zakodowanym ukrytym obrazem", 1, 1, 1)

    elif choice == '1':
        img = user_load_image("Podaj ścieżkę do obrazu z ukrytym obrazem")
        if img is None:
            return
        nbits = user_get_int("Podaj liczbe najmłodszych bitów użytą do zakodowania obrazka (liczba naturalna): ")
        hidden_image_len = user_get_int("Podaj liczbę bajtów zakodowanego obrazu: ")

        secret_image = ex.reveal_image(img, hidden_image_len, nbits)
        custom.plot(img, "Oryginalny obraz\nz zakodowanym ukrytym obrazem", 1, 2, 1)
        custom.plot(secret_image, "Ukryty obraz po odkodowaniu", 1, 2, 2)
        plt.show()


def zad5():
    print("Zadanie 5")
    image = user_load_image("Podaj scieżkę do obrazu z ukrytym obrazem (jpg): ")
    if image is None:
        return
    nbits = user_get_int("Podaj liczbe najmłodszych bitów użytą do zakodowania obrazka (liczba naturalna): ")
    if nbits is None:
        return

    secret_image = ex.reveal_image_eof(image, nbits)

    custom.plot(image, "Oryginalny obraz\nz zakodowanym ukrytym obrazem", 1, 2, 1)
    custom.plot(secret_image, "Ukryty obraz po odkodowaniu", 1, 2, 2)
    plt.show()


if __name__ == '__main__':
    user_input = ''
    while True:
        print('[0] - Wyjscie')
        print('[1] - Zadanie 1')
        print('[2] - Zadanie 2')
        print('[3] - Zadanie 3')
        print('[4] - Zadanie 4')
        print('[5] - Zadanie 5')
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
        else:
            print('Nie rozpoznano opcji')
        print('\n')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
