from random import randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20  # размер клетки
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)
# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)
# Цвет яблока
APPLE_COLOR = (255, 0, 0)
# Цвет змейки
SNAKE_COLOR = (0, 255, 0)
# Скорость движения змейки:
SPEED = 15

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Змейка')

clock = pygame.time.Clock()


class GameObject:
    """Основной Класс."""

    def __init__(self):
        """Задаёт начальную позицию игрового объекта."""
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.body_color = None

    def draw(self):
        """Каркас метода рисования объектов."""
        pass


class Apple(GameObject):
    """Класс Apple унаследовавший базовый класс GameObject."""

    def __init__(self):
        """Метод задаёт цвет и случайную позицию яблока."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Метод для рандомного размещения яблока на карте."""
        number_grid_width = randint(0, (GRID_WIDTH - 1))
        number_grid_height = randint(0, (GRID_HEIGHT - 1))
        self.position = ((number_grid_width * GRID_SIZE),
                         (number_grid_height * GRID_SIZE))

    def draw(self):
        """Метод рисования яблока на карте."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake унаследовавший базовый класс GameObject."""

    def __init__(self):
        """Метод задаёт основные начальные данные змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR  # цвет тела змейки
        self.reset()

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод движения змейки."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        new_x = ((dx * GRID_SIZE) + x) % SCREEN_WIDTH
        new_y = ((dy * GRID_SIZE) + y) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Метод обновления направления змейки."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод рисования тела змейки."""
        if self.last is not None:
            rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)

    def reset(self):
        """Метод обновления игры после проигрыша."""
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция реагирования на нажатые клавиши."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif (
                event.key == pygame.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pygame.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Функция основного цикла."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
