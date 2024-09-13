import pygame
import math
pygame.init()

screen = pygame.display.set_mode([500, 500])

speed = 0.01  
target_pos = (250, 250)
agents = [(i * 100, 450) for i in range(5)]


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        target_pos = pygame.mouse.get_pos()

    target_x, target_y = target_pos
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (target_pos), 10)

    for i in range(len(agents)):
        agent_x, agent_y = agents[i]
        #direction
        direction_x = target_x - agent_x
        direction_y = target_y - agent_y
        distance = math.hypot(direction_x, direction_y)
        #normalize
        direction_x /= distance
        direction_y /= distance
        #move
        agent_x += direction_x * speed 
        agent_y += direction_y * speed 
        agents[i] = (agent_x, agent_y)
        pygame.draw.circle(screen, (0, 0, 255), (int(agent_x), int(agent_y)), 10)

    pygame.draw.circle(screen, (255, 0, 0), (target_pos), 10)
    pygame.display.flip()

pygame.quit()