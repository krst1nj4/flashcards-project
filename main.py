import json
import os
import random
from display import show_front, show_back, wait_for_button, navigate_menu, show_screen

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
    options = ["German", "French"]
    choice = navigate_menu(options)
    if choice == 0:
        return "german"
    if choice == 1:
        return "french"

def show_categories(language):
    if language == "german":
        categories = get_categories("cards/german")
    if language == "french":
        categories = get_categories("cards/french")
    
    options = categories + ["Go back"]
    choice = navigate_menu(options)
    
    if choice == len(categories):
        return None
    return categories[choice]

def show_stats(cards, progress, category):
    sum_correct = 0
    sum_false = 0

    for card in cards:
        entry = progress.get(str(card["id"]), {"level": 1, "correct": 0, "false": 0})
        sum_correct += entry["correct"]
        sum_false += entry["false"]

    if sum_correct + sum_false == 0:
        show_screen(["STATS", "", "No practice yet!"])
        wait_for_button()
        return

    percentage = round((sum_correct / (sum_correct + sum_false)) * 100, 1)
    show_screen([
        "STATS",
        "",
        f"Correct: {sum_correct}",
        f"Wrong: {sum_false}",
        f"Score: {percentage}%"
    ])
    wait_for_button()

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
    options = ["Practice", "Stats", "Back"]
    return navigate_menu(options)
    
def main_loop():
    while True:
        language = show_languages()
        category = show_categories(language)
        if category is None:
            continue
        cards = open_cards(language, category)
        
        while True:
            progress = load_progress()
            choice = show_menu()
            if choice == 0:
                cards = order_by_priority(cards, progress)
                practice(cards, progress)
            if choice == 1:
                show_stats(cards, progress, category)
            if choice == 2:
                break


if __name__ == "__main__":
    main_loop()
