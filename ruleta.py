        import pygame
        import random
        import math

        # Configuración inicial
        def init_game():
            pygame.init()
            screen = pygame.display.set_mode((1600, 900))  # Resolución mayor
            pygame.display.set_caption("Ruleta de Casino")
            return screen, pygame.time.Clock()

        # Constantes y variables globales
        WIDTH, HEIGHT = 1600, 900  # Nueva resolución más grande
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GRAY = (169, 169, 169)  # Gris para el triángulo
        GREEN = (0, 200, 0)
        RED = (255, 0, 0)

        # Configuración de números y colores de la ruleta
        roulette_numbers = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        roulette_colors = ["GREEN"] + ["RED" if i % 2 == 0 else "BLACK" for i in range(1, 37)]

        # Dibujar texto
        def draw_text(screen, text, x, y, color=BLACK, center=False, size=20):
            font = pygame.font.SysFont("Arial", size)
            rendered = font.render(text, True, color)
            if center:
                x -= rendered.get_width() // 2
                y -= rendered.get_height() // 2
            screen.blit(rendered, (x, y))

        # Dibujar ruleta rediseñada con hueco central y bordes
        def draw_roulette(screen, angle=0, result=None):
            center_x, center_y = WIDTH // 4, HEIGHT // 2  # Cambiar posición para que esté a la izquierda
            radius_outer = 200  # Aumentamos el tamaño de la ruleta
            radius_inner = 150  # Aumentamos el radio interior también
            hole_radius = 60  # Tamaño del hueco central, también se ha aumentado

            # Dibujar círculo exterior para el fondo
            pygame.draw.circle(screen, GREEN, (center_x, center_y), radius_outer)

            # Dibujar bordes de la ruleta
            pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_outer, 5)  # Borde exterior
            pygame.draw.circle(screen, WHITE, (center_x, center_y), radius_inner, 5)  # Borde interior

            # Dibujar segmentos numerados
            num_sections = len(roulette_numbers)
            for i, number in enumerate(roulette_numbers):
                # Calcular el ángulo de cada segmento
                start_angle = math.radians((360 * i / num_sections) + angle)
                end_angle = math.radians((360 * (i + 1) / num_sections) + angle)

                # Determinar color del segmento
                color = GREEN if number == 0 else RED if roulette_colors[i] == "RED" else BLACK

                # Dibujar el segmento
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

                # Dibujar borde del segmento
                pygame.draw.lines(screen, WHITE, True, points, 2)

                # Calcular posición del texto
                text_angle = (start_angle + end_angle) / 2
                text_x = center_x + (radius_inner + radius_outer) // 2 * math.cos(text_angle)
                text_y = center_y + (radius_inner + radius_outer) // 2 * math.sin(text_angle)

                # Dibujar número
                text_color = WHITE if color != GREEN else BLACK
                draw_text(screen, str(number), text_x, text_y, text_color, center=True)

            # Dibujar hueco central
            pygame.draw.circle(screen, WHITE, (center_x, center_y), hole_radius)

            # Dibujar el triángulo gris debajo de la ruleta, apuntando hacia abajo
            triangle_height = 20  # Altura del triángulo
            triangle_width = 40   # Base del triángulo
            pygame.draw.polygon(screen, GRAY, [
                (center_x - triangle_width // 2, center_y + radius_outer),
                (center_x + triangle_width // 2, center_y + radius_outer),
                (center_x, center_y + radius_outer + triangle_height)
            ])

            # Si hay un resultado, mostrarlo en el centro
            if result is not None:
                draw_text(screen, str(result), center_x, center_y, BLACK, center=True, size=40)

        # Dibujar mesa (con tres filas de celdas)
        def draw_table(screen):
            cell_width, cell_height = 50, 50
            start_x, start_y = 750, HEIGHT // 2 - 150  # Ajustar la posición para separar la mesa de la ruleta

            # Dibujar tres filas con números
            for i in range(3):
                for j in range(12):
                    x, y = start_x + j * cell_width, start_y + i * cell_height
                    number = j * 3 + i + 1
                    if number <= 36:
                        color = RED if number % 2 != 0 else BLACK
                        pygame.draw.rect(screen, color, (x, y, cell_width, cell_height))
                        draw_text(screen, str(number), x + cell_width // 2, y + cell_height // 2, WHITE, center=True)

            # Celda verde para el 0
            pygame.draw.rect(screen, GREEN, (start_x - cell_width, start_y, cell_width, 3 * cell_height))
            draw_text(screen, "0", start_x - cell_width // 2, start_y + 3 * cell_height // 2, WHITE, center=True)

            # Opciones adicionales (1st 12, 2nd 12, etc.)
            options = ["1st 12", "2nd 12", "3rd 12"]
            for i, option in enumerate(options):
                pygame.draw.rect(screen, GREEN, (start_x + i * 4 * cell_width, start_y + 3 * cell_height, 4 * cell_width, cell_height))
                draw_text(screen, option, start_x + i * 4 * cell_width + 2 * cell_width, start_y + 3.5 * cell_height, BLACK, center=True)

            # Opciones extra (Odd, Even, etc.)
            extras = ["Odd", "Even", "Red", "Black", "1-18", "19-36"]
            extra_colors = [GREEN, GREEN, RED, BLACK, GREEN, GREEN]
            for i, option in enumerate(extras):
                x = start_x + i * 2 * cell_width
                y = start_y + 4 * cell_height
                pygame.draw.rect(screen, extra_colors[i], (x, y, 2 * cell_width, cell_height))
                text_color = WHITE if option in ["Red", "Black"] else BLACK
                draw_text(screen, option, x + cell_width, y + cell_height // 2, text_color, center=True)

            # Añadir las tres casillas para "2:1" a la derecha de la mesa
            for i in range(3):
                x = start_x + 12 * cell_width + 10  # Posición a la derecha de la mesa
                y = start_y + i * cell_height
                pygame.draw.rect(screen, GREEN, (x, y, 2 * cell_width, cell_height))
                draw_text(screen, "2:1", x + cell_width, y + cell_height // 2, BLACK, center=True)

        # Animación del giro con desaceleración progresiva
        def spin_roulette_animation(screen, clock, current_angle):
            target_angle = random.randint(0, 360)  # Ángulo aleatorio para el giro
            spins = random.randint(4, 6)  # Cuántas vueltas dará
            total_rotation = target_angle + 360 * spins
            deceleration_factor = 0.98  # Factor de desaceleración

            # Animar el giro
            while total_rotation > 0:
                total_rotation -= 5
                current_angle += 5
                update_screen(screen, int(current_angle) % 360)
                clock.tick(60)

            result = roulette_numbers[int((current_angle % 360) / (360 / len(roulette_numbers)))]
            update_screen(screen, int(current_angle) % 360, result)
            return result, target_angle % 360

        # Función para actualizar la pantalla
        def update_screen(screen, angle, result=None):
            screen.fill(BLACK)
            draw_roulette(screen, angle, result)
            draw_table(screen)
            pygame.display.update()

        # Función para dibujar el botón
        def draw_button(screen, x, y, width, height, text):
            pygame.draw.rect(screen, RED, (x, y, width, height))
            draw_text(screen, text, x + width // 2, y + height // 2, WHITE, center=True)

        # Función principal
        def main():
            screen, clock = init_game()
            angle = 0
            result = None
            can_spin = True

            while True:
                update_screen(screen, angle, result)
                draw_button(screen, WIDTH // 2 - 60, HEIGHT - 100, 120, 50, "Girar")

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        # Detectar si se hace clic en el botón "Girar"
                        if WIDTH // 2 - 60 <= event.pos[0] <= WIDTH // 2 + 60 and HEIGHT - 100 <= event.pos[1] <= HEIGHT - 50:
                            if can_spin:
                                result, angle = spin_roulette_animation(screen, clock, angle)
                                can_spin = False

                # Permitir girar nuevamente después de 1.5 segundos
                if result is not None and not can_spin:
                    pygame.time.wait(1500)
                    can_spin = True

            pygame.quit()

        if __name__ == "__main__":
            main()