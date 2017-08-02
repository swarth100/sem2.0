import serial
import time
import pygame, sys
from pygame.locals import *
from pygame.color import THECOLORS
import random

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

class radar():
    def __init__(self, x, y, color, radius, width, speed):
        self.position = (x, y)
        self.width = width
        self.color = color
        self.image = pygame.draw.circle(screen, color, (x, y), width, width)
        self.speed = speed
        self.seconds = time.time()
        self.state = time.time()
        self.radius = width
        self.max_radius = radius
    def run(self):
        self.seconds = time.time()
        new_radius = (self.seconds - self.state)*self.speed + self.radius
        self.radius = new_radius
        if self.radius > self.max_radius:
            self.radius -= self.max_radius
            self.seconds = time.time()
            self.state = time.time()
        if self.width >= self.radius:
            self.radius = self.width
        Surface = pygame.Surface((self.radius * 2, self.radius * 2))
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        #alpha =((self.max_radius - self.radius)/self.max_radius) * 255
        #Surface.set_alpha(alpha)
        self.image = pygame.draw.circle(Surface, self.color, [self.radius, self.radius], self.radius, self.width)
        alpha =((self.max_radius - self.radius)/self.max_radius) * 255
        Surface.set_alpha(alpha)
        screen.blit(Surface, (self.position[0] - self.radius, self.position[1] - self.radius))
        
ball = radar(300, 300, THECOLORS[random.choice(THECOLORS.keys())],  300, 2, 0.5)
click = 0
radar_list = []
radar_list.append(ball)

while True:
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            position_x = random.randint (0, 1000)
            position_y = random.randint (0, 600)
            position_m = (position_x + position_y)/2
            width = random.randint(1, 5)
            radius = random.randint(5, position_m)
            object = radar(position_x, position_y, THECOLORS[random.choice(THECOLORS.keys())],  radius, width, 0.5)
            radar_list.append(object)
    for radar_object in radar_list:
        radar_object.run()
    pygame.display.update()
    click += 1