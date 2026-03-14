import pygame
import math

pygame.init()

# Screen setup
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reptile Cursor")

clock = pygame.time.Clock()

# Reptile settings
segments = 40
segment_length = 12
points = [(WIDTH // 2, HEIGHT // 2)] * segments

running = True
while running:
    clock.tick(60)
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Head follows mouse
    mx, my = pygame.mouse.get_pos()
    points[0] = (mx, my)

    # Each segment follows previous
    for i in range(1, segments):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]

        dx = x1 - x2
        dy = y1 - y2
        angle = math.atan2(dy, dx)

        x = x1 - math.cos(angle) * segment_length
        y = y1 - math.sin(angle) * segment_length

        points[i] = (x, y)

    # Draw reptile body
    for i in range(segments - 1):
        thickness = max(1, 8 - i // 5)
        pygame.draw.line(screen, (200, 200, 200), points[i], points[i + 1], thickness)

    pygame.display.flip()

pygame.quit()