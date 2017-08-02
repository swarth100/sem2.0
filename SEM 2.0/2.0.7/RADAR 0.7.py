import serial
import time
import pygame, sys
from pygame.locals import *
from pygame.color import THECOLORS
import random

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([700, 700])
screen.fill ([255, 255, 255])


ID = 1
clock = pygame.time.Clock()
central_radar_list = []
radar_list = []
unit_list = []
piece_list = []
piece_unit_list = []
sprite_list = []
text_list = []
button_list = []
old_sprite_list = []
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
rendering = False
port_found = False
starting = True

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
        self.can_collide = True
        self.create_radar = True
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
        self.position = position
        self.rect.left = position[0] - 25
        self.rect.top = position[1] - 25
        self.original_place = [0, 0]
        self.type = type
        self.fading = False
        self.first_fade = True
        self.moving = False
        self.start_pos = [0, 0]
        self.alpha = 10
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
                    if self.first_fade:
                        new_alpha = self.alpha + (delta_alpha*0.3)
                    else:
                        new_alpha = self.alpha + (delta_alpha*1)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.2)
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
    def set_pos (self, pos):
        self.rect.left = pos[0]
        self.rect.top = pos[1]
    def set_moving(self, value):
        global unit_list
        self.moving = value
        for unit in unit_list:
            if unit.ID == self.ID:
                unit.moving = value
                
class image(pygame.sprite.Sprite):
    def __init__(self, position, name, dimensions, list, colorkey, enable_fade):
        global ID
        pygame.sprite.Sprite.__init__(self)
        file = str(name) + '.png'
        self.image = pygame.image.load(file).convert()
        self.image = pygame.transform.scale(self.image, (dimensions[0], dimensions[1]))
        if colorkey:
            self.image.set_colorkey([0, 0, 0])
        else:
            self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect ()
        self.rect.left = position[0] - dimensions[0]/2
        self.rect.top = position[1] - dimensions[1]/2
        self.fading = False
        self.first_fade = True
        self.alpha = 10
        self.minimum_alpha = 10
        self.max_alpha = 250
        self.enable_fade = enable_fade
        ID += 1
        self.ID = ID
        #self.image.convert_alpha()
        self.image.set_alpha(self.alpha)
        list.append(self)
        self.seconds = time.time()
        self.state = time.time()
        if self.enable_fade:
            unit_object = unit(position[0], position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
            unit_object.enable_fade = True
            unit_object.set_ID(ID)
        else:
            self.alpha = 250
    def fade(self):
        self.seconds = time.time()
        delta_time = self.seconds - self.state
        if self.enable_fade:
            if (self.seconds) != (self.state):
                if not self.fading:
                    if self.alpha >= (self.max_alpha - 10):
                        self.fading = True
                        self.first_fade = False
                    else:
                        delta_alpha = (self.max_alpha - self.alpha) * (delta_time )
                        if self.first_fade:
                            new_alpha = self.alpha + (delta_alpha*0.3)
                        else:
                            new_alpha = self.alpha + (delta_alpha*1)
                        self.alpha = new_alpha
                if self.fading:
                    delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                    new_alpha = self.alpha - (delta_alpha*0.2)
                    self.alpha = new_alpha
        self.image.set_alpha(int(self.alpha))
        self.state = time.time()

class text():
    def __init__(self, position, word_text, dimension, list, color):
        global ID
        self.fading = False
        self.first_fade = True
        self.color = color
        self.dimension = dimension
        self.alpha = 10
        self.minimum_alpha = 10
        self.max_alpha = 250
        self.word_text = word_text
        self.font = pygame.font.SysFont('times-new-roman', dimension)
        self.image = self.font.render(self.word_text, True, self.color)
        self.rect = self.image.get_rect()
        ID += 1
        self.ID = ID
        self.image.set_alpha(self.alpha)
        list.append(self)
        unit_object = unit(position[0], position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
        self.position = [position[0]- int(self.rect.width/2), position[1] - int(self.rect.height/2)]
        unit_object.enable_fade = True
        unit_object.create_radar = False
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
                    self.first_fade = False
                else:
                    delta_alpha = (self.max_alpha - self.alpha) * (delta_time )
                    if self.first_fade:
                        new_alpha = self.alpha + (delta_alpha*0.3)
                    else:
                        new_alpha = self.alpha + (delta_alpha*5)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.2)
                self.alpha = new_alpha
        self.state = time.time()
    def run(self):
        self.seconds = time.time()
        Surface = pygame.Surface([self.rect.width, self.rect.height])
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        Surface.blit(self.image, [0, 0])
        self.fade()
        alpha = self.alpha
        Surface.set_alpha(alpha)
        screen.blit(Surface, self.position)

class button():
    def __init__(self, position, word_text, dimension, list, color, function, state):
        global ID
        self.function = function
        self.function_state = state
        self.fading = False
        self.first_fade = True
        self.color = color
        self.dimension = dimension
        self.position = position
        self.alpha = 10
        self.minimum_alpha = 10
        self.max_alpha = 250
        self.word_text = word_text
        ID += 1
        self.ID = ID
        button_text = text(self.position, self.word_text, self.dimension, text_list, self.color)
        button_text.ID = self.ID
        self.image_rect = button_text.image.get_rect()
        Surface = pygame.Surface([self.image_rect.width + 10, self.image_rect.height + 10])
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        self.image = pygame.draw.rect(screen, self.color, [self.position[0]-int(self.image_rect.width/2) - 5, self.position[1] - int(self.image_rect.height/2) - 5, (self.image_rect.width + 10), (self.image_rect.height + 10)], 3)
        Surface.set_alpha(self.alpha)
        list.append(self)
        unit_object = unit(position[0], position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
        unit_object.enable_fade = True
        unit_object.create_radar = False
        self.seconds = time.time()
        self.state = time.time()
        unit_object.set_ID(self.ID)
    def fade(self):
        self.seconds = time.time()
        delta_time = self.seconds - self.state
        if (self.seconds) != (self.state):
            if not self.fading:
                if self.alpha >= (self.max_alpha - 10):
                    self.fading = True
                    self.first_fade = False
                else:
                    delta_alpha = (self.max_alpha - self.alpha) * (delta_time )
                    if self.first_fade:
                        new_alpha = self.alpha + (delta_alpha*0.3)
                    else:
                        new_alpha = self.alpha + (delta_alpha*1)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.2)
                self.alpha = new_alpha
        self.state = time.time()
    def run(self):
        self.seconds = time.time()
        Surface = pygame.Surface([self.image_rect.width + 10, self.image_rect.height + 10])
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        pygame.draw.rect(Surface, self.color ,[0, 0 , self.image_rect.width + 10, self.image_rect.height + 10], 3)
        self.fade()
        alpha = self.alpha
        Surface.set_alpha(alpha)
        screen.blit(Surface, [self.position[0]-int(self.image_rect.width/2) - 5, self.position[1] - int(self.image_rect.height/2) - 5])
    def remove(self, list):
        list.remove(self)
        for text_object in text_list:
            if text_object.ID == self.ID:
                text_list.remove(text_object)


central_radar = radar(350, 350, [0, 204, 0],  350, 2, 0.05)
central_radar.set_generation(0.6, 0)
central_radar_list.append(central_radar)

def run_graphics ():
    global central_radar_list
    global radar_list
    global unit_list
    global piece_list
    global rendering
    global sprite_list
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
                    if not starting:
                        if unit_object.create_radar:
                            new_object = radar(unit_object.object.position[0], unit_object.object.position[1], unit_object.object.color, unit_object.object.max_radius, unit_object.object.width, unit_object.object.speed)
                            new_object.determine_autokill(True)
                            if not unit_object.moving:
                                radar_list.append(new_object)
                            new_object.run()
                    if unit_object.enable_fade:
                        for object in piece_list:
                            if object.ID == unit_object.ID:
                                object.fading = False
                        for sprite in sprite_list:
                            if sprite.ID == unit_object.ID:
                                sprite.fading = False
                        for button_object in button_list:
                            if button_object.ID == unit_object.ID:
                                button_object.fading = False
                        for piece_of_text in text_list:
                            if piece_of_text.ID == unit_object.ID:
                                piece_of_text.fading = False
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
        #Whith the following line it crashes but it says the piece positions
        #piece_of_text = text([piece.position[0], piece.position[1] + 20], str(piece.original_place[0]) + ', ' + str(piece.original_place[1]), 10, text_list, [0, 51, 0])
    for sprite in sprite_list:
        sprite.fade()
        screen.blit(sprite.image, sprite.rect)
    for button_object in button_list:
        button_object.run()
    for piece_of_text in text_list:
        piece_of_text.run()
    
    #clock.tick(100)
    pygame.display.update()


while True:
    if starting:
        if not rendering:
            image([150, 300], 'python_logo', [150, 150], sprite_list, True, True)
            image([550, 300], 'pygame_logo', [296, 89], sprite_list, False, True)
            image([350, 450], 'arduino_logo', [170, 162], sprite_list, True, True)
            text([350, 125], 'SEM 2.0', 150, text_list, [0, 102, 255])
            button([350, 650], 'FIND SERIAL', 40, button_list, [0, 102, 255], 'detect_serial', False)
            rendering = True
    for button_object in button_list:
        if (button_object.function == 'detect_serial' or button_object.function == 'retry_detect_serial'):
            if button_object.function_state == True:
                if not port_found:
                    for i in range (9, 20):
                        try:
                            arduino = serial.Serial(
                                port='COM' + str(i),\
                                baudrate=9600,\
                                parity=serial.PARITY_NONE,\
                                stopbits=serial.STOPBITS_ONE,\
                                bytesize=serial.EIGHTBITS,\
                                    timeout=0)
                            port_found = True
                            break
                        except:
                            nothing = True
                    if button_object.function == 'retry_detect_serial':
                        for button_object_blob in button_list:
                            if button_object_blob.function == 'initial_next_button':
                                button_object_blob.remove(button_list)
                        for text_object in text_list:
                            if text_object.dimension == 30:
                                text_list.remove(text_object)
                if port_found:
                    com_port = 'COM' + str(i)
                    text([350, 600], 'ARDUINO ON ' + com_port, 30, text_list, [0, 102, 255])
                    button([350, 660], 'CONTINUE', 40, button_list, [0, 102, 255], 'initial_next_button', False)
                else:
                    text([350, 600], 'NO ARDUINO CONNECTION FOUND', 30, text_list, [255, 51, 0])
                    button([250, 660], 'CONTINUE', 40, button_list, [0, 102, 255], 'initial_next_button', False)
                    button([450, 660], 'RETRY', 40, button_list, [255, 102, 0], 'retry_detect_serial', False)
                button_object.remove(button_list)
        if button_object.function == 'initial_next_button':
            if button_object.function_state == True:
                radar_list = []
                unit_list = []
                piece_list = []
                piece_unit_list = []
                sprite_list = old_sprite_list
                text_list = []
                button_list = []
                button([350, 660], 'BACK', 40, button_list, [102, 255, 51], 'back_button', False)
                for i in range (0, 9):
                    image([150 + 50 * i, 350], 'vertical_piece', [3, 500], sprite_list, False, False)
                    image([350, 150 + 50 * i], 'horizontal_piece', [500, 3], sprite_list, False, False)
                    if i != 8:
                        text([175 + 50 * i, 75], str(i + 1), 25, text_list, [0, 102, 255])
                        text([75, 175 + 50 * i], alphabet[i], 25, text_list, [0, 102, 255])
                        positioned_piece = chess_piece([175 + 50 * i, 225], 'Black', 'Pawn', piece_list)
                        positioned_piece.original_place = [i + 1, 2]
                        positioned_piece = chess_piece([175 + 50 * i, 475], 'White', 'Pawn', piece_list)
                        positioned_piece.original_place = [i + 1, 7]
                for j in range (0, 2):
                    positioned_piece = chess_piece([175 + 350 * j, 175], 'Black', 'Tower', piece_list)
                    positioned_piece.original_place = [1 + j*7, 1]
                    positioned_piece = chess_piece([175 + 350 * j, 525], 'White', 'Tower', piece_list)
                    positioned_piece.original_place = [1 + j*7, 8]
                    positioned_piece = chess_piece([225 + 250 * j, 175], 'Black', 'Knight', piece_list)
                    positioned_piece.original_place = [2 + j*5, 1]
                    positioned_piece = chess_piece([225 + 250 * j, 525], 'White', 'Knight', piece_list)
                    positioned_piece.original_place = [2 + j*5, 8]
                    positioned_piece = chess_piece([275 + 150 * j, 175], 'Black', 'Bishop', piece_list)
                    positioned_piece.original_place = [3 + j*3, 1]
                    positioned_piece = chess_piece([275 + 150 * j, 525], 'White', 'Bishop', piece_list)
                    positioned_piece.original_place = [3 + j*3, 8]
                positioned_piece = chess_piece([325, 175], 'Black', 'King', piece_list)
                positioned_piece.original_place = [4, 1]
                positioned_piece = chess_piece([325, 525], 'White', 'Queen', piece_list)
                positioned_piece.original_place = [4, 8]
                positioned_piece = chess_piece([375, 175], 'Black', 'Queen', piece_list)
                positioned_piece.original_place = [5, 1]
                positioned_piece = chess_piece([375, 525], 'White', 'King', piece_list)
                positioned_piece.original_place = [5, 8]
                starting = False
                button_object.function_state = False
        if button_object.function == 'back_button':
            if button_object.function_state == True:
                old_sprite_list = sprite_list
                radar_list = []
                unit_list = []
                piece_list = []
                piece_unit_list = []
                text_list = []
                button_list = []
                sprite_list = []
                starting = True
                rendering = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == MOUSEBUTTONDOWN:
            piece_moving = False
            starting_position = [0, 0]
            (button1, button2, button3) = pygame.mouse.get_pressed()
            piece_ID = 0
            while button1 == 1:
                pygame.event.get ()
                (button1, button2, button3) = pygame.mouse.get_pressed()
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if not piece_moving:
                    for button_object in button_list:
                        if button_object.image.collidepoint (pos_x, pos_y):
                            piece_moving = True
                            if button_object.function_state == False:
                                button_object.function_state = True
                            else:
                                button_object.function_state = False
                            break
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
                            piece_list[i].start_pos = [piece_list[i].rect.left, piece_list[i].rect.top][:]
                            break
                    #if not piece_moving:
                        #if not starting:
                            #piece = chess_piece( [pos_x, pos_y], 'Black', 'Pawn', piece_list)
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
                            if not (pos_x >= 150 and pos_x <= 550) or not (pos_y >= 150 and pos_y <= 550):
                                radar_list[i].set_position(piece.start_pos[0] + 25, piece.start_pos[1] + 25)
                    ended_properly = False
                    if (pos_x >= 150 and pos_x <= 550):
                        if (pos_y >= 150 and pos_y <= 550):
                            piece.set_pos([int(pos_x/50)*50, int(pos_y/50)*50])
                            delta_x = int((pos_x - piece.start_pos[0])/50)
                            delta_y = int((pos_y - piece.start_pos[1])/50)
                            piece.original_place[0] += delta_x
                            piece.original_place[1] += delta_y
                            ended_properly = True
                    if not ended_properly:
                        piece.set_pos(piece.start_pos)
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



