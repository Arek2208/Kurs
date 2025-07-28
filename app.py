from flask import Flask, render_template, request, redirect, url_for
import os
import json

app = Flask(__name__)

# Ścieżki do plików
KONTO_FILE = "konto.txt"
MAGAZYN_FILE = "magazyn.txt"
HISTORIA_FILE = "historia.txt"

# Inicjalizacja plików
if not os.path.exists(KONTO_FILE):
    with open(KONTO_FILE, 'w') as f:
        f.write('0')

if not os.path.exists(MAGAZYN_FILE):
    with open(MAGAZYN_FILE, 'w') as f:
        json.dump({}, f)

if not os.path.exists(HISTORIA_FILE):
    with open(HISTORIA_FILE, 'w') as f:
        pass

# Pomocnicze funkcje
def get_saldo():
    with open(KONTO_FILE) as f:
        return float(f.read())

def set_saldo(value):
    with open(KONTO_FILE, 'w') as f:
        f.write(str(value))

def get_magazyn():
    with open(MAGAZYN_FILE) as f:
        return json.load(f)

def set_magazyn(mag):
    with open(MAGAZYN_FILE, 'w') as f:
        json.dump(mag, f)

def add_to_history(entry):
    with open(HISTORIA_FILE, 'a') as f:
        f.write(entry + '\n')

def get_history():
    with open(HISTORIA_FILE) as f:
        return [line.strip() for line in f.readlines()]

# Strona główna
@app.route('/', methods=['GET', 'POST'])
def index():
    saldo = get_saldo()
    magazyn = get_magazyn()

    if request.method == 'POST':
        if 'kup' in request.form:
            nazwa = request.form['kup_nazwa']
            cena = float(request.form['kup_cena'])
            ilosc = int(request.form['kup_ilosc'])
            koszt = cena * ilosc

            if saldo >= koszt:
                saldo -= koszt
                magazyn[nazwa] = magazyn.get(nazwa, 0) + ilosc
                add_to_history(f"Zakup: {nazwa}, {ilosc} szt., cena: {cena}")
                set_magazyn(magazyn)
                set_saldo(saldo)
            else:
                add_to_history("Błąd zakupu – niewystarczające środki.")

        elif 'sprzedaj' in request.form:
            nazwa = request.form['sprzedaj_nazwa']
            ilosc = int(request.form['sprzedaj_ilosc'])

            if magazyn.get(nazwa, 0) >= ilosc:
                cena_jednostkowa = 10  # domyślna cena
                przychod = cena_jednostkowa * ilosc
                saldo += przychod
                magazyn[nazwa] -= ilosc
                add_to_history(f"Sprzedaż: {nazwa}, {ilosc} szt., cena: {cena_jednostkowa}")
                set_magazyn(magazyn)
                set_saldo(saldo)
            else:
                add_to_history("Błąd sprzedaży – brak wystarczającej ilości.")

        elif 'zmien_saldo' in request.form:
            wartosc = float(request.form['zmiana_salda'])
            saldo += wartosc
            add_to_history(f"Zmiana salda: {wartosc} zł")
            set_saldo(saldo)

        return redirect(url_for('index'))

    return render_template('index.html', saldo=saldo, magazyn=magazyn)

# Historia bez zakresu
@app.route('/historia/')
@app.route('/historia/<int:start>/<int:end>/')
def historia(start=None, end=None):
    historia = get_history()
    zakres = None
    blad = None

    if start is not None and end is not None:
        if 0 <= start < end <= len(historia):
            historia = historia[start:end]
            zakres = (start, end)
        else:
            blad = f"Niepoprawny zakres! Historia ma {len(historia)} wpisów."

    return render_template('historia.html', historia=historia, zakres=zakres, blad=blad, dlugosc=len(get_history()))

if __name__ == '__main__':
    app.run(debug=True)