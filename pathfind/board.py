# A* loosely based on the pseudocode on [WIKI]
# https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode
# The following is NOT an efficent way to do it


from settings import *
import pygame, sys
from node import Node


class Board:
    def __init__(self, dijkstra=False):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("Pathfinding")
        self.is_running = True
        self.mouse_position = None
        self.is_drawing = True
        self.dijkstra = dijkstra

        self.grid = [[Node(i,j) for i in range(N)] for j in range(N)]
        self.start = self.grid[0][0]
        self.end = self.grid[N-1][N-1]
        self.add_neighbors()
        self.alg_running = False
        self.open_list = []
        self.closed_list = [self.start] #I start directly by checking the neighbors
        self.solution_found = False
        self.path = []

    
    def init_alg(self):
        self.current_node = self.start
        self.current_node = self.update_current()
        

    def main(self):
        while self.is_running:
            while self.alg_running and self.current_node is not self.end:
                self.check_events()
                #current := the node in openSet having the lowest fScore[] value [WIKI]
                if self.open_list:
                    for node in self.open_list:
                        # [WIKI]
                        #if neighbor not in openSet 
                        #    openSet.add(neighbor)
                        if self.current_node not in self.open_list:                     
                            self.current_node = node                                    
                        elif node.f < self.current_node.f:
                            self.current_node = node

                    # openSet.Remove(current) [WIKI]
                    self.open_list.remove(self.current_node)
                    self.closed_list.append(self.current_node)
                    self.current_node = self.update_current()

                    # [WIKI]
                    #if current = goal
                    #   return reconstruct_path(cameFrom, current)
                    if self.current_node is self.end:
                        self.find_path(self.end)
                        self.solution_found = True
                        print("Solution found")

                else:
                    print("No solution")
                    self.alg_running = False

                self.draw_grid(self.window, self.grid, GREY, WHITE)
                pygame.display.update()
                self.clock.tick(FPS)

            self.check_events()
            self.draw_grid(self.window, self.grid, GREY, WHITE)
            self.mouse_position = pygame.mouse.get_pos()
            
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


    def update_current(self):
        possible_next = {}
        neighbors = self.current_node.neighbors
        #for each neighbor of current [WIKI]
        for neighbor in neighbors:
            if not neighbor.is_wall and neighbor not in self.closed_list:
                #tentative_gScore := gScore[current] + d(current, neighbor) [WIKI]
                temp_g = self.current_node.g + 1 #d(current, neighbor) always = 1 on grid
                best_path = False
                
                if neighbor.g and temp_g < neighbor.g:
                    best_path = True
                elif neighbor not in self.open_list:
                    self.open_list.append(neighbor)
                    best_path = True

                if best_path:
                    #[WIKI]
                    #cameFrom[neighbor] := current
                    #gScore[neighbor] := tentative_gScore
                    #fScore[neighbor] := gScore[neighbor] + h(neighbor)
                    neighbor.previous =self.current_node
                    neighbor.g = temp_g
                    neighbor.h = self.heuristic(neighbor, self.end)
                    neighbor.f = neighbor.g + neighbor.h
                    possible_next[neighbor] = neighbor.f

        try:
            next_best = min(possible_next, key=possible_next.get) #Choose the neighbor with the lowest f cost
            return next_best
        except:
            return None


    def find_path(self, node):
        if node.previous is not None:
            self.path.append(node)
            self.find_path(node.previous)


    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.init_alg()
                self.alg_running = True
                self.is_drawing = False
            if pygame.mouse.get_pressed()[0] and self.is_drawing:
                try:
                    self.mouse_position = pygame.mouse.get_pos()
                    x, y = self.get_cell_clicked()
                    self.grid[x][y].is_wall = True
                    pygame.display.update()
                except:
                    continue
    
    
    def draw_grid(self, window, grid, color, background):
        #There's probably a better way to do this
        self.window.fill(background)
        pygame.draw.rect(window, color, (OFFSET, OFFSET, SPACING*N, SPACING*N), 2)

        for i in range(N):
            for j in range(N):
                if grid[i][j] in self.open_list:
                    pygame.draw.rect(window, RED, (OFFSET+j*SPACING, OFFSET+i*SPACING, SPACING, SPACING))
                if grid[i][j] in self.closed_list:
                    pygame.draw.rect(window, GREEN, (OFFSET+j*SPACING, OFFSET+i*SPACING, SPACING, SPACING)) 
                if grid[i][j].is_wall:
                    pygame.draw.rect(window, BLACK, (OFFSET+j*SPACING, OFFSET+i*SPACING, SPACING, SPACING))

        pygame.draw.rect(window, BLUE, (OFFSET+self.end.row*SPACING, OFFSET+self.end.col*SPACING, SPACING, SPACING))
        pygame.draw.rect(window, BLUE, (OFFSET+self.start.row*SPACING, OFFSET+self.start.col*SPACING, SPACING, SPACING))

        if self.solution_found:
            for elem in self.path:
                i = elem.col
                j = elem.row
                pygame.draw.rect(window, BLUE, (OFFSET+j*SPACING, OFFSET+i*SPACING, SPACING, SPACING))

        for i in range(1,N):
            pygame.draw.line(window, color, (OFFSET+i*SPACING, OFFSET), (OFFSET+i*SPACING, N*SPACING+OFFSET), 1)
            pygame.draw.line(window, color, (OFFSET, OFFSET+i*SPACING), (N*SPACING+OFFSET, OFFSET+i*SPACING), 1)

           
    def add_neighbors(self):
        for i in range(N):
            for j in range(N):
                self.grid[i][j].get_neighbors(self.grid)


    def get_cell_clicked(self):
        def mouse_inside_grid():
            if self.mouse_position[0] < OFFSET or self.mouse_position[1] < OFFSET:
                return False
            elif self.mouse_position[0] > SPACING*(N+1) or self.mouse_position[1] > SPACING*(N+1):
                return False
            else:
                return True

        if mouse_inside_grid():
            y_cell = int((self.mouse_position[0]-OFFSET)//SPACING)
            x_cell = int((self.mouse_position[1]-OFFSET)//SPACING)
            return (x_cell, y_cell)
        else:
            return None


    def heuristic(self, node1, node2):
        if self.dijkstra:
            return 0 #Dijkstra always h=0
        else:
            return abs(node1.row-node2.row)+abs(node1.col-node2.col) #Manhattan, no diag
            #return (node1.row-node2.row)**2+(node1.col-node2.col)**2 #Euclidean, with diag