import pygame
import time

# Инициализация Pygame
pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("1-08_-minecraft.mp3")  # Замените на свой файл
pygame.mixer.music.set_volume(0.5)  # Установите нужную громкость
pygame.mixer.music.play(-1)  # Запускаем музыку в бесконечном цикле

# Размеры экрана
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

# Загрузка изображений
floor_img = pygame.transform.scale(pygame.image.load("first_level/ordinary_grass.png"), (40, 40))
background_img = pygame.transform.scale(pygame.image.load("background.jpg"), (1200, 600))
player_img = pygame.transform.scale(pygame.image.load("player.png"), (50, 50))
spike_img = pygame.transform.scale(pygame.image.load("first_level/thorns.png"), (40, 40))
d_img = pygame.transform.scale(pygame.image.load("ordinary_land.png"), (40, 40))
water_img = pygame.transform.scale(pygame.image.load("water.png"), (40, 40))
box_img = pygame.transform.scale(pygame.image.load("first_level/box.png"), (40, 40))
heart_img = pygame.transform.scale(pygame.image.load("first_level/heart.png"), (40, 40))
game_over_img = pygame.transform.scale(pygame.image.load("first_level/game_over.png"), (1200, 600))
adding_life = pygame.transform.scale(pygame.image.load("first_level/heart.png"), (40, 40))
flag = pygame.transform.scale(pygame.image.load("first_level/flag.png"), (40, 40))
floor_snow = pygame.transform.scale(pygame.image.load("floor_snow.png"), (40, 40))
money = pygame.transform.scale(pygame.image.load("money.png"), (40, 40))
right_arrow = pygame.transform.scale(pygame.image.load("rightarrow.png"), (40, 40))
left_arrow = pygame.transform.scale(pygame.image.load("leftarrow.png"), (40, 40))
land_right = pygame.transform.scale(pygame.image.load("land is right.png"), (40, 40))
grass_right = pygame.transform.scale(pygame.image.load("grass is right.png"), (40, 40))
grass_left = pygame.transform.scale(pygame.image.load("grass_left.png"), (40, 40))
earth_left = pygame.transform.scale(pygame.image.load("earth is left.png"), (40, 40))
land_ug = pygame.transform.scale(pygame.image.load("land_ug.png"), (40, 40))
ground_down = pygame.transform.scale(pygame.image.load("ground is down.png"), (40, 40))
water2 = pygame.transform.scale(pygame.image.load("water2.png"), (40, 40))
# Размер клетки
TILE_SIZE = 40
PLAYER_SIZE = 40
MAP_WIDTH = 1200


def load_map(filename):
    with open(filename, "r") as file:
        return [list(line.strip()) for line in file]


def find_player_position(level_map):
    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            if tile == "$":
                return col_index * TILE_SIZE + (TILE_SIZE - PLAYER_SIZE) // 2, row_index * TILE_SIZE + (
                        TILE_SIZE - PLAYER_SIZE) // 2
    return 100, 0


def switch_map(new_map):
    global level_map, player
    level_map = load_map(new_map)
    player_x, player_y = find_player_position(level_map)
    player.reset_position(player_x, player_y)


def draw_hearts():
    for i in range(player.lives):
        screen.blit(heart_img, (SCREEN_WIDTH - (i + 1) * 50, 10))


def draw_coins():
    font = pygame.font.Font(None, 36)
    coin_text = font.render(f"Монеток: {player.coins}", True, (255, 215, 0))  # Золотой цвет текста
    screen.blit(coin_text, (SCREEN_WIDTH - 150, 60))  # Позиция текста с монетками


def game_over():
    screen.blit(game_over_img, (0, 0))
    pygame.display.flip()
    time.sleep(3)
    pygame.quit()
    exit()


collected_hearts = set()
collected_coins = set()


class Player:
    def __init__(self, x, y):
        self.image = player_img
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.vel_y = 0
        self.on_ground = False
        self.speed_x = 0
        self.lives = 3
        self.coins = 0  # Счетчик монеток
        self.start_x = x
        self.start_y = y

    def move(self, tiles):
        self.rect.x += self.speed_x
        self.rect.x = max(0, min(self.rect.x, MAP_WIDTH - PLAYER_SIZE))
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.speed_x > 0:
                    self.rect.right = tile.left
                if self.speed_x < 0:
                    self.rect.left = tile.right
        self.rect.y += self.vel_y
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top
                    self.on_ground = True
                    self.vel_y = 0
                if self.vel_y < 0:
                    self.rect.top = tile.bottom
                    self.vel_y = 0

    def update(self, tiles):
        self.vel_y += 0.45
        if self.vel_y > 10:
            self.vel_y = 10
        self.move(tiles)

    def draw(self, screen, camera_x):
        screen.blit(self.image, (self.rect.x - camera_x, self.rect.y))

    def reset_position(self, x, y):
        self.rect.x = x
        self.rect.y = y


level_map = load_map("Map/map.txt")
player_x, player_y = find_player_position(level_map)
player = Player(player_x, player_y)
clock = pygame.time.Clock()
running = True
camera_x = 0

while running:
    clock.tick(60)
    screen.fill((0, 0, 0))
    screen.blit(background_img, (0, 0))
    tiles = []
    obstacles = []
    hearts = []
    coins = []

    for row_index, row in enumerate(level_map):
        for col_index, tile in enumerate(row):
            x, y = col_index * TILE_SIZE, row_index * TILE_SIZE
            if tile == "%" and (x, y) not in collected_hearts:
                screen.blit(adding_life, (x - camera_x, y))
                hearts.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "0" and (x, y) not in collected_coins:
                screen.blit(money, (x - camera_x, y))
                coins.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "/":
                screen.blit(floor_img, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "g":
                screen.blit(grass_right, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "l":
                screen.blit(grass_left, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "w":
                screen.blit(water2, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == ")":
                screen.blit(land_right, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "q":
                screen.blit(floor_snow, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "u":
                screen.blit(land_ug, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "x":
                screen.blit(ground_down, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "(":
                screen.blit(earth_left, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "!":
                screen.blit(box_img, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == "*":
                screen.blit(d_img, (x - camera_x, y))
                tiles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
            if tile == ">":
                screen.blit(right_arrow, (x - camera_x, y))
            if tile == "<":
                screen.blit(left_arrow, (x - camera_x, y))
            elif tile == "?":
                screen.blit(flag, (x - camera_x, y))
                obstacles.append((pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), "flag"))
            elif tile == "^":
                screen.blit(spike_img, (x - camera_x, y))
                obstacles.append((pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), "spike"))
            elif tile == "&":
                screen.blit(water_img, (x - camera_x, y))
                obstacles.append((pygame.Rect(x, y, TILE_SIZE, TILE_SIZE), "water"))

    keys = pygame.key.get_pressed()
    player.speed_x = -5 if keys[pygame.K_a] else 5 if keys[pygame.K_d] else 0
    if keys[pygame.K_w] and player.on_ground:
        player.vel_y = -10

    player.update(tiles)
    for obstacle, obj_type in obstacles:
        if player.rect.colliderect(obstacle):
            if obj_type == "spike":
                player.lives -= 1
                player.reset_position(player_x, player_y)
                if player.lives == 0:
                    game_over()
            elif obj_type == "flag":
                switch_map("Map/map2.txt")
            elif obj_type == "water":
                player.lives = 0
                game_over()

    for heart in hearts:
        if player.rect.colliderect(heart):
            player.lives += 1
            collected_hearts.add((heart.x, heart.y))
            hearts.remove(heart)

    for coin in coins:
        if player.rect.colliderect(coin):
            player.coins += 1
            collected_coins.add((coin.x, coin.y))
            coins.remove(coin)

    camera_x = max(0, min(player.rect.x - SCREEN_WIDTH // 2, MAP_WIDTH - SCREEN_WIDTH))
    player.draw(screen, camera_x)
    draw_hearts()
    draw_coins()  # Отображение счетчика монеток
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
