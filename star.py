import pygame
from pygame.sprite import Sprite

class Star(Sprite):
    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen

        # Carga la imagen de la estrella y configura su atributo rect
        self.image = pygame.image.load("images/star.png")
        self.rect = self.image.get_rect()

        # Inicia un nuevo alien cerca de la parte superior izquierda de la pantalla
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Guarda la posicion horizontal exacta de la estrella
        self.x = float(self.rect.x)
