import math
import ex_methods as ex
import os
import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

# ================================================ EX 1
def find_closest_palette_color_for_grey(image):
    return np.round(image/255)*255

def do_dithering(image_to_change):
    image = image_to_change.copy()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            old_pixel = image[y][x]
            new_pixel = find_closest_palette_color_for_grey(old_pixel)
            image[y][x] = new_pixel
            quant_error = old_pixel - new_pixel
            if x+ 1 < image.shape[1]:
                image[y    ][x + 1] = image[y    ][x + 1] + quant_error * 7/16
            if y+ 1 < image.shape[0] and x-1 > 0 :
                image[y + 1][x - 1] = image[y + 1][x - 1] + quant_error * 3/16
            if y+ 1 < image.shape[0]:
                image[y + 1][x    ] = image[y + 1 ][x ] + quant_error * 5/16
            if x+ 1 < image.shape[1] and  y + 1 < image.shape[0]:
                image[y + 1][x + 1] = image[y + 1][x + 1] + quant_error * 1/16

    np.clip(image, 0, 255)
    #formatujemy do uint8
    image = image.astype(dtype=np.uint8)
    return image

def ex1(image):    
    original_image_rgb = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    original_image = image.copy()
    reduced_image = find_closest_palette_color_for_grey(original_image.copy())
    dithered_image = do_dithering(original_image.copy())
    
    ex.plot(original_image_rgb, 'Oryginał', 2, 2, 1)
    ex.plot(original_image, 'Oryginał (czerń-biel)', 2, 2, 2)
    ex.plot(reduced_image, 'Zredukowana paleta barw', 2, 2, 3)
    ex.plot(dithered_image, 'Dithering', 2, 2, 4)
    plt.show()

# ================================================ EX 2
def find_closest_palette_color_rgb(img, k):
    to_return = np.round(   (k - 1)*img/ 255 ) * 255 / (k-1) 
    return to_return


def do_dithering_rgb(image, k):
    reduced = image.copy()
    for y in range(image.shape[0]-1):
        for x in range(image.shape[1]-1):
            oldpixel = [image[y][x][0], image[y][x][1], image[y][x][2]]
            newpixel = [0, 0, 0]
            newpixel[0] = find_closest_palette_color_rgb(oldpixel[0], k) 
            newpixel[1] = find_closest_palette_color_rgb(oldpixel[1], k) 
            newpixel[2] = find_closest_palette_color_rgb(oldpixel[2], k) 
            reduced[y][x][0] = find_closest_palette_color_rgb(reduced[y][x][0], k)
            reduced[y][x][1] = find_closest_palette_color_rgb(reduced[y][x][1], k)
            reduced[y][x][2] = find_closest_palette_color_rgb(reduced[y][x][2], k)
            image[y][x] = newpixel
            for i in range(3):
                quant_error = oldpixel[i] - newpixel[i]
                image[y][x + 1][i] = image[y][x + 1][i] + quant_error * 7 / 16
                image[y + 1][x - 1][i] = image[y + 1][x - 1][i] + quant_error * 3 / 16
                image[y + 1][x][i] = image[y + 1][x][i] + quant_error * 5 / 16
                image[y + 1][x + 1][i] = image[y + 1][x + 1][i] + quant_error * 1 / 16
    np.clip(image, 0, 255)
    image = image.astype(dtype=np.uint8)
    return image

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

def ex2(image):
    k = None
    while k is None:
        k = user_get_int('Podaj liczbę kolorów (k): ')
        
    print(f'Wybrano k: {k}. Ładuje zadanie ...')

    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    original_image = image.copy()
    reduced_image = find_closest_palette_color_rgb(original_image.copy(), k)
    dithered_image = do_dithering_rgb(image.copy(), k)
    ex.plot(original_image, 'Oryginał', 2, 2, 1)
    ex.plot(reduced_image, f'Zredukowana paleta barw (k: {k})', 2, 2, 3)
    ex.plot(dithered_image, f'Dithering (k: {k})', 2, 2, 4)
    plt.show()
    
    color = ('r', 'g', 'b')
    for i, col in enumerate(color):
        histr = cv.calcHist([dithered_image], [i], None, [256], [0, 256])
        plt.plot(histr, color=col)
        plt.xlim([-1, 256])
        plt.xlabel('Wartośc składowej koloru')
        plt.ylabel('Liczba pikseli obrazu')
        plt.legend(['Red', 'Green', 'Blue'])
        plt.title(f'Histogram składowych kolorów obrazu (k: {k})')
    plt.show()
    
# ================================================ EX 3
def draw_point(image, x, y, color=(255, 255, 255)):
    image[image.shape[0] - 1 - y, x] = color

def get_area(a, b, c):
    return (c[0] - a[0] ) * (b[1] - a[1]) - (c[1] - a[1]) *  (b[0] - a[0]) 

def draw_point(image, x, y, color=(255, 255, 255)):
    image[image.shape[0] - 1 - y, x] = color

def get_area(a, b, c):
    return (c[0] - a[0] ) * (b[1] - a[1]) - (c[1] - a[1]) *  (b[0] - a[0]) 

def draw_line(image, x1, y1, x2, y2, col1 = (0, 0, 0), col2 = (255, 255, 255)):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    col1 = np.asarray(col1)
    col2 = np.asarray(col2)
    Xi = 0 if dx == 0 else (x2-x1)/dx 
    Yi = 0 if dy == 0 else (y2-y1)/dy 
    d = 0 
    if dx > dy:
        d = 2 * dy - dx
        diff = (col2 - col1) // dx
    else:
        d = 2 * dx - dy
        diff = (col2 - col1) // dy
    x0, y0 = x1, y1
    C = col1
    draw_point(image, x0, y0, col1)

    while x0 != x2 or y0 != y2:
        C = np.clip(C+diff, 0, 255)
        if dx > dy:
            x0+=Xi
            d+= 2* dy
            if d >= 0:
                y0+=Yi
                d -= 2 * dx
        else :
            y0+=Yi
            d+= 2*dx
            if d>=0:
                x0+=Xi
                d-= 2* dy        
        draw_point(image, int(x0), int(y0), C )

def draw_triangle(image, a, b, c, col1 = [255, 0, 0], col2 = [0, 255, 0], col3 = [0, 0, 255]):
    sign = lambda x: 0 if x == 0 else math.copysign(1, x)

    col1= np.asarray(col1)
    col2= np.asarray(col2)
    col3= np.asarray(col3)

    x_min = min(a[0], b[0], c[0])
    y_min = min(a[1], b[1], c[1])

    x_max = max(a[0], b[0], c[0])
    y_max = max(a[1], b[1], c[1])
    

    for x in range(x_min, x_max):
        for y in range(y_min, y_max):
            point = (x, y)

            p1 = get_area(a, b, point)
            p2 = get_area(b, c, point)
            p3 = get_area(c, a, point)
            l = get_area(a, b, c)
            Cp = p1/l * col1 + p2/l * col2 + p3/l * col3

            if sign(p1) == sign(p2) and sign(p2) == sign(p3) and sign(p1) == sign(p3) :
                draw_point(image, x, y, Cp)

def ex3(width, height):
    image = np.zeros((height, width, 3), np.uint8)
    
    draw_line(image, 3, 3, 10, 30, (255,255,255), (255,255,255))
    draw_triangle(image, (15, 15), (30, 45), (45, 20), [0, 255, 0], [0, 255, 0], [0, 255, 0])
    ex.plot(image, 'IMG', 1, 1, 1)
    plt.show()

# ================================================ EX 4
def ex4(width, height):
    image = np.zeros((height, width, 3), np.uint8)
    
    draw_line(image, 3, 3, 10, 30)
    draw_triangle(image, (15, 15), (30, 45), (45, 20))
    ex.plot(image, 'IMG', 1, 1, 1)
    plt.show()

# ================================================ EX 5
def ex5(width, height, scale):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image_scaled = np.zeros((height*scale, width*scale, 3), dtype=np.uint8)

    draw_line(image_scaled, 4*scale, 20*scale, 30*scale, 90*scale)
    draw_triangle(image_scaled, (10*scale, 10*scale), (45*scale, 80*scale), (160*scale, 50*scale) )

    for y in range(height):
        for x in range(width):
            sx = x * scale
            sy = y * scale
            
            scolor = [0, 0, 0]
            for i in range(scale):
                for j in range(scale):
                    scolor[0] += image_scaled[sy +i, sx+ j, 0]
                    scolor[1] += image_scaled[sy +i, sx+ j, 1]
                    scolor[2] += image_scaled[sy +i, sx+ j, 2]
            scolor[0] /= scale**2
            scolor[1] /= scale**2
            scolor[2] /= scale**2
            image[y, x] = scolor 

    ex.plot(image_scaled, 'IMG Large', 1, 2, 1)
    ex.plot(image, 'IMG SSAA', 1, 2, 2)
    plt.show()

# ================================================ MAIN
path = './img2.jpg'
while not os.path.isfile(path):
    print(f'Nie znaleziono pliku {path}!')
    path = input('Wskaz sciezke do pliku (obrazu): ')
image_global = cv.imread(path, cv.IMREAD_UNCHANGED)

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
        ex1(image_global)
    elif user_input == '2':
        print('Ładuje zadanie ...')
        ex2(image_global)
    elif user_input == '3':
        print('Ładuje zadanie ...')
        ex3(50, 50)
    elif user_input == '4':
        print('Ładuje zadanie ...')
        ex4(50, 50)
    elif user_input == '5':
        print('Ładuje zadanie ...')
        ex5(200, 100, 4)

    elif user_input == '6':
        tmp_path = input('Podaj sciezke: ')
        if os.path.isfile(tmp_path):
            path = tmp_path
            image_global = cv.imread(path, cv.IMREAD_UNCHANGED)
        else:
            print('Plik nie istnieje!')
    else:
        print('Nie rozpoznano opcji')
    print('\n')
