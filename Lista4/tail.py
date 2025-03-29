import sys
import time
import argparse
import os

def tail_lines_backwards(f, num_lines):
    f.seek(0, os.SEEK_END)
    pos = f.tell()
    buffer = b''
    lines = []

    while pos > 0 and len(lines) < num_lines:
        pos -= 1
        f.seek(pos)
        byte = f.read(1)

        if byte == b'\n' and buffer:
            lines.append(buffer[::-1].decode(errors="replace"))
            buffer = b''
        else:
            buffer += byte

    if buffer:
        lines.append(buffer[::-1].decode(errors="replace"))

    return reversed(lines)

def read_lines(path, num_lines, follow):
    try:
        with open(path, 'rb') as f:
            lines = tail_lines_backwards(f, num_lines)
            for line in lines:
                print(line)

            if not follow:
                return
            print(f"\nWykrywania zmian")

            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line:
                    print(line.decode(errors="replace"), end="")
                else:
                    time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nKoniec")
    except Exception as e:
        print(f"Błąd: {e}")

def parse_args():
    parser = argparse.ArgumentParser(description="uproszczona wersja uniksowego programu tail")
    parser.add_argument("file", nargs="?", help="Ścieżka do pliku")
    parser.add_argument("--lines", "-n", type=int, default=10, help="liczba linii do wyświetlenia (domyślnie 10)")
    parser.add_argument("--follow", "-f", action="store_true", help="sledzenie zmian w pliku")
    return parser.parse_args()

def main():
    args = parse_args()

    if args.lines < 0:
        print("Błąd: liczba linii nie może być ujemna.")
        return

    if args.file:
        if not os.path.isfile(args.file):
            print(f"Błąd: plik {args.file} nie istnieje.")
            return

        read_lines(args.file, args.lines, args.follow)

    else:
        if sys.stdin.isatty():
            print("Brak danych na wejściu standardowym i brak pliku. Przerwano.")
            return

        lines = sys.stdin.read().splitlines(keepends=True)
        for line in lines[-args.lines:]:
            print(line, end="")

if __name__ == "__main__":
    main()
