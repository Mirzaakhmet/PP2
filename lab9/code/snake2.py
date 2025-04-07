import pygame
import random
import time

# ------------------ Настройки (тут все ясно) ------------------
COLUMNS = 30       # кол-во клеток по ширине
ROWS = 20          # кол-во клеток по высоте
TARGET_WIDTH = 1200
TARGET_HEIGHT = 800

# Чтоб не криво было, считаем размер клетки
CELL_SIZE_X = TARGET_WIDTH // COLUMNS
CELL_SIZE_Y = TARGET_HEIGHT // ROWS
CELL_SIZE = min(CELL_SIZE_X, CELL_SIZE_Y)  # берем меньшую чтоб влезло

WIN_WIDTH = COLUMNS * CELL_SIZE  # итоговая ширина окна
WIN_HEIGHT = ROWS * CELL_SIZE    # итоговая высота

FPS = 60  # фпс как в AAA играх
MOVE_INTERVAL = 100  # время между движениями (мс)

INTERPOLATION_STEPS = 120  # шагов для плавности
SMOOTH_MOVE_INTERVAL = INTERPOLATION_STEPS * (90 / FPS)  # магия чисел

# ------------------ Цвета (чтоб красиво было) ------------------
BACKGROUND = (198, 225, 69)    # травка
GRID_COLOR = (178, 202, 62)    # сетка потемнее
SNAKE_COLOR = (71, 82, 25)     # змея - темная
TEXT_COLOR = (71, 82, 25)      # текст такой же
BUTTON_COLOR = (178, 202, 62)  # кнопки как сетка
BLACK = (0, 0, 0)              # рамка

# Цвета еды (по весу): красный - 3, оранж - 2, зеленый - 1
FOOD_COLORS = [
    (255, 0, 0),    # красный - самый смак
    (255, 165, 0),  # оранж - так себе
    (0, 255, 0)     # зеленый - диетический
]

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Змея 2026 - ПРО версия миллиард фпс")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)  # шрифт обычный

# ------------------ Функции (тут все важно) ------------------

def draw_button(text, y_pos):
    """Рисуем кнопку (центр по X, y_pos по Y)"""
    surf = font.render(text, True, TEXT_COLOR)
    rect = surf.get_rect(center=(WIN_WIDTH // 2, y_pos))
    pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 10))  # делаем побольше
    screen.blit(surf, rect)
    return rect  # возвращаем rect для кликов

def draw_grid():
    """Сетка как в тетрадке в клетку"""
    for x in range(COLUMNS + 1):
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, WIN_HEIGHT), 1)
    for y in range(ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, y * CELL_SIZE), (WIN_WIDTH, y * CELL_SIZE), 1)

def draw_border():
    """Рамка чтоб змея не сбежала"""
    thickness = max(4, CELL_SIZE // 5)  # толщина зависит от размера клетки
    pygame.draw.line(screen, BLACK, (0, 0), (WIN_WIDTH, 0), thickness)              # верх
    pygame.draw.line(screen, BLACK, (0, WIN_HEIGHT), (WIN_WIDTH, WIN_HEIGHT), thickness)  # низ
    pygame.draw.line(screen, BLACK, (0, 0), (0, WIN_HEIGHT), thickness)             # лево
    pygame.draw.line(screen, BLACK, (WIN_WIDTH, 0), (WIN_WIDTH, WIN_HEIGHT), thickness)  # право

def get_random_food(snake):
    """Генерим еду (не на змее) с рандомным весом и временем жизни"""
    while True:
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in snake:
            weight = random.randint(1, 3)  # вес 1-3
            lifetime = random.randint(5, 15)  # живет 5-15 сек
            return {
                'position': (x, y),
                'weight': weight,
                'lifetime': lifetime,
                'creation_time': time.time(),  # когда создали
                'color': FOOD_COLORS[weight-1]  # цвет по весу
            }

def init_game():
    """Начальные настройки новой игры"""
    start_x = COLUMNS // 2  # старт по центру
    start_y = ROWS // 2
    snake = [(start_x, start_y)]  # змея из одной клетки
    return {
        'snake': snake,
        'direction': (1, 0),  # сначала вправо
        'score': 0,
        'level': 1,
        'food': get_random_food(snake)  # первая еда
    }

def lerp(a, b, f):
    """Плавное движение от a до b (0 <= f <= 1)"""
    return a + f * (b - a)

# ------------------ Инициализация игры ------------------
game_state = init_game()
game_started = False
game_over = False
high_score = 0

move_timer = 0  # таймер для движения
current_move_computed = False  # готов ли следующий ход?

snake_prev = []  # предыдущее положение змеи
snake_target = []  # куда двигаемся
food_eaten_flag = False  # схавали еду или нет

running = True
while running:
    dt = clock.tick(FPS)  # дельтатайм в мс
    
    # ------------------ Обработка событий ------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Старт/рестарт по пробелу или клику
        elif event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
            if not game_started:
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    not draw_button("Start", WIN_HEIGHT // 2).collidepoint(event.pos)):
                    continue
                game_started = True
            elif game_over:
                if (event.type == pygame.MOUSEBUTTONDOWN and 
                    not draw_button("Restart", WIN_HEIGHT // 2).collidepoint(event.pos)):
                    continue
                game_state = init_game()
                game_over = False
                move_timer = 0
                current_move_computed = False

        # Управление змеей (WASD или стрелки)
        elif event.type == pygame.KEYDOWN and game_started and not game_over:
            dx, dy = game_state['direction']
            # Запрещаем разворот на 180 (чтоб не убивался)
            if event.key in [pygame.K_UP, pygame.K_w] and (dx, dy) != (0, 1):
                game_state['direction'] = (0, -1)
            elif event.key in [pygame.K_DOWN, pygame.K_s] and (dx, dy) != (0, -1):
                game_state['direction'] = (0, 1)
            elif event.key in [pygame.K_LEFT, pygame.K_a] and (dx, dy) != (1, 0):
                game_state['direction'] = (-1, 0)
            elif event.key in [pygame.K_RIGHT, pygame.K_d] and (dx, dy) != (-1, 0):
                game_state['direction'] = (1, 0)

    # ------------------ Отрисовка ------------------
    screen.fill(BACKGROUND)
    draw_grid()
    draw_border()

    # Стартовый экран
    if not game_started:
        draw_button("Start", WIN_HEIGHT // 2)
    else:
        # Экран после проигрыша
        if game_over:
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.fill(BACKGROUND)
            overlay.set_alpha(128)  # полупрозрачный
            screen.blit(overlay, (0, 0))
            draw_button("Restart", WIN_HEIGHT // 2)
            game_over_text = font.render(f"Game Over! High Score: {high_score}", True, TEXT_COLOR)
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2 - 50)))
        else:
            # Игровой процесс
            current_smooth_move_interval = SMOOTH_MOVE_INTERVAL * (0.9 ** (game_state['level'] - 1))  # скорость с уровнем
            
            move_timer += dt

            # Вычисляем следующий ход если нужно
            if not current_move_computed:
                dx, dy = game_state['direction']
                head = game_state['snake'][0]
                new_head = (head[0] + dx, head[1] + dy)

                # Проверяем столкновения
                if new_head[0] < 0 or new_head[0] >= COLUMNS or new_head[1] < 0 or new_head[1] >= ROWS:
                    game_over = True
                    high_score = max(high_score, game_state['score'])
                elif new_head in game_state['snake'] and new_head != game_state['snake'][-1]:
                    game_over = True
                    high_score = max(high_score, game_state['score'])
                else:
                    # Если съели еду
                    if game_state['food']['position'] == new_head:
                        food_eaten_flag = True
                        snake_target = [new_head] + game_state['snake']  # увеличиваем змею
                        snake_prev = game_state['snake'] + [game_state['snake'][-1]]
                    else:
                        food_eaten_flag = False
                        snake_target = [new_head] + game_state['snake'][:-1]  # двигаемся
                        snake_prev = game_state['snake'][:]  # копируем
                    current_move_computed = True

            # Прогресс анимации (0-1)
            f = min(move_timer / current_smooth_move_interval, 1)

            # Рисуем змею с интерполяцией
            for i in range(len(snake_target)):
                if i < len(snake_prev):
                    start_pos = snake_prev[i]
                else:
                    start_pos = snake_prev[-1]
                end_pos = snake_target[i]

                draw_x = lerp(start_pos[0], end_pos[0], f) * CELL_SIZE
                draw_y = lerp(start_pos[1], end_pos[1], f) * CELL_SIZE
                pygame.draw.rect(screen, SNAKE_COLOR, (draw_x + 2, draw_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

            # Работа с едой
            current_time = time.time()
            food = game_state['food']
            time_since_creation = current_time - food['creation_time']
            
            # Если еда "просрочена" - генерим новую
            if time_since_creation > food['lifetime']:
                game_state['food'] = get_random_food(game_state['snake'])
                food = game_state['food']
                time_since_creation = 0
            
            # Отрисовка еды с прозрачностью
            fx, fy = food['position']
            time_left = max(0, food['lifetime'] - time_since_creation)
            alpha = int(255 * (time_left / food['lifetime']))
            
            food_surface = pygame.Surface((CELL_SIZE - 4, CELL_SIZE - 4))
            food_surface.set_alpha(alpha)
            food_surface.fill(food['color'])
            screen.blit(food_surface, (fx * CELL_SIZE + 2, fy * CELL_SIZE + 2))
            
            # Контур чтоб видно было когда прозрачная
            pygame.draw.rect(screen, food['color'], (fx * CELL_SIZE + 2, fy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4), 1)

            # Обновляем состояние после анимации
            if move_timer >= current_smooth_move_interval:
                game_state['snake'] = snake_target
                
                if food_eaten_flag:
                    # Добавляем очки по весу еды
                    game_state['score'] += food['weight']
                    # Повышаем уровень каждые 4*вес очков
                    if game_state['score'] % (4 * food['weight']) == 0:
                        game_state['level'] += 1
                    game_state['food'] = get_random_food(game_state['snake'])
                
                move_timer -= current_smooth_move_interval
                current_move_computed = False

            # Счет и уровень сверху
            score_text = font.render(f"Score: {game_state['score']}  Level: {game_state['level']}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()