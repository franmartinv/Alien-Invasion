class Settings:
    """Una clase para guardar toda la configuracion de Alien Invasion"""

    def __init__(self):
        """Inicializa la configuracion del juego"""
        # Configuracion de la pantalla
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # Configuracion de la velocidad de la nave
        self.ship_speed = 1.5