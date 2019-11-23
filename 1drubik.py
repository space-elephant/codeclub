#!/usr/bin/env python3
import math
import pygame
import random
def radians(degrees):
    return degrees * math.pi / 180
def degrees(radians):
    return radians * 180 / math.pi

def arc(surface, colour, center, radius, start, end, base = []):
    start = int(start)
    end = int(end)
    end = ((end-start)%360)+start # more than start but less than start+360
    points = list(base)
    for angle in range(start, end + 1):
        trig = radians(angle)
        points.append((center[0] + radius * math.cos(trig),
                       center[1] - radius * math.sin(trig)))
    pygame.draw.polygon(surface, colour, points)

def point(float):
    return int(float[0]), int(float[1])
def midpoint(point0, point1):
    return (point0[0]+point1[0])/2, (point0[1]+point1[1])/2
def centerangle(center, angle, radius):
    return center[0]+math.cos(radians(angle))*radius, center[1]-math.sin(radians(angle))*radius
def reflect(start, mid):
    return (mid[0] * 2 - start[0], mid[1] * 2 - start[1])
def dist(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
def rect(center, radius):
    return pygame.Rect(center[0]-radius, center[1]-radius, radius*2, radius*2)
class stone:
    def __init__(self, colours, center, radius, angle):
        self.colours = colours
        self.center = center
        self.radius = radius
        self.angle = angle
        self.users = []
    def draw(self, surface):
        corners = []
        for a in range(3):
            corners.append(centerangle(self.center, self.angle + a * 120, self.radius))
        for offset in range(3):
            arc(surface, self.colours[(offset+1)%3], corners[offset], self.radius * 1.25,
                self.angle + 180 + offset * 120 - 16.15, self.angle + 180 + offset * 120, [self.center])
            arc(surface, self.colours[(offset+2)%3], corners[offset], self.radius * 1.25,
                self.angle + 180 + offset * 120, self.angle + 180 + offset * 120 + 16.15, [self.center])
            pygame.draw.arc(surface, (0, 0, 0), rect(corners[offset], self.radius * 1.25),
                            radians(self.angle + 180 + offset * 120 - 16.15), radians(self.angle + 180 + offset * 120 + 16.15), 1)
class bone:
    def __init__(self, colours, center, left, right, angle):
        self.colours = colours
        self.center = center
        self.left = left
        self.right = right
        self.angle = angle
        self.users = []
    def draw(self, surface):
        arc(surface, self.colours[0], self.center, dist(self.center, self.left) * 1.25, self.angle - 30, self.angle + 30, [self.left, self.right])
        pygame.draw.arc(surface, (0, 0, 0), rect(self.center, dist(self.center, self.left) * 1.25),
                        radians(self.angle - 30), radians(self.angle + 30), 1)
        arc(surface, self.colours[1], reflect(self.center, midpoint(self.left, self.right)), dist(self.center, self.left) * 1.25, self.angle + 150, self.angle + 210, [self.left, self.right])
        pygame.draw.arc(surface, (0, 0, 0), rect(reflect(self.center, midpoint(self.left, self.right)), dist(self.center, self.left) * 1.25),
                        radians(self.angle + 150), radians(self.angle + 210), 1)
class circle:
    def __init__(self, colours, center, radius, above=None):
        self.center = center
        self.radius = radius
        self.centercolour = colours[0]
        self.stones = [
            above.stones[2] if above else stone([colours[1], colours[2], colours[0]], centerangle(self.center, 120, self.radius), self.radius, 60), # should be same colours
            stone([colours[0], colours[2], colours[3]], centerangle(self.center, 180, self.radius), self.radius, 0),
            stone([colours[0], colours[3], colours[4]], centerangle(self.center, 240, self.radius), self.radius, 60),
            stone([colours[5], colours[0], colours[4]], centerangle(self.center, 300, self.radius), self.radius, 0),
            stone([colours[6], colours[0], colours[5]], centerangle(self.center,   0, self.radius), self.radius, 60),
            above.stones[3] if above else stone([colours[6], colours[1], colours[0]], centerangle(self.center,  60, self.radius), self.radius, 0),
        ]
        self.bones = []
        self.above = above
        self.below = None
        if above:above.below = self
        for boneid in range(6):
            self.bones.append(bone([colours[boneid+1], colours[0]], self.center, centerangle(self.center, 120+boneid*60, self.radius), centerangle(self.center, 60+boneid*60, self.radius), 90+boneid*60))
        if above:self.bones[0] = above.bones[3]
        for stonem in self.stones:stonem.users.append(self)
        for bonem in self.bones:bonem.users.append(self)
    def draw(self, surface):
        pygame.draw.circle(surface, self.centercolour, self.center, self.radius)
        for bone in self.bones:bone.draw(surface)
        for stone in self.stones:stone.draw(surface)
    def rotate(self, right):
        #self.animate(right) # appears to rotate. Would immediatly snap back.
        lastusers = self.stones[5-5*right].users
        for i in range(5) if right else range(5, 0, -1):
            self.stones[i].users = self.stones[i-1+2*right].users
        self.stones[5*right].users = lastusers
        if right:self.stones.append(self.stones.pop(0))
        else:self.stones.insert(0, self.stones.pop())
        for stonem in range(6):
            self.stones[stonem].angle = (self.stones[stonem].angle + 60 - 120 * right) % 360
            self.stones[stonem].center = centerangle(self.center, 120 + 60 * stonem, self.radius)
        if self.above:
            self.above.stones[2] = self.stones[0]
            self.above.stones[3] = self.stones[5]
        if self.below:
            self.below.stones[0] = self.stones[2]
            self.below.stones[5] = self.stones[3]
        # stones are complete
        lastusers = self.bones[5-5*right].users
        for i in range(5) if right else range(5, 0, -1):
            self.bones[i].users = self.bones[i-1+2*right].users
        self.bones[5*right].users = lastusers
        if right:self.bones.append(self.bones.pop(0))
        else:self.bones.insert(0, self.bones.pop())
        for bonem in range(6):
            self.bones[bonem].angle = (self.bones[bonem].angle + 60 - 120 * right) % 360
            if right:
                self.bones[bonem].left = self.bones[bonem].right
                self.bones[bonem].right = centerangle(self.center, 60 + bonem * 60, self.radius)
            else:
                self.bones[bonem].right = self.bones[bonem].left
                self.bones[bonem].left = centerangle(self.center, 120 + bonem * 60, self.radius)
        if self.above:self.above.bones[3] = self.bones[0]
        if self.below:self.below.bones[0] = self.bones[3]
class board:
    def __init__(self, center, radius):
        red = 255, 0, 0
        orange = 255, 128, 0
        green = 0, 255, 0
        blue = 0, 0, 255
        yellow = 255, 255, 0
        white = 255, 255, 255
        self.center = center
        self.radius = radius
        self.top = circle([yellow, red, green, orange, white, orange, blue], point((self.center[0], self.center[1] - self.radius * math.cos(radians(30)))), self.radius)
        self.bottom = circle([white, yellow, orange, blue, red, green, orange], point((self.center[0], self.center[1] + self.radius * math.cos(radians(30)))), self.radius, self.top)
    def draw(self, surface):
        self.top.draw(surface)
        self.bottom.draw(surface)
    def rotate(self, bottom, right):
        (self.bottom if bottom else self.top).rotate(right)
    def scramble(self):
        for i in range(20): # no idea if it's actually 20
            self.rotate(random.randrange(2), random.randrange(2))
            

pygame.init()
screen = pygame.display.set_mode((500, 1000))
clock = pygame.time.Clock()

board = board((250, 500), 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:board.scramble()
            elif event.key in (pygame.K_q, pygame.K_e, pygame.K_a, pygame.K_d):
                board.rotate((event.key in (pygame.K_a, pygame.K_d)), (event.key in (pygame.K_d, pygame.K_e)))
    screen.fill((0, 0, 0))
    board.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    
