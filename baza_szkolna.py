# Lista przechowująca uczniów
uczniowie = []
# Lista przechowująca nauczycieli
nauczyciele = []
# Lista przechowująca wychowawców
wychowawcy = []

# Funkcja menu głównego
def menu_glowne():
    while True:
        print("\nDostępne komendy: utwórz, zarządzaj, koniec")
        komenda = input("Wpisz komendę: ")

        if komenda == "utwórz":
            menu_utworz()
        elif komenda == "zarządzaj":
            menu_zarzadzaj()
        elif komenda == "koniec":
            print("Koniec programu.")
            break
        else:
            print("Nieznana komenda.")

# Funkcja do tworzenia użytkowników
def menu_utworz():
    while True:
        print("\nUtwórz: uczeń, nauczyciel, wychowawca, koniec")
        opcja = input("Co chcesz utworzyć? ")

        if opcja == "uczeń":
            imie_nazwisko = input("Podaj imię i nazwisko ucznia: ")
            klasa = input("Podaj klasę ucznia: ")
            uczen = {
                "imie_nazwisko": imie_nazwisko,
                "klasa": klasa
            }
            uczniowie.append(uczen)
            print("Dodano ucznia.")
        elif opcja == "nauczyciel":
            imie_nazwisko = input("Podaj imię i nazwisko nauczyciela: ")
            przedmiot = input("Podaj przedmiot: ")
            klasy = []

            print("Podaj klasy, które prowadzi nauczyciel (wpisz pustą linię, aby zakończyć):")
            while True:
                klasa = input("Klasa: ")
                if klasa == "":
                    break
                klasy.append(klasa)

            nauczyciel = {
                "imie_nazwisko": imie_nazwisko,
                "przedmiot": przedmiot,
                "klasy": klasy
            }
            nauczyciele.append(nauczyciel)
            print("Dodano nauczyciela.")
        elif opcja == "wychowawca":
            imie_nazwisko = input("Podaj imię i nazwisko wychowawcy: ")
            klasa = input("Podaj klasę: ")
            wychowawca = {
                "imie_nazwisko": imie_nazwisko,
                "klasa": klasa
            }
            wychowawcy.append(wychowawca)
            print("Dodano wychowawcę.")
        elif opcja == "koniec":
            break
        else:
            print("Nieznana opcja.")

# Funkcja do zarządzania użytkownikami
def menu_zarzadzaj():
    while True:
        print("\nZarządzaj: klasa, uczeń, nauczyciel, wychowawca, koniec")
        opcja = input("Co chcesz wyświetlić? ")

        if opcja == "klasa":
            klasa = input("Podaj klasę: ")
            print("Uczniowie klasy " + klasa + ":")
            for uczen in uczniowie:
                if uczen["klasa"] == klasa:
                    print("- " + uczen["imie_nazwisko"])
            znaleziono = False
            for wych in wychowawcy:
                if wych["klasa"] == klasa:
                    print("Wychowawca: " + wych["imie_nazwisko"])
                    znaleziono = True
            if not znaleziono:
                print("Brak wychowawcy.")
        elif opcja == "uczeń":
            imie_nazwisko = input("Podaj imię i nazwisko ucznia: ")
            klasa_ucznia = ""
            for uczen in uczniowie:
                if uczen["imie_nazwisko"] == imie_nazwisko:
                    klasa_ucznia = uczen["klasa"]
                    break
            if klasa_ucznia == "":
                print("Nie znaleziono ucznia.")
            else:
                print("Lekcje ucznia " + imie_nazwisko + ":")
                for nauczyciel in nauczyciele:
                    if klasa_ucznia in nauczyciel["klasy"]:
                        print("- " + nauczyciel["przedmiot"] + " (nauczyciel: " + nauczyciel["imie_nazwisko"] + ")")
        elif opcja == "nauczyciel":
            imie_nazwisko = input("Podaj imię i nazwisko nauczyciela: ")
            znaleziono = False
            for nauczyciel in nauczyciele:
                if nauczyciel["imie_nazwisko"] == imie_nazwisko:
                    print("Nauczyciel prowadzi klasy:")
                    for klasa in nauczyciel["klasy"]:
                        print("- " + klasa)
                    znaleziono = True
            if not znaleziono:
                print("Nie znaleziono nauczyciela.")
        elif opcja == "wychowawca":
            imie_nazwisko = input("Podaj imię i nazwisko wychowawcy: ")
            znaleziono = False
            for wychowawca in wychowawcy:
                if wychowawca["imie_nazwisko"] == imie_nazwisko:
                    klasa = wychowawca["klasa"]
                    print("Uczniowie klasy " + klasa + ":")
                    for uczen in uczniowie:
                        if uczen["klasa"] == klasa:
                            print("- " + uczen["imie_nazwisko"])
                    znaleziono = True
            if not znaleziono:
                print("Nie znaleziono wychowawcy.")
        elif opcja == "koniec":
            break
        else:
            print("Nieznana opcja.")

if __name__ == "__main__":
    menu_glowne()