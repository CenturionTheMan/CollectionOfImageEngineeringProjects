# Zad 1

## Teoria

### Redukcja palety barw

Redukcja palety kolorów obrazu polega na zmniejszeniu liczby unikalnych kolorów w celu uproszczenia danych
obrazu, zmniejszenia zużycia pamięci lub uzyskania określonego efektu wizualnego.
Typowo każdą składową koloru reprezentujemy jako jedną z 256 wartości, co daje 16 777 216 unikalnych odcieni. Niektóre urządzenia i formaty graficzne są ograniczone w tej kwestii, co skutkuje mniejszą liczbą dostępnych odcieni.

Redukcja palety kolorów zmniejsza liczbę tych odcieni, mapując każdą wartość koloru do najbliższego odpowiednika w ograniczonej przestrzeni kolorów. Na przykład, przy redukcji do dwóch kolorów (czarny i biały), wartości kolorów poniżej 128 są zaokrąglane do 0 (czarny), a powyżej 128 do 255 (biały).

W obrazach RGB zmniejsza się paletę kolorów dla każdego z kanałów osobno, traktując każdy kanał jako oddzielny
obraz w skali szarości. Rezultatem jest obraz używający mniej unikalnych kolorów, ale zachowujący ogólną
strukturę i wygląd oryginału.

### Dithering

Dithering to technika stosowana w grafice komputerowej w celu symulacji większej liczby kolorów i odcieni w obrazach o ograniczonej palecie kolorów. Polega na rozmieszczaniu pikseli o różnych kolorach w taki sposób, aby stworzyć iluzję dodatkowych kolorów i płynniejszych przejść tonalnych.

Dithering działa poprzez wprowadzanie drobnych, losowych wzorców lub regularnych układów pikseli, które ludzkie oko interpretuje jako nowe odcienie. Na przykład, na obrazie zredukowanym do czerni i bieli, dithering może mieszać czarne i białe piksele, aby zasymulować odcienie szarości.

### Algorytm Floyda-Steinberga

Algorytm Floyda-Steinberga to jeden z najpopularniejszych algorytmów ditheringu, stosowany do poprawy jakości
obrazów o ograniczonej liczbie kolorów. Algorytm ten jest techniką ditheringu rozproszonego błędu (error
diffusion dithering), co oznacza, że błąd powstały podczas kwantyzacji koloru jest rozpraszany na sąsiednie
piksele, co skutkuje bardziej naturalnym wyglądem obrazu.

Algorytm Floyda-Steinberga działa w następujący sposób:

1. Kwantyzacja piksela: Każdy piksel w obrazie jest przetwarzany pojedynczo. Kolor aktualnego piksela jest
   zaokrąglany do najbliższego koloru w ograniczonej palecie.
2. Obliczenie błędu: Błąd kwantyzacji jest różnicą między oryginalnym kolorem piksela a nowym kolorem po
   kwantyzacji.
3. Rozproszenie błędu: Błąd ten jest następnie rozpraszany na sąsiednie piksele, które jeszcze nie zostały
   przetworzone. Rozproszenie błędu odbywa się według macierzy:
   | - | \* | 7/16 |
   | :--: | :--: | :--: |
   | 3/16 | 5/16 | 1/16 |

   Dodajemy bład przeskalowany przez wartość z macierzy do pikseli sąsiednich (względem piksela oznaczonego \*).

## Zadania do wykonania

Zadanie pierwsze polegało na zaimplementowaniu ditheringu dla obrazu w skali szarości. W tym celu wykonałem
następujące kroki:

1. Przeniosłem obraz z przestrzeni barw RGB na skalę szarości.
2. Użyłem algorytmu Floyda-Steinberga do nałożenia ditheringu na obraz.
3. Wyświetliłem obraz oryginalny, obraz po redukcji kolorów i obraz przetworzony.

## Realizacja zadania

$$ zdjęcie 1 $$
$$ zdjęcie 2 $$

# Zad 2

## Zadania do wykonania

Zadanie drugie polegało na zaimplementowaniu ditheringu dla obrazu w kolorze.
Wykonane kroki były analogiczne do poprzedniego zadania, z tą różnicą, że kazdy kanał koloru był przetwarzany osobno.

Dodatkowo została zaimplementowana możliwość wyboru liczby kolorów, do których ma zostać zredukowana paleta.

## Realizacja zadania

$$ zdjęcie 1 $$
$$ zdjęcie 2 $$
$$ zdjęcie 3 $$
$$ zdjęcie 4 $$
$$ zdjęcie 5 $$
$$ zdjęcie 6 $$

# Zad 3

## Teoria

### Algorytm Bresenhama

Algorytm Bresenhama to wydajna metoda rysowania linii prostych na rastrowym wyświetlaczu komputerowym.
Algorytm działa poprzez iteracyjne wyznaczanie pikseli najbliższych idealnej linii prostej między dwoma
punktami.

Kroki algorytmu Bresenhama:

1. Wyznaczenie wielkości pomocniczych:
   - Oblicz różnice w pozycjach końcowych punktów linii:
     - $dx = |x_2 - x_1|$
     - $dy = |y_2 - y_1|$
   - Określ kierunki kroków
     - $Xi$ = 0 jeżeli $dx = 0$ w innym przypadku $znak(x_2 - x_1)$
     - $Yi$ = 0 jeżeli $yx = 0$ w innym przypadku $znak(y_2 - y_1)$
2. Określenie początkowej wartości błędu:
   - Jeżeli $dx > dy$ to $d = 2*dy - dx$
   - Jeżeli $dy > dx$ to $d = 2*dx - dy$
3. Rysowanie w punkcie początkowym:
   - Narysuj piksel w punkcie $(x_0, y_0)$
4. Powtarzanie w pętli aż do osiągnięcia punktu docelowego:
   - Jeżeli $dx > dy$:
     - $x_0 += Xi$
     - $d += 2*dy$
     - Jeżeli $d >= 0:
       - $y_0 += Yi$
       - $d -= 2*dx$
   - Jeżeli $dy > dx$:
     - $y_0 += Yi$
     - $d += 2*dx$
     - Jeżeli $d >= 0:
       - $x_0 += Xi$
       - $d -= 2*dy$

\*gdzie znak() - funkcja zwracająca znak liczby (+1 / -1)

### Rysownie trójkątów

Trójkąt jest powszechnie używaną figurą w grafice komputerowej. Na jego podstawie buduję się bardziej
skomplikowane kształty, takie jak wielokąty, krzywe czy powierzchnie.

Do rysownia trójkątów można użyć różnych algorytmów, na potrzeby zadania zaimplementowałem algorytm,
którego kroki przedstawiają się następująco:

1. Wyznaczenie pomocniczych wartości:
   - Wyznaczenie czworokąta otaczającego trójkąt (Trójkąt ma boki: a, b, c. a kazdy bok ma składową x i y):
     - $x_{min} = min(a, b, c)$
     - $y_{min} = min(a, b, c)$
     - $x_{max} = max(a, b, c)$
     - $y_{max} = max(a, b, c)$
2. Dla każdego punktu (p.x, p.y) wewnątrz czworokąta:
   - Sprawdź, czy punkt znajduje się wewnątrz trójkąta:
     - $znak_1 = (p.x - a.x)(b.y - a.y)(p.y - a.y)(b.x - a.x) $
     - $znak_2 = (p.x - b.x)(c.y - b.y)(p.y - b.y)(c.x - b.x) $
     - $znak_3 = (p.x - c.x)(a.y - c.y)(p.y - c.y)(a.x - c.x) $
     - Jeżeli $znak_1 = znak_2 = znak_3$ to punkt znajduje się wewnątrz trójkąta

## Zadania do wykonania

Zadanie trzecie polegało na zaimplementowaniu algorytmu Bresenhama do rysowania linii oraz algorytmu do
rysowania trójkątów. Figury miały być jednolite kolorystycznie.

## Realizacja zadania

$$ zdjęcie 1 $$

# Zadanie 4

## Zadania do wykonania

W tym zadaniu tak samo jak poprzednio mielismy narysować linię i trójkąt, ale tym razem kolory nie miały być
jednolite, a miały byc gradientem.

Dla lini wykorzystałem interpolację liniową koloru w zależności od położenia piksela na linii. Im bliżej
punktu poczatkowego linii
