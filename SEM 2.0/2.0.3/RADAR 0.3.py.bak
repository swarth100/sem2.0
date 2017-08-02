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
        self.generation_frequency = 0.6
        self.number_of_generations = 0
        self.generation_created = False
        self.die = False
    def get_enable(self):
        self.seconds = time.time()
        if int(self.seconds) != int(self.state):
            new_radius = int(self.seconds - self.state)*self.speed + self.radius
            if new_radius > self.max_radius:
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
        #if self.radius > self.max_radius:
            #self.radius = self.width
            #self.seconds = time.time()
            #self.state = time.time()
        if self.width >= self.radius:
            self.radius = self.width
        Surface = pygame.Surface((int(self.radius * 2), int(self.radius * 2)))
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        self.image = pygame.draw.circle(Surface, self.color, [int(self.radius), int(self.radius)], int(self.radius), self.width)
        alpha =((self.max_radius - self.radius)/self.max_radius)**(0.5) * 255
        Surface.set_alpha(alpha)
        screen.blit(Surface, (self.position[0] - self.radius, self.position[1] - self.radius))
    def set_generation(self, frequency, number_of_generations):
        self.generation_frequency = frequency
        self.number_of_generations = number_of_generations
    def create_generation (self):
        if not self.generation_created:
            if self.radius >= (self.max_radius * self.generation_frequency):
                if self.number_of_generations >= 1:
                    self.generation_created = True
                    new_generation =  radar(self.position[0], self.position[1], self.color,  self.max_radius, self.width, self.speed)
                    new_generation.set_generation(self.generation_frequency, (self.number_of_generations - 1))
                    return new_generation
                elif self.number_of_generations == 0:
                    self.generation_created = True
                    new_generation =  radar(self.position[0], self.position[1], self.color,  self.max_radius, self.width, self.speed)
                    return new_generation
                else:
                    return None
        else:
            return None
    def determine_death(self):
        self.seconds = time.time()
        new_radius = int(self.seconds - self.state)*self.speed + self.radius
        if new_radius > self.max_radius:
            self.die = True

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
    def determine_death(self):
        self.object.determine_death()
        self.die = self.object.die
    def create_generation(self):
        generation = self.object.create_generation()
        return generation
    def detect_collision(self, circumference):
        if abs(((self.position[0]-circumference.position[0])**2 + (self.position[1]-circumference.position[1])**2) - (int(circumference.radius)**2))<= circumference.radius:
            #self.run()
            self.enable = True
            return True
        else:
            return False

clock = pygame.time.Clock()
central_radar = radar(300, 300, [0, 204, 0],  300, 2, 0.2)
central_radar.set_generation(0.01, 20)
central_radar_list = []
central_radar_list.append(central_radar)
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
            object = unit(pos_x, pos_y, [0, 102, 255], 50, 2, 0.1)
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
    for green_radar in central_radar_list:
        new_green_radar = green_radar.create_generation()
        if new_green_radar != None:
            central_radar_list.append(new_green_radar)
        green_radar.determine_death()
        if green_radar.die:
            central_radar_list.remove(green_radar)
        else:
            green_radar.run()
            for unit_object in unit_list:
                if unit_object.detect_collision(green_radar):
                    new_object = radar(unit_object.object.position[0], unit_object.object.position[1], unit_object.object.color, unit_object.object.max_radius, unit_object.object.width, unit_object.object.speed)
                    new_object.set_generation(0.6, -1)
                    radar_list.append(new_object)
    for radar_object in radar_list:
        new_radar_object = radar_object.create_generation()
        if new_radar_object != None:
            radar_list.append(new_radar_object)
        radar_object.determine_death()
        if radar_object.die:
            radar_list.remove(radar_object)
        else:
            radar_object.run()
    
    clock.tick(100)
    pygame.display.update()
    click += 1