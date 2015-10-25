import pygame               # engine for drawing screen
import time                 # time module with delay function to control fps
import random               # random module for replacing food
from pygame.locals import * # list of constants in pygame

fps = 120       # frequency of processing
speed = 30      # frequency of snake moves
max_passed_frames = fps/speed   # how much frames need to pass for making right speed

sw = 640        # screen width
sh = 480        # screen height
size = 20       # size of cell - snake consists of squares [size x size]
w = sw//size    # number of cells in width
h = sh//size    # number of cells in height

class Point:
    def __init__(self, x=0, y=0):
        self.x = x      #(x, y) coordinates
        self.y = y
        
    def __add__(self, other):       # C = A+B
        return Point(self.x + other.x, self.y + other.y)
        
    def __sub__(self, other):       # C = A-B
        return Point(self.x - other.x, self.y - other.y)
        
    def __eq__(self, other):        # A==B?
        return self.x == other.x and self.y == other.y
        
    def __ne__(self, other):        # A!=B?
        return not(self == other)

class Head:     #snake's head
    def __init__(self, pos, vel, image):
        self.pos = pos  # position
        self.vel = vel  # velocity, means where snake moves in next iteration
        self.img = image    # picture of snake's head

    def set_velocity(self, v):  # changes velocity, checking that snake will not turn at 180 degrees
        if(self.vel+v != Point(0, 0)):
            self.vel = v

    def update(self):   # makes iteration, moving head on new position
        self.pos = self.vel+self.pos
        self.pos.x %= w
        self.pos.y %= h

    def draw_on(self, surface):     # draws head on surface
        surface.blit(self.img, (size*self.pos.x,
                                size*self.pos.y))

class Body:     # describing all snake's body elements, that follows the head
    def __init__(self, positions, img):
        self.positions = positions      # list of each element position
        self.last = len(positions)-1    # the tail number in list
        self.img = img                  # picture of body element

    def update(self, new_pos):          # iteration processing, moves tail element to head position
        self.positions[self.last] = new_pos
        self.last-=1
        if self.last < 0:
            self.last+= len(self.positions)

    def grow(self):                     # if snake eats food, it inserts new body element as tail
        pos1 = self.positions[self.last-1]
        pos2 = self.positions[self.last]
        new_pos = pos2+(pos2-pos1)
        self.last += 1
        
        self.positions = (self.positions[:self.last] +
                            [new_pos] +
                            self.positions[self.last:])

    def draw_on(self, surface):         # draws body on surface
        for pos in self.positions:
            surface.blit(self.img, (size*pos.x,
                               size*pos.y))

class Food:     # food, if snake eat food, it will grow
    def __init__(self, img):
        self.pos = Point(0, 0)  # position of food
        self.img = img          # picture will be drawn as food
        
    def change_pos(self, badpos):   # move food to new random position, cheking, that food don't collide with the snake
        while(True):
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            if Point(x, y) not in badpos:
                break
        self.pos = Point(x, y)

    def draw_on(self, surface):
        surface.blit(self.img, (size*self.pos.x,
                                size*self.pos.y))

pygame.init()                                   # load pygame

screen = pygame.display.set_mode((sw, sh))      # generate screen

cube = pygame.Surface((size-1, size-1))         # make head and body as simple
cube.fill((255, 0, 0))                          # red colored squears
cube2 = pygame.Surface((size-1, size-1))        # make food as
cube2.fill((0,255,0))                           # green colored squear

pos = Point(w//2, h//2)                         # head on the center of screen
vel = Point(1, 0)                               # looks in right edge of screen
positions = [pos - Point(1, 0),                 # 3 body elements generates left from head
             pos - Point(2, 0),
             pos - Point(3, 0)]
head = Head(pos, vel, cube)                     # create head in it's positon
body = Body(positions, cube)                    # create body near the head
food = Food(cube2)                              # create food somewhere

running = True              # flag checking if loop wasn't interrupted

passed_frames = 0           # frames that skips without redraw
velocity_changed = False    # check if velocity already changed

while(running):             #mainloop
    for event in pygame.event.get():    # event processing
        if event.type == KEYUP:
            
            if event.key == K_ESCAPE:   # exit on escape
                running = False
                break
            
            # change velocity vector if arrows pressed
            if velocity_changed:        # velocity must not change twice between frame
                continue

            velocity_changed = True     # changing velocity
            if event.key == K_UP:
                head.set_velocity(Point(0, -1))
            if event.key == K_DOWN:
                head.set_velocity(Point(0,  1))
            if event.key == K_LEFT:
                head.set_velocity(Point(-1, 0))
            if event.key == K_RIGHT:
                head.set_velocity(Point( 1, 0))
                
    if(passed_frames != max_passed_frames):     #if not ready for iteration and redraw
        passed_frames += 1
        time.sleep(1.0/fps)
        continue
    
    passed_frames = 0
    velocity_changed = False

    # new iteration
    body.update(head.pos)
    head.update()

    # check if snake eats food
    if head.pos == food.pos:
        body.grow()
        food.change_pos([head.pos]+body.positions)

    # check if snake hits itself
    if head.pos in body.positions:
        running = False     # game over
        
    # redraw all
    screen.fill((255, 255, 255))    # clear screen
    head.draw_on(screen)            # draw head
    body.draw_on(screen)            # draw body
    food.draw_on(screen)            # draw food
    pygame.display.flip()           # redraw screen
    
    # wait
    time.sleep(1.0/fps)

pygame.quit() # destroy pygame
#end
