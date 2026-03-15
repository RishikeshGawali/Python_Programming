import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Realistic Skeleton Lizard")
clock = pygame.time.Clock()

# Body settings
segments = 55
segment_length = 10
points = [(WIDTH//2, HEIGHT//2)] * segments

# Walking control
prev_mouse = pygame.mouse.get_pos()
walk_cycle = 0

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def draw_ribs(surface):
    for i in range(5, 25, 2):
        x1, y1 = points[i]
        x2, y2 = points[i+1]
        angle = math.atan2(y2-y1, x2-x1)

        perp = angle + math.pi/2
        rib_length = 18 - i//3

        rx1 = x1 + math.cos(perp)*rib_length
        ry1 = y1 + math.sin(perp)*rib_length
        rx2 = x1 - math.cos(perp)*rib_length
        ry2 = y1 - math.sin(perp)*rib_length

        pygame.draw.line(surface, (220,220,220), (rx1,ry1), (rx2,ry2), 1)

def draw_leg(surface, index, side, phase):
    base = points[index]
    next_p = points[index+1]

    angle = math.atan2(next_p[1]-base[1], next_p[0]-base[0])
    side_angle = angle + (math.pi/2 * side)

    # Walking animation
    swing = math.sin(walk_cycle + phase) * 20

    upper_len = 25
    lower_len = 25

    # Shoulder to elbow
    ex = base[0] + math.cos(side_angle) * upper_len
    ey = base[1] + math.sin(side_angle) * upper_len

    # Elbow bend (forward/back motion)
    foot_angle = side_angle + math.radians(swing)

    fx = ex + math.cos(foot_angle) * lower_len
    fy = ey + math.sin(foot_angle) * lower_len

    # Draw bones
    pygame.draw.line(surface, (240,240,240), base, (ex,ey), 2)
    pygame.draw.line(surface, (240,240,240), (ex,ey), (fx,fy), 2)

    # Fingers (3 claws)
    for spread in [-0.3, 0, 0.3]:
        tx = fx + math.cos(foot_angle+spread)*10
        ty = fy + math.sin(foot_angle+spread)*10
        pygame.draw.line(surface, (240,240,240), (fx,fy), (tx,ty), 1)

running = True
while running:
    clock.tick(60)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()

    # Detect movement
    moving = distance(mouse, prev_mouse) > 1
    prev_mouse = mouse

    if moving:
        walk_cycle += 0.1

    # Head follows cursor
    points[0] = mouse

    # Spine
    for i in range(1, segments):
        x1,y1 = points[i-1]
        x2,y2 = points[i]

        dx = x1-x2
        dy = y1-y2
        angle = math.atan2(dy, dx)

        x = x1 - math.cos(angle)*segment_length
        y = y1 - math.sin(angle)*segment_length

        points[i] = (x,y)

    # Draw spine & tail
    for i in range(segments-1):
        thickness = max(1, 6 - i//8)
        pygame.draw.line(screen,(200,200,200),points[i],points[i+1],thickness)

    # Draw ribs
    draw_ribs(screen)

    # 3 Pairs of legs
    leg_positions = [8, 18, 28]

    for i, pos in enumerate(leg_positions):
        if pos < segments-1:
            # Right side
            draw_leg(screen, pos, 1, i*math.pi)
            # Left side (opposite phase for natural gait)
            draw_leg(screen, pos, -1, i*math.pi + math.pi)

    pygame.display.flip()

pygame.quit()