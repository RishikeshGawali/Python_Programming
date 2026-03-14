import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Reptile with Legs - Cursor Follower")

clock = pygame.time.Clock()

segments = 45
segment_length = 12
points = [(WIDTH // 2, HEIGHT // 2)] * segments

def draw_leg(surface, base_pos, angle, side, t):
    leg_length1 = 18
    leg_length2 = 18

    offset_angle = angle + (math.pi/2 * side)

    knee_x = base_pos[0] + math.cos(offset_angle) * leg_length1
    knee_y = base_pos[1] + math.sin(offset_angle) * leg_length1

    wave = math.sin(t * 0.1) * 0.5
    foot_angle = offset_angle + wave

    foot_x = knee_x + math.cos(foot_angle) * leg_length2
    foot_y = knee_y + math.sin(foot_angle) * leg_length2

    pygame.draw.line(surface, (220,220,220), base_pos, (knee_x, knee_y), 3)
    pygame.draw.line(surface, (220,220,220), (knee_x, knee_y), (foot_x, foot_y), 3)

running = True
time_tick = 0

while running:
    clock.tick(60)
    time_tick += 1
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()
    points[0] = (mx, my)

    for i in range(1, segments):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]

        dx = x1 - x2
        dy = y1 - y2
        angle = math.atan2(dy, dx)

        x = x1 - math.cos(angle) * segment_length
        y = y1 - math.sin(angle) * segment_length

        points[i] = (x, y)

    # Draw body
    for i in range(segments - 1):
        thickness = max(1, 10 - i // 4)
        pygame.draw.line(screen, (200, 200, 200), points[i], points[i + 1], thickness)

    # Draw legs on selected segments
    leg_positions = [8, 15, 22, 30]
    for idx in leg_positions:
        if idx < segments - 1:
            x1, y1 = points[idx]
            x2, y2 = points[idx + 1]
            angle = math.atan2(y2 - y1, x2 - x1)

            draw_leg(screen, points[idx], angle, 1, time_tick)   # right
            draw_leg(screen, points[idx], angle, -1, time_tick)  # left

    pygame.display.flip()

pygame.quit()