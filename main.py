import pygame
import sys
import os
import signal
import time
import json
import tempfile
import random

from display import (draw_text_centered, draw_button, WIDTH, HEIGHT, screen, 
                     font_large, font_medium, font_small, 
                     WHITE, BLACK, GRAY, ljub1, ljub2, roz1, roz2)


def save_progress_atomic(progress, path="progress.json"):
    dir_name = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix=".tmp_progress_")
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(progress, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except Exception as e:
        print(f"Greška pri čuvanju: {e}")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def load_progress(path="progress.json"):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)


running = True

def signal_handler(signum, frame):
    global running
    print(f"\n[INFO] Primljen signal {signum}. Započinjem sigurno gašenje...")
    running = False

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


class HardwareWatchdog:
    def __init__(self):
        self.fd = None
        try:
            self.fd = os.open("/dev/watchdog", os.O_WRONLY)
            print("[WATCHDOG] Hardverski watchdog aktiviran.")
        except OSError:
            print("[WATCHDOG] /dev/watchdog ne postoji (normalno za lokalni PC).")

    def feed(self):
        if self.fd is not None:
            try:
                os.write(self.fd, b"1")
            except OSError:
                pass

    def close(self):
        if self.fd is not None:
            try:
                os.write(self.fd, b"V")
                os.close(self.fd)
                print("[WATCHDOG] Watchdog bezbedno ugašen.")
            except OSError:
                pass


def get_categories(path):
    """Pregleda folder i vraća imena svih .json fajlova bez ekstenzije."""
    categories = []
    if not os.path.exists(path):
        return categories
    for file in os.listdir(path):
        if file == "all.json":
            continue
        if file.endswith(".json"):
            cat = file.split(".")[0]
            categories.append(cat)
    return categories

def open_cards(language, category):
    path = f"cards/{language}/{category}.json"
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def order_by_priority(cards, progress):
    def priority(k):
        return progress.get(str(k["id"]), {}).get("level", 1)
    return sorted(cards, key=priority)

def level_up(card, knew, progress):
    if str(card["id"]) not in progress:
        progress[str(card["id"])] = {"level": 1, "correct": 0, "false": 0}
    
    level = progress[str(card["id"])]["level"]
    
    if knew:
        progress[str(card["id"])]["level"] = min(5, level + 1)
        progress[str(card["id"])]["correct"] += 1
    else:
        progress[str(card["id"])]["level"] = max(1, level - 1)
        progress[str(card["id"])]["false"] += 1


def main():
    global running
    watchdog = HardwareWatchdog()
    last_feed_time = time.time()
    
    current_state = "LANGUAGES"
    selected_language = None
    selected_category = None
    cards = []
    progress = load_progress()
    categories_list = []
    
    current_card_index = 0
    show_translation = False

    btn_back = pygame.Rect(10, 10, 60, 30)
    
    # Glavni meni (Vežbaj / Statistika)
    btn_practice = pygame.Rect(40, 150, 240, 60)
    btn_stats = pygame.Rect(40, 230, 240, 60)
    
    # Dugmići za jezike
    btn_german = pygame.Rect(40, 150, 240, 60)
    btn_french = pygame.Rect(40, 230, 240, 60)
    
    # Kartice (Practice)
    btn_znam = pygame.Rect(0, 380, 160, 100)
    btn_neznam = pygame.Rect(160, 380, 160, 100)
    flip_zone = pygame.Rect(0, 60, 320, 310) 

    while running:
        current_time = time.time()
        if current_time - last_feed_time > 5.0:
            watchdog.feed()
            last_feed_time = current_time

        cat_rects = []
        if current_state == "CATEGORIES":
            y_start = 100
            for i, cat in enumerate(categories_list):
                rect = pygame.Rect(40, y_start, 240, 50)
                cat_rects.append(rect)
                y_start += 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                click_pos = event.pos
                
                if current_state == "LANGUAGES":
                    if btn_german.collidepoint(click_pos):
                        selected_language = "german"
                        categories_list = get_categories(f"cards/{selected_language}")
                        current_state = "CATEGORIES"
                    elif btn_french.collidepoint(click_pos):
                        selected_language = "french"
                        categories_list = get_categories(f"cards/{selected_language}")
                        current_state = "CATEGORIES"
                        
                elif current_state == "CATEGORIES":
                    if btn_back.collidepoint(click_pos):
                        current_state = "LANGUAGES"
                    else:
                    
                        for i, rect in enumerate(cat_rects):
                            if rect.collidepoint(click_pos) and i < len(categories_list):
                                selected_category = categories_list[i]
                                cards = open_cards(selected_language, selected_category)
                                if cards:
                                    cards = order_by_priority(cards, progress)
                                    current_state = "MENU"
                                    break
                                    
                elif current_state == "MENU":
                    if btn_back.collidepoint(click_pos):
                        current_state = "CATEGORIES"
                    elif btn_practice.collidepoint(click_pos):
                        current_card_index = 0
                        show_translation = False
                        current_state = "PRACTICE"
                    elif btn_stats.collidepoint(click_pos):
                        current_state = "STATS"
                        
                elif current_state == "PRACTICE":
                    if btn_back.collidepoint(click_pos):
                        current_state = "MENU"
                    elif btn_znam.collidepoint(click_pos):
                        if show_translation:
                            level_up(cards[current_card_index], True, progress)
                            save_progress_atomic(progress)
                            current_card_index = (current_card_index + 1) % len(cards)
                            show_translation = False
                    elif btn_neznam.collidepoint(click_pos):
                        if show_translation:
                            level_up(cards[current_card_index], False, progress)
                            save_progress_atomic(progress)
                            current_card_index = (current_card_index + 1) % len(cards)
                            show_translation = False
                    elif flip_zone.collidepoint(click_pos):
                        show_translation = not show_translation
                        
                elif current_state == "STATS":
                    if btn_back.collidepoint(click_pos):
                        current_state = "MENU"

        
        screen.fill(ljub1)  
        
        if current_state == "LANGUAGES":
            draw_text_centered("Izaberi Jezik", font_large, WHITE, 40)
            draw_button(btn_german, "Nemacki", roz2)
            draw_button(btn_french, "Francuski", ljub2)
            
        elif current_state == "CATEGORIES":
            draw_text_centered("Kategorije", font_large, WHITE, 40)
            draw_button(btn_back, "Nazad", roz1)
            
            for i, rect in enumerate(cat_rects):
                display_name = categories_list[i].replace("_", " ").capitalize()
                draw_button(rect, display_name, ljub2)
            
        elif current_state == "MENU":
            draw_text_centered(f"{selected_language.upper()}", font_large, WHITE, 40)
            draw_button(btn_back, "Nazad", roz1)
            draw_button(btn_practice, "VEZBAJ", roz2)
            draw_button(btn_stats, "STATISTIKA", ljub2)
            
        elif current_state == "PRACTICE":
            if len(cards) > 0:
                card = cards[current_card_index]
                
                if show_translation:
                    draw_text_centered(card["translation"], font_large, WHITE, 200)
                else:
                    draw_text_centered(card["word"], font_large, WHITE, 200)
                    draw_text_centered("(Dodirni za prevod)", font_small, roz1, 250)
                
                draw_button(btn_back, "Nazad", roz1)
                
                if show_translation:
                    draw_button(btn_znam, "ZNAM", roz2)
                    draw_button(btn_neznam, "NE ZNAM", ljub2)
                else:
                    draw_button(btn_znam, "ZNAM", GRAY)      
                    draw_button(btn_neznam, "NE ZNAM", GRAY) 
                    
        elif current_state == "STATS":
            draw_text_centered("STATS FOR NERDS", font_large, roz2, 40)
            draw_button(btn_back, "Nazad", roz1)
            
            sum_correct = 0
            sum_false = 0
            for card in cards:
                entry = progress.get(str(card["id"]), {"correct": 0, "false": 0})
                sum_correct += entry["correct"]
                sum_false += entry["false"]
                
            percentage = 0
            if sum_correct + sum_false > 0:
                percentage = round((sum_correct / (sum_correct + sum_false)) * 100, 1)
                
            draw_text_centered(f"Tacno: {sum_correct}", font_medium, roz2, 150)
            draw_text_centered(f"Pogresno: {sum_false}", font_medium, ljub2, 200)
            draw_text_centered(f"Uspesnost: {percentage}%", font_large, WHITE, 280)

        pygame.display.flip()


    print("[INFO] Čistim i čuvam podatke...")
    save_progress_atomic(progress)
    watchdog.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()