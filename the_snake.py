from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
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
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject():
    """Базовый класс.
    Атрибуты:
    position расположен в центр экрана.
    body_color равен 0.
    Метод draw - пустой.
    """

    def __init__(self) -> None:
        self.position: tuple[int, int] = (
            (SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color: tuple[int, int, int] = (0, 0, 0)

    def draw(self):
        """Метод для наследования"""
        pass


class Apple(GameObject):
    """Описывает поведение яблока, наследуется от GameObject.
    Атрибуты:
    body_color равен цвету яблока.
    position вычисляется случайно методом randomize_position.
    Методы:
    randomize_position - возвращает случайную позицию.
    draw - отрисовывает яблоко.
    """

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self) -> tuple[int, int]:
        """Устанавливает случайную позицию яблока."""
        return (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self) -> None:
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Описывает поведение змейки, наследуется от GameObject.
    Атрибуты:
    length — длина змейки. Равна 1.
    positions — список, содержащий позиции всех сегментов тела змейки.
    Начальная позиция — центр экрана.
    next_direction — следующее направление движения,
    которое будет применено после обработки нажатия клавиши.
    body_color — цвет змейки.
    last - последний сегмент змейки.
    Методы:
    update_direction — обновляет направление движения змейки.
    move — обновляет позицию змейки.
    draw — отрисовывает змейку на экране.
    get_head_position — возвращает позицию головы змейки.
    reset — сбрасывает змейку в начальное состояние.
    """

    def __init__(self) -> None:
        super().__init__()
        self.length: int = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction: None | tuple[int, int] = None
        self.body_color = SNAKE_COLOR
        self.last: tuple[int, int] | None = None

    def update_direction(self) -> None:
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self) -> None:
        """Реализовано движение змейки.
        head_position - текущее расположение головы змейки.
        new_head_position - будущее расположение головы змейки.
        Реализован проход через границы экрана.
        Если длина змейки не увеличилась, то удаляем последний сегмент.
        """
        head_position = self.get_head_position()
        new_head_position = ((head_position[0] + self.direction[0]
                             * GRID_SIZE) % SCREEN_WIDTH, (head_position[1]
                             + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop(-1)

    def draw(self):
        """Отрисовывает змейку на игровой поверхности."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple[int, int]:
        """Реализован метод нахождения головы змейки."""
        return self.positions[0]

    def reset(self) -> None:
        """Реализован сброс змейки. Атрибуты приравниваются
        к изначальным параметрам, кроме direction.
        direction выбирается случайно из возможных вариантов.
        """
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = choice([RIGHT, LEFT, DOWN, UP])
        self.last = None
        self.next_direction = None


def handle_keys(game_object) -> None:
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main() -> None:
    """Основная функция проекта. Включает в себя
    иницилизацию классов и логику игры.
    apple - экземпляр яблока.
    snake - экземпляр змейки.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
            while apple.position in snake.position:
                # Гарантируем появление яблока вне змейки
                apple.position = apple.randomize_position()
        # Если змейка сталкивается с самой собой
        if snake.positions[0] in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()
        pygame.display.update()
        snake.move()


if __name__ == '__main__':
    main()
