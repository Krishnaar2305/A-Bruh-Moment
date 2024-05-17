import pygame
import object_classes
from csv import reader
from pygame import mixer
mixer.init()

#music files

coin_group = pygame.sprite.Group()
blob_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
mad_block_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
ladder_group = pygame.sprite.Group()
ice_block_group = pygame.sprite.Group()
bg_block_group = pygame.sprite.Group()
frog_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
spring_group = pygame.sprite.Group()
key_group = pygame.sprite.Group()


tile_size = object_classes.tile_size





def reset_level(level,player):
    player.reset(20, 770)
    blob_group.empty()
    mad_block_group.empty()
    bg_block_group.empty()
    ladder_group.empty()
    ice_block_group.empty()
    lava_group.empty()
    exit_group.empty()
    coin_group.empty()
    key_group.empty()
    frog_group.empty()
    spring_group.empty()
    platform_group.empty()
    mixer.music.stop()

    level_data = f'levels/level{level}/level{level}.csv'
    world_data = import_csv_layout(level_data)
    stage = World(world_data)
    return stage

            
def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter=',')
        for row in level:
            terrain_map.append(list(row))
    return terrain_map

def draw_text(text, font, color, x, y, screen):
    img = font.render(text, True, color)
    screen.blit(img,(x,y))

class World():
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == '1':
                    img1 = pygame.image.load('images/tiles/grass.png')
                elif tile == '2':
                    img1 = pygame.image.load('images/tiles/dirt.png')
                elif tile == '3':
                    exit = object_classes.Exit(col_count * tile_size, row_count * tile_size )
                    exit_group.add(exit)
                elif tile == '4':
                    lava = object_classes.Lava(4, col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                elif tile == '5':
                    lava = object_classes.Lava(5, col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == '6' or tile == '8':
                    coin = object_classes.Coin(tile, col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                elif tile == '12' or tile == '57':
                    mad_block = object_classes.Mad_block(tile, col_count * tile_size + 20, row_count * tile_size)
                    mad_block_group.add(mad_block)
                elif tile == '14':
                    blob = object_classes.Pink_blob(tile, col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                elif tile == '15':
                    ladder = object_classes.Ladder(col_count * tile_size, row_count * tile_size)
                    ladder_group.add(ladder)
                elif tile == '17':
                    ice_block = object_classes.Ice_block(col_count * tile_size, row_count * tile_size)
                    ice_block_group.add(ice_block)
                elif tile == '9' or tile == '10' or tile == '18' or tile == '26' or tile == '27':
                    bg_block = object_classes.bg(tile, col_count * tile_size, row_count * tile_size)
                    bg_block_group.add(bg_block)
                elif tile == '19':
                    img1 = pygame.image.load('images/ice level/tundraCenter.png')
                elif tile == '20':
                    img1 = pygame.image.load('images/ice level/tundra.png')
                elif tile == '28':
                    frog = object_classes.Frog(tile, col_count * tile_size, row_count * tile_size + 13, tile_size - 7)
                    frog_group.add(frog)
                elif tile == '34':
                    lava = object_classes.Lava(34, col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                elif tile == '35':
                    lava = object_classes.Lava(35, col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                elif tile == '40' or tile == '58':
                    platform = object_classes.Platform(tile, col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                elif tile == '41' or tile == '60':
                    platform = object_classes.Platform(tile, col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                elif tile == '42':
                    img1 = pygame.image.load('images/metal level/metalCenter.png')
                elif tile == '45':
                    spring = object_classes.Spring(col_count * tile_size, row_count * tile_size)
                    spring_group.add(spring)
                elif tile == '48':
                    key = object_classes.Key(col_count * tile_size, row_count * tile_size)
                    key_group.add(key)
                elif tile == '52':
                    lava = object_classes.Lava(52, (col_count * tile_size), (row_count * tile_size) + 10)
                    lava_group.add(lava)
                elif tile == '53':
                    lava = object_classes.Lava(53, (col_count * tile_size) + 10, row_count * tile_size)
                    lava_group.add(lava)
                elif tile == '55':
                    rat = object_classes.Pink_blob(tile, col_count * tile_size, row_count * tile_size + 5)
                    blob_group.add(rat)
                elif tile == '56':
                    ghost = object_classes.Frog(tile, col_count * tile_size, row_count * tile_size, tile_size)
                    frog_group.add(ghost)
                elif tile == '59':
                    img1 = pygame.image.load('images/metal level/laserUp.png')
                if tile == '1' or tile == '2' or tile == '19' or tile == '20' or tile == '42' or tile == '59':
                    img = pygame.transform.scale(img1, (tile_size, tile_size))
                    img_rect = img.get_rect()  # creating rectangle
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1

    def draw(self,screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            pygame.draw.rect(screen, (255, 255, 255), tile[1], 1)

