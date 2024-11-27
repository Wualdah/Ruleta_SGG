import pygame
import random
import math

# Configuración inicial
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((1600, 900))  # Resolución mayor
    pygame.display.set_caption("Ruleta de Casino Realista con Cruz y Bolitas")
    return screen, pygame.time.Clock()

# Constantes y variables globales
WIDTH, HEIGHT = 1600, 900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 120, 0)  # Verde más oscuro
RED = (255, 0, 0)
GRAY = (169, 169, 169)
SILVER = (192, 192, 192)
WOOD_BROWN = (139, 69, 19)  # Color marrón madera para el borde y las bolas
LIGHT_GRAY = (211, 211, 211)  # Gris claro para detalles de bordes
DARK_GRAY = (100, 100, 100)  # Gris oscuro para sombras
BULLET_COLOR = WOOD_BROWN  # Color de las bolitas de la cruz (madera)

# Configuración de números y colores de la ruleta
roulette_numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
roulette_colors = ["GREEN"] + ["RED" if i % 2 == 0 else "BLACK" for i in range(1, 37)]

# Función para dibujar un texto
def draw_text(screen, text, x, y, color=BLACK, center=False, size=20):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    if center:
        x -= rendered.get_width() // 2
        y -= rendered.get_height() // 2
    screen.blit(rendered, (x, y))

# Función para dibujar la ruleta con perspectiva 3D y la cruz en el centro con bolitas
def draw_roulette(screen, angle=0, result=None):
    center_x, center_y = WIDTH // 4, HEIGHT // 2  # Posición de la ruleta
    radius_outer = 250
    radius_inner = 200
    hole_radius = 60

    # Dibujar la base metálica de la ruleta (usando gradientes)
    pygame.draw.circle(screen, WOOD_BROWN, (center_x, center_y), radius_outer + 10)  # Borde de madera más pequeño
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius_outer)  # Cuerpo de la ruleta
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_outer, 5)  # Borde exterior (brillante)
    pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_inner, 5)  # Borde interior (brillante)

    # Agregar un efecto de profundidad al centro de la ruleta
    pygame.draw.circle(screen, LIGHT_GRAY, (center_x, center_y), hole_radius)  # Hueco central más detallado
    pygame.draw.circle(screen, DARK_GRAY, (center_x, center_y), hole_radius - 10)  # Detalle en el borde del hueco

    # Dibujar la cruz en el centro de la ruleta (simulando lo que aparece en las ruletas reales)
    cross_size = 90  # Aumentado tamaño de la cruz
    pygame.draw.line(screen, WOOD_BROWN, (center_x - cross_size, center_y), (center_x + cross_size, center_y), 8)  # Línea horizontal más gruesa
    pygame.draw.line(screen, WOOD_BROWN, (center_x, center_y - cross_size), (center_x, center_y + cross_size), 8)  # Línea vertical más gruesa

    # Dibujar bolitas en las puntas de la cruz (más grandes y marrones como la cruz)
    ball_radius = 12  # Tamaño de las bolitas más grandes
    pygame.draw.circle(screen, BULLET_COLOR, (center_x - cross_size, center_y), ball_radius)  # Bolita en la punta izquierda
    pygame.draw.circle(screen, BULLET_COLOR, (center_x + cross_size, center_y), ball_radius)  # Bolita en la punta derecha
    pygame.draw.circle(screen, BULLET_COLOR, (center_x, center_y - cross_size), ball_radius)  # Bolita en la punta superior
    pygame.draw.circle(screen, BULLET_COLOR, (center_x, center_y + cross_size), ball_radius)  # Bolita en la punta inferior
    pygame.draw.circle(screen, BULLET_COLOR, (center_x, center_y), ball_radius)  # Bolita en el centro de la cruz

    # Dibujar segmentos numerados con un diseño 3D
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
        pygame.draw.lines(screen, SILVER, True, points, 3)  # Líneas plateadas para bordes

        # Dibujar los números dentro de la ruleta (con perspectiva)
        text_angle = (start_angle + end_angle) / 2
        text_x = center_x + (radius_inner + radius_outer) // 2 * math.cos(text_angle)
        text_y = center_y + (radius_inner + radius_outer) // 2 * math.sin(text_angle)
        text_color = WHITE if color != GREEN else BLACK
        draw_text(screen, str(number), text_x, text_y, text_color, center=True)

    # Añadir un brillo metálico al borde exterior de la ruleta
    pygame.draw.circle(screen, WOOD_BROWN, (center_x, center_y), radius_outer, 5)  # Borde exterior de madera

    # Dibujar triángulo apuntando hacia abajo (más nítido y detallado)
    triangle_height = 40
    triangle_width = 60
    pygame.draw.polygon(screen, GRAY, [
        (center_x - triangle_width // 2, center_y - radius_outer - triangle_height),
        (center_x + triangle_width // 2, center_y - radius_outer - triangle_height),
        (center_x, center_y - radius_outer)
    ])

# Función para obtener el número en función del ángulo
def get_number_from_angle(angle):
    angle_per_number = 360 / len(roulette_numbers)
    initial_index = roulette_numbers.index(9)  # Suponemos que el número inicial en el centro es 29
    
    # Calcular el índice del número en función del ángulo
    index = (initial_index + int(angle / angle_per_number)) % len(roulette_numbers)
    
    return roulette_numbers[index]

# Función para actualizar la pantalla
def update_screen(screen, angle, result):
    screen.fill(BLACK)
    draw_roulette(screen, angle, result)
    pygame.display.update()

# Función para animación de la ruleta con un giro más fluido
def spin_roulette_animation(screen, clock, initial_angle):
    current_angle = initial_angle
    initial_speed = 30  # Velocidad inicial
    deceleration_factor = 0.98  # Factor de desaceleración
    max_time = 5  # Tiempo máximo en segundos
    elapsed_time = 0  # Tiempo transcurrido

    while elapsed_time < max_time:
        current_angle += initial_speed
        current_angle %= 360  # Asegurarse de que el ángulo no exceda 360
        initial_speed *= deceleration_factor
        elapsed_time += 1 / 60  # Actualizar el tiempo

        # Calcular el número en el ángulo actual
        result = get_number_from_angle(current_angle)

        # Actualizar pantalla
        update_screen(screen, current_angle, result)
        clock.tick(60)

    return result, current_angle

# Función principal
def main():
    screen, clock = init_game()
    angle = 0
    result = None
    running = True

    while running:
        screen.fill(BLACK)
        draw_roulette(screen, angle, result)

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

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()