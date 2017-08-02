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


ID = 1
clock = pygame.time.Clock()
central_radar_list = []
radar_list = []
unit_list = []
piece_list = []
piece_unit_list = []

class radar():
    def __init__(self, x, y, color, radius, width, speed):
        self.position = [x, y]
        self.width = width
        self.color = color
        self.radius = width
        Surface = pygame.Surface((int(self.radius * 2), int(self.radius * 2)))
        self.image = pygame.draw.circle(Surface, color, (x, y), self.radius, self.width)
        self.speed = speed
        self.seconds = time.time()
        self.state = time.time()
        self.max_radius = radius
        self.generation_frequency = 0.6
        self.number_of_generations = 0
        self.generation_created = False
        self.die = False
        self.autokill = False
        self.ID = 0
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
    def set_ID (self, ID):
        self.ID = ID
    def set_position(self, x, y):
        self.position[0] = x
        self.position[1] = y
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
    def determine_autokill(self, state):
        self.autokill = state
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
                    if self.autokill:
                        new_generation.determine_autokill(True)
                    return new_generation
                elif self.number_of_generations == 0:
                    if not self.autokill:
                        self.generation_created = True
                        new_generation =  radar(self.position[0], self.position[1], self.color,  self.max_radius, self.width, self.speed)
                        return new_generation
                    else:
                        return None
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
    def __init__(self, x, y, color, radius, width, speed, list):
        self.rect = pygame.draw.rect(screen, [255, 255, 255] ,[x, y , 1, 1], 1)
        self.object = radar(x, y, color, radius, width, speed)
        self.position = [x, y]
        self.enable = False
        self.colliding = False
        self.enable_fade =  False
        self.moving = False
        self.ID = 0
        list.append(self)
    def set_ID (self, ID):
        self.ID = ID
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
            self.enable = True
            return True
        else:
            return False


class chess_piece(pygame.sprite.Sprite):
    def __init__(self, position, color,  type, list):
        global ID
        pygame.sprite.Sprite.__init__(self)
        file = str(color) + '_' + str(type) + '.jpg'
        self.image = pygame.image.load(file).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect ()
        self.rect.left = position[0] - 25
        self.rect.top = position[1] - 25
        self.type = type
        self.fading = True
        self.moving = False
        self.alpha = 150
        self.minimum_alpha = 10
        self.max_alpha = 250
        ID += 1
        self.ID = ID
        #self.image.convert_alpha()
        self.image.set_alpha(self.alpha)
        list.append(self)
        unit_object = unit(position[0], position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
        unit_object.enable_fade = True
        self.seconds = time.time()
        self.state = time.time()
        unit_object.set_ID(ID)
    def fade(self):
        self.seconds = time.time()
        delta_time = self.seconds - self.state
        if (self.seconds) != (self.state):
            if not self.fading:
                if self.alpha >= (self.max_alpha - 10):
                    self.fading = True
                else:
                    delta_alpha = (self.max_alpha - self.alpha) * (delta_time )
                    new_alpha = self.alpha + (delta_alpha*1)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.35)
                self.alpha = new_alpha
        self.image.set_alpha(int(self.alpha))
        self.state = time.time()
    def move (self, position):
        global unit_list
        self.alpha = self.max_alpha
        self.rect.left += position[0]
        self.rect.top += position[1]
        for unit_object in unit_list:
            if unit_object.ID == self.ID:
                old_fading = unit_object.enable_fade
                unit_list.remove(unit_object)
        unit_object = unit(self.rect.left+25+position[0], self.rect.top+25+position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
        unit_object.ID = self.ID
        unit_object.enable_fade = old_fading
    def set_moving(self, value):
        global unit_list
        self.moving = value
        for unit in unit_list:
            if unit.ID == self.ID:
                unit.moving = value

central_radar = radar(300, 300, [0, 204, 0],  300, 2, 0.1)
central_radar.set_generation(0.5, 0)
central_radar_list.append(central_radar)

def run_graphics ():
    global central_radar_list
    global radar_list
    global unit_list
    global piece_list
    screen.fill([255, 255, 255])
    for green_radar in central_radar_list:
        new_green_radar = green_radar.create_generation()
        if new_green_radar != None:
            central_radar_list.append(new_green_radar)
        green_radar.determine_death()
        if green_radar.die:
            central_radar_list.remove(green_radar)
        else:
            green_radar.run()
        for i in range (0, len(unit_list)):
            unit_object = unit_list[i]
            if unit_object.detect_collision(green_radar):
                if not unit_object.colliding:
                    unit_object.colliding = True
                    new_object = radar(unit_object.object.position[0], unit_object.object.position[1], unit_object.object.color, unit_object.object.max_radius, unit_object.object.width, unit_object.object.speed)
                    new_object.determine_autokill(True)
                    if not unit_object.moving:
                        radar_list.append(new_object)
                    new_object.run()
                    if unit_object.enable_fade:
                        for object in piece_list:
                            if object.ID == unit_object.ID:
                                object.fading = False
            else:
                unit_object.colliding = False
    for radar_object in radar_list:
        new_radar_object = radar_object.create_generation()
        if new_radar_object != None:
            old_ID = radar_object.ID
            radar_list.append(new_radar_object)
            new_radar_object.set_ID(old_ID)
        radar_object.determine_death()
        if radar_object.die:
            radar_list.remove(radar_object)
        else:
            radar_object.run()
    for piece in piece_list:
        piece.fade()
        screen.blit(piece.image, piece.rect)
    
    clock.tick(100)
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == MOUSEBUTTONDOWN:
            piece_moving = False
            starting_position = []
            (button1, button2, button3) = pygame.mouse.get_pressed()
            while button1 == 1:
                pygame.event.get ()
                (button1, button2, button3) = pygame.mouse.get_pressed()
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if not piece_moving:
                    for i in range (0, len(piece_list)):
                        if piece_list[i].rect.collidepoint (pos_x, pos_y):
                            piece_moving = True
                            piece_ID = piece_list[i].ID
                            starting_position = [pos_x, pos_y]
                            for unit_object in unit_list:
                                if unit_object.ID == piece_list[i].ID:
                                    radar_object = radar(pos_x, pos_y, [255, 255, 0], 50, 2, 0.09)
                                    radar_object.set_generation(0.05, 999)
                                    radar_object.set_ID(piece_list[i].ID)
                                    radar_list.append(radar_object)
                            break
                    if not piece_moving:
                        piece = chess_piece( [pos_x, pos_y], 'Black', 'Pawn', piece_list)
                        #unit(pos_x, pos_y, [0, 102, 255], 50, 2, 0.09, unit_list
                else:
                    for piece in piece_list:
                        if piece_ID == piece.ID:
                            piece.move([pos_x - starting_position[0], pos_y - starting_position[1]])
                            piece.set_moving(True)
                            for radar_object in radar_list:
                                if radar_object.ID == piece.ID:
                                    radar_object.set_position(radar_object.position[0] + pos_x - starting_position[0], radar_object.position[1] + pos_y - starting_position[1])
                    starting_position[0] = pos_x
                    starting_position[1] = pos_y
                run_graphics()
            for piece in piece_list:
                if piece_ID == piece.ID:
                    piece.set_moving(False)
                    to_be_removed = []
                    difference = 0
                    for i in range (0, len(radar_list)):
                        if radar_list[i-difference].ID == piece.ID:
                            #del radar_list[i-difference]
                            #difference += 1
                            radar_list[i].set_generation(1, 0)
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
    run_graphics ()