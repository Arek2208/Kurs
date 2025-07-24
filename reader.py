import sys
import csv

# Funkcja, która zmienia dane według listy zmian
def apply_changes(data, changes):
    for change in changes:
        # Rozdziel zmianę na kolumnę, wiersz i wartość
        parts = change.split(',')
        if len(parts) != 3:
            print("Nieprawidłowy format zmiany:", change)
            continue

        x = int(parts[0])  # kolumna
        y = int(parts[1])  # wiersz
        value = parts[2]   # nowa wartość

        # Sprawdzenie czy wiersz i kolumna istnieją
        if y < len(data) and x < len(data[y]):
            data[y][x] = value
        else:
            print("Zmiana poza zakresem:", change)

    return data

# Główna funkcja programu
def main():
    # Sprawdzenie czy podano wystarczającą liczbę argumentów
    if len(sys.argv) < 3:
        print("Użycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ...")
        return

    # Odczytanie nazw plików z argumentów
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    changes = sys.argv[3:]

    # Wczytanie danych z pliku CSV
    with open(input_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row)

    # Zastosowanie zmian
    new_data = apply_changes(data, changes)

    # Wyświetlenie zmodyfikowanych danych w terminalu
    for row in new_data:
        print(','.join(row))

    # Zapisanie danych do pliku wyjściowego
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in new_data:
            writer.writerow(row)

# Uruchomienie programu
if __name__ == "__main__":
    main()
