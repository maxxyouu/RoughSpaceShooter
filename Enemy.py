import pygame
import Constants
import random
from Health import Enemy_Health
from SurvivalPacks import PowerUp, MedicalPack

class Enemy(pygame.sprite.Sprite):
    """Enemy class
    1: handle movement of the enermy
    2: handle random bullet fire of the enermy only 10% chance of the time fire bullet
    3: update enermy health
    """
    enemy_width = 20
    enemy_height = 20
    enemy_color = (0, 0, 0)
    
    def __init__(self):
        """
        @type size_x: int the width of the enermy
        @type size_y: int the height of the enermy
        @type color: tuple the RGB color value of the enemy
        @type pos: tuple of coordinates of the enermy
        """
        super().__init__()

        self.image = pygame.Surface([self.enemy_width, self.enemy_height])
        self.image.fill(self.enemy_color)
        self.rect = self.image.get_rect()

        pos_x, pos_y = random.randrange(0, Constants.SCREEN_WIDTH), random.randint(-Constants.SCREEN_HEIGHT, 0)
        self.rect.x, self.rect.y = pos_x, pos_y

        # set random speed and direction of the enemy
        self.x_speed= random.randrange(-1,1)
        self.y_speed = 2

        self.enemy_health = Enemy_Health(self.rect, self.x_speed, self.y_speed)
        self.enemy_health.enemy_pos = self.rect.x, self.rect.y

        # generate random position to fire
        self.rand_y = random.randint(-Constants.SCREEN_HEIGHT, -(Constants.SCREEN_HEIGHT // 2)) 

        # every enemy object has inheritance packs after being destroyed
        # the amount the type of packs are randomized
        pack_determinant = random.randint(-1, 1)
        if pack_determinant == -1 or pack_determinant == 0:  # has powerup pack
            self.inheritance_packs = PowerUp(self)
        elif pack_determinant == 1:
            self.inheritance_packs = MedicalPack(self)

        self.damage_value = random.randrange(2, 6)

    def update(self):
        """update this sprite each frame, return None"""
        self.handle_movement()
        self.handle_side_boundaries()
        self.handle_vertical_boundaries()
    
    def handle_movement(self):
        """random movments in x direction, move down the screen in constant speed and direction"""
        # update the change of position so healthbar can track
        self.enemy_health.update_current_enemy_pos(self.rect)
        
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
    
    def handle_side_boundaries(self):
        """if the enemy hit the side boundary, come back from the other sides"""
        if self.rect.x < 0 or self.rect.x > (Constants.SCREEN_WIDTH-20):
            self.x_speed = -self.x_speed
            self.enemy_health.update_speed_change(self.x_speed, self.y_speed)
        
    def handle_vertical_boundaries(self):
        """delete self sprite from all group in sprite list
        @type sprite_list: a list of sprite group
        """
        if self.rect.y > Constants.SCREEN_HEIGHT:
            self.kill()
    
    def handle_bullet_collisions(self):
        """remove self and self.health sprites from sprite_group if <= 0
           else: reduce health value

        assump the self is collided
        @return None|inheritance pack
        """
        # reduce the health value of the enemy
        self.enemy_health.reduce_health(10)

        if self.enemy_health.current_health <= 0: # remove enemy sprite from enemies Group
            self.kill()
            self.inheritance_packs.update_enemy_pos(self.rect.x, self.rect.y)
            return self.inheritance_packs
        return None
