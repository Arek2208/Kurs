# Kółko i krzyżyk

def drukuj_plansze(plansza):
    for i in range(0, 9, 3):
        print(plansza[i] + plansza[i+1] + plansza[i+2])

def sprawdz_wygrana(plansza, gracz):
    # Sprawdzamy wszystkie wygrane kombinacje
    wygrane = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for linia in wygrane:
        if plansza[linia[0]] == gracz and plansza[linia[1]] == gracz and plansza[linia[2]] == gracz:
            return True
    return False

def remis(plansza):
    return '-' not in plansza

def dostepne_ruchy(plansza):
    return [i for i in range(9) if plansza[i] == '-']

def minimax(plansza, komputer_ruch):
    if sprawdz_wygrana(plansza, 'X'):
        return 1
    elif sprawdz_wygrana(plansza, 'O'):
        return -1
    elif remis(plansza):
        return 0

    if komputer_ruch:
        najlepszy_wynik = -999
        for i in dostepne_ruchy(plansza):
            plansza[i] = 'X'
            wynik = minimax(plansza, False)
            plansza[i] = '-'
            if wynik > najlepszy_wynik:
                najlepszy_wynik = wynik
        return najlepszy_wynik
    else:
        najlepszy_wynik = 999
        for i in dostepne_ruchy(plansza):
            plansza[i] = 'O'
            wynik = minimax(plansza, True)
            plansza[i] = '-'
            if wynik < najlepszy_wynik:
                najlepszy_wynik = wynik
        return najlepszy_wynik

def ruch_komputera(plansza):
    najlepszy_wynik = -999
    najlepszy_ruch = None
    for i in dostepne_ruchy(plansza):
        plansza[i] = 'X'
        wynik = minimax(plansza, False)
        plansza[i] = '-'
        if wynik > najlepszy_wynik:
            najlepszy_wynik = wynik
            najlepszy_ruch = i
    return najlepszy_ruch

def gra():
    plansza = ['-' for _ in range(9)]

    while True:
        # Komputer wykonuje ruch
        ruch = ruch_komputera(plansza)
        plansza[ruch] = 'X'
        drukuj_plansze(plansza)

        if sprawdz_wygrana(plansza, 'X'):
            print("Przegrana")
            break
        if remis(plansza):
            print("Remis")
            break

        # Ruch użytkownika
        while True:
            try:
                pole = int(input()) - 1
                if pole < 0 or pole > 8 or plansza[pole]!= '-':
                    print("Błąd")
                else:
                    plansza[pole] = 'O'
                    break
            except:
                print("Błąd")

        if sprawdz_wygrana(plansza, 'O'):
            drukuj_plansze(plansza)
            print("Wygrana")
            break
        if remis(plansza):
            drukuj_plansze(plansza)
            print("Remis")
            break

# Uruchomienie gry
gra()