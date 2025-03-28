import pygame
import random
import time
from itertools import chain

pygame.init()

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Game variables
screen_width = 400
screen_height = 600
speed = 5
score = 0
coin_score = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, black)

# Load sounds
crash_sound = pygame.mixer.Sound("C:/Users/Asus/Documents/Little/PP2/lab8/sounds/crash.wav")
coin_sound = pygame.mixer.Sound("C:/Users/Asus/Documents/Little/PP2/lab8/sounds/getcoin.mp3")

# Background
background = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab8/image/AnimatedStreet.png")

# Screen setup
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game")
clock = pygame.time.Clock()

# Classes
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab8/image/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), -20)
    
    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            score += 1
            self.rect.center = (random.randint(40, screen_width - 40), -20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab8/image/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
    
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < screen_width and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.image = pygame.image.load("C:/Users/Asus/Documents/Little/PP2/lab8/image/coin.png")
        self.rect = self.image.get_rect()
        self.spawn(enemy)
    
    def spawn(self, enemy):
        coord_range = list(chain(range(22, enemy.rect.center[0] - 46), range(enemy.rect.center[0] + 46, screen_width - 22)))
        if coord_range:
            self.rect.center = (random.choice(coord_range), 0)
        else:
            self.rect.center = (random.randint(22, screen_width - 22), 0)
    
    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.rect.top = 0
            self.spawn(E1)

# Game setup
P1 = Player()
E1 = Enemy()
coins = pygame.sprite.Group()
for _ in range(3):
    coins.add(Coin(E1))

all_sprites = pygame.sprite.Group(P1, E1, *coins)

# Speed increase event
inc_speed = pygame.USEREVENT + 1
pygame.time.set_timer(inc_speed, 1000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == inc_speed:
            speed += 1
    
    screen.blit(background, (0, 0))
    screen.blit(font_small.render(str(score), True, black), (10, 10))
    screen.blit(font_small.render(f"Coins: {coin_score}", True, black), (300, 10))
    
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()
    
    if pygame.sprite.spritecollideany(P1, coins):
        coin_score += 1
        coin_sound.play()
        for coin in coins:
            if P1.rect.colliderect(coin.rect):
                coin.spawn(E1)
                break
    
    if pygame.sprite.spritecollideany(P1, pygame.sprite.Group(E1)):
        crash_sound.play()
        screen.fill(red)
        screen.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        running = False
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()