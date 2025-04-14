import psycopg2
import pygame
import random
import sys

# Подключение к PostgreSQL
conn = psycopg2.connect(
    dbname="lab10",
    user="postgres",
    password="AkhmetMK07",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Создание таблиц
cur.execute('''
    CREATE TABLE IF NOT EXISTS game_user (
        username VARCHAR(50) PRIMARY KEY
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS user_score (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) REFERENCES game_user(username),
        score INTEGER,
        level INTEGER
    );
''')

conn.commit()

# Получение уровня пользователя
def get_user_level(username):
    cur.execute("SELECT MAX(level) FROM user_score WHERE username = %s", (username,))
    result = cur.fetchone()[0]
    return result if result else 1

# Сохранение результата
def save_game(username, score, level):
    cur.execute("INSERT INTO game_user (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
    cur.execute("INSERT INTO user_score (username, score, level) VALUES (%s, %s, %s)", (username, score, level))
    conn.commit()

# Ввод имени
username = input("Введите имя игрока: ")

# Получаем уровень, но позволим повышать его во время игры
level = get_user_level(username)
initial_level = level  # Сохраняем, чтобы потом сравнить
score = 0

def recalculate_level(score):
    # Новый уровень каждые 5 очков
    return 1 + score // 5

print(f"Текущий уровень игрока: {level}")

# Настройки уровня
speed = 10 + (level - 1) * 3
wall_color = (139, 0, 0) if level >= 2 else (0, 0, 0)  # Тёмно-красный

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Размеры
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Окно поверх всех (только Windows)
import ctypes
hwnd = pygame.display.get_wm_info()['window']
ctypes.windll.user32.SetWindowPos(hwnd, -1, 0, 0, 0, 0, 0x0001 | 0x0002)

pygame.display.set_caption("Snake")

# Начальная позиция
snake = [(100, 100), (90, 100), (80, 100)]
direction = (CELL_SIZE, 0)
paused = False

# Стены
walls = []
if level >= 2:
    for i in range(100, 500, 40):
        walls.append((i, 200))  # Горизонтальная линия
if level >= 3:
    for i in range(100, 300, 40):
        walls.append((300, i))  # Вертикальная

# Безопасный спавн еды
def spawn_food():
    while True:
        pos = (random.randrange(0, WIDTH, CELL_SIZE), random.randrange(0, HEIGHT, CELL_SIZE))
        if pos not in snake and pos not in walls:
            return pos

food = spawn_food()

# Рисование
def draw_snake():
    for x, y in snake:
        pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE))

def draw_food():
    pygame.draw.rect(screen, (255, 0, 0), (food[0], food[1], CELL_SIZE, CELL_SIZE))

def draw_walls():
    for x, y in walls:
        pygame.draw.rect(screen, wall_color, (x, y, CELL_SIZE, CELL_SIZE))

def show_text(text, x, y):
    img = font.render(text, True, (255, 255, 255))
    screen.blit(img, (x, y))

# Основной цикл
running = True
game_over = False

while running:
    screen.fill((0, 0, 0))

    if not paused and not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(username, score, level)
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, CELL_SIZE):
                    direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -CELL_SIZE):
                    direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT and direction != (CELL_SIZE, 0):
                    direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-CELL_SIZE, 0):
                    direction = (CELL_SIZE, 0)
                elif event.key == pygame.K_p:
                    paused = True
                    save_game(username, score, level)
                    print("Игра на паузе. Сохранено в базу данных.")

        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake or head in walls:
            print("Игра окончена!")
            save_game(username, score, level)
            game_over = True

        if not game_over:
            snake.insert(0, head)

            if head == food:
                score += 1
                food = spawn_food()
                new_level = recalculate_level(score)
                if new_level > level:
                    level = new_level
                    speed += 2
                    print(f"Новый уровень: {level}")

                    if level == 2:
                        for i in range(100, 500, 40):
                            walls.append((i, 200))
                    elif level == 3:
                        for i in range(100, 300, 40):
                            walls.append((300, i))
            else:
                snake.pop()

        draw_snake()
        draw_food()
        draw_walls()
        show_text(f"Очки: {score}  Уровень: {level}", 10, 10)

    elif paused:
        show_text("Игра на паузе (нажми P, чтобы продолжить)", 100, HEIGHT // 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(username, score, level)
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                paused = False

    elif game_over:
        show_text("Игра окончена! Нажмите R, чтобы начать заново", 100, HEIGHT // 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Сброс игры
                snake = [(100, 100), (90, 100), (80, 100)]
                direction = (CELL_SIZE, 0)
                score = 0
                level = get_user_level(username)
                speed = 10 + (level - 1) * 3
                walls = []
                if level >= 2:
                    for i in range(100, 500, 40):
                        walls.append((i, 200))
                if level >= 3:
                    for i in range(100, 300, 40):
                        walls.append((300, i))
                food = spawn_food()
                game_over = False
                paused = False

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
