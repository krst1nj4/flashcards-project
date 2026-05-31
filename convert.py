import csv
import json
import os

def convert_category(path_csv, language, category):
    cards = []
    with open(path_csv, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        for i, row in enumerate(reader):
            cards.append({
                "id": i+1,
                "word": row[1].strip(),
                "translation": row[0].strip(),
                "example": "",
                "category": category,
                "language": language
            })
    return cards

def convert_all(folder, language, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    all_cards = []

    for file in os.listdir(folder):
        if file.endswith(".csv"):
            category = file.split("_")[-1].replace(".csv", "")
            path = os.path.join(folder, file)
            cards = convert_category(path, language, category)

            out = os.path.join(output_folder, f"{category}.json")
            with open(out, "w", encoding="utf-8") as f:
                json.dump(cards, f, ensure_ascii=False, indent=2)
            
            print(f"{category}: {len(cards)} card")
            all_cards.extend(cards)
    
    with open(os.path.join(output_folder, "all.json"), "w", encoding="utf-8") as f:
        json.dump(all_cards, f, ensure_ascii=False, indent=2)
    
    print(f"\nTotal: {len(all_cards)} cards!")


convert_all(
    "basic-vocabulary-word-lists/wordlists/de-en",
    "german",
    "cards/german"
)

convert_all(
    "basic-vocabulary-word-lists/wordlists/fr-en",
    "french",
    "cards/french"
)