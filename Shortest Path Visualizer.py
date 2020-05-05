import pygame
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
import math


win_len = 600

game_display = pygame.display.set_mode((win_len, win_len))
pygame.display.set_caption("Shortest Path Visualizer")
pygame.init()
game_display.fill((0,0,0))
pygame.display.update()


open_list = []
closed_list = []
rows = 30
cols = 30
cell_size = win_len/rows
black = (0,0,0)
white = (255,255,255)
cell_color = (171,203,255)


class Cell:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.f = 0
        self.g = 0
        self.h = 0
        self.color = white
        self.neighbours = []
        self.isObs = False
        self.parent = None
        self.was_closed = False
    
    def add_neighbours(self):
        # ngbr is a list of tuples containing the cell 
        # and a bool specifying if the ngbr is diagonal to the curr cell or not
        
        ngbr = []
        if self.y - 1 >= 0 and grid[self.x][self.y - 1].isObs == False:
            ngbr.append((grid[self.x][self.y - 1], False))
        if self.x+1 < cols and self.y-1 >= 0 and grid[self.x + 1][self.y - 1].isObs == False:
            ngbr.append((grid[self.x + 1][self.y - 1], True))
        if self.x+1 < cols and grid[self.x + 1][self.y].isObs == False:
            ngbr.append((grid[self.x + 1][self.y], False))
        if self.x+1 < cols and self.y+1 < rows and grid[self.x + 1][self.y + 1].isObs == False:
            ngbr.append((grid[self.x + 1][self.y + 1], True))
        if self.y+1 < rows and grid[self.x][self.y + 1].isObs == False:
            ngbr.append((grid[self.x][self.y + 1], False))
        if self.x-1 >= 0 and self.y+1 < rows and grid[self.x - 1][self.y + 1].isObs == False:
            ngbr.append((grid[self.x - 1][self.y + 1], True))
        if self.x-1 >= 0 and grid[self.x - 1][self.y].isObs == False:
            ngbr.append((grid[self.x - 1][self.y], False))
        if self.x-1 >= 0 and self.y-1 >= 0 and grid[self.x - 1][self.y - 1].isObs == False:
            ngbr.append((grid[self.x - 1][self.y - 1], True))   
            
        self.neighbours = ngbr
    
    def display_cell(self, colr, border):
        pygame.draw.rect(game_display, colr, (self.x * cell_size, self.y * cell_size, cell_size, cell_size), border)
        pygame.display.update()


# creating a 2D array
grid = [0 for i in range(cols)]
for i in range(cols):
    grid[i] = [0 for i in range(rows)]

# add cells to grid
for c in range(cols):
    for r in range(rows):
        grid[c][r] = Cell(c, r)
        
# displays the cells
for c in range(cols):
    for r in range(rows):
        grid[c][r].display_cell(cell_color, 1)
        
start = grid[0][0]
end = grid[cols - 1][rows-1]


# setting up tkinter
# the function called when submit buttom is pressed
def submit():
    global start
    global end
    st = st_entry.get().split(',')
    ed = en_entry.get().split(',')
    start = grid[int(st[0])][int(st[1])]
    end = grid[int(ed[0])][int(ed[1])]
    showinfo("Obstacles", "Select obstacle path (click and drag), press ENTER when ready to proceed")
    window.quit()
    window.destroy()
    

window = Tk()
w = 300
h = 200
window.geometry("300x200")
screen_w = window.winfo_screenwidth()
screen_h = window.winfo_screenheight()
pos_x = int(screen_w/2 - w/2)
pos_y = int(screen_h/2 - h/2)
window.geometry("+{}+{}".format(pos_x, pos_y))

window['bg'] = '#ffffff'

empty_label = Label(window, text=' ', bg='#ffffff')
st_label = Label(window, text='Start(x,y): ', bg='#ffffff')
st_entry = Entry(window)
en_label = Label(window, text='End(x,y): ', bg='#ffffff')
en_entry = Entry(window)
var = IntVar()

s = ttk.Style()
s.configure('TCheckbutton', background='#ffffff')
show_steps = ttk.Checkbutton(window, text='Show Steps :', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Submit', command=submit, bg='#abcbff')

empty_label.grid(pady=10, padx=20)
st_label.grid(row=1, column=1, pady=3)
st_entry.grid(row=1, column=2, pady=3)
en_label.grid(row=2, column=1, pady=3)
en_entry.grid(row=2, column=2, pady=3)
show_steps.grid(columnspan=2, column=1, row=3)
submit.grid(columnspan=2, column=1, row=4)

window.update()
mainloop()


start.display_cell((255, 128, 0), 0)
end.display_cell((255, 128, 0), 0)
drag = False
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                run = False
                break
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            drag = True
            pos = pygame.mouse.get_pos()
            x = int(pos[0]/cell_size)
            y = int(pos[1]/cell_size)
            grid[x][y] = Cell(x,y)
            grid[x][y].isObs = True
            grid[x][y].color = white
            grid[x][y].display_cell(white, 0)
            
        if event.type == pygame.MOUSEBUTTONUP:
            drag = False
       
        if drag and event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            x = int(pos[0]/cell_size)
            y = int(pos[1]/cell_size)
            grid[x][y] = Cell(x,y)
            grid[x][y].isObs = True
            grid[x][y].color = white
            grid[x][y].display_cell(white, 0)

        
# the euclidean distance heuristics
# this is the approx distance between current cell and end cell
def heuristic(curr_x, curr_y):
    h = math.sqrt((curr_x - end.x)**2 + (curr_y - end.y)**2)
    return h

# return a list containing the final path
def path(cell):
    p = []
    p.append(cell)
    while not cell.parent == None:
        cell = cell.parent
        p.append(cell)

    p.reverse()
    return p

# already initialized start and end cells
start.f = start.g + heuristic(start.x, start.y)
open_list.append(start)

# the A* search algorithm
def search(steps):
    while open_list:
        #finding the cell with the least f in open list
        indx = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[indx].f and not open_list[indx].was_closed:
                indx = i
        q = open_list[indx]

        q.add_neighbours()
        
        # reached goal
        if q.x == end.x and q.y == end.y:
            p = path(q)    
            for cell in p:
                cell.display_cell((255, 178, 102), 3)
            root = Tk()
            root.withdraw()
            showinfo("Result", "Path found!\nThe path length is: {0:.2f}".format(q.f))
            return True
                            
        open_list.pop(indx)
        closed_list.append(q)

        q.was_closed = True
        
        for ngbr_tup in q.neighbours:
            ngbr = ngbr_tup[0]
            if ngbr.was_closed:
                continue
                
            if ngbr not in closed_list:
            # calculating ngbr's g
                g = 0
                if ngbr_tup[1]:
                    g = q.g + math.sqrt(2)
                else:
                    g = q.g + 1
            

                if ngbr.parent == None:
                    ngbr.parent =  q
                
                if ngbr in open_list:
                    if g < ngbr.g:
                        ngbr.g = g
                else:
                    ngbr.g = g
                    open_list.append(ngbr) 

                ngbr.h = heuristic(ngbr.x, ngbr.y)
                ngbr.f = ngbr.g + ngbr.h 

        if steps == 1:
            for cell in open_list:
                if cell.x == end.x and cell.y == end.y:
                    continue
                cell.display_cell((245, 66, 90), 3) 

            for cell in closed_list:
                if cell.x == end.x and cell.y == end.y:
                    continue
                if cell.x == q.x and cell.y == q.y:
                    cell.display_cell((255, 178, 102), 3)
                    continue
                cell.display_cell((144, 66, 245), 3)
    
    root = Tk()
    root.withdraw()
    showinfo("Path not found", "No path was found!")
    return False


res = search(var.get())

while True:
    event = pygame.event.poll()    
    if event.type == pygame.QUIT:   
        break

pygame.quit()
