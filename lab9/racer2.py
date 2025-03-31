import pygame 
import random
import time
from itertools import chain

pygame.init()

# Определение цветов
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Игровые переменные
screen_width = 400
screen_height = 600
speed = 5  # Начальная скорость врагов и монет
score = 0  # Счетчик очков
coin_score = 0  # Счетчик набранных монет
N = 10  # Количество монет для увеличения скорости

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

# Загрузка звуков
crash_sound = pygame.mixer.Sound("C:/Users/Asus/Documents/Little/PP2/lab9/sounds/crash.wav")
coin_sound = pygame.mixer.Sound("C:/Users/Asus/Documents/Little/PP2/lab9/sounds/getcoin.mp3")

# Загрузка фона
background = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab9/image/AnimatedStreet.png")

# Настройка экрана
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab9/image/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), -20)
    
    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            score += 1  # Увеличение счета при прохождении врага
            self.rect.center = (random.randint(40, screen_width - 40), -20)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab9/image/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < screen_width and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Вес монет и соответствующие изображения
        self.weights = {1: "C:/Users/Asus/Documents/Little/PP2/lab9/image/coin1.png", 
                        2: "C:/Users/Asus/Documents/Little/PP2/lab9/image/coin2.jpeg", 
                        5: "C:/Users/Asus/Documents/Little/PP2/lab9/image/coin.png"}
        self.value, image_path = self.random_coin()
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (80, 80))  # Установка одинакового размера монет
        self.rect = self.image.get_rect()
        self.spawn()
    
    def random_coin(self):
        # Выбор случайной монеты (1, 2 или 5 очков)
        value = random.choices([1, 2, 5], weights=[70, 20, 10])[0]
        return value, self.weights[value]
    
    def spawn(self):
        # Спавн монеты в случайном месте
        self.rect.center = (random.randint(22, screen_width - 22), random.randint(-100, -20))
    
    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.spawn()

# Настройка игры
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()
for _ in range(3):
    coins.add(Coin())

all_sprites = pygame.sprite.Group(P1, E1, *coins)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.blit(background, (0, 0))
    screen.blit(font_small.render(str(score), True, black), (10, 10))
    screen.blit(font_small.render(f"Coins: {coin_score}", True, black), (300, 10))
    
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    for coin in coins:
        if pygame.sprite.collide_circle(P1, coin):
            coin_score += coin.value  # Увеличение счетчика монет на значение монеты
            coin_sound.play()
            coin.spawn()
            if coin_score >= N:
                speed += 1  # Увеличение скорости врагов при наборе N монет
                coin_score = 0
    
    if pygame.sprite.spritecollideany(P1, pygame.sprite.Group(E1)):
        # Проверка столкновения с врагом (конец игры)
        crash_sound.play()
        screen.fill(red)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()