import pygame

# Configuración inicial
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 700))  # Resolución ajustada
    pygame.display.set_caption("Mesa de Apuestas Ruleta")
    return screen, pygame.time.Clock()

# Constantes y colores
WIDTH, HEIGHT = 1200, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
LIGHT_GRAY = (220, 220, 220)

# Configuración de números y colores de la ruleta
numbers = [i for i in range(1, 37)]
numbers_colors = ["RED" if i % 2 != 0 else "BLACK" for i in range(1, 37)]

# Fichas
chips = [1, 5, 10, 25, 50, 100, 250, 500]
chip_colors = [BLUE, GREEN, RED, YELLOW, ORANGE, RED, WHITE, BLACK]

# Función para dibujar texto
def draw_text(screen, text, x, y, color=BLACK, center=False, size=20):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    if center:
        x -= rendered.get_width() // 2
        y -= rendered.get_height() // 2
    screen.blit(rendered, (x, y))

# Función para dibujar una celda con sombra
def draw_cell(screen, x, y, width, height, color, border_color=BLACK):
    shadow_offset = 3
    pygame.draw.rect(screen, GRAY, (x + shadow_offset, y + shadow_offset, width, height))
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)

# Función para dibujar el tablero de apuestas
def draw_betting_table(screen):
    # Tamaño ajustado
    cell_width, cell_height = 70, 40
    start_x, start_y = (WIDTH - 12 * cell_width) // 2, HEIGHT // 3 - 100

    # Dibujar números (1-36)
    for i in range(3):
        for j in range(12):
            number = j * 3 + i + 1
            if number <= 36:
                x, y = start_x + j * cell_width, start_y + i * cell_height
                color = RED if numbers_colors[number - 1] == "RED" else BLACK
                draw_cell(screen, x, y, cell_width, cell_height, color)
                draw_text(screen, str(number), x + cell_width // 2, y + cell_height // 2, WHITE, center=True)

    # Casilla para "0"
    draw_cell(screen, start_x - cell_width, start_y, cell_width, cell_height * 3, GREEN)
    draw_text(screen, "0", start_x - cell_width // 2, start_y + cell_height * 1.5, WHITE, center=True)

    # Opciones adicionales
    options = ["1st 12", "2nd 12", "3rd 12"]
    for i, option in enumerate(options):
        draw_cell(screen, start_x + i * 4 * cell_width, start_y + 3 * cell_height, 4 * cell_width, cell_height, DARK_GREEN)
        draw_text(screen, option, start_x + i * 4 * cell_width + 2 * cell_width, start_y + 3.5 * cell_height, BLACK, center=True)

    # Opciones extra (Odd, Even, Red, Black, 1-18, 19-36)
    extras = ["Odd", "Even", "Red", "Black", "1-18", "19-36"]
    extra_colors = [DARK_GREEN, DARK_GREEN, RED, BLACK, DARK_GREEN, DARK_GREEN]
    for i, option in enumerate(extras):
        x = start_x + i * 2 * cell_width
        y = start_y + 4 * cell_height
        draw_cell(screen, x, y, 2 * cell_width, cell_height, extra_colors[i])
        text_color = WHITE if option in ["Red", "Black"] else BLACK
        draw_text(screen, option, x + cell_width, y + cell_height // 2, text_color, center=True)

    # Opciones "2:1"
    for i in range(3):
        x = start_x + 12 * cell_width
        y = start_y + i * cell_height
        draw_cell(screen, x, y, cell_width, cell_height, DARK_GREEN)
        draw_text(screen, "2:1", x + cell_width // 2, y + cell_height // 2, BLACK, center=True)

# Función para dibujar fichas estilizadas
def draw_chip(screen, x, y, color, value):
    radius = 25
    border_thickness = 4

    # Borde externo
    pygame.draw.circle(screen, LIGHT_GRAY, (x, y), radius + border_thickness)

    # Cuerpo principal
    pygame.draw.circle(screen, color, (x, y), radius)

    # Círculo interno
    pygame.draw.circle(screen, LIGHT_GRAY, (x, y), radius - 8)

    # Valor de la ficha
    draw_text(screen, str(value), x, y, BLACK, center=True, size=16)

# Dibujar fichas
def draw_chips(screen):
    chip_x, chip_y = (WIDTH - 8 * 80) // 2, HEIGHT - 80
    for i, chip in enumerate(chips):
        draw_chip(screen, chip_x + i * 80, chip_y, chip_colors[i], chip)


# Loop principal
def main():
    screen, clock = init_game()

    while True:
        screen.fill(WHITE)

        draw_betting_table(screen)  # Dibujar tablero
        draw_chips(screen)  # Dibujar fichas


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.flip()
        clock.tick(60)

# Iniciar el juego
if __name__ == "__main__":
    main()
