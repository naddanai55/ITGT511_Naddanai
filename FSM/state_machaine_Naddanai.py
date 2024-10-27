import pygame
import random
import math
from enum import Enum
from abc import ABC, abstractmethod

WIDTH, HEIGHT = 800, 600
NUM_AGENTS = 1
FOOD_SIZE = 5
MAX_SPEED = 1.5

MAX_SPEED_IDLE = 0.8
MAX_SPEED_ATK = 0.5
MAX_SPEED_EAT = 0.1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("State Machine")
font = pygame.font.Font(None, 28)

idle_sprite_sheet = pygame.image.load('./assets/idle.png').convert_alpha()
zombie_idle = [idle_sprite_sheet.subsurface(pygame.Rect(x * 96, 0, 96, 96)) for x in range(8)]

chase_sprite_sheet = pygame.image.load('./assets/chase.png').convert_alpha()
zombie_chase = [chase_sprite_sheet.subsurface(pygame.Rect(x * 96, 0, 96, 96)) for x in range(10)]

attack_sprite_sheet = pygame.image.load('./assets/attack.png').convert_alpha()
zombie_attack = [attack_sprite_sheet.subsurface(pygame.Rect(x * 96, 0, 96, 96)) for x in range(4)]

eat_sprite_sheet = pygame.image.load('./assets/eat.png').convert_alpha()
zombie_eat = [eat_sprite_sheet.subsurface(pygame.Rect(x * 96, 0, 96, 96)) for x in range(11)]

# Animation frame rate
FRAME_RATE = 0.1

class State(ABC):
    @abstractmethod
    def enter(self, agent):
        pass

    @abstractmethod
    def update(self, agent, target):
        pass
    
    @abstractmethod
    def exit(self, agent):
        pass

class StateMachine():
    def __init__(self) -> None:
        self.states = {
            'idle': IdleState(),
            'chase': ChaseState(),
            'attack': AtkState(),
            'eat' : EatState()
        }
        self.current_state = 'idle'

    def transition_to(self, agent, new_state):
        self.states[self.current_state].exit(agent)
        self.current_state = new_state
        self.states[self.current_state].enter(agent)

    def update(self, agent, target):
        new_state = self.states[self.current_state].update(agent, target)
        if new_state:
            print(new_state)
            print()
            self.transition_to(agent, new_state)

class IdleState(State):
    def enter(self, agent):
        agent.current_animation = zombie_idle

    def update(self, agent, target):
        agent.velocity.x = random.randint(0, 600)
        agent.velocity.y = random.randint(0, 600)
        if agent.velocity.length() > MAX_SPEED_IDLE:
            agent.velocity.scale_to_length(MAX_SPEED_IDLE)
        agent.position += agent.velocity
        dist = (target - agent.position).length()
        if dist < 300:
            return 'chase'

    def exit(self, agent):
        pass

class ChaseState(State):
    def enter(self, agent):
        agent.current_animation = zombie_chase

    def update(self, agent, target):
        a = (target - agent.position).normalize() * 5
        agent.velocity += a
        if agent.velocity.length() > MAX_SPEED:
            agent.velocity.scale_to_length(MAX_SPEED)
        agent.position += agent.velocity

        dist = (target - agent.position).length()
        if dist > 400:
            return 'idle'
        if dist < 80:
            return 'attack'

    def exit(self, agent):
        pass

class AtkState(State):
    def enter(self, agent):
        agent.current_animation = zombie_attack
        
    def update(self, agent, target):
        a = (target - agent.position).normalize() * 5
        agent.velocity += a
        if agent.velocity.length() > MAX_SPEED_ATK:
            agent.velocity.scale_to_length(MAX_SPEED_ATK)
        agent.position += agent.velocity

        dist = (target - agent.position).length()
        if dist >= 80:
            return 'chase'
        if dist < 15:
             return 'eat'

    def exit(self, agent):
        pass

class EatState(State):
    def __init__(self):
        self.eat_time = 3000
        self.timer = 0 

    def enter(self, agent):
        agent.current_animation = zombie_eat
        self.timer = 0 

    def update(self, agent, target):
        if agent.velocity.length() > MAX_SPEED_EAT:
            agent.velocity.scale_to_length(MAX_SPEED_EAT)
        agent.position += agent.velocity
        self.timer += pygame.time.get_ticks() / 1000
        if self.timer >= self.eat_time:
            return 'idle'

    def exit(self, agent):
        pass

class Agent:
    def __init__(self):
        self.position = pygame.Vector2(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize() * MAX_SPEED
        self.frame_index = 0
        self.state_machine = StateMachine()
        self.current_animation = zombie_idle

    def update(self, target):
        self.state_machine.update(self, target)

        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

        return True

    def draw(self, screen):
        self.frame_index = (self.frame_index + FRAME_RATE) % len(self.current_animation)
        current_frame = self.current_animation[int(self.frame_index)]

        if self.velocity.x < 0:
            current_frame = pygame.transform.flip(current_frame, True, False)

        if self.state_machine.current_state == 'idle':
            pygame.draw.circle(screen, (0,0,255), self.position, 10 )
        elif self.state_machine.current_state == 'chase':
            pygame.draw.circle(screen, (255, 255, 0 ), self.position, 10)
        elif self.state_machine.current_state == 'attack':
            pygame.draw.circle(screen, (255, 0, 0 ), self.position, 10)
        elif self.state_machine.current_state == 'eat':
            pygame.draw.circle(screen, (255, 0, 255 ), self.position, 10)
        
        screen.blit(current_frame, (int(self.position.x) - 50, int(self.position.y) - 50))

def main():
    agents = [Agent() for _ in range(NUM_AGENTS)]
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            target = pygame.Vector2(pygame.mouse.get_pos())

        agents = [fish for fish in agents if fish.update(target)]
        for agent in agents:
            agent.draw(screen)

        pygame.draw.circle(screen, (255, 0, 0), (int(target.x), int(target.y)), FOOD_SIZE)

        pygame.display.flip()
        clock.tick(60)
        screen.fill((100, 100, 100))
        fps = int(clock.get_fps())

        fps_text = font.render(f"FPS: {fps}", True, pygame.Color('black'))
        screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    pygame.quit()

if __name__ == "__main__":
    main()