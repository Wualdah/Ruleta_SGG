import pygame
import random
import math

# Configuración inicial
def init_game():
    pygame.init()
    screen = pygame.display.set_mode((1200, 800))
    pygame.display.set_caption("Ruleta de Casino")
    return screen, pygame.time.Clock()

# Colores y constantes
WIDTH, HEIGHT = 1200, 800
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

# Números y colores de la ruleta
numbers = [0] + [i for i in range(1, 37)]
numbers_colors = ["GREEN"] + ["RED" if i % 2 != 0 else "BLACK" for i in range(1, 37)]

# Fichas
chips = [1, 5, 10, 25, 50, 100]
chip_colors = [BLUE, GREEN, RED, YELLOW, ORANGE, BLACK]
selected_chip = None  # Ficha seleccionada por el jugador

# Apuestas
bets = []  # Lista de apuestas: [(posición, valor, tipo), ...]
balance = 1000  # Dinero disponible

# Estados del juego
winner = None  # Número ganador
spinning = False  # Si la ruleta está girando

# Función para dibujar texto
def draw_text(screen, text, x, y, color=BLACK, center=False, size=20):
    font = pygame.font.SysFont("Arial", size)
    rendered = font.render(text, True, color)
    if center:
        x -= rendered.get_width() // 2
        y -= rendered.get_height() // 2
    screen.blit(rendered, (x, y))

# Dibujar el tablero de apuestas
def draw_betting_table(screen):
    cell_width, cell_height = 70, 50
    start_x, start_y = (WIDTH - 12 * cell_width) // 2, HEIGHT // 3 - 100

    # Dibujar números (1-36)
    for i in range(3):
        for j in range(12):
            number = j * 3 + i + 1
            if number <= 36:
                x, y = start_x + j * cell_width, start_y + i * cell_height
                color = RED if numbers_colors[number] == "RED" else BLACK
                pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
                pygame.draw.rect(screen, BLACK, (x, y, cell_width, cell_height), 2)
                draw_text(screen, str(number), x + cell_width // 2, y + cell_height // 2, WHITE, center=True)

    # Casilla para "0"
    pygame.draw.rect(screen, GREEN, (start_x - cell_width, start_y, cell_width, cell_height * 3))
    pygame.draw.rect(screen, BLACK, (start_x - cell_width, start_y, cell_width, cell_height * 3), 2)
    draw_text(screen, "0", start_x - cell_width // 2, start_y + cell_height * 1.5, WHITE, center=True)

    # Opciones adicionales (1st 12, 2nd 12, 3rd 12)
    options = ["1st 12", "2nd 12", "3rd 12"]
    for i, option in enumerate(options):
        x = start_x + i * 4 * cell_width
        y = start_y + 3 * cell_height
        pygame.draw.rect(screen, DARK_GREEN, (x, y, 4 * cell_width, cell_height))
        pygame.draw.rect(screen, BLACK, (x, y, 4 * cell_width, cell_height), 2)
        draw_text(screen, option, x + 2 * cell_width, y + cell_height // 2, WHITE, center=True)

    # Opciones de color/par/impar
    extras = ["Odd", "Even", "Red", "Black", "1-18", "19-36"]
    extra_colors = [DARK_GREEN, DARK_GREEN, RED, BLACK, DARK_GREEN, DARK_GREEN]
    for i, option in enumerate(extras):
        x = start_x + i * 2 * cell_width
        y = start_y + 4 * cell_height
        pygame.draw.rect(screen, extra_colors[i], (x, y, 2 * cell_width, cell_height))
        pygame.draw.rect(screen, BLACK, (x, y, 2 * cell_width, cell_height), 2)
        text_color = WHITE if option in ["Red", "Black"] else BLACK
        draw_text(screen, option, x + cell_width, y + cell_height // 2, text_color, center=True)

# Dibujar las fichas disponibles
def draw_chips(screen):
    chip_x, chip_y = 50, HEIGHT - 150
    for i, chip in enumerate(chips):
        x = chip_x + i * 80
        y = chip_y
        radius = 30
        pygame.draw.circle(screen, chip_colors[i], (x, y), radius)
        draw_text(screen, str(chip), x, y, WHITE, center=True, size=20)
        if chip == selected_chip:
            pygame.draw.circle(screen, RED, (x, y), radius + 5, 3)

# Dibujar la ruleta
def draw_roulette(screen, angle):
    center_x, center_y = WIDTH // 2, HEIGHT // 6
    radius = 120
    pygame.draw.circle(screen, GREEN, (center_x, center_y), radius)
    for i, number in enumerate(numbers):
        theta = math.radians((angle + i * 360 / len(numbers)) % 360)
        x = center_x + int(radius * math.cos(theta))
        y = center_y + int(radius * math.sin(theta))
        color = RED if numbers_colors[i] == "RED" else BLACK
        if numbers_colors[i] == "GREEN":
            color = GREEN
        pygame.draw.circle(screen, color, (x, y), 20)
        draw_text(screen, str(number), x, y, WHITE, center=True, size=15)

# Animación de la ruleta
def spin_roulette_animation(screen):
    angle = 0
    for _ in range(180):  # Duración de la animación
        screen.fill(WHITE)
        draw_betting_table(screen)
        draw_chips(screen)
        draw_roulette(screen, angle)
        draw_text(screen, "Girando...", WIDTH // 2, HEIGHT - 50, BLACK, center=True, size=30)
        pygame.display.flip()
        angle += 10

    # Determinar el número ganador
    return random.choice(numbers)

# Manejar clics en las fichas
def handle_chip_click(pos):
    global selected_chip
    chip_x, chip_y = 50, HEIGHT - 150
    for i, chip in enumerate(chips):
        x = chip_x + i * 80
        y = chip_y
        if math.sqrt((pos[0] - x) ** 2 + (pos[1] - y) ** 2) <= 30:
            selected_chip = chip
            break

# Manejar clics en el tablero
def handle_board_click(pos):
    global selected_chip, balance
    if not selected_chip or balance < selected_chip:
        return

    cell_width, cell_height = 70, 50
    start_x, start_y = (WIDTH - 12 * cell_width) // 2, HEIGHT // 3 - 100

    # Detectar celda del tablero
    x, y = pos
    col = (x - start_x) // cell_width
    row = (y - start_y) // cell_height

    if 0 <= col < 12 and 0 <= row < 3:
        bet_x = start_x + col * cell_width + cell_width // 2
        bet_y = start_y + row * cell_height + cell_height // 2
        bets.append((bet_x, bet_y, selected_chip))
        balance -= selected_chip

# Calcular pagos
def calculate_payout(winner):
    global balance
    for bet in bets:
        _, _, value = bet
        if winner == 0:  # Simulación básica
            balance += value * 35  # Apuesta directa
        else:
            balance += value * 2  # Apuesta general

# Main loop
def main():
    global balance, bets, winner, spinning

    screen, clock = init_game()
    while True:
        screen.fill(WHITE)

        draw_betting_table(screen)
        draw_chips(screen)
        draw_roulette(screen, 0 if not spinning else random.randint(0, 360))
        draw_text(screen, f"Saldo: ${balance}", 100, 50, BLACK, size=30)

        if winner is not None:
            draw_text(screen, f"Número Ganador: {winner}", WIDTH // 2, HEIGHT - 100, BLACK, center=True, size=30)

        for bet in bets:
            pygame.draw.circle(screen, RED, (bet[0], bet[1]), 15)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if spinning:
                    continue
                if HEIGHT - 200 < event.pos[1] < HEIGHT - 100:
                    handle_chip_click(event.pos)
                else:
                    handle_board_click(event.pos)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not spinning:
                spinning = True
                winner = spin_roulette_animation(screen)
                calculate_payout(winner)
                spinning = False
                bets.clear()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
