import pygame
import random
import heapq

WIDTH, HEIGHT = 1400, 800
tile_size = 100
cols = WIDTH // tile_size
rows = HEIGHT // tile_size
directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
start = (0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Path Finding Algorithm")

dfs_agent = pygame.image.load('./assets/biden.png')
dfs_agent = pygame.transform.scale(dfs_agent, (tile_size, tile_size))

bfs_agent = pygame.image.load('./assets/harris.png')
bfs_agent = pygame.transform.scale(bfs_agent, (tile_size, tile_size))

dijkstra_agent = pygame.image.load('./assets/trump.png')
dijkstra_agent = pygame.transform.scale(dijkstra_agent, (tile_size, tile_size))

class Graph:
    def __init__(self):
        self.grid = [[{
                        "weight" : random.uniform(0, 3)
                        } for _ in range(cols)] for _ in range(rows)]
        
        self.end = (random.randint(0, cols - 1), random.randint(0, rows - 1))
    
    def print_graph(self):
        for y in range(rows):
            for x in range(cols):
                print(self.grid[y][x]["weight"], x, y)

    def draw_grid(self):
        for y in range(rows):
            for x in range(cols):
                pygame.draw.rect(screen, (255, 255, 255), (x * tile_size, y * tile_size, tile_size, tile_size))
                pygame.draw.rect(screen, pygame.Color(0, 0, 0), (x * tile_size, y * tile_size, tile_size, tile_size), 1)
        
        pygame.draw.rect(screen, (0, 255, 0), (self.end[0] * tile_size, self.end[1] * tile_size, tile_size, tile_size))

def dfs(grid, start, end, visited=None):
    if visited is None:
        visited = []
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) == end:
            visited.append((x, y))
            return visited
        
        if (x, y) not in visited:
            visited.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                    stack.append((nx, ny)) 
    return visited

def bfs(grid, start, end, visited=None):
    if visited is None:
        visited = []

    queue = [start]
    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            visited.append((x, y))
            return visited
        
        if (x, y) not in visited:
            visited.append((x, y))
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < cols and 0 <= ny < rows and (nx, ny) not in visited:
                    queue.append((nx, ny))
    return visited

def dijkstra(grid, start, end):
    pq = []  
    heapq.heappush(pq, (0, start))  
    distances = {start: 0}  
    previous = {start: None}  
    visited = set()  
    while pq: 
        current_distance, current_node = heapq.heappop(pq)
        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            break

        x, y = current_node
        for dx, dy in directions:  
            neighbor = (x + dx, y + dy)  
            if 0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows:
                weight = grid[neighbor[1]][neighbor[0]]["weight"]
                distance = current_distance + weight
                if neighbor not in distances or distance < distances[neighbor]:
                    distances[neighbor] = distance  
                    previous[neighbor] = current_node  
                    heapq.heappush(pq, (distance, neighbor))
    
    path = []
    node = end  
    while node is not None: 
        path.append(node) 
        node = previous.get(node)  
    path.reverse()  

    return path  
    
def main():
    clock = pygame.time.Clock()
    running = True

    graph = Graph()

    path_dfs = dfs(graph.grid, start, graph.end)
    path_dfs_index = 0

    path_bfs = bfs(graph.grid, start, graph.end) 
    path_bfs_index = 0

    path_dijkstra = dijkstra(graph.grid, start, graph.end)  
    path_dijkstra_index = 0

    dfs_visited = []
    bfs_visited = []
    dijkstra_visited = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        graph.draw_grid()

        for i in dfs_visited:
            pygame.draw.circle(screen, (255, 0, 0), (i[0] * tile_size + tile_size // 2, i[1] * tile_size + tile_size // 2), tile_size // 3)
        
        for i in bfs_visited:
            pygame.draw.circle(screen, (0, 0, 255), (i[0] * tile_size + tile_size // 2, i[1] * tile_size + tile_size // 2), tile_size // 5)
        
        for i in dijkstra_visited:
            pygame.draw.circle(screen, (0, 0, 0), (i[0] * tile_size + tile_size // 2, i[1] * tile_size + tile_size // 2), tile_size // 7)

        if path_dfs_index < len(path_dfs):
            step_dfs = path_dfs[path_dfs_index]
            screen.blit(dfs_agent, (step_dfs[0] * tile_size, step_dfs[1] * tile_size))
            dfs_visited.append(step_dfs)
            path_dfs_index += 1
            pygame.time.delay(50)
        else:
            step_dfs = path_dfs[-1]
            screen.blit(dfs_agent, (step_dfs[0] * tile_size, step_dfs[1] * tile_size))
        
        if path_bfs_index < len(path_bfs):  
            step_bfs = path_bfs[path_bfs_index]
            screen.blit(bfs_agent, (step_bfs[0] * tile_size, step_bfs[1] * tile_size))
            bfs_visited.append(step_bfs)
            path_bfs_index += 1
            pygame.time.delay(50)
        else:
            final_step_bfs = path_bfs[-1]
            screen.blit(bfs_agent, (final_step_bfs[0] * tile_size, final_step_bfs[1] * tile_size))
        
        if path_dijkstra_index < len(path_dijkstra):
            step_dijkstra = path_dijkstra[path_dijkstra_index]
            screen.blit(dijkstra_agent, (step_dijkstra[0] * tile_size, step_dijkstra[1] * tile_size))
            dijkstra_visited.append(step_dijkstra)
            path_dijkstra_index += 1
            pygame.time.delay(50)
        else:
            final_step_dijkstra = path_dijkstra[-1]
            screen.blit(dijkstra_agent, (final_step_dijkstra[0] * tile_size, final_step_dijkstra[1] * tile_size))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit() 

if __name__ == "__main__":
    main()