#!/usr/bin/env python3
import math
import pygame
def radians(degrees):
    return degrees * math.pi / 180

def arc(surface, colour, center, radius, start, end):
    end = ((end-start)%360)+start # more than start but less than start+360
    points = [center]
    for angle in range(start, end + 1):
        trig = radians(angle)
        points.append((center[0] + radius * math.cos(trig),
                       center[1] - radius * math.sin(trig)))
    pygame.draw.polygon(surface, colour, points)

def point(float):
    return int(float[0]), int(float[1])
class stone:
    def __init__(self, colours, center, radius, angle):
        self.colours = colours
        self.center = center
        self.radius = radius
        self.angle = angle
    def draw(self, surface):
        corners = []
        for angle in range(self.angle, self.angle + 360, 120):
            print(angle, math.cos(radians(angle)), math.sin(radians(angle)))
            corners.append((self.center[0] + self.radius * math.cos(radians(angle)),
                            self.center[1] - self.radius * math.sin(radians(angle))))
        cornerdist = self.radius * 2 * math.sin(radians(60))
        # end of final
        for index in range(3):
            surface.set_at(point(corners[index]), self.colours[index])

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
    
