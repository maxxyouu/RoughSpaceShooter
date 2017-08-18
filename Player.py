import pygame
import random
import Constants

from Health import *
from Bullets import *

class Player(pygame.sprite.Sprite):
    """single player class"""
    
    def __init__(self):
        """
        @type size_x: int the width of the enemy
        @type size_y: int the height of the enemy
        @type color: tuple the RGB color value of the enemy
        """
        super().__init__()

        self.image = pygame.Surface([Constants.PLAYER_WIDTH, Constants.PLAYER_HEIGHT])
        self.image.fill(Constants.PLAYER_COLOR)
        self.rect = self.image.get_rect()

        # assign midbottom position to the player
        pos_x, pos_y = Constants.SCREEN_WIDTH // 2, Constants.SCREEN_HEIGHT - 100
        self.rect.x, self.rect.y = pos_x, pos_y
        self.change_x, self.change_y = 0, 0
        self.position = self.rect.x, self.rect.y  # use for animation


        self.player_health = Player_Health()

        self.enemy_targets = None  # a group of enemy sprites for colision uses
        self.enemy_killed = 0
        self.double_SMbullet_threhold = 0
        self.double_BGbullet_threhold = 0


        # handle fire frequency
        self.enemy_timer = pygame.time.get_ticks()
        self.smBullet_timer = pygame.time.get_ticks()
        self.bgBullet_timer = pygame.time.get_ticks()
        # the follow are valuables that smooth the game
        self.enemy_attact_interval = 80
        self.sm_bullet_attack_interval = 100
        self.bg_bullet_attack_interval = 100

        # used to increase the streth for each weapon
        self.power = Power()

        # sprite group of the game
        self.allSprites_group = None
        self.bullets_group = None

    def update(self):
        #handle speed
        self.rect.x += self.change_x
        self.rect.y += self.change_y

        self.handle_enemy_collisions()

    def handle_enemy_collisions(self):
        """handle collision with enemy objects"""
        now = pygame.time.get_ticks()
        if now - self.enemy_timer >= self.enemy_attact_interval:
            self.enemy_timer = now
            hit_list = pygame.sprite.spritecollide(self, self.enemy_targets, False)
            if len(hit_list) > 0:  # handle animation here
                hit_animation = PlayerHitAnimator([20, 20], self)
                self.allSprites_group.add(hit_animation)
                for enemy in hit_list:
                    self.player_health.reduce_health(enemy.damage_value)
    
    def update_enemy_kills(self, killed):
        """update the enemy kills"""
        self.enemy_killed += killed

    def handle_movement(self, pos_x, pos_y):
        """handle event to move the player
        @type key_pressed: returned get_pressed obj
        @type reset: bool
            if true, set all value back to zero
        """
        self.rect.x, self.rect.y = pos_x, pos_y
        self.position = self.rect.x, self.rect.y  # update the position

    def fire_bullets(self, event):
        """handle event to fire bullets
        @return bullet or tuple of bullets
        """
        if event.key == pygame.K_z:
            self.fire_smallWeapon()
        if event.key == pygame.K_x:
            self.fire_bigWeapon()
        if event.key == pygame.K_c:
            if self.power.current_power >= 100:
                self.double_fire_smallBullet()
        if event.key == pygame.K_v:
            if self.power.current_power >= 150:
                self.double_fire_bigBullet()

    def fire_smallWeapon(self):
        """fire small bullet within the fire_interval
        @return smallWeapon()
        """
        now = pygame.time.get_ticks()
        if now - self.smBullet_timer >= self.sm_bullet_attack_interval:
            self.smBullet_timer = now

            sm_bullet = SmallWeapon()
            # place it the position of the player
            mid_x, mid_y = self.rect.midtop
            sm_bullet.rect.x = mid_x
            sm_bullet.rect.y = mid_y
            sm_bullet.add(self.allSprites_group, self.bullets_group)
    
    def fire_bigWeapon(self):
        """fire big weapon within the fire_interval
        @return BigWeapon()
        """
        now = pygame.time.get_ticks()
        if now - self.bgBullet_timer >= self.bg_bullet_attack_interval:
            self.bgBullet_timer = now

            bg_bullet = BigWeapon()
            # place it the position of the player
            mid_x, mid_y = self.rect.midtop
            bg_bullet.rect.x = mid_x
            bg_bullet.rect.y = mid_y
            bg_bullet.add(self.allSprites_group, self.bullets_group)

    def double_fire_smallBullet(self):
        """double fire side by side
        only fire this if the power value is greater than 100
        """
        
        leftB = SmallWeapon()
        rightB = SmallWeapon()
        leftB.rect.x, leftB.rect.y = self.rect.topleft
        rightB.rect.x, rightB.rect.y = self.rect.topright

        # reset the power value and bar
        self.power.clear_power(100)
        self.bullets_group.add(leftB, rightB)
        self.allSprites_group.add(leftB, rightB)

    def double_fire_bigBullet(self):
        """double fire side by side"""
        leftB = BigWeapon()
        rightB = BigWeapon()
        leftB.rect.x, leftB.rect.y = self.rect.topleft
        rightB.rect.x, rightB.rect.y = self.rect.topright

        # reset the power bar and value
        self.power.clear_power(200)
        self.bullets_group.add(leftB, rightB)
        self.allSprites_group.add(leftB, rightB)

    # handle all the survival pack collisions

    def handle_collisions_with_medicalPack(self, healthPack):
        """handle collisions with the medical pack
        @type healthPack: medicalsprite obj
        TODO:
        1: increase the health if not full
        this method intends to handle in the gmaeController class
        """
        self.player_health.gain_health(healthPack.health_value)

    def handle_collisions_with_powerUp(self, powerUpPack):
        """handle collisions with powerup packs
        @type powerUpPack: powerUp sprite obj
        TODO:
        1: increase the self.power obj value
        """
        self.power.gain_power(powerUpPack.power_value)


    def handle_bullet_collisions(self):
        """ collisions with enemy bullets

        assump the self is collided
        @type sprite_groups: a list of sprite groups
        """
        if self.player_health.current_health <= 0:
            self.kill()
        else:
            # remove health value
            self.player_health.reduce_health(10)


class PlayerHitAnimator(pygame.sprite.Sprite):
    """once the player get hitted, play the animation"""

    def __init__(self, size, player):
        """
        @type player:player sprite
        """
        super().__init__()
        self.player = player
        self.size = size
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.player.rect.x, self.player.rect.y
        self.image.fill(Constants.BLUE)
        self.frame_Rate = 20  # smooth timer
        self.current_time = pygame.time.get_ticks()
        self.tracker = 0

    def update(self):
        """update the animation"""
        now = pygame.time.get_ticks()
        if now - self.current_time >= self.frame_Rate:

            #get the current position of the player
            position = self.player.position  # tuple of position

            if self.tracker == 4:
                self.kill()
            self.current_time = now
            self.image = pygame.Surface(self.size)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = position  # put the image at the player location
            if self.tracker % 2 == 0:
                self.image.fill(Constants.RED)
            else:
                self.image.fill(Constants.BLUE)
            self.tracker += 1

    
