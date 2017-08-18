"""
all the medical and powerup packs only move 1-dimensional (y-axis)
"""
import pygame
import Constants
import random

class SurvivalPacks(pygame.sprite.Sprite):
    """super class for player survival packs
    """
    size = (10, 10)
    def __init__(self, enemy):
        """
        @type enemy: enemy sprite object
            this get the position for the powerup object after the object is destroyed
        """
        super().__init__()
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()

        self.rect.x, self.rect.y = enemy.rect.x, enemy.rect.y

        # generate random velocity and direction both x and y
        self.y_velocity = random.randrange(1,2)
        self.x_velocity = random.randrange(-1, 1)
        
        # identity of this sprite
        self.id = 0

    def update(self):
        self.rect.y += self.y_velocity
        self.rect.x += self.x_velocity

        self.handle_boundaries()

    def update_enemy_pos(self, pos_x, pos_y):
        """update the enemy position"""
        self.rect.x, self.rect.y = pos_x, pos_y
    
    def handle_boundaries(self):
        """when it hit boundaries, it is removed from the game"""
        if self.rect.x < 0 or self.rect.x > Constants.SCREEN_WIDTH or self.rect.y > Constants.SCREEN_HEIGHT:
            self.kill()
        
class PowerUp(SurvivalPacks):
    """
    power up object for the player
    1. this power up object is appeared after the enemy is destroyed
    """

    def __init__(self, enemy):
        """
        @type enemy: enemy sprite object
            this get the position for the powerup object after the object is destroyed
        """
        super().__init__(enemy)
        self.image.fill(Constants.BLUE)
        # randomize the powerup value
        self.power_value = random.randint(20, 60)

        # identity of this sprite
        self.id = 1
    
    
class MedicalPack(SurvivalPacks):
    """
    medical pack for the player
    1: used to gain health for the player
    """

    def __init__(self, enemy):
        """
        @type enemy: enemy sprite object
            this get the position for the powerup object after the object is destroyed
        """
        super().__init__(enemy)
        self.image.fill(Constants.GREEN)
        
        # randomized the health value assigned to this objects
        self.health_value = random.randint(20, 50)

