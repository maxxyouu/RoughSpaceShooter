import pygame
import Constants

class Bullets(pygame.sprite.Sprite):
    """General class for all the bullets in the game"""

    def __init__(self, size, bullet_type):
        """
        @type size: tuple width and height
        @type bullet_type: int|Str
            player bullets are int, enemy bullets are str
        """
        super().__init__()

        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()

        self.bullet_type = bullet_type

        # fill the color for the weapon
        if self.bullet_type == 0: 
            self.image.fill(Constants.BLACK)
        elif self.bullet_type == 1: 
            self.image.fill(Constants.RED)
        elif  self.bullet_type == 'A':
            self.image.fill(Constants.GREEN)
    
    def handle_boundaries_collisions(self):
        """remove self from all the sprite_groups
        @type sprite_groups: list of groups
        """
        if self.rect.y < 0:
            self.kill()

    def update(self):
        """update the position of the smallweaphon down the screen"""
        # self.handle_enemy_collision()
        self.rect.y -= 6
        self.handle_boundaries_collisions()

class SmallWeapon(Bullets):
    """small weapon for the player"""
    
    size = (4, 10)

    def __init__(self):
        Bullets.__init__(self, self.size, 0)


class BigWeapon(Bullets):
    """big weaphon for the player
    instiazite this when have enough power
    """
    
    size = (4, 10)

    def __init__(self):
        Bullets.__init__(self, self.size, 1)