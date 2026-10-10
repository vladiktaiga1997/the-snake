from random import choice, randint

import pygame as pg

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

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Основной Класс."""

    def __init__(self, body_color=None):
        """Задаёт начальную позицию игрового объекта."""
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.body_color = body_color

    def draw(self):
        """Каркас метода рисования объектов."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс Apple унаследовавший базовый класс GameObject."""

    def __init__(self, body_color=APPLE_COLOR, occupied_positions=None):
        """Метод задаёт цвет и случайную позицию яблока."""
        super().__init__(body_color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Метод для рандомного размещения яблока на карте."""
        if occupied_positions is None:
            occupied_positions = []
        self.position = (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                         randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)
        while self.position in occupied_positions:
            self.position = (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE,
                             randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE)

    def draw(self):
        """Метод рисования яблока на карте."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс Snake унаследовавший базовый класс GameObject."""

    def __init__(self, body_color=SNAKE_COLOR):
        """Метод задаёт основные начальные данные змейки."""
        super().__init__(body_color)
        self.reset()
        self.direction = RIGHT

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """Метод движения змейки."""
        x_position, y_position = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = (
            (direction_x * GRID_SIZE + x_position) % SCREEN_WIDTH,
            (direction_y * GRID_SIZE + y_position) % SCREEN_HEIGHT
        )
        self.positions.insert(0, self.position)
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
        if self.last:
            rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)
        for position in self.positions:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)

    def reset(self):
        """Метод обновления игры после проигрыша."""
        self.length = 1
        self.position = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        self.positions = [self.position]
        self.direction = choice([LEFT, RIGHT, UP, DOWN])
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Функция реагирования на нажатые клавиши."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif (
                event.key == pg.K_LEFT
                and game_object.direction != RIGHT
            ):
                game_object.next_direction = LEFT
            elif (
                event.key == pg.K_RIGHT
                and game_object.direction != LEFT
            ):
                game_object.next_direction = RIGHT


def main():
    """Функция основного цикла."""
    pg.init()
    snake = Snake()
    apple = Apple(occupied_positions=snake.positions)
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw()
        pg.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
