#!/usr/bin/env python3
import math
import pygame
def radians(degrees):
    return degrees * math.pi / 180
def degrees(radians):
    return radians * 180 / math.pi

def arc(surface, colour, center, radius, start, end):
    start = int(start)
    end = int(end)
    end = ((end-start)%360)+start # more than start but less than start+360
    points = [center]
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
class stone:
    def __init__(self, colours, center, radius, angle):
        self.colours = colours
        self.center = center
        self.radius = radius
        self.angle = angle
    def draw(self, surface):
        corners = []
        for a in range(3):
            corners.append(centerangle(self.center, self.angle + a * 120, self.radius))
        for offset in range(3):
            arc(surface, colours[(offset+2)%3], corners[offset], self.radius * 1.25,
                self.angle + 180 + offset * 120 - 16.15, self.angle + 180 + offset * 120)
            arc(surface, colours[(offset+1)%3], corners[offset], self.radius * 1.25,
                self.angle + 180 + offset * 120, self.angle + 180 + offset * 120 + 16.15)
class bone:
    def __init__(self, colours, center, radius, angle):
        self.colours = colours
        self.center = center
        self.radius = radius
        self.angle = angle
    def draw(self, surface):
        pass

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

testStone = stone([(255, 0, 0), (0, 255, 0), (0, 0, 255)], (250, 250), 100, 0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:exit()
    screen.fill((0, 0, 0))
    testStone.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    
