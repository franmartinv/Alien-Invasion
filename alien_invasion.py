import sys

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()    # sirve para agrupar los sprites de las balas
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Configura el color de fondo
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:
            self._check_events()
            self.ship.update()
            self.bullets.update()
            self._update_bullets()
            self._update_screen()
    
    def _check_events(self):
        """Responde a las pulsaciones de teclas y eventos de raton"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Responde a pulsaciones de teclas
        if event.key == pygame.K_RIGHT:
            # Mueve la nave a la derecha
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # Mueve la nave a la izquierda
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            # Mueve la nave abajo
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            # Mueve la nave arriba
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            # Disparo una bala
            self._fire_bullet()
        elif event.key == pygame.K_q:
            sys.exit()
    
    def _check_keyup_events(self, event):
        # Responde a liberacion de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """Crea una bala nueva y la añade al grupo de balas"""
        if len(self.bullets) < self.settings.bullets_allowed:   # limitacion del numero de balas en pantalla
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Actualiza la posicion de las balas y se deshace de las viejas"""
        # Actualiza las posiciones de las balas
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))

    def _create_fleet(self):
        """Crea una flota de aliens"""
        # Crea un alien y halla el numero de aliens en una fila
        # El espacio entre aliens es igual a la anchura de un alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        #number_aliens_x = available_space_x // (2 * alien_width) # si metes un +1 queda mejor visualmente
        number_aliens_x = 1 + available_space_x // (2 * alien_width)

        # Determinar el numero de filas de aliens que caben en la pantalla
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Crea la flota completa de aliens
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x): 
                self._create_alien(alien_number, row_number)
            
    
    def _create_alien(self, alien_number, row_number):
        # Crea un alien y lo coloca en la fila
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _update_screen(self):
        # Redibuja la pantalla en cada paso por el bucle
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        
        # Hace visible la última pantalla dibujada
        pygame.display.flip()

if __name__ == "__main__":
    # hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game()
