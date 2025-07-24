import sys
import csv
import json
import pickle
import os

class FileHandler:
    def read_file(self, filename):
        pass

    def write_file(self, filename, data):
        pass

class CSVHandler(FileHandler):
    def read_file(self, filename):
        with open(filename, newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            return [row for row in reader]

    def write_file(self, filename, data):
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(data)

class TXTHandler(FileHandler):
    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return [line.strip().split(',') for line in file]

    def write_file(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as file:
            for row in data:
                file.write(','.join(row) + '\n')


class PickleHandler(FileHandler):
    def read_file(self, filename):
        with open(filename, 'rb') as file:
            return pickle.load(file)

    def write_file(self, filename, data):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

class JSONHandler(FileHandler):
    def read_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)

    def write_file(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)

def choose_handler(filename):
    if filename.endswith('.csv'):
        return CSVHandler()
    elif filename.endswith('.txt'):
        return TXTHandler()
    elif filename.endswith('.json'):
        return JSONHandler()
    elif filename.endswith('.pickle'):
        return PickleHandler()
    else:
        print("Nieznany typ pliku:", filename)
        sys.exit(1)

def apply_changes(data, changes):
    for change in changes:
        try:
            x_str, y_str, value = change.split(',', 2)
            x = int(x_str)
            y = int(y_str)
            if y < len(data) and x < len(data[y]):
                data[y][x] = value
            else:
                print("Zmiana poza zakresem:", change)
        except Exception as e:
            print("Błąd przy zmianie:", change, "|", str(e))
    return data
def main():
    if len(sys.argv) < 3:
        print("Użycie: python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiany...>")
        return

    plik_wejsciowy = sys.argv[1]
    plik_wyjsciowy = sys.argv[2]
    zmiany = sys.argv[3:]

    czytnik = choose_handler(plik_wejsciowy)
    zapis = choose_handler(plik_wyjsciowy)

    dane = czytnik.read_file(plik_wejsciowy)


    dane = apply_changes(dane, zmiany)

    print("Zmodyfikowana zawartość:")
    for wiersz in dane:
        print(','.join(wiersz))

    zapis.write_file(plik_wyjsciowy, dane)
    print("\nZapisano do pliku:", plik_wyjsciowy)


if __name__ == '__main__':
    main()