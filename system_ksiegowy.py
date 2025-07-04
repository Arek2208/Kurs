import os

def wczytaj_saldo():
    if os.path.exists("saldo.txt"):
        with open("saldo.txt") as f:
            return float(f.read())
    return 0.0

def zapisz_saldo(saldo):
    with open("saldo.txt", "w") as f:
        f.write(str(saldo))

def wczytaj_magazyn():
    magazyn = {}
    if os.path.exists("magazyn.txt"):
        with open("magazyn.txt") as f:
            for linia in f:
                nazwa, cena, ilosc = linia.strip().split(",")
                magazyn[nazwa] = {"cena": float(cena), "ilosc": int(ilosc)}
    return magazyn

def zapisz_magazyn(magazyn):
    with open("magazyn.txt", "w") as f:
        for nazwa, dane in magazyn.items():
            f.write(f"{nazwa},{dane['cena']},{dane['ilosc']}\n")

def dopisz_historie(op):
    with open("historia.txt", "a") as f:
        f.write(op + "\n")

def wczytaj_historie():
    if os.path.exists("historia.txt"):
        with open("historia.txt") as f:
            return [linia.strip() for linia in f]
    return []

def main():
    saldo = wczytaj_saldo()
    magazyn = wczytaj_magazyn()
    historia = wczytaj_historie()

    while True:
        print("\nDostępne komendy:")
        print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")
        komenda = input("Wprowadź komendę:")

        if komenda == "saldo":
            try:
                kwota = float(input("Podaj kwotę (może być ujemna):"))
                opis = input("Opis operacji:")
                saldo += kwota
                dopisz_historie(f"saldo,{kwota},{opis}")
                zapisz_saldo(saldo)
            except:
                print("Nieprawidłowa kwota!")

        elif komenda == "sprzedaż":
            nazwa = input("Nazwa produktu:")
            try:
                cena = float(input("Cena sprzedaży:"))
                ilosc = int(input("Ilość:"))
                if cena < 0 or ilosc < 0:
                    print("Cena i ilość nie mogą być ujemne.")
                    continue
                if nazwa in magazyn and magazyn[nazwa]["ilosc"] >= ilosc:
                    magazyn[nazwa]["ilosc"] -= ilosc
                    saldo += cena * ilosc
                    dopisz_historie(f"sprzedaż,{nazwa},{cena},{ilosc}")
                    if magazyn[nazwa]["ilosc"] == 0:
                        del magazyn[nazwa]
                    zapisz_saldo(saldo)
                    zapisz_magazyn(magazyn)
                else:
                    print("Brak wystarczającej ilości w magazynie.")
            except:
                print("Nieprawidłowe dane!")

        elif komenda == "zakup":
            nazwa = input("Nazwa produktu:")
            try:
                cena = float(input("Cena zakupu:"))
                ilosc = int(input("Ilość:"))
                koszt = cena * ilosc
                if cena < 0 or ilosc < 0:
                    print("Cena i ilość nie mogą być ujemne.")
                    continue
                if saldo >= koszt:
                    saldo -= koszt
                    if nazwa in magazyn:
                        magazyn[nazwa]["ilosc"] += ilosc
                        magazyn[nazwa]["cena"] = cena
                    else:
                        magazyn[nazwa] = {"cena": cena, "ilosc": ilosc}
                    dopisz_historie(f"zakup,{nazwa},{cena},{ilosc}")
                    zapisz_saldo(saldo)
                    zapisz_magazyn(magazyn)
                else:
                    print("Nie masz wystarczającego salda.")
            except:
                print("Nieprawidłowe dane!")

        elif komenda == "konto":
            print(f"Aktualny stan konta: {saldo:.2f}")

        elif komenda == "lista":
            if not magazyn:
                print("Magazyn jest pusty.")
            else:
                for nazwa, dane in magazyn.items():
                    print(f"{nazwa} - cena: {dane['cena']:.2f}, ilość: {dane['ilosc']}")

        elif komenda == "magazyn":
            nazwa = input("Podaj nazwę produktu: ")
            if nazwa in magazyn:
                dane = magazyn[nazwa]
                print(f"{nazwa} - cena: {dane['cena']:.2f}, ilość: {dane['ilosc']}")
            else:
                print("Taki produkt nie istnieje w magazynie.")

        elif komenda == "przegląd":
            try:
                od = input("Od (indeks): ")
                do = input("Do (indeks): ")
                od = int(od) if od else 0
                do = int(do) if do else len(historia)
                if 0 <= od <= do <= len(historia):
                    for i in range(od, do):
                        print(f"{i}: {historia[i]}")
                else:
                    print(f"Nieprawidłowy zakres! Liczba zapisanych operacji: {len(historia)}")
            except:
                print("Nieprawidłowe dane wejściowe.")

        elif komenda == "koniec":
            print("Kończę działanie programu.")
            break

        else:
            print("Nieznana komenda. Spróbuj ponownie.")

if __name__ == "__main__":
    main()