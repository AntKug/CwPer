import curses
import random
import time
import json

def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    center_y, center_x = h // 2, w // 2

    results = []

    for i in range(5):
        stdscr.clear()
        stdscr.addstr(center_y, center_x, "X")
        stdscr.refresh()

        # Losuj pozycję cyfry w całym terminalu, ale nie na X ani jego sąsiadach
        while True:
            digit_y = random.randint(0, h - 1)
            digit_x = random.randint(0, w - 2)  # -2 to avoid writing at the last column
            if abs(digit_y - center_y) <= 1 and abs(digit_x - center_x) <= 1:
                continue  # nie na X ani sąsiadach
            break

        cyfra = str(random.randint(0, 9))

        # Sprawdź czy cyfra nie wychodzi poza ekran (już zapewnione przez losowanie)
        stdscr.addstr(digit_y, digit_x, cyfra)
        stdscr.refresh()
        time.sleep(0.5)
        stdscr.addstr(digit_y, digit_x, " ")
        stdscr.refresh()

        stdscr.nodelay(0)
        stdscr.addstr(center_y + 3, center_x - 15, f"Wpisz cyfrę, którą widziałeś ({i+1}/3): ")
        stdscr.refresh()
        inp = stdscr.getstr(center_y + 3, center_x + 18, 1)
        inp = inp.decode("utf-8")

        correct = inp == cyfra
        results.append({
            "round": i + 1,
            "shown_digit": cyfra,
            "user_input": inp,
            "correct": correct
        })

        stdscr.addstr(center_y + 5, center_x - 15, f"Poprawna cyfra: {cyfra}, wpisałeś: {inp}")
        if correct:
            stdscr.addstr(center_y + 6, center_x - 15, "Brawo!")
        else:
            stdscr.addstr(center_y + 6, center_x - 15, "Niestety, spróbuj ponownie.")
        stdscr.addstr(center_y + 7, center_x - 15, "Naciśnij dowolny klawisz, aby kontynuować...")
        stdscr.refresh()
        stdscr.getch()
        stdscr.clear()
        stdscr.refresh()

    stdscr.addstr(center_y, center_x - 10, "Koniec gry! Dziękujemy za udział.")
    stdscr.refresh()
    time.sleep(2)

    # Zapisz wyniki do pliku results.json
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    curses.wrapper(main)