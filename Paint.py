# ShockingRotom Aug 2021
# click left mouse button on different tools and colours
# pencil tool drawing with selected colour by holding/clicking left mouse button
# eraser tool erasing by holding/clicking left mouse button
# fill tool fills space with selected colour by clicking left mouse button
# line tool draws line from starting point to ending point in selected colour by holding left mouse button
# rectangle tool draws rectangle from starting point to ending point in selected colour by holding left mouse button
# colour selector tool changes selected colour to colour clicked on by left mouse button
# selector tool not properly implemented yet
# save tool saves currently drawn image as png file

import pygame
import numpy as np
import os

pygame.init()

# Colours
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

# Important Vars
COUNT = 50
SIZE = 10
OFFSET = 120

size = (OFFSET + SIZE * COUNT, OFFSET + SIZE * COUNT)
screen = pygame.display.set_mode(size, 0, 32)
subscreenrect = pygame.Rect(120, 0, 500, 500)
subscreen = screen.subsurface(subscreenrect)

screen.fill(WHITE)

pygame.display.set_caption("MS Paint")
logo = pygame.image.load('extra/MSPaint.png')
pygame.display.set_icon(logo)

# Images
grey_square = pygame.transform.scale(pygame.image.load("extra/Grey.png"), (40, 40))
black_square = pygame.transform.scale(pygame.image.load("extra/Black.png"), (40, 40))
red_square = pygame.transform.scale(pygame.image.load("extra/Red.png"), (40, 40))
orange_square = pygame.transform.scale(pygame.image.load("extra/Orange.png"), (40, 40))
yellow_square = pygame.transform.scale(pygame.image.load("extra/Yellow.png"), (40, 40))
green_square = pygame.transform.scale(pygame.image.load("extra/Green.png"), (40, 40))
blue_square = pygame.transform.scale(pygame.image.load("extra/Blue.png"), (40, 40))
purple_square = pygame.transform.scale(pygame.image.load("extra/Purple.png"), (40, 40))
pencil_square = pygame.transform.scale(pygame.image.load("extra/Pencil.png"), (40, 40))
bucket_square = pygame.transform.scale(pygame.image.load("extra/Bucket.png"), (40, 40))
eraser_square = pygame.transform.scale(pygame.image.load("extra/Eraser.png"), (40, 40))
line_square = pygame.transform.scale(pygame.image.load("extra/Line.png"), (40, 40))
rectangle_square = pygame.transform.scale(pygame.image.load("extra/Rectangle.png"), (40, 40))
save_square = pygame.transform.scale(pygame.image.load("extra/Save.png"), (40, 40))
colourselector_square = pygame.transform.scale(pygame.image.load("extra/ColourSelector.png"), (40, 40))
selector_square = pygame.transform.scale(pygame.image.load("extra/Selector.png"), (40, 40))


# Objects
class Colours(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = black_square
        self.colour = BLACK
        self.value = 2

        self.rect = self.image.get_rect()
        self.rect.x = 140
        self.rect.y = 540

    def colour_switch(self):
        return self.colour, self.value

    def update(self, position, colour, value):
        if self.rect.collidepoint(position):
            colour, value = self.colour_switch()
        return colour, value


class Tools(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pencil_square
        self.tool = "pencil"

        self.rect = self.image.get_rect()
        self.rect.x = 40
        self.rect.y = 40

    def tool_switch(self):
        return self.tool

    def update(self, position, tool):
        if self.rect.collidepoint(position):
            tool = self.tool_switch()
        return tool


# Functions
# Creates a matrix of the board
def create_matrix(x):
    matrix = np.zeros((x, x))
    return matrix


# Draws matrix
def draw_matrix(screen, countr, countc, SIZE, array, OFFSETr, OFFSETc):
    for r in range(countr):
        for c in range(countc):
            if array[r][c] == 0:
                colour = WHITE
            elif array[r][c] == 1:
                colour = GREY
            elif array[r][c] == 2:
                colour = BLACK
            elif array[r][c] == 3:
                colour = RED
            elif array[r][c] == 4:
                colour = ORANGE
            elif array[r][c] == 5:
                colour = YELLOW
            elif array[r][c] == 6:
                colour = GREEN
            elif array[r][c] == 7:
                colour = BLUE
            else:
                colour = PURPLE
            pygame.draw.rect(screen, colour, (OFFSETr + r * SIZE, OFFSETc + c * SIZE, SIZE, SIZE))


# Draws highlight
def draw_highlight(screen, count, SIZE, OFFSET, colour):
    c = int(pygame.mouse.get_pos()[1] / SIZE) * SIZE
    r = int(pygame.mouse.get_pos()[0] / SIZE) * SIZE
    if r < OFFSET:
        r = OFFSET
    if c > (count - 1) * SIZE:
        c = (count - 1) * SIZE
    pos = (r, c)
    select = pygame.Surface((SIZE, SIZE))
    # Makes square semi transparent
    select.set_alpha(128)
    select.fill(colour)
    screen.blit(select, pos)


# Flood fill algorithm
def flood_fill(x, y, old, new, matrix, maxnum):
    if old == new:
        pass
    else:
        theStack = [(x, y)]
        while len(theStack) > 0:

            x, y = theStack.pop()

            if x < 0 or x >= maxnum or y < 0 or y >= maxnum or matrix[x][y] != old:
                continue

            matrix[x][y] = new
            theStack.append((x + 1, y))
            theStack.append((x - 1, y))
            theStack.append((x, y + 1))
            theStack.append((x, y - 1))


# Line Algorithm
def line(startpos, endpos, c_value, matrix):
    x1, y1 = startpos
    x2, y2 = endpos
    dx = x2 - x1
    dy = y2 - y1

    is_steep = abs(dy) > abs(dx)

    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    dx = x2 - x1
    dy = y2 - y1

    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    if swapped:
        points.reverse()

    for p in points:
        matrix[p] = c_value

    return matrix


# Rectangle Algorithm
def rectangle(startpos, endpos, c_value, matrix):
    x = endpos[0] - startpos[0]
    y = endpos[1] - startpos[1]
    signx = 1
    signy = 1

    if x < 0:
        signx = -1
        x = abs(x)
    if y < 0:
        signy = -1
        y = abs(y)

    for i in range(x):
        matrix[startpos[0] + (signx * i), startpos[1]] = c_value
        matrix[startpos[0] + (signx * i), endpos[1]] = c_value
    for j in range(y):
        matrix[startpos[0], startpos[1] + (signy * j)] = c_value
        matrix[endpos[0], startpos[1] + (signy * j)] = c_value

    matrix[endpos] = c_value

    return matrix


# Selecting Algorithm
def selectings(startpos, endpos, matrix):
    x = endpos[0] - startpos[0]
    y = endpos[1] - startpos[1]
    signx = 1
    signy = 1

    if x < 0:
        signx = -1
        x = abs(x)
    if y < 0:
        signy = -1
        y = abs(y)

    count = 0
    for i in range(x):
        if count == 2:
            count = 0
            continue
        matrix[startpos[0] + (signx * i), startpos[1]] = 2
        matrix[startpos[0] + (signx * i), endpos[1]] = 2
        count += 1
    count = 0
    for j in range(y):
        if count == 2:
            count = 0
            continue
        matrix[startpos[0], startpos[1] + (signy * j)] = 2
        matrix[endpos[0], startpos[1] + (signy * j)] = 2
        count += 1

    matrix[endpos] = 2

    return matrix


# Selection Saving
def selection_save(startpos, endpos, matrix):
    submatrix = matrix[startpos[0]:endpos[0], startpos[1]:endpos[1]].copy()
    return submatrix


matrix = create_matrix(COUNT)
draw_matrix(screen, COUNT, COUNT, SIZE, matrix, OFFSET, 0)
pygame.display.flip()

creating = True
drawing = False
filling = False
erasing = False
lining = False
rectanging = False
colourselecting = False
selecting = False
selected = False
selectionmove = False

selected_colour = BLACK
selected_value = 2

colour_sprites = pygame.sprite.Group()
tool_sprites = pygame.sprite.Group()

grey = Colours()
grey.image = grey_square
grey.colour = GREY
grey.value = 1
grey.rect.x += 60
colour_sprites.add(grey)
black = Colours()
colour_sprites.add(black)
red = Colours()
red.image = red_square
red.colour = RED
red.value = 3
red.rect.x += 120
colour_sprites.add(red)
orange = Colours()
orange.image = orange_square
orange.colour = ORANGE
orange.value = 4
orange.rect.x += 180
colour_sprites.add(orange)
yellow = Colours()
yellow.image = yellow_square
yellow.colour = YELLOW
yellow.value = 5
yellow.rect.x += 240
colour_sprites.add(yellow)
green = Colours()
green.image = green_square
green.colour = GREEN
green.value = 6
green.rect.x += 300
colour_sprites.add(green)
blue = Colours()
blue.image = blue_square
blue.colour = BLUE
blue.value = 7
blue.rect.x += 360
colour_sprites.add(blue)
purple = Colours()
purple.image = purple_square
purple.colour = PURPLE
purple.value = 8
purple.rect.x += 420
colour_sprites.add(purple)
pencil = Tools()
tool_sprites.add(pencil)
eraser = Tools()
eraser.tool = "eraser"
eraser.image = eraser_square
eraser.rect.y += 70
tool_sprites.add(eraser)
bucket = Tools()
bucket.tool = "bucket"
bucket.image = bucket_square
bucket.rect.y += 140
tool_sprites.add(bucket)
lines = Tools()
lines.tool = "line"
lines.image = line_square
lines.rect.y += 210
tool_sprites.add(lines)
rectangles = Tools()
rectangles.tool = "rectangle"
rectangles.image = rectangle_square
rectangles.rect.y += 280
tool_sprites.add(rectangles)
colourselector = Tools()
colourselector.tool = "colourselector"
colourselector.image = colourselector_square
colourselector.rect.y += 350
tool_sprites.add(colourselector)
selector = Tools()
selector.tool = "selector"
selector.image = selector_square
selector.rect.y += 420
tool_sprites.add(selector)
save = Tools()
save.tool = "save"
save.image = save_square
save.rect.y += 490
tool_sprites.add(save)

# Tools
# pencil
# eraser
# bucket
# line
# rectangle
# colourselector
# selector
# save
tool = "pencil"
tool_copy = tool
r = 0
c = 0
posr = 0
posc = 0
selectstartpos = (0, 0)
selectendpos = (0, 0)
matrix_copy = matrix.copy()
submatrix = matrix[0:0, 0:0]
directory = 'saves'
selectmoveoffsetr = 0
selectmoveoffsetc = 0

while creating:
    # User Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            creating = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                creating = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            value_copy = selected_value
            for cs in colour_sprites:
                selected_colour, selected_value = cs.update(event.pos, selected_colour, selected_value)
            tool_copy = tool
            for ts in tool_sprites:
                tool = ts.update(event.pos, tool)
            if selected_value == value_copy and tool == tool_copy:
                if tool == "pencil":
                    drawing = True
                elif tool == "bucket":
                    filling = True
                elif tool == "eraser":
                    erasing = True
                elif tool == "line":
                    lining = True
                    matrix_copy = matrix.copy()
                    posc = int((pygame.mouse.get_pos()[1]) / SIZE)
                    posr = int((pygame.mouse.get_pos()[0] - OFFSET) / SIZE)
                elif tool == "rectangle":
                    rectanging = True
                    matrix_copy = matrix.copy()
                    posc = int((pygame.mouse.get_pos()[1]) / SIZE)
                    posr = int((pygame.mouse.get_pos()[0] - OFFSET) / SIZE)
                elif tool == "colourselector":
                    colourselecting = True
                elif tool == "selector" and not selected:
                    selecting = True
                    matrix_copy = matrix.copy()
                    posc = int((pygame.mouse.get_pos()[1]) / SIZE)
                    posr = int((pygame.mouse.get_pos()[0] - OFFSET) / SIZE)
                elif tool == "selector" and selected:
                    if (OFFSET + (selectstartpos[0] * SIZE) <= r * SIZE <= selectendpos[0] * SIZE) and (selectstartpos[1] * SIZE <= c * SIZE <= selectendpos[1] * SIZE):
                        selectionmove = True
                        selectmoveoffsetr = (r * SIZE) - (OFFSET + (selectstartpos[0] * SIZE))
                        selectmoveoffsetc = (c * SIZE) - (selectstartpos[1] * SIZE)
                    else:
                        selected = False
                        matrix[selectstartpos[0]:selectendpos[0], selectstartpos[1]:selectendpos[1]] = submatrix
                        submatrix = matrix[0:0, 0:0]

        elif event.type == pygame.MOUSEBUTTONUP:
            if tool == "pencil" and drawing:
                drawing = False
            elif tool == "eraser" and erasing:
                erasing = False
            elif tool == "line" and lining:
                lining = False
            elif tool == "rectangle" and rectanging:
                rectanging = False
            elif tool == "selector" and selecting:
                selecting = False
                matrix = matrix_copy.copy()
                selectstartpos = [posr, posc]
                selectendpos = [r, c]
                if selectstartpos[0] > selectendpos[0]:
                    selectstartpos[0], selectendpos[0] = selectendpos[0], selectstartpos[0]
                if selectstartpos[1] > selectendpos[1]:
                    selectstartpos[1], selectendpos[1] = selectendpos[1], selectstartpos[1]
                submatrix = selection_save(selectstartpos, selectendpos, matrix)
                matrix[selectstartpos[0]:selectendpos[0], selectstartpos[1]:selectendpos[1]] = 0
                selected = True
            elif tool == "selector" and selected:
                print("Selection moved")
                selected = False
                selectionmove = False
                newr = int(((r * SIZE) - (selectmoveoffsetr * SIZE) - OFFSET) / SIZE)
                newc = int(((c * SIZE) - (selectmoveoffsetc * SIZE)) / SIZE)
                print(newr, newc)
                matrix[newr:newr + submatrix.shape[0], newc:newc + submatrix.shape[1]] = submatrix.copy()
                submatrix = matrix[0:0, 0:0].copy()

    if tool == "save":
        pygame.image.save(subscreen, directory + '/image' + str(len(os.listdir(directory))) + '.png')
        print("Saved")
        tool = tool_copy

    c = int((pygame.mouse.get_pos()[1]) / SIZE)
    r = int((pygame.mouse.get_pos()[0] - OFFSET) / SIZE)

    if c < 0:
        c = 0
    elif c > COUNT - 1:
        c = COUNT - 1
    if r < 0:
        r = 0
    elif r > COUNT - 1:
        r = COUNT - 1

    if posc < 0:
        posc = 0
    elif posc > COUNT - 1:
        posc = COUNT - 1
    if posr < 0:
        posr = 0
    elif posr > COUNT - 1:
        posr = COUNT - 1

    if tool == "pencil" and drawing:
        matrix[r][c] = selected_value
    if tool == "eraser" and erasing:
        matrix[r][c] = 0
    if tool == "bucket" and filling:
        flood_fill(r, c, matrix[r][c], selected_value, matrix, COUNT)
        filling = False
    if tool == "line" and lining:
        matrix = matrix_copy.copy()
        matrix = line((posr, posc), (r, c), selected_value, matrix)
    if tool == "rectangle" and rectanging:
        matrix = matrix_copy.copy()
        matrix = rectangle((posr, posc), (r, c), selected_value, matrix)
    if tool == "colourselector" and colourselecting:
        if matrix[r][c] != 0:
            selected_value = matrix[r][c]
            for cs in colour_sprites:
                if cs.value == selected_value:
                    selected_colour, selected_value = cs.colour_switch()
        colourselecting = False
    if tool == "selector" and selecting:
        matrix = matrix_copy.copy()
        matrix = selectings((posr, posc), (r, c), matrix)
    if tool == "selector":
        if len(submatrix) > 0:
            draw_matrix(screen, submatrix.shape[0], submatrix.shape[1], SIZE, submatrix, posr + selectmoveoffsetr,
                        posc + selectmoveoffsetc)
        if selectionmove:
            pass

    pygame.draw.rect(screen, BLACK, (0, 0, 620, 620))
    pygame.draw.rect(screen, WHITE, (1, 0, 619, 619))
    pygame.draw.rect(screen, BLACK, (119, 0, 501, 501))
    draw_matrix(screen, COUNT, COUNT, SIZE, matrix, OFFSET, 0)
    if tool == "eraser":
        colour_parameter = WHITE
    else:
        colour_parameter = selected_colour
    draw_highlight(screen, COUNT, SIZE, OFFSET, colour_parameter)
    colour_sprites.draw(screen)
    tool_sprites.draw(screen)

    pygame.display.flip()
