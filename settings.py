class Settings:
    """Una clase para guardar toda la configuracion de Alien Invasion"""

    def __init__(self):
        """Inicializa la configuracion del juego"""
        # Configuracion de la pantalla
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Configuracion de la velocidad de la nave
        self.ship_speed = 3
        self.ship_limit = 5

        # Configuracion de las balas
        self.bullet_speed = 2
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,0,0)   # color rojo en este caso: RGB
        self.bullets_allowed = 20

        # Configuracion del alien
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction de 1 representa derercha; -1 representa izquierda
        self.fleet_direction = 1

        # lo rapido que aumenta el valor en puntos de los aliens
        self.score_scale = 1.5

        # Rapidez con la que se acelera el juego
        self.speedup_scale = 1.1

        self.initialize_dynamic_settins()

    def initialize_dynamic_settins(self):
        """Inicializa las configuraciones que cambian durante el juego"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        #fleet_direction de 1 representa derecha, y -1 izquierda
        self.fleet_direction = 1

        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)