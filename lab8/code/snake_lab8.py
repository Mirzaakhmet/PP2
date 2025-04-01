import pygame
import random

# ------------------ Параметры поля, ну типа Настройки ------------------
COLUMNS = 30       # кол-во клеток по горизонтали
ROWS = 20          # кол-во клеток по вертикали
TARGET_WIDTH = 1200
TARGET_HEIGHT = 800

# Тут, чтобы все было пропоционально
CELL_SIZE_X = TARGET_WIDTH // COLUMNS
CELL_SIZE_Y = TARGET_HEIGHT // ROWS
CELL_SIZE = min(CELL_SIZE_X, CELL_SIZE_Y)

WIN_WIDTH = COLUMNS * CELL_SIZE
WIN_HEIGHT = ROWS * CELL_SIZE

FPS = 60
MOVE_INTERVAL = 100  # время (мс) на переход из одной клетки в другую

INTERPOLATION_STEPS = 120  # количество маленьких движений до следующей клетки, чтобы было плавно
# скорость перехода между клетками
SMOOTH_MOVE_INTERVAL = INTERPOLATION_STEPS * (90 / FPS)

# ------------------ Цвета, тут у меня Классик ------------------
BACKGROUND = (198, 225, 69)
GRID_COLOR = (178, 202, 62)
SNAKE_COLOR = (71, 82, 25)
FOOD_COLOR = (71, 82, 25)
TEXT_COLOR = (71, 82, 25)
BUTTON_COLOR = (178, 202, 62)
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Змея миллиард фпс 2025")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# ------------------ Вспомогательные функции ------------------
def draw_button(text, y_pos):
    surf = font.render(text, True, TEXT_COLOR)
    rect = surf.get_rect(center=(WIN_WIDTH // 2, y_pos))
    pygame.draw.rect(screen, BUTTON_COLOR, rect.inflate(20, 10))
    screen.blit(surf, rect)
    return rect

def draw_grid():
    for x in range(COLUMNS + 1):
        pygame.draw.line(screen, GRID_COLOR, (x * CELL_SIZE, 0), (x * CELL_SIZE, WIN_HEIGHT), 1)
    for y in range(ROWS + 1):
        pygame.draw.line(screen, GRID_COLOR, (0, y * CELL_SIZE), (WIN_WIDTH, y * CELL_SIZE), 1)

def draw_border():
    # Тут, чтобы все было пропоционально толщина рамки масштабируется от размера клетки
    thickness = max(4, CELL_SIZE // 5)
    pygame.draw.line(screen, BLACK, (0, 0), (WIN_WIDTH, 0), thickness)              # үстіге
    pygame.draw.line(screen, BLACK, (0, WIN_HEIGHT), (WIN_WIDTH, WIN_HEIGHT), thickness)  # астыға
    pygame.draw.line(screen, BLACK, (0, 0), (0, WIN_HEIGHT), thickness)             # солға
    pygame.draw.line(screen, BLACK, (WIN_WIDTH, 0), (WIN_WIDTH, WIN_HEIGHT), thickness)  # оңға

def get_random_food(snake):
    while True:
        x = random.randint(0, COLUMNS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in snake:
            return (x, y)

def init_game():
    start_x = COLUMNS // 2
    start_y = ROWS // 2
    snake = [(start_x, start_y)]
    return {
        'snake': snake,           
        'direction': (1, 0),
        'score': 0,
        'level': 1,
        'food': get_random_food(snake)
    }

# (0<=f<=1)
def lerp(a, b, f):
    return a + f * (b - a)


game_state = init_game()
game_started = False
game_over = False
high_score = 0

move_timer = 0         
current_move_computed = False  # вычислена ли цель для текущего хода?

snake_prev = []
snake_target = []
food_eaten_flag = False  # съедена ли еда в данном ходе

running = True
while running:
    dt = clock.tick(FPS)  # dt в мс
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Старт и Рестарт на пробел, мне так удобно
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

        # Управление на кнопки и цфыв, но че та цфыв у мя не регает (на входе меняется направление, но оно применяется к следующему ходу)
        elif event.type == pygame.KEYDOWN and game_started and not game_over:
            dx, dy = game_state['direction']
            # Бан разворота на 180 градусов, а то был баг. Умирал, когда нажимал одновременно влево и вправо
            if event.key in [pygame.K_UP, pygame.K_w] and (dx, dy) != (0, 1):
                game_state['direction'] = (0, -1)
            elif event.key in [pygame.K_DOWN, pygame.K_s] and (dx, dy) != (0, -1):
                game_state['direction'] = (0, 1)
            elif event.key in [pygame.K_LEFT, pygame.K_a] and (dx, dy) != (1, 0):
                game_state['direction'] = (-1, 0)
            elif event.key in [pygame.K_RIGHT, pygame.K_d] and (dx, dy) != (-1, 0):
                game_state['direction'] = (1, 0)

    screen.fill(BACKGROUND)
    draw_grid()
    draw_border()

    # Кнопка старта
    if not game_started:
        draw_button("Start", WIN_HEIGHT // 2)
    else:
        # оверлей и рестарт
        if game_over:
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
            overlay.fill(BACKGROUND)
            overlay.set_alpha(128)
            screen.blit(overlay, (0, 0))
            draw_button("Restart", WIN_HEIGHT // 2)
            game_over_text = font.render(f"Game Over! High Score: {high_score}", True, TEXT_COLOR)
            screen.blit(game_over_text, game_over_text.get_rect(center=(WIN_WIDTH//2, WIN_HEIGHT//2 - 50)))
        else:
            # Рассчитываем текущую скорость в зависимости от уровня
            current_smooth_move_interval = SMOOTH_MOVE_INTERVAL * (0.9 ** (game_state['level'] - 1))
            
            move_timer += dt

            if not current_move_computed:
                dx, dy = game_state['direction']
                head = game_state['snake'][0]
                new_head = (head[0] + dx, head[1] + dy)

                # чек на столкновение с границами 
                if new_head[0] < 0 or new_head[0] >= COLUMNS or new_head[1] < 0 or new_head[1] >= ROWS:
                    game_over = True
                    high_score = max(high_score, game_state['score'])
                # так же чек столк-я с телом
                elif new_head in game_state['snake'] and new_head != game_state['snake'][-1]:
                    game_over = True
                    high_score = max(high_score, game_state['score'])
                else:
                    # таргет для хода
                    if game_state['food'] == new_head:
                        # растет если сожрал еду
                        food_eaten_flag = True
                        snake_target = [new_head] + game_state['snake']

                        snake_prev = game_state['snake'] + [game_state['snake'][-1]]
                    else:
                        food_eaten_flag = False
                        snake_target = [new_head] + game_state['snake'][:-1]
                        snake_prev = game_state['snake'][:]  # копия
                    current_move_computed = True


            f = min(move_timer / current_smooth_move_interval, 1)


            for i in range(len(snake_target)):

                if i < len(snake_prev):
                    start_pos = snake_prev[i]
                else:
                    start_pos = snake_prev[-1]
                end_pos = snake_target[i]

                draw_x = lerp(start_pos[0], end_pos[0], f) * CELL_SIZE
                draw_y = lerp(start_pos[1], end_pos[1], f) * CELL_SIZE
                pygame.draw.rect(screen, SNAKE_COLOR, (draw_x + 2, draw_y + 2, CELL_SIZE - 4, CELL_SIZE - 4))

            # спавн еды
            fx, fy = game_state['food']
            pygame.draw.rect(screen, FOOD_COLOR, (fx * CELL_SIZE + 2, fy * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4))


            if move_timer >= current_smooth_move_interval:
                # обнова состояние змейки
                game_state['snake'] = snake_target
                # если уже хавнул еду, то спавним новую и счет +1
                if food_eaten_flag:
                    game_state['score'] += 1
                    if game_state['score'] % 4 == 0:
                        game_state['level'] += 1
                    game_state['food'] = get_random_food(game_state['snake'])
                # сброс таймера для анимации
                move_timer -= current_smooth_move_interval
                current_move_computed = False

            # счетчик сверху
            score_text = font.render(f"Score: {game_state['score']}  Level: {game_state['level']}", True, TEXT_COLOR)
            screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()