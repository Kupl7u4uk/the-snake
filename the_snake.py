from random import choice, randint

import pygame as pg


# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

OPPOSITE_DIRECTIONS = {
    UP: DOWN,
    DOWN: UP,
    LEFT: RIGHT,
    RIGHT: LEFT
}
KEY_TO_DIRECTION = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT
}

BOARD_BACKGROUND_COLOR = (220, 220, 220)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка | Стрелки - управление | ESC - выход')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс для всех игровых объектов."""

    def __init__(self, color):
        """Инициализация игрового объекта."""
        self.position = CENTER_POSITION
        self.body_color = color

    def draw_cell(self, position, color=None):
        """Отрисовка клетки игрового поля."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        cell_color = self.body_color if color is None else color
        pg.draw.rect(screen, cell_color, rect)
        if cell_color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Отрисовка игрового объекта."""
        raise NotImplementedError(
            f'Метод draw() не реализован в классе {type(self).__name__}'
        )


class Apple(GameObject):
    """Яблоко, появляющееся в случайной клетке игрового поля."""

    def __init__(self, occupied_positions, color=APPLE_COLOR):
        """Инициализация цвета и положения яблока."""
        super().__init__(color)
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Рандомизация положения яблока."""
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if self.position not in occupied_positions:
                break

    def draw(self):
        """Отрисовка яблока."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self, color=SNAKE_COLOR):
        """Инициализация змейки на старте игры."""
        super().__init__(color)
        self.reset()

    def update_direction(self, new_direction):
        """Обновление направления движения змейки."""
        if new_direction != OPPOSITE_DIRECTIONS[self.direction]:
            self.direction = new_direction

    def get_head_position(self):
        """Получение координат головы змейки."""
        return self.positions[0]

    def move(self):
        """Перемещение змейки."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction

        self.positions.insert(0, (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        ))

        self.last = (
            self.positions.pop() if len(self.positions) > self.length else None
        )

    def reset(self):
        """Возвращение змейки в исходную позицию"""
        self.length = 1
        self.positions = [CENTER_POSITION]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.last = None

    def draw(self):
        """Отрисовка змейки."""
        if self.last and self.last not in self.positions:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)
        self.draw_cell(self.get_head_position())


def handle_keys(snake):
    """Обработка закрытия окна и нажатия клавиш."""
    direction_changed = False
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:  # Ниже, до main() воспользовался подсказками ИИ
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            new_directions = KEY_TO_DIRECTION.get(event.key)
            if new_directions and not direction_changed:
                old_direction = snake.direction
                snake.update_direction(new_directions)
                direction_changed = snake.direction != old_direction


def main():
    """Запуск игрового цикла."""
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)
    screen.fill(BOARD_BACKGROUND_COLOR)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.move()

        head_position = snake.get_head_position()
        if head_position == apple.position:
            snake.length += 1
            if snake.length == GRID_WIDTH * GRID_HEIGHT:
                snake.reset()
                screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)
        elif head_position in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            if apple.position in snake.positions:
                apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
