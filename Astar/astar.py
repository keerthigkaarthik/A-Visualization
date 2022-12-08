import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE= (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_position(self):
        return self.row, self.col    

    def alr_visited(self):
        return self.colour == RED

    def is_frontier(self):
        return self.colour == GREEN

    def is_obstacle(self):
        return self.colour == BLACK  

    def is_start(self):
        return self.colour == ORANGE

    def is_goal(self):
        return self.colour == TURQUOISE

    def reset(self):
        self.colour = WHITE 

    def make_visited(self):
        self.colour = RED

    def make_frontier(self):
        self.colour = GREEN

    def make_obstacle(self):
        self.colour = BLACK  

    def make_start(self):
        self.colour = ORANGE

    def make_goal(self):
        self.colour = TURQUOISE

    def make_path(self):
        self.colour = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if self.row < self.total_rows - 1 and not grid[self.col][self.row + 1].is_obstacle(): #down
            self.neighbours.append(grid[self.col][self.row + 1])
        if self.row > 0 and not grid[self.col][self.row - 1].is_obstacle(): #up
            self.neighbours.append(grid[self.col][self.row - 1])
        if self.col < self.total_rows - 1 and not grid[self.col + 1][self.row].is_obstacle(): #right
            self.neighbours.append(grid[self.col + 1][self.row])
        if self.col > 0 and not grid[self.col - 1][self.row].is_obstacle(): #left
            self.neighbours.append(grid[self.col - 1][self.row])         
        

    def __lt__(self, other):
        return False


def h(n1, n2):
    y1, x1 = n1
    y2, x2 = n2
    return abs(y1-y2)+abs(x1-x2)

def make_grid(rows, width):
    grid = []
    gap = width // rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap, rows)
            grid[i].append(node)

    return grid

def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GREY, (i * gap, 0), (i * gap, width))

def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

def draw_path(came_from, start, end, draw):
    current = end
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()
    
    end.make_goal()
    start.make_start()

def pathfinder(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set_hash = {start}
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = g_score[start] + h(start.get_position(), end.get_position())
    open_set.put((f_score[start], count, start))
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()
        current_node = current[2]
        open_set_hash.remove(current_node)

        if current_node == end:
            draw_path(came_from, start, end, draw)
            return True

        for neighbour in current_node.neighbours:
            temp_g_score = g_score[current_node] + 1
            if temp_g_score < g_score[neighbour]:
                g_score[neighbour] = temp_g_score
                came_from[neighbour] = current_node
                f_score[neighbour] = g_score[neighbour] + h(neighbour.get_position(), end.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_frontier()
        
        draw()

        if current_node != start:
            current_node.make_visited()
        
    return False





def main(window, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[col][row]
                if not start and node != end:
                    start = node
                    start.make_start()
                elif not end and node != start:
                    end = node
                    end.make_goal()
                elif node != start and node != end:
                    node.make_obstacle()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[col][row]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    started = True
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    
                    pathfinder(lambda: draw(window, grid, ROWS, width), grid, start, end)
            



    pygame.quit()

main(WINDOW,WIDTH)