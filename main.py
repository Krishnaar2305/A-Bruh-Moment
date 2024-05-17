import pygame
from pygame.locals import *
import object_classes, world
from pygame import mixer
import asyncio


pygame.mixer.pre_init(4400, -16, 2, 51)
mixer.init()
pygame.init()
# fps
clock = pygame.time.Clock()
fps = 60
screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("A Bruh Moment")
# define font
font_score = pygame.font.SysFont('Bahaus 93', 35)
# game variables
game_over = 0
tile_size = object_classes.tile_size
score = 0

world.key = 0
# define colors
white = (255,255,255)


#music
def play_music(lv):
    ground_level.stop()
    night_sound.stop()
    scary_sound.stop()
    if lv == 1 or lv == 2:
        ground_level.play(-1)
    elif lv == 3 or lv == 4:

        night_sound.play(-1)
    elif lv == 5:
        scary_sound.play(-1)
    else:
        victory_sound.play(-1)


jump_sound = mixer.Sound('music/jump.wav')
death_sound = mixer.Sound('music/bruh.wav')
ground_level = mixer.Sound('music/lv1and2.wav')
coin_sound = mixer.Sound('music/coin.wav')
night_sound = mixer.Sound('music/nightlevel.wav')
scary_sound = mixer.Sound('music/scaarymusic.wav')
victory_sound = mixer.Sound('music/victory.wav')
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over, stage):
        # get keys
        self.dx = 0
        self.dy = 0
        walk_cooldown = 10
        col_threshold = 20
        # print(self.index)
        key = pygame.key.get_pressed()
        if game_over == 0:
            if self.counter >= walk_cooldown:
                self.counter = 0
                if self.index == 0:
                    self.index = 1
                else:
                    self.index = 0
            # is_run = False
            speed = 3
            if key[pygame.K_LEFT]:
                self.dx -= speed
                self.image = self.images_left[self.index]
                self.counter += 1
            if key[pygame.K_RIGHT]:
                self.dx += speed
                self.image = self.images_right[self.index]
                self.counter += 1
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                self.vel_y = -12.5
                self.jumped = True
                jump_sound.play()
            # if key[pygame.K_SPACE] == False:
            #     self.jumped = False
            # self.image = self.img
            ladder_collide = pygame.sprite.spritecollide(self, ladder_group, False)
            if key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
                self.image = self.default
                self.counter = 0
            # update player coordinates
            self.vel_y += 0.5
            if self.vel_y > 10:
                self.vel_y = 10
            self.dy += self.vel_y
            if ladder_collide:
                self.vel_y = 0
                self.dy = 0
                if self.climbed >= 10:
                    if self.index == 1:
                        self.index = 0
                        self.climbed = 0
                    else:
                        self.index = 1
                        self.climbed = 0
                if key[pygame.K_UP]:
                    self.dy -= 3
                    self.climbed += 1
                    # print(self.climbed)
                    self.image = self.climb[self.index]
                if key[pygame.K_DOWN]:
                    self.dy += 3
                    self.climbed += 1
                    self.image = self.climb[self.index]
                else:
                    self.image = self.climb[self.index]
            # check collision
            self.in_air = True
            #1 tiles
            ice_check = pygame.sprite.spritecollide(self, ice_block_group, False)
            for ice in ice_block_group:
                if ice.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.player[0], self.player[1]):
                    self.dx = 0
                if ice.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.player[0], self.player[1]):
                    if abs((self.rect.top + self.dy) - ice.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        self.dy = ice.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + self.dy) - ice.rect.top) < col_threshold:
                        self.rect.bottom = ice.rect.top - 1
                        self.dy = 0
                        if self.dx > 0:
                            self.dx -= self.dx/2
                        if self.dx < 0:
                            self.dx += self.dx/2
                        self.jumped = False
                        self.in_air = False
            for tile in stage.tile_list:
                if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.player[0], self.player[1]):
                    self.dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.player[0], self.player[1]):
                    if self.vel_y < 0:
                        self.dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        self.dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.jumped = False
                        self.in_air = False

            #2 enemy
            blobcol = pygame.sprite.spritecollide(self, blob_group, False)
            if blobcol:
                for blob in blobcol:
                    blob_center = blob.rect.centery
                    blob_top = blob.rect.top
                    player_bottom = self.rect.bottom
                    if blob_top < player_bottom < blob_center and self.vel_y > 0:
                        blob.kill()
                    else:
                        game_over = -1
            if pygame.sprite.spritecollide(self, lava_group, False) or pygame.sprite.spritecollide(self, mad_block_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, frog_group, False):
                game_over = -1
            if pygame.sprite.spritecollide(self, spring_group, False):
                world.draw_text('hold space', font_score, white, 350, 350, screen)
                if key[pygame.K_SPACE] and self.jumped == False:
                    self.vel_y = -16
                    self.jumped = True

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1
                # play_music(level + 1)

            #3 platforms
            for platform in platform_group:
                #x dir
                if platform.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.player[0], self.player[1]):
                    self.dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.player[0], self.player[1]):
                    if abs((self.rect.top + self.dy) - platform.rect.bottom) < col_threshold:
                        self.vel_y = 0
                        self.dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + self.dy) - platform.rect.top) < col_threshold:
                        self.rect.bottom = platform.rect.top - 1
                        self.dy = 0
                        self.jumped = False
                        self.in_air = False
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            if pygame.sprite.spritecollide(self, key_group, True):
                lava_group.empty()

            self.rect.x += self.dx
            self.rect.y += self.dy
            if self.rect.y >= 800:
                game_over = -1
            if self.rect.y <= 0:
                self.rect.y = 0
            if self.rect.x <= 0:
                self.rect.x = 0
        elif game_over == -1:
            self.image = pygame.image.load('images/alienblue/alienBlue_hurt.png')
        self.image = pygame.transform.scale(self.image, self.player)
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, (0,0,0), self, 2)

        return game_over

    def reset(self, x, y):
        self.player = (40, 60)
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        self.climb = []
        for num in range(1, 3):
            img_right = pygame.image.load(f"images/alienblue/alienBlue_walk{num}.png")
            self.images_right.append(img_right)
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_left.append(img_left)
            self.climb_img = pygame.image.load(f'images/alienblue/alienBlue_climb{num}.png')
            self.climb.append(self.climb_img)
        self.default = pygame.image.load("images/alienblue/alienBlue.png")
        self.image = self.default
        self.image = pygame.transform.scale(self.image, self.player)
        self.img_jump = pygame.image.load("images/alienblue/alienBlue_jump.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.double_jumped = False
        self.bottom = self.rect.bottom
        self.climbed = 0
        self.dx = 0
        self.dy = 0
        self.in_air = True
# load images
start_screen = pygame.image.load('images/startscreen.jpg')
sun_img = pygame.image.load('images/sun.png')
sun_img = pygame.transform.scale(sun_img, (200, 200))
bg_img = pygame.image.load('images/sky.jpg')
bg_img = pygame.transform.scale(bg_img, (800, 800))
night_img = pygame.image.load('images/night.jpg')
night_img = pygame.transform.scale(night_img, (800, 800))
castle_img = pygame.image.load('images/castle.jpg')
castle_img = pygame.transform.scale(castle_img, (800, 800))
over_img = pygame.image.load('images/gameover.png')
over_img = pygame.transform.scale(over_img, (350, 350))
try_img = pygame.image.load('images/try again.png')
try_img = pygame.transform.scale(try_img, (350, 200))
start_img = pygame.image.load('images/start.png')
start_img = pygame.transform.scale(start_img, (200, 200))
exit_img = pygame.image.load('images/exit.png')
exit_img = pygame.transform.scale(exit_img, (200, 200))
end_img = pygame.image.load('images/gg.jpg')

coin_group = world.coin_group
blob_group = world.blob_group
lava_group = world.lava_group
mad_block_group = world.mad_block_group
exit_group = world.exit_group
ladder_group = world.ladder_group
ice_block_group = world.ice_block_group
bg_block_group = world.bg_block_group
frog_group = world.frog_group
platform_group = world.platform_group
spring_group = world.spring_group
key_group = world.key_group
score_coin = object_classes.Coin('8', tile_size//2,tile_size//2)
player = Player(20, 770)
restart_button = object_classes.Button(250, 450, try_img)
start_button = object_classes.Button(0, 0, start_screen)
exit_button = object_classes.Button(450, 350, exit_img)
tile_size = object_classes.tile_size

async def main():
    level = 1
    play_music(level)
    max_levels = 5
    level_data = f'levels/level{level}/level{level}.csv'
    world_data = world.import_csv_layout(level_data)
    stage = world.World(world_data)
    death_count = 0
    score = 0
    start = False
    run = True
    game_over = 0
    while run:
        clock.tick(90)
        if level == 1 or level == 2:
            screen.blit(bg_img, (0, 0))
            screen.blit(sun_img, (300, 0))
        elif level == 3 or level == 4:
            screen.blit(night_img,(0,0))
        else:
            screen.blit(castle_img,(0,0))
        # draw_text(frames,font_score,white,60,10)
        if not start:
            # screen.blit(start_screen,(0,0))
            start = start_button.draw(screen)
        if start:
            stage.draw(screen)
            coin_group.add(score_coin)
            bg_block_group.draw(screen)
            blob_group.draw(screen)
            lava_group.draw(screen)
            coin_group.draw(screen)
            exit_group.draw(screen)
            ladder_group.draw(screen)
            spring_group.draw(screen)
            ice_block_group.draw(screen)
            platform_group.draw(screen)
            key_group.draw(screen)
            game_over = player.update(game_over,stage)
            if game_over == 0:
                # stage = world.reset_level(level, player)
                blob_group.update()
                frog_group.draw(screen)
                frog_group.update()
                platform_group.update()
                mad_block_group.draw(screen)
                if pygame.sprite.spritecollide(player, coin_group, True ):
                    score += 1
                    coin_sound.play()
                world.draw_text('x' + str(score),font_score,white,30,10, screen)

            if game_over == -1:
                if death_count == 0:
                    death_sound.play()
                    death_count = 1
                screen.blit(over_img, (250, 150))
                score = 0
                if restart_button.draw(screen):
                    death_count = 0
                    # world_data = []
                    stage = world.reset_level(level,player)
                    game_over = 0
            #
            if game_over == 1:
                level += 1
                if level <= max_levels:
                    world_data = []
                    play_music(level)
                    stage = world.reset_level(level,player)
                    game_over = 0
                if level > max_levels:
                    screen.blit(end_img,(0, 0))
                    play_music(level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        await asyncio.sleep(0)

asyncio.run(main())

