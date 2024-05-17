import pygame
tile_size = 40
class Mad_block(pygame.sprite.Sprite):
    def __init__(self,tile,  x, y):
        pygame.sprite.Sprite.__init__(self)
        if tile == '12':
            self.image = pygame.image.load('images/enemies/blockerMad.png')
        else:
            self.image = pygame.image.load('images/enemies/spinner_spin.png')
        self.image = pygame.transform.scale(self.image, (tile_size-5, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

class Pink_blob(pygame.sprite.Sprite):
    def __init__(self,n, x, y):
        pygame.sprite.Sprite.__init__(self)
        if n == '14':
            self.img_right = pygame.image.load(f"images/enemies/slimeWalk1.png")
        elif n == '55':
            self.img_right = pygame.image.load('images/enemies/mouse.png')
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.image = self.img_right
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        self.max_move = tile_size * 3

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) == self.max_move:
            self.move_direction *= -1
            self.move_counter = 0

        if self.move_direction > 0:
            self.image = self.img_right
        else:
            self.image = self.img_left

class Frog(pygame.sprite.Sprite):
    def __init__(self,n , x, y, y_size):
        pygame.sprite.Sprite.__init__(self)
        if n == '28':
            self.img_right = pygame.image.load(f"images/enemies/frog_leap.png")
            self.max_x = 3 * tile_size
            self.max_y = 1.5 * tile_size
        elif n == '56':
            self.img_right = pygame.image.load('images/enemies/ghost.png')
            self.max_x = 5 * tile_size
            self.max_y = 2.5 * tile_size
        # self.image = pygame.transform.scale(self.image, (tile_size,tile_size-10))
        self.img_left = pygame.transform.flip(self.img_right, True, False)
        self.moving_img = [self.img_left, self.img_right]
        self.image = self.moving_img[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dx = 1
        self.dy = 1
        self.x_disp = 0
        self.y_disp = 0
        self.index = 0
        self.y_size = y_size
        self.moved_x = 0
        self.moved_y = 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y -= self.dy
        self.moved_x += self.dx
        self.moved_y += self.dy
        self.image = self.moving_img[self.index]
        self.image = pygame.transform.scale(self.image, (tile_size-5,self.y_size))
        if self.moved_x == self.max_x:
            self.moved_x = 0
            self.max_x = -self.max_x
            self.dx = -self.dx
            if self.index == 0:
                self.index = 1
            else:
                self.index = 0
        if self.moved_y == self.max_y:
            self.moved_y = 0
            self.max_y = -self.max_y
            self.dy = -self.dy


class Coin(pygame.sprite.Sprite):
    def __init__(self,tile, x, y):
        pygame.sprite.Sprite.__init__(self)
        if tile == '8':
            coin_img = pygame.image.load('images/tiles/coinGold.png')
        else:
            coin_img = pygame.image.load('images/tiles/coinSilver.png')
        self.image = pygame.transform.scale(coin_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        coin_img = pygame.image.load('images/tiles/flagRed.png')
        self.image = pygame.transform.scale(coin_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Spring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        coin_img = pygame.image.load('images/metal level/beam.png')
        self.image = pygame.transform.scale(coin_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Button():
    def __init__(self, x, y, img):
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self,screen):
        action = False
        # mouse pos
        pos = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        # check collision for mouse
        if key[pygame.K_RETURN]:
            action = True
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)
        return action


class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        ladder_img = pygame.image.load('images/tiles/ladder_mid.png')
        self.image = pygame.transform.scale(ladder_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Ice_block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        ice_block_img = pygame.image.load('images/ice level/iceBlock.png')
        self.image = pygame.transform.scale(ice_block_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class bg(pygame.sprite.Sprite):
    def __init__(self,n , x, y):
        pygame.sprite.Sprite.__init__(self)
        if n == '9':
            bg_img = pygame.image.load('images/tiles/bush.png')
        elif n == '10':
            bg_img = pygame.image.load('images/tiles/plant.png')
        elif n == '26':
            bg_img = pygame.image.load('images/ice level/caneGreen.png')
        elif n == '27':
            bg_img = pygame.image.load('images/ice level/caneGreenTop.png')
        elif n == '18':
            bg_img = pygame.image.load('images/ice level/pineSapling.png')
        self.image = pygame.transform.scale(bg_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Platform(pygame.sprite.Sprite):
    def __init__(self,tile, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        if tile == '40' or tile == '41':
            img = pygame.image.load('images/ice level/snowHalf.png')
        else:
            img = pygame.image.load('images/metal level/metalPlatform.png')
        self.image = pygame.transform.scale(img, (tile_size, tile_size//2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > tile_size * 4:
            self.move_direction *= -1
            self.move_counter = 0

class Lava(pygame.sprite.Sprite):
    def __init__(self, n, x, y):
        pygame.sprite.Sprite.__init__(self)
        if n == 5:
            img = pygame.image.load('images/tiles/liquidLavaTop.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        elif n == 4:
            img = pygame.image.load('images/tiles/liquidLava.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size))
        elif n == 35:
            img = pygame.image.load('images/ice level/iceWater.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        elif n == 34:
            img = pygame.image.load('images/ice level/iceWaterDeep.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size))
        elif n == 52:
            img = pygame.image.load('images/metal level/laserBlueHorizontal.png')
            self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        else:
            img = pygame.image.load('images/metal level/laserBlueVertical.png')
            self.image = pygame.transform.scale(img, (tile_size//2, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Key(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        ladder_img = pygame.image.load('images/metal level/hud_keyBlue.png')
        self.image = pygame.transform.scale(ladder_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


