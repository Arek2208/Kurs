
#TWORZYMY APLIKACJE
print("Ładowarka paczek")
maksymalnie_elementow = int(input("Wprowadz ilosc elementow, ktora przyjmie aplikacja: "))
print(f"Aplikacja przyjmie {maksymalnie_elementow} elementow.")

biezace_elementy = 0
waga_paczki = 0
lista_paczek = []

while biezace_elementy < maksymalnie_elementow:
    waga_elementu = int(input("Podaj element (waga z przedzialu 1 a 10 kg): "))
    if 1 <= waga_elementu <= 10:
        biezace_elementy += 1
        print(f"Dodajemy do paczki - obecna ilosc elementow: {biezace_elementy}")
        if waga_paczki + waga_elementu > 20:
            (lista.paczek.append(waga_paczki))
            waga_paczki= 0
        waga_paczki += waga_elementu
    else:
        print("Przekroczono limit - koncze dzialanie.")
    break

lista_paczek.append(waga_paczki)
liczba_paczek_na_liscie = len(lista_paczek)
suma_wag_paczek = sum(lista_paczek)
puste_kilogramy = min(lista_paczek)

print("Podsumowanie:")
print(f"Liczba paczek wyslanych: {liczba_paczek_na_liscie}")
print(f"Liczba kilogramow wyslanych: {suma_wag_paczek}")
print(f"Suma pustych kilogramow: {liczba_paczek_na_liscie * 20 - suma_wag_paczek }")
print(f"Paczka ktora miala najwiecej pustych kilogramow: Najmniej kilogramow miala paczka "
      f"{lista_paczek.index(puste_kilogramy) + 1} : {20 - puste_kilogramy}")
