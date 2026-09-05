import os
import pygame

# Proveravamo da li postoji fajl /etc/rpi-issue (to znači da smo na RPi-ju)
is_pi = os.path.exists('/etc/rpi-issue')

if is_pi:
    # Ako smo na RPi-ju, kažemo Pygame-u da crta direktno na SPI ekran preko framebuffer-a
    os.environ["SDL_FBDEV"] = "/dev/fb0"
    os.environ["SDL_MOUSEDEV"] = "/dev/input/event0"
    os.environ["SDL_MOUSEDRV"] = "TSLIB"

pygame.init()

WIDTH = 320
HEIGHT = 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

if is_pi:
    pygame.mouse.set_visible(False)
else:
    pygame.mouse.set_visible(True)

ljub1 = (17, 8, 24)       
ljub2 = (48, 22, 49)      
roz1 = (99, 55, 102)      
roz2 = (194, 101, 169)    

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (50, 50, 50)

font_large = pygame.font.SysFont("dejavusans", 40)
font_medium = pygame.font.SysFont("dejavusans", 30)
font_small = pygame.font.SysFont("dejavusans", 20)

def draw_text_centered(text, font, color, y):
    """Crta tekst centrirano po X osi na zadatoj Y koordinati."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(WIDTH // 2, y))
    screen.blit(text_surface, text_rect)

def draw_button(rect, text, color):
    """Crta dugme (pravougaonik) i centriran tekst unutar njega."""
    pygame.draw.rect(screen, color, rect)
    
    # Tekst unutar dugmeta je uvek beli
    text_surface = font_small.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)