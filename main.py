import json
import os
import random
from display import show_front, show_back, wait_for_button

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

def order_by_priority(cards, progress):
    def priority(k):
        level = progress.get(str(k["id"]), {}).get("level", 1)
        return level
    return sorted(cards, key=priority)

def level_up(card, knew, progress):
    if str(card["id"]) not in progress:
        progress[str(card["id"])] = {
            "level": 1,
            "correct": 0,
            "false": 0
        }
    level = progress[str(card["id"])]["level"]
    if knew == True:
        progress[str(card["id"])]["level"] = min(5, level + 1)
        progress[str(card["id"])]["correct"] += 1
    if knew == False:
        progress[str(card["id"])]["level"] = max(1, level - 1)
        progress[str(card["id"])]["false"] += 1

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
        return "german"
    if choice == "2":
        return "french"
    

def show_categories(language):
    clear()
    categories = []
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
        return
    selected_category = categories[choice-1]
    return selected_category

def show_stats(cards, progress, category):
    clear()
    print("=" * 45)
    print("STATS")
    print("=" * 45)

    sum_correct = 0
    sum_false = 0

    for card in cards:
        entry = progress.get(str(card["id"]), {"level": 1, "correct": 0, "false": 0})
        print(f"{card["word"]}, {entry["level"]}, {entry["correct"]}, {entry["false"]}")
        sum_correct += entry["correct"]
        sum_false += entry["false"]

    if(sum_correct + sum_false == 0):
        print("No practice yet!")
        return

    percentage = (sum_correct / (sum_correct + sum_false)) * 100
    print(f"Percentage for this category: {percentage}")
    input("Press Enter to go back...")

def practice(cards, progress):
    for card in cards:
        show_front(card["word"])
        while wait_for_button() != 3:
            pass
        
        show_back(card["translation"])
        button = wait_for_button()

        if button == 2:
            level_up(card, False, progress)
        if button == 1:
            level_up(card, True, progress)
        
        save_progress(progress)


def show_menu():
    clear()
    print("=" * 45)
    print("FLASHCARDS")
    print("=" * 45)
    
    print("\n1. Practice")
    print("2. Stats")
    print("3. Back")

    choice = int(input(" > "))
    return choice
    
def main_loop():
    while True:
        language = show_languages()
        category = show_categories(language)
        cards = open_cards(language, category)
        progress = load_progress()

        if category is None:
            continue

        while True:
            choice = show_menu()
            if choice == 1:
                cards = order_by_priority(cards, progress)
                practice(cards, progress)
                print("No more cards. Return?")
                choice_1 = input("(y/n) > ")
                if(choice_1 == "y"):
                    show_categories(language)
                    continue
                if(choice_1 == "n"):
                    practice(cards, progress)
            
            if choice == 2:
                show_stats(cards, progress, category)
            
            if choice == 3:
                clear()
                break


if __name__ == "__main__":
    main_loop()
