import pygame
import time
import random
from pygame.locals import *

fps = 120
speed = 30
max_passed_frames = fps/speed

sw = 640
sh = 480
size = 20
w = sw//size
h = sh//size

class Point:
    x = 0
    y = 0
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        
    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return not(self == other)

class Head:
    def __init__(self, pos, vel, image):
        self.pos = pos
        self.vel = vel
        self.img = image

    def set_velocity(self, v):
        if(self.vel+v != Point(0, 0)):
            self.vel = v

    def update(self):
        self.pos = self.vel+self.pos
        self.pos.x %= w
        self.pos.y %= h

    def draw_on(self, surface):
        surface.blit(self.img, (size*self.pos.x,
                                size*self.pos.y))

class Body:
    def __init__(self, positions, img):
        self.positions = positions
        self.last = len(positions)-1
        self.img = img

    def update(self, new_pos):
        self.positions[self.last] = new_pos
        self.last-=1
        if self.last < 0:
            self.last+= len(self.positions)

    def grow(self):
        pos1 = self.positions[self.last-1]
        pos2 = self.positions[self.last]
        new_pos = pos2+(pos2-pos1)
        self.last += 1
        
        self.positions = (self.positions[:self.last] +
                            [new_pos] +
                            self.positions[self.last:])

    def draw_on(self, surface):
        for pos in self.positions:
            surface.blit(self.img, (size*pos.x,
                               size*pos.y))

class Food:
    def __init__(self, img):
        self.pos = Point(0, 0)
        self.img = img
        
    def change_pos(self, badpos):
        while(True):
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            if Point(x, y) not in badpos:
                break
        self.pos = Point(x, y)

    def draw_on(self, surface):
        surface.blit(self.img, (size*self.pos.x,
                                size*self.pos.y))

pygame.init()

screen = pygame.display.set_mode((sw, sh))

cube = pygame.Surface((size-1, size-1))
cube.fill((255, 0, 0))
cube2 = pygame.Surface((size-1, size-1))
cube2.fill((0,255,0))

pos = Point(w//2, h//2)
vel = Point(1, 0)
positions = [pos - Point(1, 0),
             pos - Point(2, 0),
             pos - Point(3, 0)]
head = Head(pos, vel, cube)
body = Body(positions, cube)
food = Food(cube2)

running = True

passed_frames = 0
velocity_changed = False

#mainloop:
while(running):
    # event processing
    for event in pygame.event.get():
        if event.type == KEYUP:
            
            # exit on escape
            if event.key == K_ESCAPE:
                running = False
                break
            
            # change velocity vector if arrows pressed
            if velocity_changed:
                continue

            velocity_changed = True
            if event.key == K_UP:
                head.set_velocity(Point(0, -1))
            if event.key == K_DOWN:
                head.set_velocity(Point(0,  1))
            if event.key == K_LEFT:
                head.set_velocity(Point(-1, 0))
            if event.key == K_RIGHT:
                head.set_velocity(Point( 1, 0))    
    if(passed_frames != max_passed_frames):
        passed_frames += 1
        time.sleep(1.0/fps)
        continue
    
    passed_frames = 0
    velocity_changed = False

    body.update(head.pos)
    head.update()

    if head.pos == food.pos:
        body.grow()
        food.change_pos([head.pos]+body.positions)

    if head.pos in body.positions:
        running = False
        
    # redraw
    screen.fill((255, 255, 255)) # clear screen
    head.draw_on(screen) # draw head
    body.draw_on(screen) # draw body
    food.draw_on(screen)
    pygame.display.flip() # redraw screen
    
    # wait
    time.sleep(1.0/fps)

pygame.quit()
