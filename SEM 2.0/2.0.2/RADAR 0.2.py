import serial
import time
import pygame, sys
from pygame.locals import *
from pygame.color import THECOLORS
import random

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([600, 600])
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
    def get_enable(self):
        self.seconds = time.time()
        if int(self.seconds) != int(self.state):
            new_radius = int(self.seconds - self.state)*self.speed + self.radius
            if new_radius > self.max_radius:
                self.radius = new_radius
                self.radius = self.width
                self.seconds = time.time()
                self.state = time.time()
                return False
            else:
                return True
        else:
            return True
    def run(self):
        self.seconds = time.time()
        if int(self.seconds) != int(self.state):
            new_radius = int(self.seconds - self.state)*self.speed + self.radius
            self.radius = new_radius
        if self.radius > self.max_radius:
            self.radius = self.width
            self.seconds = time.time()
            self.state = time.time()
        if self.width >= self.radius:
            self.radius = self.width
        Surface = pygame.Surface((self.radius * 2, self.radius * 2))
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        self.image = pygame.draw.circle(Surface, self.color, [self.radius, self.radius], int(self.radius), self.width)
        alpha =((self.max_radius - self.radius)/self.max_radius)**(0.5) * 255
        Surface.set_alpha(alpha)
        screen.blit(Surface, (self.position[0] - self.radius, self.position[1] - self.radius))

class unit():
    def __init__(self, x, y, color, radius, width, speed):
        self.rect = pygame.draw.rect(screen, [255, 255, 255] ,[x, y , 1, 1], 1)
        self.object = radar(x, y, color, radius, width, speed)
        self.position = [x, y]
        self.enable = False
    def run(self):
        if self.enable:
            self.enable = self.object.get_enable()
            if self.enable:
                self.object.run()

clock = pygame.time.Clock()
green_radar = radar(300, 300, [0, 204, 0],  300, 2, 0.2)
click = 0
radar_list = []
unit_list = []

while True:
    screen.fill([255, 255, 255])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == MOUSEBUTTONDOWN:
            (pos_x, pos_y) = pygame.mouse.get_pos()
            object = unit(pos_x, pos_y, [0, 102, 255], 50, 2, 0.05)
            unit_list.append(object)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            position_x = random.randint (0, 600)
            position_y = random.randint (0, 600)
            position_m = (position_x + position_y)/2
            width = random.randint(1, 5)
            radius = random.randint(5, position_m)
            speed = random.randint(1, 99) / 100.0
            object = radar(position_x, position_y, THECOLORS[random.choice(THECOLORS.keys())],  radius, width, speed)
            radar_list.append(object)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            unit_list = []
            radar_list = []
    green_radar.run()
    for unit_object in unit_list:
        #print ((unit_object.position[0]-green_radar.position[0])**2 + (unit_object.position[1]-green_radar.position[1])**2) - (int(green_radar.radius)**2)
        if abs(((unit_object.position[0]-green_radar.position[0])**2 + (unit_object.position[1]-green_radar.position[1])**2) - (int(green_radar.radius)**2))<= green_radar.radius:
        #if unit_object.rect.colliderect(green_radar.image):
            unit_object.run()
            unit_object.enable = True
            if unit_object not in radar_list:
                radar_list.append(unit_object)
    for radar_object in radar_list:
        radar_object.run()
    
    clock.tick(100)
    pygame.display.update()
    click += 1