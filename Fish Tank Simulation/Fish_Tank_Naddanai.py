# Example file showing a basic pygame "game loop"
import pygame
import random
import os

# Set up the screen dimensions and maximum speed for agents
WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 1
NUMBER_AGENT = 100  # Number of agents in the simulation

# Factors controlling the behavior of the agents
COHERENCE_FACTOR = 0.005 # Controls how strongly agents are attracted to the center of mass
ALIGNMENT_FACTOR = 0.01  # Controls how strongly agents align their direction with others
SEPARATION_FACTOR = 0.01  # Controls how strongly agents avoid each other
SEPARATION_DIST = 25  # Minimum distance to maintain between agents

FOODSEEK_FACTOR = 0.5
OBSTACLES_FACTOR = 1

food_pos = None
time_ran = 15
tree_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
offset_skull = pygame.Vector2(112, 112)
# -----------------------------------------------------------------------
# Agent class represents each moving entity in the simulation
# -----------------------------------------------------------------------

class Agent:
    def __init__(self, x, y) -> None:
        # Initialize agent's position and velocity with random values
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(     
            random.uniform(-MAX_SPEED, MAX_SPEED), random.uniform(-MAX_SPEED, MAX_SPEED))
        self.acceleration = pygame.Vector2(0, 0)
        self.mass = 1  # Mass of the agent used in force calculation
        
        self.sight_range_for_food = 200
        self.sight_range = 130
        self.hungrytime = 0
        self.is_hungry = False

        self.frame_size = 48
        self.fx = 0
        self.fy = 4
        self.agent_frame = agent_sprite.subsurface(pygame.Rect( self.fx * self.frame_size, 
                                                        self.fy * self.frame_size,
                                                        self.frame_size,
                                                        self.frame_size       ))
        
        self.time = 0
        self.animation_frame_rate = 60 
    def update(self):
        self.update_animation()
        # Update velocity and position of the agent based on current acceleration
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            # Limit the speed to MAX_SPEED
            self.velocity = self.velocity.normalize() * MAX_SPEED
        self.position += self.velocity
        # Reset acceleration after each update
        self.acceleration = pygame.Vector2(0, 0)
        self.update_hungry_status()

    def update_animation(self):
        if self.is_hungry:
            self.fy = 0
        else:
            self.fy = 4

        if self.time > self.animation_frame_rate:
            self.fx = self.fx + 1
            self.fx = self.fx % 3
            self.agent_frame = agent_sprite.subsurface(pygame.Rect( 
                                                    self.fx * self.frame_size, 
                                                    self.fy * self.frame_size,
                                                    self.frame_size,
                                                    self.frame_size       ))
            self.time = 0
        else:
            self.time = self.time + 1

    def apply_force(self, x, y):
        # Apply a force to the agent, adjusting acceleration based on mass
        force = pygame.Vector2(x, y)
        self.acceleration += force / self.mass

    def seek(self, x, y):
        # Calculate the direction towards a target point and apply a small force in that direction
        d = pygame.Vector2(x, y) - self.position
        d = d.normalize() * 0.1  # Adjust the force magnitude
        seeking_force = d
        self.apply_force(seeking_force.x, seeking_force.y)

    def coherence(self, agents):
        # Steer towards the average position (center of mass) of neighboring agents
        center_of_mass = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    center_of_mass += agent.position
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            center_of_mass /= agent_in_range_count  # Calculate average position
            d = center_of_mass - self.position
            f = d * COHERENCE_FACTOR  
            self.apply_force(f.x, f.y)  # Apply coherence force

    def separation(self, agents):
        # Steer to avoid crowding neighbors (separation behavior)
        d = pygame.Vector2(0, 0)
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < SEPARATION_DIST:  # Only consider agents within separation distance
                    d += self.position - agent.position

        separation_force = d * SEPARATION_FACTOR  
        # Apply separation force
        self.apply_force(separation_force.x, separation_force.y)

    def alignment(self, agents):
        # Steer towards the average heading (velocity) of nearby agents (alignment behavior)
        v = pygame.Vector2(0, 0)
        agent_in_range_count = 0
        for agent in agents:
            if agent != self:
                dist = self.position.distance_to(agent.position)
                if dist < 100:  # Only consider nearby agents within 100 units
                    v += agent.velocity
                    agent_in_range_count += 1

        if agent_in_range_count > 0:
            v /= agent_in_range_count  # Calculate average velocity
            alignment_force = v * ALIGNMENT_FACTOR  # Apply alignment force
            self.apply_force(alignment_force.x, alignment_force.y)

    def food_sight_range(self, food_pos):
        dist = self.position.distance_to(food_pos)
        if dist <= self.sight_range_for_food:
            return True
        return False

    def obstacles(self, tree_pos):
        d = pygame.Vector2(tree_pos) - self.position
        # tree_pos_ob = pygame.Vector2(tree_pos.x -112, tree_pos.y -112) 
        dist = self.position.distance_to(tree_pos)
        if dist <= self.sight_range:
            d.normalize() * OBSTACLES_FACTOR
            obstacles_force = d
            self.apply_force(obstacles_force.x * -1, obstacles_force.y * -1)

    def foodseek(self, food_pos):
        d = pygame.Vector2(food_pos) - self.position
        d.normalize() * FOODSEEK_FACTOR
        foodseek_force = d
        self.apply_force(foodseek_force.x, foodseek_force.y)

    def update_hungry_status(self):
        if not self.is_hungry: 
            if (pygame.time.get_ticks() - self.hungrytime) / 1000 >= time_ran:
                self.is_hungry = random.random() < 0.2
                self.hungrytime = pygame.time.get_ticks()

    def is_on_food(self, food_pos): 
        pos_diff = self.position - food_pos
        if abs(pos_diff.x) <= 1 and abs(pos_diff.y) <= 1:
            self.is_hungry = False
            return True
        return False

    def draw(self, screen):
        screen.blit(self.agent_frame, self.position - pygame.Vector2(32, 32))
        pygame.draw.line(screen, "red", self.position, self.position + self.velocity * 10 )

# -----------------------------------------------------------------------
#  Begin 
# -----------------------------------------------------------------------
pygame.init()
# Create a window with the specified dimensions
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()  # Initialize a clock to manage frame rate

sprite_path_betta = os.path.join(os.getcwd(),"sprite","betta.png")
sprite_path_trex = os.path.join(os.getcwd(),"sprite","trex.png")
sprite_path_tree1 = os.path.join(os.getcwd(),"sprite","rz_tree1.png")
sprite_path_tree2 = os.path.join(os.getcwd(),"sprite","rz_tree2.png")

agent_sprite = pygame.image.load(sprite_path_betta)
obstacles_sprite = pygame.image.load(sprite_path_trex)
tree1_sprite = pygame.image.load(sprite_path_tree1)
tree2_sprite = pygame.image.load(sprite_path_tree2)

# Set up font for displaying FPS (frames per second)
font = pygame.font.Font(None, 36)

# Create a list of agents at random positions within the screen
agents = [Agent(random.uniform(0, WIDTH), random.uniform(0, HEIGHT))
          for _ in range(NUMBER_AGENT)]

# ----- GAME LOOP ------------
running = True  # Variable to control the main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user closed the window
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and food_pos is None:
            food_pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            food_pos = None
            # if event.key == pygame.K_SPACE:
            #     reset_game()
            
    # Fill the screen with water color to clear the previous frame
    screen.fill((153, 255, 255))
    screen.blit(tree1_sprite, (0, 5))
    screen.blit(tree2_sprite, (1000, 500))
    # Update and draw each agent on the screen
    for agent in agents:
        # Uncomment the next line to make agents seek towards a fixed point (e.g., the center of the screen)
        # agent.seek(400, 400)
        agent.obstacles(tree_pos)
        if food_pos and agent.is_hungry and agent.food_sight_range(food_pos):
            agent.obstacles(tree_pos)
            agent.separation(agents)
            agent.foodseek(food_pos)
            if agent.is_on_food(food_pos):
                food_pos = None
        else:
            agent.coherence(agents)  # Apply coherence behavior
            agent.separation(agents)  # Apply separation behavior
            agent.alignment(agents)  # Apply alignment behavior
        agent.update()  # Update the agent's position and update_hungry_status
        agent.draw(screen)  # Draw the agent on the screen

    # Boundary wrapping: make agents appear on the opposite side when they move off the screen
    for agent in agents:
        if agent.position.x > WIDTH:
            agent.position.x = 0
        elif agent.position.x < 0:
            agent.position.x = WIDTH
        if agent.position.y > HEIGHT:
            agent.position.y = 0
        elif agent.position.y < 0:
            agent.position.y = HEIGHT

    pygame.draw.circle(screen, (153, 255, 255), tree_pos, 120, 1)
    screen.blit(obstacles_sprite, tree_pos - offset_skull)

    if food_pos:
        pygame.draw.circle(screen, (128, 0, 0), food_pos, 5)

    # Calculate and display FPS (frames per second) in the top-right corner of the screen
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, pygame.Color('white'))
    screen.blit(fps_text, (WIDTH - fps_text.get_width() - 10, 10))

    pygame.display.flip()  # Update the screen with the drawn frame
    clock.tick(60)  # Limit the frame rate to 60 frames per second

pygame.quit()  # Clean up and close the game window when the loop ends