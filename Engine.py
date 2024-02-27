import pygame, sys
from random import choice, randint
from Settings import *
from Player import *
from Alien import *
from Laser import *
import Obstacle

class Game:
    def __init__(self):
        #Player
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10), SCREEN_WIDTH, 5)
        self.player = pygame.sprite.GroupSingle(player_sprite)

        #Health / Score
        self.lives = 3
        self.live_surface = pygame.image.load("Sprites\player.png").convert_alpha()
        self.live_x_start_pos = SCREEN_WIDTH - (self.live_surface.get_size()[0] * 2 + 20)
        self.score = 0
        self.font = pygame.font.Font("Font\Pixeled.ttf")

        #Obstacle
        self.shape = Obstacle.shape
        self.block_size = 6
        self.blocks = pygame.sprite.Group()
        self.obstacle_amount = 4
        self.obstacle_x_position = [num * (SCREEN_WIDTH / self.obstacle_amount) for num in range(self.obstacle_amount)]
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start = SCREEN_WIDTH / 14, y_start = 480)

        #Alien
        self.aliens = pygame.sprite.Group()
        self.alien_lasers = pygame.sprite.Group()
        self.alien_setup(rows = 6, cols = 8)
        self.alien_direction = 1

        #Extra
        self.extra = pygame.sprite.GroupSingle()
        self.extra_spawn_time = randint(40, 80)

    def create_obstacle(self, x_start, y_start, offset_x):
        for row_index, row in enumerate(self.shape):
            for col_index, col in enumerate(row):
                if col == "x":
                    x = x_start + col_index * self.block_size + offset_x
                    y = y_start + row_index * self.block_size
                    block = Obstacle.Block(self.block_size, (241, 79, 80), x, y)
                    self.blocks.add(block)

    def create_multiple_obstacles(self, *offset, x_start, y_start):
        for offset_x in offset:
            self.create_obstacle(x_start, y_start, offset_x)
    
    def alien_setup(self, rows, cols, x_offset = 70, y_offset = 100, x_distance = 60, y_distance = 48):
        for row_index, row in enumerate(range(rows)):
            for col_index, col in enumerate(range(cols)):
                x = col_index * x_distance + x_offset
                y = row_index * y_distance + y_offset
                if row_index == 0:
                    alien_sprite = Alien("yellow", x, y)
                elif 1 <= row_index <= 2:
                    alien_sprite = Alien("green", x, y)
                else:
                    alien_sprite = Alien("red", x, y)
                self.aliens.add(alien_sprite)

    def alien_position_check(self):
        all_aliens = self.aliens.sprites()
        for alien in all_aliens:
            if alien.rect.right >= SCREEN_WIDTH:
                self.alien_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= 0:
                self.alien_direction = 1
                self.alien_move_down(2)

    def alien_move_down(self, distance):
        if self.aliens:
            for alien in self.aliens.sprites():
                alien.rect.y += distance

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, SCREEN_HEIGHT)
            self.alien_lasers.add(laser_sprite)

    def extra_alien_time(self):
        self.extra_spawn_time -= 1
        if self.extra_spawn_time <= 0:
            self.extra.add(Extra(choice(["right", "left"]), SCREEN_WIDTH))
            self.extra_spawn_time = randint(0, SCREEN_WIDTH)

    def collision_check(self):
        #Player laser
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                #Obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                #Alien
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.value
                    laser.kill()
                #Extra
                if pygame.sprite.spritecollide(laser, self.extra, True):
                    self.score += 1000
                    laser.kill()

        #Alien laser
        if self.alien_lasers:
            for laser in self.alien_lasers:
                #Obstacle
                if pygame.sprite.spritecollide(laser, self.blocks, True):
                    laser.kill()
                #Player
                if pygame.sprite.spritecollide(laser, self.player, False):
                    laser.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        pygame.quit()
                        sys.exit()

        #Alien
        if self.aliens:
            for alien in self.aliens:
                pygame.sprite.spritecollide(alien, self.blocks, True)
                if pygame.sprite.spritecollide(alien, self.player, False):
                    pygame.quit()
                    sys.exit()
                
    def display_lives(self):
        for live in range(self.lives - 1):
            x = self.live_x_start_pos + (live * (self.live_surface.get_size()[0] + 10))
            screen.blit(self.live_surface, (x, 8))

    def display_score(self):
        score_surface = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surface.get_rect(topleft = (10, -10))
        screen.blit(score_surface, score_rect)

    def run(self):
        self.player.update()
        self.aliens.update(self.alien_direction)
        self.alien_position_check()
        self.alien_lasers.update()
        self.extra_alien_time()
        self.extra.update()
        self.collision_check()
        self.display_lives()

        self.player.sprite.lasers.draw(screen)
        self.player.draw(screen)        

        self.blocks.draw(screen)
        self.aliens.draw(screen)
        self.alien_lasers.draw(screen)
        self.extra.draw(screen)
        self.display_score()

if __name__ == '__main__':

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    game = Game()

    ALIENLASER = pygame.USEREVENT + 1
    pygame.time.set_timer(ALIENLASER, 800)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == ALIENLASER:
                game.alien_shoot()

    
        screen.fill(SCREEN_COLOR)
        game.run()
    
        pygame.display.flip()
        clock.tick(CLOCK_TICK)