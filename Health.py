import pygame
import Constants

class Health(pygame.sprite.Sprite):
    def __init__(self, health_size, color, position):
        """
        @type health_size: tuple
        @type color: RGB tuple
        @type position: tuple
        """
        super().__init__()

        self.image = pygame.Surface(health_size)
        self.rect = self.image.get_rect()

        self.health_color = color
        # set the color of the rectangle
        self.image.fill(self.health_color)

        self.position = position
        # set the position of the healthbar
        self.rect.x, self.rect.y = self.position
        self.current_health = health_size[0]
    
    def reduce_health(self, amount):
        """reduce the health value by that <amount>"""
        self.current_health -= amount


class Player_Health(Health):
    """healthbar for the player"""

    health_size = (10, 20)
    full_size = 200
    health_color = (0, 255, 0)
    health_posi = (10, 550)

    def __init__(self):
        Health.__init__(self, self.health_size, self.health_color, self.health_posi)
        self.current_health = self.health_size[0]

    def gain_health(self, amount):
        """gain the health value by that <amount>"""

        total_health = self.current_health + amount
        # only gain health when no excess
        if total_health <= self.full_size:
            self.current_health = total_health
        # erase the color
        self.image = pygame.Surface([self.current_health, self.health_size[1]])
        self.rect = self.image.get_rect()
        self.image.fill(Constants.GREEN)
        # update the power bar position
        self.rect.x, self.rect.y = self.position

    def reduce_health(self, amount):

        super().reduce_health(amount)
        # erase the color
        self.image.fill(Constants.WHITE)
        
        if self.current_health <= 0:
            self.current_health = 0

        self.image = pygame.Surface([self.current_health, self.rect.height])
        if self.current_health <= 10:
            self.image.fill(Constants.RED)
        else:
            self.image.fill(self.health_color)

        self.rect = self.image.get_rect()
        # update the position of the health bar
        self.rect.x, self.rect.y = self.position


class Enemy_Health(Health):

    offset = 10  # initial offset position
    enemy_health_size = (50, 10)
    health_color = (0, 255, 0)

    def __init__(self, enemy_rect, enemy_x_speed, enemy_y_speed):
        """
        @type enemy: enemy obj
        """
        # control the enemy position
        self.current_enemy_pos = enemy_rect.x, enemy_rect.y - self.offset

        Health.__init__(self, self.enemy_health_size, self.health_color, self.current_enemy_pos)

        # used to track the enemy at the same relative position
        self.enemy_x_speed = enemy_x_speed
        self.enemy_y_speed = enemy_y_speed
        self.current_health = self.enemy_health_size[0]

    def reduce_health(self, amount):
        super().reduce_health(amount)

        self.image.fill(Constants.WHITE)

        if self.current_health >= 0:
            # update current health value
            self.image = pygame.Surface([self.current_health, self.rect.height])

            # change the health bar color at th end
            if self.current_health <= 10:
                self.image.fill(Constants.RED)
            else:
                self.image.fill(self.health_color)

            self.rect = self.image.get_rect()
            # get the position of the enemy
            self.rect.x = self.current_enemy_pos[0]
            self.rect.y = self.current_enemy_pos[1] - self.offset # minus the delta position
            self.position = self.rect.x, self.rect.y

    def update_speed_change(self, newX, newY):
        """update the parent enemy speed for tracking"""
        self.enemy_x_speed = newX
        self.enemy_y_speed = newY

    def update_current_enemy_pos(self, enemy_rect):
        """update the enemy position
        @type enemy: enemy rectangle object
        """
        self.current_enemy_pos = enemy_rect.x, enemy_rect.y

    def update(self):
        """follow the path of the enemy_Rect"""
        # follow enemy
        self.rect.x += self.enemy_x_speed
        self.rect.y += self.enemy_y_speed
        # follow enemy position when reduce


class Power(pygame.sprite.Sprite):
    """power values for the player"""

    #size = (200, 20)
    size = (200, 20)
    full_size = 200
    position = (10, 520)

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_rect()
        
        self.image.fill(Constants.BLUE)

        self.rect.x, self.rect.y = self.position

        self.current_power = self.size[0]
    
    def gain_power(self, amount):
        """gain the <amount> power of this object once collided with survial packs"""
        
        total_power = self.current_power + amount

        # if total power not exceed the limits
        if total_power <= self.full_size:
            #update power value
            self.current_power += amount
            # erase the color
            self.image.fill(Constants.WHITE)
            # draw the powerbar
            self._draw_powerbar(self.current_power)

    def clear_power(self, amount=200):
        """clear the current powervalue up to amount
        clear the power by that amount: default is total length of the bar
        """
        if self.current_power >= amount:
            # clear the value and rectangle image
            self.current_power -= amount
        else:
            self.current_power = 0
        self.image.fill(Constants.WHITE)
        self._draw_powerbar(self.current_power)
    
    def _draw_powerbar(self, width):
        self.image = pygame.Surface([width, self.size[1]])
        self.rect = self.image.get_rect()
        self.image.fill(Constants.BLUE)
        # update the power bar position
        self.rect.x, self.rect.y = self.position


