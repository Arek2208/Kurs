def collatz_sequence(x):
    while x != 1:
        print(x, end=" -> ")
        if x % 2 == 0:
            x = x // 2
        else:
            x = 3 * x + 1
    print(1)  #####ostatnia cyfra w ciagu

####Odczytanie liczby od użytkownika
x = int(input("Podaj liczbę x (1-100): "))

###Sprawdzenie poprawności działania
if 1 <= x <= 100:
    print("Ciąg Collatza:")
    collatz_sequence(x)
else:
    print("Liczba musi być z zakresu od 1 do 100.")