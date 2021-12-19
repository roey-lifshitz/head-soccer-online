import socket
import pygame
from pygame.locals import *

pygame.init()

PORT = 5555
HOST = socket.gethostbyname(socket.gethostname())  # Automatically get local ip4 address
ADDR = (HOST, PORT)

RESIZE_PERCENT = 1
SCREEN_WIDTH = int(pygame.display.Info().current_w * RESIZE_PERCENT)
SCREEN_HEIGHT = int(pygame.display.Info().current_h * RESIZE_PERCENT)

DISPLAY_PRINT = False
FPS = 60
TARGET_FPS = 60


# Imports pygame constant keybinds for easier access




