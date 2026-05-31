import json
import os
import random

def ucitaj_kartice(putanja="kartice.json"):
    with open(putanja, "r", encoding="utf-8") as f:
        return json.load(f)

def ucitaj_progres(putanja="progres.json"):
    if not os.path.exists(putanja):
        return {}
    with open(putanja, "r") as f:
        return json.load(f)

def sacuvaj_progres(progres, putanja="progres.json"):
    with open(putanja, "w") as f:
        json.dump(progres, f, indent=2)

def sortiraj_po_prioritetu(kartice, progres):
    def prioritet(k):
        nivo = progres.get(str(k["id"]), {}).get("nivo", 1)
        return nivo
    return sorted(kartice, key=prioritet)

def azuriraj_nivo(kartica_id, znala, progres):
    key = str(kartica_id)
    if key not in progres:
        progres[key] = {"nivo": 1, "tacno": 0, "pogresno": 0}
    if znala:
        progres[key]["nivo"]    = min(5, progres[key]["nivo"] + 1)
        progres[key]["tacno"]  += 1
    else:
        progres[key]["nivo"]     = max(1, progres[key]["nivo"] - 1)
        progres[key]["pogresno"] += 1

def clear():
    os.system("clear")

def prikazi_karticu(kartica, progres, index, ukupno):
    clear()
    nivo = progres.get(str(kartica["id"]), {}).get("nivo", 1)
    print("=" * 45)
    print(f"  Kartica {index + 1}/{ukupno}   |   Nivo: {'★' * nivo}{'☆' * (5 - nivo)}")
    print("=" * 45)
    print(f"\n  {kartica['rec'].upper()}\n")
    input("  [ENTER za prevod]")
    print(f"\n  ➜  {kartica['prevod']}")
    print(f"\n  Primer: {kartica['primer']}")
    print()
    while True:
        odgovor = input("  Znala si? (d/n): ").strip().lower()
        if odgovor in ("d", "n"):
            return odgovor == "d"

def prikazi_statistiku(progres, kartice):
    clear()
    print("=" * 45)
    print("  STATISTIKA")
    print("=" * 45)
    ukupno_tacno    = sum(v["tacno"]    for v in progres.values())
    ukupno_pogresno = sum(v["pogresno"] for v in progres.values())
    print(f"\n  Tačnih odgovora:    {ukupno_tacno}")
    print(f"  Pogrešnih odgovora: {ukupno_pogresno}")
    print()
    print(f"  {'Reč':<15} {'Nivo':<10} {'✓':<6} {'✗'}")
    print(f"  {'-'*35}")
    for k in kartice:
        p    = progres.get(str(k["id"]), {"nivo": 1, "tacno": 0, "pogresno": 0})
        nivo = "★" * p["nivo"] + "☆" * (5 - p["nivo"])
        print(f"  {k['rec']:<15} {nivo:<10} {p['tacno']:<6} {p['pogresno']}")
    print()

def glavni_loop(kartice):
    progres = ucitaj_progres()
    while True:
        clear()
        print("=" * 45)
        print("  FLASHCARDS")
        print("=" * 45)
        print("\n  1. Vežbaj")
        print("  2. Statistika")
        print("  3. Izlaz\n")
        izbor = input("  > ").strip()
        if izbor == "1":
            redosled = sortiraj_po_prioritetu(kartice, progres)
            for i, kartica in enumerate(redosled):
                znala = prikazi_karticu(kartica, progres, i, len(redosled))
                azuriraj_nivo(kartica["id"], znala, progres)
                sacuvaj_progres(progres)
            clear()
            print("\n  Završila si rundu! Progres sačuvan.\n")
            input("  [ENTER za meni]")
        elif izbor == "2":
            prikazi_statistiku(progres, kartice)
            input("  [ENTER za meni]")
        elif izbor == "3":
            clear()
            print("\n  Doviđenja! 👋\n")
            break

if __name__ == "__main__":
    kartice = ucitaj_kartice()
    glavni_loop(kartice)


-------------------------------------
# screen = "language"
# selected_language = None
# selected_category = None

def open_cards(language, category):
    path = f"cards/{language}/{category}.json"
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_progress(path = "progress.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_progress(progress, path = "progress.json"):
    with open(path, "w") as f:
        json.dump(progress, f, indent=2)

def sort_by_priority():


def get_categories(path):
    categories = []
    for file in os.listdir(path):
        if file == "all.json":
            continue
        if file.endswith(".json"):
             cat = file.split(".")[0]

             categories.append(cat)
    return categories

def get_all_cards(path):
    with open(path, "r", encoding="utf-8") as f:
        cards = json.load(f)
    return cards

def clear():
    os.system("clear")

def show_languages():
    clear()
    print("=" * 45)
    print("LANGUAGES")
    print("=" * 45)
    
    print("\n1. German")
    print("2. French")

    choice = input("> ").strip()

    if choice == "1":
        show_categories("german")
    
    if choice == "2":
        show_categories("french")
    
        

def show_categories(language):
    clear()
    if language == "german":
        categories = get_categories("cards/german")
 
    if language == "french":
        categories = get_categories("cards/french")

    for i, cat in enumerate(categories):
        print(f"{i + 1}> {cat}")
    
    print(f"{len(categories) + 1} > Go back")

    choice = int(input(" > "))
    if(choice == len(categories) + 1):
        clear()
        show_languages()
        return None
    selected_category = categories[choice-1]
    return selected_category

    

def show_menu():
    clear()
    print("=" * 45)
    print("FLASHCARDS")
    print("=" * 45)
    
    print("\n1. Practice")
    print("2. Stats")
    print("3. Back")

    choice = int(input(" > "))
    if(choice == 1):
        clear()
        practice

    if(choice == 2):
        clear()
        show_stats()
        return None
    
    if(choice == 3):
        clear()
        show_categories()
        return None

def main_loop():