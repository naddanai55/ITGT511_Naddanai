import pygame
from utility import Mining_random

pygame.init()

WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  
font = pygame.font.Font(None, 28)
block_size = 240
mineral_drop = None
mineral_colors = {"silver": (176, 196, 222),
                  "gold": (255, 215, 0),
                  "diamond": (0, 255, 255)}   
mineral_text = None
block_break_status = True

mouse_click_count = 0
break_count = 0
no_drop_count = 0
no_break_count = 0
silver_count = 0
gold_count = 0
diamond_count = 0

mining_random = Mining_random()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click_count += 1
            mouse_x, mouse_y = event.pos
            if (WIDTH / 2) - (block_size / 2) <= mouse_x <= (WIDTH / 2) + (block_size / 2) and (HEIGHT / 2) - (block_size / 2) <= mouse_y <= (HEIGHT / 2) + (block_size / 2):
                if mining_random.to_break():
                    break_count += 1
                    print("break")
                    block_break_status = False
                    if mining_random.to_drop():
                        print("drop")
                        mineral_drop = mining_random.shuffle_draw()
                        mineral_text = mineral_drop
                        if mineral_drop == "silver":
                            silver_count += 1
                        if mineral_drop == "gold":
                            gold_count += 1
                        if mineral_drop == "diamond":
                            diamond_count += 1
                    else:
                        no_drop_count += 1
                        print("no drop")
                        mineral_drop = None
                        mineral_text = "no drop"
                else:
                    no_break_count += 1
                    print("no break")
                    mineral_text = None
                    mineral_drop = None
                    block_break_status = True
    
    screen.fill((177, 177, 163))
    mineral_drop_text = font.render(mineral_text, True, pygame.Color('black'))

    if mineral_drop:
        pygame.draw.circle(screen, mineral_colors[mineral_drop], ((WIDTH / 2), (HEIGHT / 2)), 60)
        screen.blit(mineral_drop_text,((WIDTH / 2) + 150, (HEIGHT / 2)))

    if mineral_text == "no drop":
        screen.blit(mineral_drop_text,((WIDTH / 2), (HEIGHT / 2)))

    if block_break_status:
        pygame.draw.rect(screen, (69, 0, 0), (WIDTH / 2 - block_size / 2, HEIGHT / 2 - block_size / 2, block_size, block_size))

    mouse_click = font.render(f"mouse click: {mouse_click_count}", True, pygame.Color('black'))
    break_text = font.render(f"break: {break_count}", True, pygame.Color('black'))
    no_break_text = font.render(f"no break: {no_break_count}", True, pygame.Color('black'))
    no_drop_text = font.render(f"no drop: {no_drop_count}", True, pygame.Color('black'))
    silver_text = font.render(f"silver: {silver_count}", True, pygame.Color('black'))
    gold_text = font.render(f"gold: {gold_count}", True, pygame.Color('black'))
    diamond_text = font.render(f"diamond: {diamond_count}", True, pygame.Color('black'))

    screen.blit(mouse_click, (WIDTH - mouse_click.get_width() - 10, 30))
    screen.blit(break_text, (WIDTH - break_text.get_width() - 10, 50))
    screen.blit(no_break_text, (WIDTH - no_break_text.get_width() - 10, 70))
    screen.blit(no_drop_text, (WIDTH - no_drop_text.get_width() - 10, 90))
    screen.blit(silver_text, (WIDTH - silver_text.get_width() - 10, 110))
    screen.blit(gold_text, (WIDTH - gold_text.get_width() - 10, 130))
    screen.blit(diamond_text, (WIDTH - diamond_text.get_width() - 10, 150))

    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('black'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    pygame.display.flip() 
    clock.tick(60)  
pygame.quit() 