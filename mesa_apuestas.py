import pygame
import random
import math

# Configuración inicial
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))  # Resolución ajustada
    pygame.display.set_caption("Ruleta de Casino Realista con Mesa de Apuestas")
    return screen, pygame.time.Clock()

# Constantes y colores
WIDTH, HEIGHT = 1600, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 120, 0)
DARK_GREEN = (0, 100, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (169, 169, 169)
LIGHT_GRAY = (211, 211, 211)
SILVER = (192, 192, 192)
WOOD_BROWN = (139, 69, 19)
DARK_GRAY = (105, 105, 105)
BULLET_COLOR = WOOD_BROWN

# Configuración de números y colores de la ruleta
roulette_numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
roulette_colors = [
    "GREEN", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK",
    "RED", "BLACK", "BLACK", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK",
    "RED", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK",
    "RED", "BLACK", "BLACK", "RED", "BLACK", "RED", "BLACK", "RED", "BLACK", "RED"
]
chips = [1, 5, 10, 25, 50, 100, 250, 500]
chip_colors = [BLUE, GREEN, RED, YELLOW, ORANGE, RED, WHITE, BLACK]

balance = 1000  # Saldo inicial del jugador
bet_total = 0  # Total apostado
betting_area = []  # Área donde se colocan las fichas

# Dibujar texto
def draw_text(screen, text, x, y, color=BLACK, center=False, size=20):
    try:
        font = pygame.font.SysFont("Arial", size)
    except pygame.error:
        font = pygame.font.Font(None, size)
    rendered = font.render(text, True, color)
    if center:
        x -= rendered.get_width() // 2
        y -= rendered.get_height() // 2
    screen.blit(rendered, (x, y))


# Dibujar celda
def draw_cell(screen, x, y, width, height, color, border_color=BLACK):
    shadow_offset = 3
    pygame.draw.rect(screen, GRAY, (x + shadow_offset, y + shadow_offset, width, height))
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, border_color, (x, y, width, height), 2)

# Dibujar la ruleta
def draw_roulette(screen, angle=0):
    center_x, center_y = WIDTH // 5.2, HEIGHT // 2
    radius_outer = 250
    radius_inner = 200
    hole_radius = 60
    pygame.draw.circle(screen, WOOD_BROWN, (center_x, center_y), radius_outer + 10)
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius_outer)
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_outer, 5)
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_inner, 5)
    pygame.draw.circle(screen, LIGHT_GRAY, (center_x, center_y), hole_radius)
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), hole_radius - 10)

    # Dibujar la cruz
    cross_size = 90
    pygame.draw.line(screen, WOOD_BROWN, (center_x - cross_size, center_y), (center_x + cross_size, center_y), 8)
    pygame.draw.line(screen, WOOD_BROWN, (center_x, center_y - cross_size), (center_x, center_y + cross_size), 8)
    ball_radius = 12
    pygame.draw.circle(screen, BULLET_COLOR, (center_x, center_y), ball_radius)

    # Dibujar las secciones de la ruleta
    num_sections = len(roulette_numbers)
    for i, number in enumerate(roulette_numbers):
        start_angle = math.radians((360 * i / num_sections) + angle)
        end_angle = math.radians((360 * (i + 1) / num_sections) + angle)
        color = GREEN if number == 0 else RED if roulette_colors[i] == "RED" else BLACK
        points = [
            (
                center_x + radius_inner * math.cos(start_angle),
                center_y + radius_inner * math.sin(start_angle),
            ),
            (
                center_x + radius_outer * math.cos(start_angle),
                center_y + radius_outer * math.sin(start_angle),
            ),
            (
                center_x + radius_outer * math.cos(end_angle),
                center_y + radius_outer * math.sin(end_angle),
            ),
            (
                center_x + radius_inner * math.cos(end_angle),
                center_y + radius_inner * math.sin(end_angle),
            ),
        ]
        pygame.draw.polygon(screen, color, points)
        pygame.draw.lines(screen, SILVER, True, points, 3)

        text_angle = (start_angle + end_angle) / 2
        text_x = center_x + (radius_inner + radius_outer) // 2 * math.cos(text_angle)
        text_y = center_y + (radius_inner + radius_outer) // 2 * math.sin(text_angle)
        text_color = WHITE if color != GREEN else BLACK
        draw_text(screen, str(number), text_x, text_y, text_color, center=True)

# Dibujar mesa de apuestas
def draw_betting_table(screen):
    # Definir el tamaño de las celdas de la mesa de apuestas
    cell_width, cell_height = 70, 40
    
    # Ajustar la posición inicial para mover la mesa a la derecha
    start_x, start_y = WIDTH // 2.1 - 100, HEIGHT // 2.2 - 100  


    # Dibujar números (1-36)
    for i in range(3):
        for j in range(12):
            number = j * 3 + i + 1
            if number <= 36:
                x, y = start_x + j * cell_width, start_y + i * cell_height
                color = RED if roulette_colors[number] == "RED" else BLACK
                draw_cell(screen, x, y, cell_width, cell_height, color)
                draw_text(screen, str(number), x + cell_width // 2, y + cell_height // 2, WHITE, center=True)

    # Casilla para "0"
    draw_cell(screen, start_x - cell_width, start_y, cell_width, cell_height * 3, GREEN)
    draw_text(screen, "0", start_x - cell_width // 2, start_y + cell_height * 1.5, WHITE, center=True)

    # Opciones adicionales (1st 12, 2nd 12, 3rd 12)
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

# Dibujar fichas
# Dibujar fichas
# Dibujar fichas con nuevo diseño estético
def draw_chips(screen):
    # Establecer la posición inicial de las fichas
    start_x, chip_y = WIDTH // 1.9, HEIGHT // 1.5  # Colocar las fichas debajo de la mesa de apuestas, ajustando el eje X para distribuirlas
    
    for i, chip in enumerate(chips):
        chip_x = start_x + i * 60  # Ajustar la separación horizontal entre fichas
        
        color = chip_colors[i]
        
        # Sombra de la ficha (para dar un efecto 3D)
        # Dibujo del círculo principal (ficha)
        pygame.draw.circle(screen, color, (chip_x, chip_y), 25)
        
        # Borde exterior (para darle más énfasis a la ficha)
        pygame.draw.circle(screen, BLACK, (chip_x, chip_y), 25, 3)  # Borde negro
        
        # Agregar un texto con un poco de estilo (con fondo y bordes)
        draw_text(screen, str(chip), chip_x, chip_y, WHITE, center=True, size=24)  # Texto en blanco
        
        # Añadir un efecto de borde en el texto
        draw_text(screen, str(chip), chip_x - 1, chip_y - 1, BLACK, center=True, size=24)  # Borde negro en el texto

def place_chip_on_betting_table(event, chips, betting_area):
    global balance, bet_total

    for i, chip in enumerate(chips):
        chip_x, chip_y = WIDTH - 150, HEIGHT // 3 + i * 50
        chip_rect = pygame.Rect(chip_x - 25, chip_y - 25, 50, 50)  # Rectángulo para la ficha

        # Si el jugador hace clic sobre una ficha, agregarla a la mesa de apuestas
        if chip_rect.collidepoint(event.pos) and balance >= chip:
            bet_total += chip  # Añadir el valor de la ficha a la apuesta total
            balance -= chip  # Restar el valor de la ficha del saldo
            betting_area.append(chip)  # Agregar la ficha al área de apuestas

def get_number_from_angle(angle):
    # Orden correcto de los números en la ruleta, en sentido horario desde el triángulo
    numbers = [9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31]

    # Cada número ocupa una fracción del círculo completo (360° / 37 números)
    sector_angle = 360 / len(numbers)

    # Ajustar el ángulo para que el triángulo quede sincronizado con el número
    adjusted_angle = (angle + (sector_angle / 2)) % 360

    # Determinar el índice del número apuntado por el triángulo
    index = int(adjusted_angle // sector_angle)

    # Retornar el número correspondiente
    return numbers[index]

def draw_triangle(screen):
    # Posición del triángulo
    center_x, center_y = WIDTH // 5.2, HEIGHT // 2
    triangle_width = 30
    triangle_height = 20
    
    # Coordenadas del triángulo (apuntando hacia abajo)
    triangle_points = [
        (center_x, center_y - 260),  # Vértice superior
        (center_x - triangle_width // 2, center_y - 260 - triangle_height),  # Esquina izquierda
        (center_x + triangle_width // 2, center_y - 260 - triangle_height),  # Esquina derecha
    ]

    # Dibujar el triángulo
    pygame.draw.polygon(screen, RED, triangle_points)
    pygame.draw.lines(screen, BLACK, True, triangle_points, 2)  # Borde negro


def spin_roulette_animation(screen, clock, initial_angle):
    current_angle = initial_angle
    speed = random.uniform(15, 20)  # Velocidad inicial
    deceleration = 0.98  # Desaceleración

    while speed > 0.1:
        current_angle += speed
        current_angle %= 360
        speed *= deceleration

        # Dibujar todo durante la animación
        screen.fill(WHITE)
        draw_roulette(screen, current_angle)  # Dibujar ruleta girando
        draw_triangle(screen)  # Dibujar triángulo después de la ruleta
        pygame.display.flip()
        clock.tick(60)

    # Obtener el número final basado en el ángulo
    result = get_number_from_angle(current_angle)
    return result, current_angle

# Bucle principal
def main():
    screen, clock = init_game()
    angle = 0
    result = None
    running = True

    while running:
        screen.fill(WHITE)

    # Dibujar la ruleta
        draw_roulette(screen, angle)

    # Dibujar el triángulo indicador (siempre visible)
        draw_triangle(screen)

    # Dibujar la mesa de apuestas y fichas
        draw_betting_table(screen)
        draw_chips(screen)

    # Dibujar el botón "Girar"
        button_x, button_y = WIDTH // 2 - 60, HEIGHT - 100
        button_width, button_height = 120, 50
        pygame.draw.rect(screen, RED, (button_x, button_y, button_width, button_height))
        draw_text(screen, "Girar", button_x + button_width // 2, button_y + button_height // 2, WHITE, center=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[1] <= button_y + button_height:
                    result, angle = spin_roulette_animation(screen, clock, angle)

    # Mostrar el resultado
        draw_text(screen, f"Resultado: {result}" if result is not None else "Resultado: ---", WIDTH // 2, 50, BLACK, center=True)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
