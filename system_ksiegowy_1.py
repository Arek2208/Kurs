def main():
    saldo = 0
    magazyn = {}
    historia = []

    while True:
        print("\nDostępne komendy:")
        print("saldo, sprzedaż, zakup, konto, lista, magazyn, przegląd, koniec")
        komenda = input("Wprowadź komendę:")

        if komenda == "saldo":
            try:
                kwota = float(input("Podaj kwotę (może być ujemna):"))
                opis = input("Opis operacji:")
                saldo += kwota
                historia.append(("saldo", kwota, opis))
            except :
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
                    historia.append(("sprzedaż", nazwa, cena, ilosc))
                    if magazyn[nazwa]["ilosc"] == 0:
                        del magazyn [saldo]
                else:
                    print("Brak wystarczającej ilości w magazynie.")
            except :
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
                    historia.append(("zakup", nazwa, cena, ilosc))
                else:
                    print("Nie masz wystarczającego salda.")
            except :
                print("Nieprawidłowe dane!")

        elif komenda == "konto":
            print(f"Aktualny stan konta: {saldo:.2f}")

        elif komenda == "lista":
            if not magazyn:
                print("Magazyn jest pusty.")
            else:
                for nazwa, dane in magazyn.items():
                    print(f"{nazwa} - cena: {dane['cena']}, ilość: {dane['ilosc']}")

        elif komenda == "magazyn":
            nazwa = input("Podaj nazwę produktu: ")
            if nazwa in magazyn:
                dane = magazyn[nazwa]
                print(f"{nazwa} - cena: {dane['cena']}, ilość: {dane['ilosc']}")
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
                        print(f"{i}:{historia[i]}")
                else:
                    print(f"Nieprawidłowy zakres! Liczba zapisanych operacji: {len(historia)}")
            except :
                print("Nieprawidłowe dane wejściowe.")

        elif komenda == "koniec":
            print("Kończę działanie programu.")
            break

        else:
            print("Nieznana komenda. Spróbuj ponownie.")


if __name__== "__main__":
    main()
