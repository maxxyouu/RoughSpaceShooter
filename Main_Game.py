import pygame
import random

from Enemy import *
from Player import *
import Constants
from SurvivalPacks import MedicalPack, PowerUp


class GameController(object):
    """
    Hanle all the gameController logic within the gameController
    1: handle spawn internval time
    2: handle objects interations
    """
    def __init__(self, screen_x, screen_y, lower_enemies_bound, uppper_enemies_bound):
        """initialze all the gameController objects in the gameController
        """
        self.width, self.height = screen_x, screen_y

        self.enemy_upper_bound = uppper_enemies_bound
        self.enemy_lower_bound = lower_enemies_bound

        # initialize all sprite group
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.inheritance_packs = pygame.sprite.Group()
        # set up enemies objs and assign to the Groups

        self.enemies_counter = random.randint(self.enemy_lower_bound, self.enemy_upper_bound)
        self.enemies_set = {Enemy() for _ in range(self.enemies_counter)}
        self.enemy_spawn_wave_time = 1000
        self.enemy_spawn_timer = pygame.time.get_ticks()

        self.enemies_per_wave = 1  # increase this value to spawn enemies
        self.enemies_incrementer = 1  # crease this value


        #player obj
        self.player = Player()
        self.player_group.add(self.player)
        # add the power obj to the sprite
        self.all_sprites.add(self.player.power)
        # assign the sprite groups to the player for interaction
        self.player.allSprites_group = self.all_sprites
        self.player.bullets_group = self.bullets

        #update the enemies targets
        self.player.enemy_targets = self.enemies  
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.player.player_health)

    def spawn_enemies(self):
        """spawn enemies with random number of enemies per wave by add the enemy to the sprite group"""
        now = pygame.time.get_ticks()
        if (now - self.enemy_spawn_wave_time) >= self.enemy_spawn_timer:
            self.enemy_spawn_timer = now

            enemiesNum = self.enemies_per_wave
            # update the enemies for next round 
            self.enemies_per_wave += self.enemies_incrementer
            # self.enemies_incrementer += 1

            self.enemies_counter -= enemiesNum
            if enemiesNum <= len(self.enemies_set):
                for _ in range(enemiesNum):
                    random_enemy = self.enemies_set.pop()
                    random_enemy.add(self.enemies, self.all_sprites)
                    # add health sprite
                    self.all_sprites.add(random_enemy.enemy_health)
           

    def events_handler(self):
        """handle exit events and movemnt events"""
        # handle movements from the mouse
        pos_x, pos_y = pygame.mouse.get_pos()
        self.player.handle_movement(pos_x, pos_y)  # change the self.change_x & y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_z 
                    or event.key == pygame.K_x 
                    or event.key == pygame.K_c 
                    or event.key == pygame.K_v):
                    # restrite key input prevent crccashes
                    self.player.fire_bullets(event)
        return False

    def playerBullets_enemies_collision_handler(self):
        """z
        TODO:
        1: remove playerBullet objects
        2: enemies collisions
        3: handle inheritance packs if enemy died
        """
        for p_bullet in self.bullets:
            hit_list = pygame.sprite.spritecollide(p_bullet, self.enemies, False)
            all_enemies = len(hit_list)
            if all_enemies != 0:
                # update player number of kills
                self.player.update_enemy_kills(all_enemies)
                # remove the bullet from the screen
                p_bullet.kill()
                # remove enemy objs if nessary
                for enemy in hit_list:
                    packs = enemy.handle_bullet_collisions()
                    # here, add the inheritance pack to the sprite gorup
                    if packs is not None:
                        packs.add([self.inheritance_packs, self.all_sprites])  # which mean there exist a pack

    def player_SurvivalPack_collisions_handler(self):
        """handle the collisions between player and survival packs"""
        hitted_packs = pygame.sprite.spritecollide(self.player, self.inheritance_packs, True)
        for pack in hitted_packs:
            if pack.id == 0:  # if this is a medical pack
                # handle player and medical pack collisions
                print('in the health pack')
                self.player.handle_collisions_with_medicalPack(pack)
            elif pack.id == 1:
                self.player.handle_collisions_with_powerUp(pack)

    def draw_frame(self, screen):
        """update the screen by updating all sprites and screen"""
        
        # call all the update funtions in the all sprites group
        self.all_sprites.update()

        screen.fill(Constants.WHITE)
        
        self.all_sprites.draw(screen)
        
        pygame.display.flip()


def main():
    gameController = GameController(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 30, 50)
    
    screen = pygame.display.set_mode([Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT])  # screen Surface
    screen.fill(Constants.WHITE)
    pygame.display.set_caption('Ultimate Space Shooter')
    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    
    done = False
    while not done:
        # handle all events
        done = gameController.events_handler()

        gameController.spawn_enemies()
        # handle logic part
        gameController.playerBullets_enemies_collision_handler()
        # gameController.player_enemies_collision_handler()
        gameController.player_SurvivalPack_collisions_handler()
        # handle flip animate
        gameController.draw_frame(screen)


        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()