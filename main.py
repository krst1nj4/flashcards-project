import json
import os
import random

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

def order_by_priority():
    

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


# while True:
#     if(screen == "language"):
#         for cat in category:
#             print(f"{category}")
#         screen = "category"
#         selected_language = language
#         selected_category = category

#     if (screen == "category"):
#         print("Practice")
#         print("Stats")
#         print("Back")


# 📝 practice(cards)          — vrti kartice jednu po jednu
# 📝 update_score(card, knew) — ažurira Leitner nivo kartice

# 📝 show_stats(cards)        — ispisuje statistiku za kategoriju
# 📝 main()                   — glavni loop sa while True