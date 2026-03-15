import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skeleton Reptile Cursor")

clock = pygame.time.Clock()

SEGMENTS = 55
LENGTH = 10

points = [(WIDTH//2, HEIGHT//2) for _ in range(SEGMENTS)]

def draw_leg(base, angle, side):
    l1 = 18
    l2 = 20

    offset = angle + (math.pi/2 * side)

    knee = (
        base[0] + math.cos(offset) * l1,
        base[1] + math.sin(offset) * l1
    )

    foot = (
        knee[0] + math.cos(offset) * l2,
        knee[1] + math.sin(offset) * l2
    )

    pygame.draw.line(screen, (230,230,230), base, knee, 2)
    pygame.draw.line(screen, (230,230,230), knee, foot, 2)

running = True

while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    points[0] = (mx, my)

    # Inverse kinematics body
    for i in range(1, SEGMENTS):
        x1, y1 = points[i-1]
        x2, y2 = points[i]

        dx = x1 - x2
        dy = y1 - y2
        angle = math.atan2(dy, dx)

        x = x1 - math.cos(angle) * LENGTH
        y = y1 - math.sin(angle) * LENGTH
        points[i] = (x, y)

    # Draw spine
    for i in range(SEGMENTS-1):
        pygame.draw.line(screen, (200,200,200), points[i], points[i+1], 1)

    # Draw ribs
    for i in range(5, 35, 2):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        angle = math.atan2(y2-y1, x2-x1)

        rib_len = 10
        left = (
            x1 + math.cos(angle + math.pi/2) * rib_len,
            y1 + math.sin(angle + math.pi/2) * rib_len
        )
        right = (
            x1 + math.cos(angle - math.pi/2) * rib_len,
            y1 + math.sin(angle - math.pi/2) * rib_len
        )

        pygame.draw.line(screen, (200,200,200), left, right, 1)

    # Draw legs
    for idx in [10, 18, 26, 34]:
        if idx < SEGMENTS-1:
            x1, y1 = points[idx]
            x2, y2 = points[idx+1]
            ang = math.atan2(y2-y1, x2-x1)
            draw_leg(points[idx], ang, 1)
            draw_leg(points[idx], ang, -1)

    pygame.display.flip()

pygame.quit()