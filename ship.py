import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """Una clase para gestionar la nave"""

    def __init__(self, ai_game):
        """Inicializa la nave y configura su posición inicial"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        """Carga la imagen de la nave y obtiene su rect"""
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()

        # Coloca individualmente cada nave nueva en el centro de la parte inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        # Guarda un valor decimal para la posición horizontal de la nave
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Bandera de movimiento
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
    
    def update(self):
        """Actualiza la posicion de la nave en funcion de la bandera de movimiento"""
        # Actualiza el valor x de la nave, no el rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        
        # Actualiza el valor y de la nave, no el rect
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom <= self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        # Actualiza el objeto rect de self.x
        self.rect.x = self.x

        # Actualizo el objeto rect de self.y
        self.rect.y = self.y

    def blitme(self):
        """Dibuja la nave en su ubicación actual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centrar la nave en la pantalla"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)