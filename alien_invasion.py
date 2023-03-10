import sys
from random import randint
from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from star import Star
from button import Button
from scoreboard import Scoreboard

class AlienInvasion:
    """Clase general para gestionar los recursos y el comportamiento del juego"""

    def __init__(self):
        """Inicializa el juego y crea recursos"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Crea una instancia para guardar las estadisticas del juego y un marcador
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()    # sirve para agrupar los sprites de las balas
        self.aliens = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        self._create_stars()
        self._create_fleet()
        self.play_button = Button(self, "Play")

        # Configura el color de fondo
        self.bg_color = (230, 230, 230)

    def run_game(self):
        """Inicia el bucle principal para el juego"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()    
    
    def _check_events(self):
        """Responde a las pulsaciones de teclas y eventos de raton"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_play_button(self, mouse_pos):
        """Inicia el juego una vez el jugador clickee en Play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Restablece las configuraciones del juego
            self.settings.initialize_dynamic_settins()
            
            # Restablece las estadisticas del juego
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            # Oculta el cursor del raton
            pygame.mouse.set_visible(False)

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
        """Crea una bala nueva y la a??ade al grupo de balas"""
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

        self._check_bullet_alien_collisions()        
    
    def _check_bullet_alien_collisions(self):
        # Responde a las colisiones bala-alien
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        if not self.aliens:
            # Destruye las balas existentes y crea una flota nueva
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Aumenta el nivel
            self.stats.level += 1
            self.sb.prep_level()

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

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
          then update the positions of all aliens in the fleet.
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Busca colisiones alien-nave
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Nave herida!!")
            self._ship_hit()

        # Busca aliens llegando al fondo de la pantalla
        self._check_aliens_bottom()

    def _change_fleet_direction(self):
        """Baja toda la flota y cambia su direccion"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_fleet_edges(self):
        """Responde adecuadamente si alg??n alien ha llegado a un borde"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _ship_hit(self):
        """Responde al impacto nave-alien"""
        if self.stats.ships_left > 0:
            # Disminuye ships_left y actualiza el marcador
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            # Se deshace de los aliens y balas restantes
            self.aliens.empty()
            self.bullets.empty()

            # Crea una flota nueva y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            # Pausa el juego
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Comprueba si algun alien ha llegado al fondo de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Trata esto como si la nave hubiese sido alcanzada
                self._ship_hit()
                break

    def _create_stars(self):
        """Create a sky full of stars."""
        # Create an star and find the number of stars in a row.
        # Spacing between each star is equal to two star widths.
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - (star_width)
        number_stars_x = available_space_x // (2 * star_width)
        
        # Determine the number of rows of stars that fit on the screen.
        #   We'll just fill most of the screen with stars.
        available_space_y = (self.settings.screen_height -
                                (2 * star_height))
        number_rows = available_space_y // (2 * star_height)
        
        # Fill the sky with stars.
        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        """Create an star and place it in the row."""
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = star_width + 2 * star_width * star_number
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number

        # Randomize the positions of the stars.
        #  This effect looks much better with a tiny star. If you're curious,
        #  you might want to play around with the spacing a little.
        star.rect.x += randint(-5, 5)
        star.rect.y += randint(-5, 5)

        self.stars.add(star)

    def _update_screen(self):
        # Redibuja la pantalla en cada paso por el bucle
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Dibuja la informacion de la puntuacion
        self.sb.show_score()

        # Dibuja el boton para jugar si el juego esta inactivo
        if not self.stats.game_active:
            self.play_button.draw_button()
        
        # Hace visible la ??ltima pantalla dibujada
        pygame.display.flip()

if __name__ == "__main__":
    # hace una instancia del juego y lo ejecuta
    ai = AlienInvasion()
    ai.run_game()
