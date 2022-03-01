import pygame
import random


class Board:
    def __init__(self, x_cells=2, y_cells=2, cell_size=30, edge=(10, 10)):
        self.edge, self.cell_size = edge, cell_size
        self.recount(x_cells=x_cells, y_cells=y_cells)

    def recount(self, x_cells=2, y_cells=2):
        self.x_cells, self.y_cells = x_cells, y_cells
        self.states = [[0] * self.x_cells for i in range(self.y_cells)]

    def set_view(self, left=0, top=0, cell_size=-1):
        self.edge = (left, top)
        if cell_size != -1:
            self.cell_size = cell_size

    def set_cell_size(self, cell_size):
        self.cell_size = cell_size

    def render(self, screen):
        self.curr_screen = screen
        for i in range(self.y_cells):
            for j in range(self.x_cells):
                self.reform(self.curr_screen, cell_x=j, cell_y=i)
                self.draw_grid(self.curr_screen)

    def reform(self, screen, cell_x, cell_y):
        if self.states[cell_y][cell_x] == 0:
            color = '#000000'
        elif self.states[cell_y][cell_x] == 1:
            color = '#ffffff'
        pygame.draw.rect(screen, color,
                         (self.edge[0] + cell_x * self.cell_size + 1,
                          self.edge[1] + cell_y * self.cell_size + 1,
                          self.cell_size - 2, self.cell_size - 2))

    def draw_grid(self, screen):
        for i in range(self.y_cells):
            for j in range(self.x_cells):
                pygame.draw.rect(screen, '#ffffff',
                                 (self.edge[0] + j * self.cell_size,
                                  self.edge[1] + i * self.cell_size,
                                  self.cell_size, self.cell_size), width=1)

    def crosshair(self, screen, coords):
        pygame.draw.line(screen, '#00ff00', (self.edge[0] + coords[0], self.edge[1]),
                         (self.edge[0] + coords[0], self.edge[1] + self.y_cells * self.cell_size))
        pygame.draw.line(screen, '#00ff00', (self.edge[0], self.edge[1] + coords[1]),
                         (self.edge[0] + self.x_cells * self.cell_size, self.edge[1] + coords[1]))

    def get_cell(self, mouse_pos):
        if (self.edge[0] <= mouse_pos[0] <=
            self.edge[0] + self.x_cells * self.cell_size) and \
           (self.edge[1] <= mouse_pos[1] <=
            self.edge[1] + self.y_cells * self.cell_size):
            #
            x = (mouse_pos[0] - self.edge[0]) // self.cell_size
            y = (mouse_pos[1] - self.edge[1]) // self.cell_size
            return (x, y)
        else:
            return None

    def on_click(self, cell_coords):
        cell_x, cell_y = cell_coords
        if self.states[cell_y][cell_x] == 0:
            self.states[cell_y][cell_x] = 1
        elif self.states[cell_y][cell_x] == 1:
            self.states[cell_y][cell_x] = 0
        self.reform(self.curr_screen, cell_x, cell_y)

    def get_click(self, mouse_pos):
        if self.get_cell(mouse_pos) is None:
            return
        cell_x, cell_y = self.get_cell(mouse_pos)
        self.on_click((cell_x, cell_y))


class Life(Board):
    def friend_count(self, arr, cell_x, cell_y):
        ans = 0
        for i in range(-1, 2):
            if not (0 <= cell_y + i < len(arr)):
                continue
            for j in range(-1, 2):
                if i == 0 == j:
                    continue
                if 0 <= cell_x + j < len(arr[0]):
                    if arr[cell_y + i][cell_x + j] == 1:
                        ans += 1
        return ans

    def form_next(self, arr):
        ans_list = [[0] * len(arr[0]) for i in range(len(arr))]
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                ans_list[i][j] = arr[i][j]
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if self.friend_count(arr, j, i) == 3:
                    ans_list[i][j] = 1
                elif not (2 <= self.friend_count(arr, j, i) <= 3):
                    ans_list[i][j] = 0
        return ans_list


def main():
    size = (800, 500)
    stopped = True
    position = (0, 0)
    clock = pygame.time.Clock()
    #
    #
    pygame.display.set_caption('"Жизнь" наоборот')
    screen = pygame.display.set_mode(size)
    #
    #
    board = Life(6, 6)
    board_2 = Life(board.x_cells, board.y_cells, edge=(350, 10))
    #
    while True:
        first = [[random.randrange(0, 2) for i in range(board.x_cells)] for j in range(board.y_cells)]
        curr = board.form_next(first)
        if curr != board.states:
            board.states = curr
            break
    #
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    board_2.get_click(event.pos)
                if event.button == 3:
                    if board_2.form_next(board_2.states) == curr:
                        running = False
                        print('Верно')
                    else:
                        board_2.states = first
                        print('Неверно')
            if event.type == pygame.MOUSEMOTION:
                position = (event.pos[0] - board_2.edge[0], event.pos[1] - board_2.edge[1])
                position = (max(position[0], 0), max(position[1], 0))
                position = (min(position[0], board_2.x_cells * board_2.cell_size),
                            min(position[1], board_2.y_cells * board_2.cell_size))
        screen.fill((0, 0, 0))
        board.render(screen)
        board_2.render(screen)
        board.crosshair(screen, position)
        board_2.crosshair(screen, position)
        pygame.display.flip()


main()
