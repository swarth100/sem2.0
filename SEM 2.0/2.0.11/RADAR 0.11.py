try:
    import serial
except:
    print 'PySerial has not ben installed: download it for python 2.7 or LOWER'
import chess
import time
import pygame, sys
from pygame.locals import *
from pygame.color import THECOLORS
import random
import subprocess, time

import Tkinter

root = Tkinter.Tk()

full_screen_width = root.winfo_screenwidth()
full_screen_height = root.winfo_screenheight()

extra_x = 0
extra_y = 0

pygame.init()
pygame.display.set_caption('#SEM 2.0.11')
screen = pygame.display.set_mode([700, 700])
screen.fill ([255, 255, 255])

engine = subprocess.Popen(
    'C:\Python27\stockfish-5-win\stockfish-5-win\Windows\stockfish_14053109_32bit.exe',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

board = chess.Bitboard()

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
old_piece_list = []
comand_list = []
current_radar_pieces = []
general_list = [[], [], [], [], [], [], []]
chess_alphabet = [ ' ', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
dead_white_list = [[4, 9], [5, 9], [3, 9], [6, 9], [2, 9], [7, 9], [1, 9], [8, 9], [0, 9], [9, 9], [0, 8], [9, 8], [0, 7], [9, 7], [0, 6], [9, 6]]
dead_black_list = [[4, 0], [5, 0], [3, 0], [6, 0], [2, 0], [7, 0], [1, 0], [8, 0], [0, 0], [9, 0], [0, 1], [9, 1], [0, 2], [9, 2], [0, 3], [9, 3]]
alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
window_fullscreen = False
rendering = False
port_found = False
starting = True
first_time = False
arduino_in_motion = False
page_one_uploaded = False
page_two_uploaded = False
page_three_uploaded = False
checkmate = False
running = False
start_time = 0
arduino_position = [0, 0]
list_of_moves = []
turn = 'white'
upper_text = ''
global_output = ''
function_list = [['arduino_autolock', 'off'], ['AI_player', 'off'], ['black_AI', 'off'], ['white_AI_difficulty', 'off'], ['black_AI_difficulty', 'off']]

def send_AI_comand(command):
    #print('\nyou:\n\t'+command)
    engine.stdin.write(command+'\n')

def get_AI_comand():
    global global_output
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    engine.stdin.write('isready\n')
    #print('\nengine:')
    global_output = ''
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':
            global_output = global_output + ' ' + text
            #print('\t'+text)

get_AI_comand()
def run_AI():
    global running, turn, start_time, list_of_moves, engine, global_output, chess_alphabet, piece_list, check_mate
    for function in function_list:
        if function[0] == 'AI_player':
            state = function[1]
        if function[0] == 'black_AI':
            black_state = function[1]
        if function[0] == 'black_AI_difficulty':
            if turn == 'black':
                if function[1] == 'on':
                    delta_time = 0.1
                else:
                    delta_time = 1
        if function[0] == 'white_AI_difficulty':
            if turn == 'white':
                if function[1] == 'on':
                    delta_time = 0.1
                else:
                    delta_time = 1
    if (piece_list != []) and (not checkmate):
        if ((turn == 'white') and (state == 'on')) or ((turn == 'black') and (black_state == 'on')):
            for function in function_list:
                if function[0] == 'arduino_autolock':
                    if (function[1] == 'off') or ((function[1] == 'on') and (len(comand_list) == 0)):
                        if not running:
                            send_AI_comand('uci')
                            get_AI_comand()
                            send_AI_comand('setoption name Hash value 128')
                            get_AI_comand()
                            send_AI_comand('ucinewgame')
                            get_AI_comand()
                            extra_moves = ' '
                            for i in range (0, len(list_of_moves)):
                                extra_moves = extra_moves + list_of_moves[i] + ' '
                            send_AI_comand('position startpos moves ' + extra_moves)
                            get_AI_comand()
                            send_AI_comand('go infinite')
                            running = True
                            start_time = time.time()
                        if running:
                            if (time.time()-start_time) >= delta_time:
                                try:
                                    get_AI_comand()
                                    #print global_output
                                    output_string = global_output.split(' ')
                                    #print output_string
                                    for i in range (0, len(output_string)):
                                        if output_string[len(output_string) - i - 1] == 'pv':
                                            movement = output_string[len(output_string) - i]
                                            #list_of_moves.append(movement)
                                            #print movement
                                            break
                                    send_AI_comand('stop')
                                    get_AI_comand()
                                    movement_list = list(movement)
                                    for i in range (0, len(chess_alphabet)):
                                        if movement_list[0] == chess_alphabet[i]:
                                            start_pos = [i, int(movement_list[1])]
                                        if movement_list[2] == chess_alphabet[i]:
                                            end_pos = [i, int(movement_list[3])]
                                    #print 'FOUND MOVE'
                                    #print start_pos
                                    for piece_object in piece_list:
                                        #print piece_object.original_place
                                        if piece_object.original_place == start_pos:
                                            #print piece_object.original_place
                                            deploy_move(piece_object, start_pos, end_pos, movement)
                                            #print piece_object.original_place
                                            piece_object.set_pos([100 + end_pos[0]*50, 100 + end_pos[1]*50])

                                    running = False
                                except:
                                    nothing = True

def refresh_dead_lists ():
    global dead_black_list, dead_white_list
    dead_white_list = [[4, 9], [5, 9], [3, 9], [6, 9], [2, 9], [7, 9], [1, 9], [8, 9], [0, 9], [9, 9], [0, 8], [9, 8], [0, 7], [9, 7], [0, 6], [9, 6]]
    dead_black_list = [[4, 0], [5, 0], [3, 0], [6, 0], [2, 0], [7, 0], [1, 0], [8, 0], [0, 0], [9, 0], [0, 1], [9, 1], [0, 2], [9, 2], [0, 3], [9, 3]]

def determine_ratio ():
    global full_screen_height, full_screen_width, extra_x, extra_y, window_fullscreen
    if window_fullscreen:
        extra_x = int((full_screen_width-700)/2)
        extra_y = int((full_screen_height-700)/2)
    else:
        extra_x = 0
        extra_y = 0

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
        global extra_x, extra_y
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
        screen.blit(Surface, (self.position[0] - self.radius + extra_x, self.position[1] - self.radius + extra_y))
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
                        new_generation = radar(self.position[0], self.position[1], self.color,  self.max_radius, self.width, self.speed)
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
        self.frequency = 0.6
        self.number_of_generations = -1
        self.ID = 0
        self.color = color
        list.append(self)
        self.back_fade = False
    def set_ID (self, ID):
        self.ID = ID
    def run(self):
        #Apparently UNUSED function
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
    def push_off_fade(self):
        if self.back_fade:
            self.back_fade = False
            return True
        else:
            return False
    def detect_collision(self, circumference):
        if abs(((self.position[0]-circumference.position[0])**2 + (self.position[1]-circumference.position[1])**2) - (int(circumference.radius)**2))<= circumference.radius:
            self.enable = True
            return True
        else:
            return self.push_off_fade()
    def change_color(self, new_color):
        self.object.color = new_color
        #print self.ID
    def set_generation(self, frequency, number):
        self.frequency = frequency
        self.number_of_generations = number



class chess_piece(pygame.sprite.Sprite):
    def __init__(self, position, color,  type, list, unit_type):
        global ID
        pygame.sprite.Sprite.__init__(self)
        file = str(color) + '_' + str(type) + '.jpg'
        self.unit_type = unit_type
        self.image = pygame.image.load(file).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey([255, 255, 255])
        self.rect = self.image.get_rect ()
        self.color = color
        self.position = position
        self.rect.left = position[0] - 25
        self.rect.top = position[1] - 25
        self.original_place = [0, 0]
        self.type = type
        self.fading = False
        self.first_fade = True
        self.moving = False
        self.can_move = True
        self.not_moved = True
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
        unit_object.create_radar = False
        self.seconds = time.time()
        self.state = time.time()
        unit_object.set_ID(ID)
    def enable_radar(self, color, value, super):
        for unit_object in unit_list:
            if unit_object.ID == self.ID:
                unit_object.create_radar = value
                unit_object.change_color(color)
                if not super:
                    unit_object.set_generation(0.05, 2)
                else:
                    unit_object.set_generation(0.05, 8)
    def change_icon(self):
        file = str(self.color) + '_' + str(self.type) + '.jpg'
        self.image = pygame.image.load(file).convert()
        self.image = pygame.transform.scale(self.image, (50, 50))
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
                        new_alpha = self.alpha + (delta_alpha*0.5)
                    else:
                        new_alpha = self.alpha + (delta_alpha*1.6)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.15)
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
                old_create_radar = unit_object.create_radar
                unit_list.remove(unit_object)
        unit_object = unit(self.rect.left+25+position[0], self.rect.top+25+position[1], [0, 102, 255], 50, 2, 0.09, unit_list)
        unit_object.ID = self.ID
        unit_object.create_radar = old_create_radar
        unit_object.enable_fade = old_fading
    def set_pos (self, pos):
        global unit_list, extra_x, extra_y
        self.rect.left = pos[0]
        self.rect.top = pos[1]
        for unit_object in unit_list:
            if unit_object.ID == self.ID:
                old_fading = unit_object.enable_fade
                old_create_radar = unit_object.create_radar
                unit_color = unit_object.object.color[:]
                unit_list.remove(unit_object)
                new_unit_object = unit(25+pos[0], 25+pos[1], unit_color, 50, 2, 0.09, unit_list)
                new_unit_object.ID = self.ID
                new_unit_object.create_radar = old_create_radar
                new_unit_object.enable_fade = old_fading
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
                            new_alpha = self.alpha + (delta_alpha*0.5)
                        else:
                            new_alpha = self.alpha + (delta_alpha*1.6)
                        self.alpha = new_alpha
                if self.fading:
                    delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                    new_alpha = self.alpha - (delta_alpha*0.15)
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
                        new_alpha = self.alpha + (delta_alpha*0.5)
                    else:
                        new_alpha = self.alpha + (delta_alpha*1.6)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.15)
                self.alpha = new_alpha
        self.state = time.time()
    def run(self):
        global extra_x, extra_y
        self.image = self.font.render(self.word_text, True, self.color)
        self.seconds = time.time()
        Surface = pygame.Surface([self.rect.width, self.rect.height])
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        Surface.blit(self.image, [0, 0])
        self.fade()
        alpha = self.alpha
        Surface.set_alpha(alpha)
        screen.blit(Surface, [self.position[0] + extra_x, self.position[1] + extra_y])

class button():
    def __init__(self, position, word_text, dimension, list, color, function, state):
        global ID
        self.function = function
        self.slider_state = False
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
        self.image_button = False
        unit_object.set_ID(self.ID)
        self.slider= False
        self.slider_value = ''
        self.slider_trigger = ''
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
                        new_alpha = self.alpha + (delta_alpha*0.5)
                    else:
                        new_alpha = self.alpha + (delta_alpha*1.6)
                    self.alpha = new_alpha
            if self.fading:
                delta_alpha = (self.alpha - self.minimum_alpha) * (delta_time )
                new_alpha = self.alpha - (delta_alpha*0.15)
                self.alpha = new_alpha
        self.state = time.time()
    def set_image (self, file, dimensions):
        self.sprite = pygame.image.load(file).convert()
        self.sprite = pygame.transform.scale(self.sprite, (dimensions[0], dimensions[1]))
        self.image_rect = self.sprite.get_rect()
        self.image_button = True
        self.image = pygame.draw.rect(screen, self.color, [self.position[0]-int(self.image_rect.width/2), self.position[1] - int(self.image_rect.height/2), (self.image_rect.width + 10), (self.image_rect.height + 10)], 3)
    def run(self):
        global text_list, extra_x, extra_y
        self.seconds = time.time()
        self.fade()
        alpha = self.alpha
        Surface = pygame.Surface([self.image_rect.width + 10, self.image_rect.height + 10])
        Surface.fill ([255, 255, 255])
        Surface.set_colorkey((255, 255, 255))
        for text_object in text_list:
            if text_object.ID == self.ID:
                object_in_question = text_object
        if self.slider:
            if self.slider_state == True:
                self.color = self.active_color
                object_in_question.color = self.active_color
            else:
                self.color = [150, 150, 150]
                object_in_question.color = [150, 150, 150]
        if not self.image_button:
            pygame.draw.rect(Surface, self.color ,[0, 0 , self.image_rect.width + 10, self.image_rect.height + 10], 3)
            Surface.set_alpha(alpha)
            screen.blit(Surface, [self.position[0]-int(self.image_rect.width/2) - 5 + extra_x, self.position[1] - int(self.image_rect.height/2) - 5 + extra_y])
        else:
            self.sprite.set_colorkey([0, 0, 0])
            pygame.draw.rect(Surface, self.color ,[0, 0, self.image_rect.width + 10, self.image_rect.height + 10], 3)
            Surface.set_alpha(alpha)
            screen.blit(Surface, [self.position[0]-int(self.image_rect.width/2) - 5 + extra_x, self.position[1] - int(self.image_rect.height/2) - 5 + extra_y])
            self.sprite.set_alpha(alpha)
            screen.blit(self.sprite, [self.position[0]-int(self.image_rect.width/2) + extra_x, self.position[1] - int(self.image_rect.height/2) + extra_y])
    def remove(self, list):
        list.remove(self)
        for text_object in text_list:
            if text_object.ID == self.ID:
                text_list.remove(text_object)
    def set_active_color(self, color):
        self.active_color = color
    def bind(self, other_button, function):
        global function_list
        self.slider = True
        self.slider_button = other_button
        other_button.slider = True
        other_button.slider_button = self
        self.slider_state = True
        self.slider_value = 'off'
        other_button.slider_value = 'on'
        self.slider_trigger = function
        other_button.slider_trigger = function
    def switch(self):
        global function_list
        if self.slider:
            for function_object in function_list:
                if function_object[0] == self.slider_trigger:
                    button_function = function_object
            if self.slider_state == True:
                self.slider_button.slider_state = False
                button_function[1] = self.slider_value
            else:
                self.slider_button.slider_state = True
                button_function[1] = self.slider_button.slider_value


central_radar = radar(350, 350, [0, 204, 0],  350, 2, 0.05)
central_radar.set_generation(0.6, 0)
central_radar_list.append(central_radar)

def run_graphics ():
    global central_radar_list
    global radar_list
    global unit_list
    global piece_list
    global text_list
    global sprite_list
    global button_list
    global rendering
    global sprite_list, extra_x, extra_y
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
                            new_object.set_generation(unit_object.frequency, unit_object.number_of_generations)
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
        screen.blit(piece.image, [piece.rect[0] + extra_x, piece.rect[1] + extra_y] )
        #Whith the following line it crashes but it says the piece positions
        #piece_of_text = text([piece.position[0], piece.position[1] + 20], str(piece.original_place[0]) + ', ' + str(piece.original_place[1]), 10, text_list, [0, 51, 0])
    for sprite in sprite_list:
        sprite.fade()
        screen.blit(sprite.image, [sprite.rect[0] + extra_x, sprite.rect[1] + extra_y])
    for button_object in button_list:
        button_object.run()
    for piece_of_text in text_list:
        piece_of_text.run()
    
    #clock.tick(100)
    pygame.display.update()
    
def move_arduino (delta_x, delta_y, half):
    global comand_list
    comand = ''
    if delta_x >= 0:
        verse_x = 1
    else:
        verse_x = 0
    if delta_y >= 0:
        verse_y = 1
    else:
        verse_y = 0
    if delta_x != 0:
        if delta_y != 0:
            comand = 8
        else:
            comand = 2
    else:
        if delta_y != 0:
            comand = 6
    if comand != '':
        if half == True:
            comand = comand/2
        comand_list.append([str(comand), str(verse_x), str(verse_y)])
    
def make_move (position, avoid_collisions):
    global arduino_position
    global piece_list
    delta_x = arduino_position[0] - position[0]
    delta_y = arduino_position[1] - position[1]
    #Enable the following to get clues on arduino's movement
    #if (delta_x != 0) or (delta_y != 0):
        #print 'MOVEMENT......'
        #print 'HORIZONTAL ' + str(delta_x * -1)
        #print 'VERTICAL ' + str(delta_y * -1)
        #print '---'
    if abs(delta_x) >= abs(delta_y):
        greater_delta = abs(delta_x)
    else:
        greater_delta = abs(delta_y)
    move_x_count = 0
    move_y_count = 0
    move_x = 0
    move_y = 0
    to_be_done = []
    for i in range(0, greater_delta):
        half = False
        move_x = 0
        move_y = 0
        if (abs(delta_x) - i) > 0:
            if delta_x > 0 :
                move_x = 1
            else:
                move_x = -1
        if (abs(delta_y) - i) > 0:
            if delta_y > 0:
                move_y = 1
            else:
                move_y = -1
        move_x_count += move_x
        move_y_count += move_y
        if avoid_collisions:
            for piece_object in piece_list:
                if piece_object.original_place == [arduino_position[0] - move_x_count, arduino_position[1] - move_y_count]:
                    half = True
                    to_be_done.append([move_x, move_y, True])
        move_arduino(move_x, move_y, half)
    for item in to_be_done:
        move_arduino(item[0], item[1], item[2])
    if avoid_collisions:
        move_arduino(0, 1, True)
        move_arduino(0, -1, True)

def determine_moves (starting_position, ending_position):
    global arduino_position, comand_list
    make_move(starting_position, False)
    arduino_position = starting_position[:]
    comand_list.append(['5', '0', '0'])
    make_move(ending_position, True)
    arduino_position = ending_position[:]
    comand_list.append(['7', '0', '0'])

def place_dead (piece_object):
    global arduino_position, comand_list, unit_list
    for unit_object in unit_list:
        if unit_object.ID == piece_object.ID:
            #unit_object.change_color ([255, 0, 0])
            unit_object.object.color = [255, 0, 0]
    comand_list.append(['5', '0', '0'])
    if piece_object.color == 'White':
        free_place = dead_white_list[0]
        piece_object.set_pos([free_place[0] * 50 + 100, free_place[1]*50 + 100])
        #piece_object.original_place = free_place[:]
        dead_white_list.remove(free_place)
        len_list = len(dead_white_list)
        move_arduino(-1, -1, True)
        for i in range (0, (abs(free_place[1] - piece_object.original_place[1] - 1))):
            #print i
            #print 'piece'
            move_arduino(0, -1, False)
    else:
        free_place = dead_black_list[0]
        #piece_object.original_place = free_place[:]
        piece_object.set_pos([free_place[0] * 50 + 100, free_place[1]*50 + 100])
        dead_black_list.remove(free_place)
        len_list = len(dead_black_list)
        move_arduino(-1, 1, True)
        for i in range (2, (abs(free_place[1] - piece_object.original_place[1] - 1))):
            #print i
            move_arduino(0, 1, False)
    delta_pos = piece_object.original_place[0]-free_place[0]
    piece_object.can_move = False
    for i in range (0, abs(delta_pos)):
        if delta_pos > 0:
            move_arduino(1, 0, False)
        else:
            move_arduino(-1, 0, False)
    if piece_object.color == 'White':
        move_arduino(1, -1, True)
    else:
        move_arduino(1, 1, True)
    move_arduino(1, 0, True)
    move_arduino(-1, 0, True)
    arduino_position = free_place[:]
    piece_object.original_place = free_place[:]
    comand_list.append(['7', '0', '0'])
def place_arrocco (new_place, rook_list, piece_position):
    global arduino_position
    determine_moves (new_place, new_place)
    comand_list.append(['5', '0', '0'])
    move_arduino(-1, -1, True)
    make_move([rook_list[0], rook_list[1]], False)
    arduino_position = rook_list[:]
    move_arduino(1, 1, True)
    comand_list.append(['7', '0', '0'])



def reset_fade ():
    #Unused
    global unit_list
    for unit_object in unit_list:
        unit_object.back_fade = True
def upload_lists(page_number):
    try:
        general_list[0][page_number] = radar_list[:]
        general_list[1][page_number] = unit_list[:]
        general_list[2][page_number] = piece_list[:]
        general_list[3][page_number] = piece_unit_list[:]
        general_list[4][page_number] = text_list[:]
        general_list[5][page_number] = button_list[:]
        general_list[6][page_number] = sprite_list[:]
    except:
        general_list[0].append(radar_list[:])
        general_list[1].append(unit_list[:])
        general_list[2].append(piece_list[:])
        general_list[3].append(piece_unit_list[:])
        general_list[4].append(text_list[:])
        general_list[5].append(button_list[:])
        general_list[6].append(sprite_list[:])
    
def change_lists(page_number):
    global radar_list, unit_list, piece_list, piece_unit_list, text_list, button_list, sprite_list, general_list
    radar_list = general_list[0][page_number][:]
    unit_list = general_list[1][page_number][:]
    piece_list = general_list[2][page_number][:]
    piece_unit_list = general_list[3][page_number][:]
    text_list = general_list[4][page_number][:]
    button_list = general_list[5][page_number][:]
    sprite_list = general_list[6][page_number][:]
    #Graphical refade:
    for object in piece_list:
        object.fade()
        object.alpha = 250
    for sprite in sprite_list:
        sprite.fade()
        sprite.alpha = 250
    for button_object in button_list:
        button_object.fade()
        button_object.alpha = 250
    for piece_of_text in text_list:
        piece_of_text.fade()
        piece_of_text.alpha = 250
    run_graphics()
def empty_lists():
    global radar_list, unit_list, piece_list, piece_unit_list, text_list, button_list, sprite_list, general_list
    radar_list = []
    unit_list = []
    sprite_list = []
    piece_unit_list = []
    piece_list = []
    old_piece_list = []
    text_list = []
    button_list = []

def deploy_move (piece, old_place, new_place, small_movement_string):
    global turn, piece_list, list_of_moves, checkmate, current_radar_pieces
    #print new_place
    capture = ''
    can_move = True
    for piece_value in current_radar_pieces:
        piece_value.enable_radar([255, 255, 255], False, False)
    current_radar_pieces = []
    for piece_object in piece_list:
        if piece_object.original_place == new_place:
            if piece_object.color != piece.color:
                #print piece_object.color
                #print piece_color
                determine_moves(piece_object.original_place, piece_object.original_place)
                place_dead(piece_object)
                piece_object.enable_radar([255, 102, 0], True, False)
                current_radar_pieces.append(piece_object)
                capture = 'x'
            else:
                piece.set_pos([piece.start_pos[0], piece.start_pos[1]])
                new_place = old_place[:]
        if ((piece.type == 'King') and piece.not_moved) and ((piece_object.type == 'Tower') and piece_object.not_moved):
            if (abs(old_place[0] - new_place[0]) >= 2) and (piece.color == piece_object.color):
                #print piece_object.original_place[0]
                #print new_place[0]
                if (piece_object.original_place[0] == (new_place[0] + 1)):
                    rook_list = [new_place[0]-1, new_place[1]]
                    determine_moves(old_place, new_place)
                    place_arrocco(piece_object.original_place, rook_list, piece.position)
                    piece_object.original_place = rook_list
                    piece_object.set_pos([rook_list[0] * 50 + 100, rook_list[1]*50 + 100])
                    print 'RIGHT ARROCCO'
                    can_move = False
                    piece_object.enable_radar([0, 102, 255], True, False)
                    current_radar_pieces.append(piece_object)
                if (piece_object.original_place[0] == (new_place[0] -2)):
                    print 'LEFT ARROCCO'
                    rook_list = [new_place[0]+1, new_place[1]]
                    determine_moves(old_place, new_place)
                    place_arrocco(piece_object.original_place, rook_list, piece.position)
                    piece_object.original_place = rook_list
                    piece_object.set_pos([rook_list[0] * 50 + 100, rook_list[1]*50 + 100])
                    can_move = False
                    piece_object.enable_radar([0, 102, 255], True, False)
                    current_radar_pieces.append(piece_object)
        if (piece.type == 'Pawn') and ((new_place[1]==8) or (new_place[1] == 1)):
            piece.type = 'Queen'
            piece.change_icon()
        #else:
        #    piece.original_place[0] += delta_x
        #    piece.original_place[1] += delta_y
    #if ((piece.unit_type!= 'K') and (piece.unit_type != 'Q')):
    #    movement_string = piece.unit_type + chess_alphabet[old_place[0]] + str(old_place[1]) + capture + chess_alphabet[new_place[0]] + str(new_place[1])
    #else:
    #    movement_string = piece.unit_type + capture + chess_alphabet[new_place[0]] + str(new_place[1])
    if can_move:
        determine_moves(old_place, new_place)
        piece.enable_radar([0, 102, 255], True, False)
        current_radar_pieces.append(piece)
    #print movement_string
    #print board.is_legal(movement_string)
    board.push(chess.Move.from_uci(small_movement_string))
    print chess.Move.from_uci(small_movement_string)
    if board.is_checkmate():
        for piece_object in piece_list:
            if ((piece_object.type == 'King') and (((piece_object.color == 'White') and (turn == 'black')) or ((piece_object.color == 'Black') and (turn == 'white')))):
                piece_object.enable_radar([255, 0, 0], True, True)
                current_radar_pieces.append(piece)
        text([350, 325], 'CHECKMATE', 40, text_list, [255, 102, 0])
        if turn == 'white':
            text([350, 375], 'WHITE WINS', 40, text_list, [255, 102, 0])
        else:
            text([350, 375], 'BLACK WINS', 40, text_list, [255, 102, 0])
        print 'CHECKMATE!'
        checkmate = True
    elif board.is_check():
        for piece_object in piece_list:
            if ((piece_object.type == 'King') and (((piece_object.color == 'White') and (turn == 'black')) or ((piece_object.color == 'Black') and (turn == 'white')))):
                piece_object.enable_radar([255, 0, 0], True, True)
                current_radar_pieces.append(piece)
        print 'CHECK!'
    list_of_moves.append(small_movement_string)
    if turn == 'white':
        turn = 'black'
    else:
        turn = 'white'
    #board.push_san(movement_string)
    #Problem in the following code: to be reseen
    ### 23-08-14 patch: fixed
    piece.not_moved = False
    piece.original_place = new_place[:]
    return True




while True:
    try:
        serial_lenght = arduino.inWaiting()
    except:
        serial_lenght = 0
    if (serial_lenght >= 1) or (first_time == True):
        if comand_list != []:
            arduino.read()
            first_time = False
            arduino.write(str(comand_list[0][0]))
            arduino.write(str(comand_list[0][1]))
            arduino.write(str(comand_list[0][2]))
            comand_list.remove(comand_list[0])
    if len(comand_list) > 0:
        if arduino_in_motion != True:
            arduino_in_motion = True
    else:
        if arduino_in_motion != False:
            arduino_in_motion = False
    if starting:
        if (not rendering) and (not running):
            if not page_one_uploaded:
                image([150, 300], 'python_logo', [150, 150], sprite_list, True, True)
                image([550, 300], 'pygame_logo', [296, 89], sprite_list, False, True)
                image([250, 450], 'arduino_logo', [170, 162], sprite_list, True, True)
                image([450, 450], 'CASA_logo', [216, 216], sprite_list, False, True)
                text([350, 125], '#SEM 2.0', 150, text_list, [0, 102, 255])
                button([350, 650], 'FIND SERIAL', 40, button_list, [0, 102, 255], 'detect_serial', False)
                upload_lists(0)
                page_one_uploaded = True
            else:
                upload_lists(1)
                change_lists(0)
            rendering = True
    for button_object in button_list:
        if (button_object.function == 'detect_serial' or button_object.function == 'retry_detect_serial'):
            if button_object.function_state == True:
                if not port_found:
                    for porty in range (9, 10):
                        try:
                            arduino = serial.Serial(
                                port='COM' + str(porty),\
                                baudrate=9600,\
                                parity=serial.PARITY_NONE,\
                                stopbits=serial.STOPBITS_ONE,\
                                bytesize=serial.EIGHTBITS,\
                                timeout=0,\
                                writeTimeout=0)
                            port_found = True
                            first_time = True
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
                    com_port = 'COM' + str(porty)
                    text([350, 600], 'ARDUINO ON ' + com_port, 30, text_list, [0, 102, 255])
                    button([350, 660], 'CONTINUE', 40, button_list, [0, 102, 255], 'initial_next_button', False)
                else:
                    text([350, 600], 'NO ARDUINO CONNECTION FOUND', 30, text_list, [255, 51, 0])
                    button([250, 660], 'CONTINUE', 40, button_list, [0, 102, 255], 'initial_next_button', False)
                    button([450, 660], 'RETRY', 40, button_list, [255, 102, 0], 'retry_detect_serial', False)
                button_object.remove(button_list)
        if button_object.function == 'initial_next_button':
            if button_object.function_state == True:
                if (not page_two_uploaded) or (button_object.word_text == 'RESET'):
                    board = chess.Bitboard()
                    list_of_moves = []
                    turn = 'white'
                    checkmate = False
                    if not page_two_uploaded:
                        upload_lists(0)
                    for function in function_list:
                        if function[0] == 'AI_player':
                            function[1] = 'off'
                    page_two_uploaded = True
                    determine_moves([0, 0], [0, 0])
                    refresh_dead_lists ()
                    empty_lists()
                    text([350, 35], '#SEM 2.0', 40, text_list, [255, 102, 0])
                    button([225, 660], 'BACK', 40, button_list, [51, 255, 51], 'back_button', False)
                    button([475, 660], 'RESET', 40, button_list, [255, 0, 0], 'initial_next_button', False)
                    settings_button = button([350, 660], 'X', 1, button_list, [0, 102, 255], 'settings_button', False)
                    settings_button.set_image('Settings.png', [51, 51])
                    for i in range (0, 9):
                        image([150 + 50 * i, 350], 'vertical_piece', [3, 500], sprite_list, False, False)
                        image([350, 150 + 50 * i], 'horizontal_piece', [500, 3], sprite_list, False, False)
                        if i != 8:
                            text([175 + 50 * i, 75], alphabet[i], 25, text_list, [0, 102, 255])
                            text([75, 175 + 50 * i], str(i + 1), 25, text_list, [0, 102, 255])
                            positioned_piece = chess_piece([175 + 50 * i, 225], 'White', 'Pawn', piece_list, '')
                            positioned_piece.original_place = [i + 1, 2]
                            positioned_piece = chess_piece([175 + 50 * i, 475], 'Black', 'Pawn', piece_list, '')
                            positioned_piece.original_place = [i + 1, 7]
                    for j in range (0, 2):
                        positioned_piece = chess_piece([175 + 350 * j, 175], 'White', 'Tower', piece_list, 'R')
                        positioned_piece.original_place = [1 + j*7, 1]
                        positioned_piece = chess_piece([175 + 350 * j, 525], 'Black', 'Tower', piece_list, 'R')
                        positioned_piece.original_place = [1 + j*7, 8]
                        positioned_piece = chess_piece([225 + 250 * j, 175], 'White', 'Knight', piece_list, 'N')
                        positioned_piece.original_place = [2 + j*5, 1]
                        positioned_piece = chess_piece([225 + 250 * j, 525], 'Black', 'Knight', piece_list, 'N')
                        positioned_piece.original_place = [2 + j*5, 8]
                        positioned_piece = chess_piece([275 + 150 * j, 175], 'White', 'Bishop', piece_list, 'B')
                        positioned_piece.original_place = [3 + j*3, 1]
                        positioned_piece = chess_piece([275 + 150 * j, 525], 'Black', 'Bishop', piece_list, 'B')
                        positioned_piece.original_place = [3 + j*3, 8]
                    positioned_piece = chess_piece([325, 175], 'White', 'Queen', piece_list, 'Q')
                    positioned_piece.original_place = [4, 1]
                    positioned_piece = chess_piece([325, 525], 'Black', 'Queen', piece_list, 'Q')
                    positioned_piece.original_place = [4, 8]
                    positioned_piece = chess_piece([375, 175], 'White', 'King', piece_list, 'K')
                    positioned_piece.original_place = [5, 1]
                    positioned_piece = chess_piece([375, 525], 'Black', 'King', piece_list, 'K')
                    positioned_piece.original_place = [5, 8]
                else:
                    change_lists(1)
                starting = False
                button_object.function_state = False
        if button_object.function == 'back_button':
            if button_object.function_state == True:
                button_object.function_state = False
                upload_lists(1)
                page_two_uploaded = True
                starting = True
                rendering = False
        if button_object.function == 'settings_button':
            if (button_object.function_state == True) and (not running):
                button_object.function_state = False
                upload_lists(1)
                if not page_three_uploaded:
                    #When changes will be made with buttons: CALL UPLOAD AFTER EVERY CHANGE!!!!
                    page_three_uploaded = True
                    empty_lists()
                    text([350, 50], 'SETTINGS', 50, text_list, [0, 102, 255])
                    text([200, 150], 'ARDUINO AUTOLOCK', 25, text_list, [255, 102, 0])
                    text([200, 250], 'WHITE PLAYER AI', 25, text_list, [255, 102, 0])
                    text([200, 300], 'DIFFICULTY', 20, text_list, [255, 102, 0])
                    text([200, 400], 'BLACK PLAYER AI', 25, text_list, [255, 102, 0])
                    text([200, 450], 'DIFFICULTY', 20, text_list, [255, 102, 0])
                    text([200, 550], 'ARDUINO ON BOARD', 25, text_list, [255, 102, 0])
                    on_button = button([420, 150], 'ON', 25, button_list, [150, 150, 150], 'slider', False)
                    on_button.set_active_color([0, 255, 0])
                    off_button = button([480, 150], 'OFF', 25, button_list, [150, 150, 150], 'slider', False)
                    off_button.set_active_color([255, 0, 0])
                    off_button.bind(on_button, 'arduino_autolock')
                    on_button = button([420, 250], 'ON', 25, button_list, [150, 150, 150], 'slider', False)
                    on_button.set_active_color([0, 255, 0])
                    off_button = button([480, 250], 'OFF', 25, button_list, [150, 150, 150], 'slider', False)
                    off_button.set_active_color([255, 0, 0])
                    off_button.bind(on_button, 'AI_player')
                    on_button = button([420, 400], 'ON', 25, button_list, [150, 150, 150], 'slider', False)
                    on_button.set_active_color([0, 255, 0])
                    off_button = button([480, 400], 'OFF', 25, button_list, [150, 150, 150], 'slider', False)
                    off_button.set_active_color([255, 0, 0])
                    off_button.bind(on_button, 'black_AI')
                    on_button = button([410, 300], 'EASY', 20, button_list, [150, 150, 150], 'slider', False)
                    on_button.set_active_color([0, 255, 0])
                    off_button = button([490, 300], 'HARD', 20, button_list, [150, 150, 150], 'slider', False)
                    off_button.set_active_color([255, 0, 0])
                    off_button.bind(on_button, 'white_AI_difficulty')
                    on_button = button([410, 450], 'EASY', 20, button_list, [150, 150, 150], 'slider', False)
                    on_button.set_active_color([0, 255, 0])
                    off_button = button([490, 450], 'HARD', 20, button_list, [150, 150, 150], 'slider', False)
                    off_button.set_active_color([255, 0, 0])
                    off_button.bind(on_button, 'black_AI_difficulty')
                    for i in range (0, 1):
                        text([200, 575 + (i*100)], 'COMING SOON', 10, text_list, [255, 0, 0])
                        button([420, 550 + (i*100)], 'ON', 25, button_list, [150, 150, 150], 'blob', False)
                        button([480, 550 + (i*100)], 'OFF', 25, button_list, [150, 150, 150], 'blob', False)
                    button([350, 660], 'BACK', 40, button_list, [51, 255, 51], 'initial_next_button', False)
                    upload_lists(3)
                else:
                    change_lists(2)
        if button_object.function == 'slider':
            if button_object.function_state == True:
                button_object.function_state = False
                button_object.slider_state = True
                button_object.switch()
                upload_lists(3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            determine_moves([0, 0], [0, 0])
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
                pos_x -= + extra_x
                pos_y -= + extra_y
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
                            if piece_list[i].can_move:
                                piece_moving = True
                                piece_ID = piece_list[i].ID
                                starting_position = [pos_x, pos_y]
                                #for unit_object in unit_list:
                                    #if unit_object.ID == piece_list[i].ID:
                                radar_object = radar(piece_list[i].rect.height/2 + piece_list[i].rect.left, piece_list[i].rect.width/2 + piece_list[i].rect.top, [255, 255, 0], 50, 2, 0.09)
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
            ended_properly = False
            for function in function_list:
                if function[0] == 'AI_player':
                    AI_state = function[1]
                if function[0] == 'black_AI':
                    black_AI_state = function[1]
            for piece in piece_list:
                if piece_ID == piece.ID:
                    for function in function_list:
                        if function[0] == 'arduino_autolock':
                            if (function[1] == 'off') or ((function[1] == 'on') and (len(comand_list) == 0)):
                                piece.set_moving(False)
                                to_be_removed = []
                                if (pos_x >= 150 and pos_x <= 550):
                                    if (pos_y >= 150 and pos_y <= 550):
                                        if ((turn == 'black') and (black_AI_state == 'off')) or ((turn == 'white') and (AI_state == 'off')):
                                            if ((piece.color == 'Black') and (black_AI_state == 'off')) or ((piece.color == 'White') and (AI_state == 'off')):
                                                piece.set_pos([int(pos_x/50)*50, int(pos_y/50)*50])
                                                delta_x = int((pos_x - piece.start_pos[0])/50)
                                                delta_y = int((pos_y - piece.start_pos[1])/50)
                                                old_place = piece.original_place[:]
                                                new_place = [old_place[0] + delta_x, old_place[1] + delta_y]
                                                small_movement_string = chess_alphabet[old_place[0]] + str(old_place[1]) + chess_alphabet[new_place[0]] + str(new_place[1])
                                                if chess.Move.from_uci(small_movement_string) in board.legal_moves:
                                                    ended_properly = deploy_move (piece, old_place, new_place, small_movement_string)
                                for i in range (0, len(radar_list)):
                                    if radar_list[i].ID == piece.ID:
                                        #del radar_list[i-difference]
                                        #difference += 1
                                        radar_list[i].set_generation(1, -1)
                                        if ended_properly:
                                            radar_list[i].set_position((new_place[0]*50 + 125), (new_place[1]*50 + 125))
                    if not ended_properly:
                        piece.set_pos([piece.start_pos[0], piece.start_pos[1]])
                        radar_list[i].set_position((piece.start_pos[0]*50 + 125), (piece.start_pos[1]*50 + 125))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            comand_list = []
            arduino_position = [0,0]
            #position_x = random.randint (0, 600)
            #position_y = random.randint (0, 600)
            #position_m = (position_x + position_y)/2
            #width = random.randint(1, 5)
            #radius = random.randint(5, position_m)
            #speed = random.randint(1, 99) / 100.0
            #object = radar(position_x, position_y, THECOLORS[random.choice(THECOLORS.keys())],  radius, width, speed)
            #radar_list.append(object)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            determine_moves([-1, 0], [-1, 0])
            arduino_position = [0, 0]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            determine_moves([0, -1], [0, -1])
            arduino_position = [0, 0]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_DELETE:
            unit_list = []
            radar_list = []
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_F5:
            window_fullscreen = True
            pygame.init()
            determine_ratio ()
            screen = pygame.display.set_mode([full_screen_width, full_screen_height], FULLSCREEN)
        elif event.type == pygame.KEYDOWN and ((event.key == pygame.K_F4) or (event.key == pygame.K_ESCAPE)):
            window_fullscreen = False
            pygame.init()
            determine_ratio ()
            pygame.display.set_caption('#SEM 2.0.11')
            screen = pygame.display.set_mode([700, 700])
    run_graphics ()
    run_AI()



