from PIL import Image, ImageDraw, ImageFont
import subprocess
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)

WIDTH = 480
HEIGHT = 320
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FB_DEVICE = "/dev/fb0"

def show_screen(lines):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 30)
    x = 20
    y = 20
    for line in lines:
        draw.text((x, y), line, font=font, fill=(255,255,255))
        y+= 40
    img.save("/home/pi/screen.png")
    subprocess.run(["fbi", "-T", "1", "-d", "/dev/fb0", "-noverbose", "-a", "/home/pi/screen.png"])

def wait_for_button():
    while True:
        if GPIO.input(13) == GPIO.LOW:
            time.sleep(0.3)
            return 3
        if GPIO.input(16) == GPIO.LOW:
            time.sleep(0.3)
            return 2
        if GPIO.input(26) == GPIO.LOW:
            time.sleep(0.3)
            return 1
        

def show_front(word):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 30)

    x = WIDTH // 2 - (len(word) * 30 // 4)
    y = HEIGHT // 2 - 30
    draw.text((x, y), word, font=font, fill=(255, 255, 255))
    img.save("/home/pi/screen.png")
    subprocess.run(["fbi", "-T", "1", "-d", "/dev/fb0", "-noverbose", "-a", "/home/pi/screen.png"])

def show_back(translation):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 30)

    x = WIDTH // 2 - (len(translation) * 30 // 4)
    y = HEIGHT // 2 - 30
    draw.text((x, y), translation, font=font, fill=(255, 255, 255))
    img.save("/home/pi/screen.png")
    subprocess.run(["fbi", "-T", "1", "-d", "/dev/fb0", "-noverbose", "-a", "/home/pi/screen.png"])

def show_menu_select(options, selected):
    img = Image.new("RGB", (WIDTH, HEIGHT), color=(0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, 30)
    y = 20
    for i, option in enumerate(options):
        if i == selected:
            draw.rectangle([(0, y), (WIDTH, y+35)], fill=(255, 255, 255))
            draw.text((20, y), option, font=font, fill=(0, 0, 0))
        else:
            draw.text((20, y), option, font=font, fill=(255, 255, 255))
        y += 50
    img.save("/home/pi/screen.png")
    subprocess.run(["fbi", "-T", "1", "-d", "/dev/fb0", "-noverbose", "-a", "/home/pi/screen.png"])

def navigate_menu(options):
    selected = 0
    show_menu_select(options, selected)
    while True:
        button = wait_for_button()
        if button == 1: 
            selected = (selected - 1) % len(options)
            show_menu_select(options, selected)
        if button == 2: 
            selected = (selected + 1) % len(options)
            show_menu_select(options, selected)
        if button == 3:  
            return selected