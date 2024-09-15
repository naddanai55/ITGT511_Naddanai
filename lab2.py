import pygame
pygame.init()

screen = pygame.display.set_mode([1280, 720])

class Agent:
    def __init__(self, x, y):
        self.position = pygame.Vector2(100, 100)
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1

    def apply_force(self, x, y):
        force = pygame.Vector2(x, y)
        self.acceleration = self.acceleration + pygame.Vector2(force / self.mass)

    def update(self):
        self.velocity = self.velocity + self.acceleration
        self.position = self.position + self.velocity
        self.acceleration = pygame.Vector2(0, 0)
        
    def draw(self):
        pygame.draw.circle(screen, "red", self.position, 20)

agent1 = Agent(300 ,200)
agent1.apply_force(0, 1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")
    agent1.update()
    agent1.draw()
    pygame.display.flip()

pygame.quit()

