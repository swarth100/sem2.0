import pygame, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

choice = 'python'

machine_x = 65
machine_y = 65

up_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 5, 40, 40], 0)
left_arrow = pygame.draw.rect(screen, [0, 0, 255], [5, 280, 40, 40], 0)
right_arrow = pygame.draw.rect(screen, [0, 0, 255], [555, 280, 40, 40], 0)
bot_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 555, 40, 40], 0)

try:
    import serial
    arduino = serial.Serial("COM8", 9600)
    choice = 'arduino'
except:
    python = open('arduino_file.txt', 'w')
    python.close() 
    choice = 'python'   

def chessboard_background ():
    for x in range (0, 12):
        for y in range (0, 12):
            if (y == 0) or (y == 11):
                color = [204, 51, 0]
                border_color = [204, 51, 0]
            elif (x == 0) or (x == 11):
                if (y == 0) or (y == 11):
                    color = [204, 51, 0]
                    border_color = [204, 51, 0]
            elif ((x / 2.0) == int(x / 2)):
                if (y / 2.0) == int(y / 2):
                    color = [50, 50, 50]
                else:
                    color = [200, 200, 200]
                border_color = [0, 0, 0]
            else:
                if (y / 2.0) == int(y / 2):
                    color = [200, 200, 200]
                else:
                    color = [50, 50, 50]
                border_color = [0, 0, 0]
            pygame.draw.rect(screen, color, [x*50, y*50, 50, 50], 0)
            pygame.draw.rect(screen, border_color, [x*50, y*50, 50, 50], 1)
    pygame.draw.rect(screen, [0, 0, 0], [0, 0, 600, 600], 1)
    up_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 5, 40, 40], 0)
    left_arrow = pygame.draw.rect(screen, [0, 0, 255], [5, 280, 40, 40], 0)
    right_arrow = pygame.draw.rect(screen, [0, 0, 255], [555, 280, 40, 40], 0)
    bot_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 555, 40, 40], 0)
        
def get_command():
    global arduino, python
    try:
        programm = arduino.readline ()
        if programm == 'arduino':
            nothing = True
            #
            #Here attach arduino inputs
            #
    except:
        python = open('arduino_file.txt', 'r')
        programm = python.readline()
        if programm == 'arduino\n':
            arduino_command_1 = python.readline()
            arduino_command_2 = python.readline()
            arduino_command_3 = python.readline()
            return [programm, arduino_command_1, arduino_command_2, arduino_command_3]
        elif programm == 'python\n':
            python_command_1 = python.readline()
            python_command_2 = python.readline()
            python_command_3 = python.readline()
            return [programm, python_command_1, python_command_2, python_command_3]
        python.close() 

def print_command (command, second_command, third_command, programm):
    global arduino, python
    try:
        arduino.write(programm + '\n')
        arduino.write(command + '\n')
        arduino.write(second_command + '\n')
        arduino.write(third_command)
    except:
        python = open('arduino_file.txt', 'w')
        python.write(programm + '\n')
        python.write(command + '\n')
        python.write(second_command + '\n')
        python.write(third_command)
        python.close() 

def deploy_machine ():
    global machine_x, machine_y
    chessboard_background ()
    pygame.draw.rect(screen, [255, 0, 0] ,[machine_x + 9, 50 , 2, 500], 0)
    pygame.draw.rect(screen, [255, 0, 0] ,[50, machine_y + 9 , 500, 2], 0)
    pygame.draw.rect(screen, [0, 0, 0] ,[machine_x, machine_y , 20, 20], 0)
    pygame.display.update ()
        
    
def main ():
    import pygame
    
    global screen, arduino, python, choice, machine_x, machine_y
    global up_arrow, left_arrow, right_arrow, bot_arrow
    
    moving_right = False 
    moving_left = False
    calibrating = True
    buttons_enabled = False
    calibrating_right = True
    
    chessboard_background ()
    
    right_lenght = 0
    left_lenght = 0
    
    print_command ('/move_right', 'clockwise', '10', 'python')
    
    while True:
        deploy_machine ()
        command = get_command ()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit ()
            if event.type == MOUSEBUTTONDOWN:
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if up_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        machine_y -= (left_lenght/9)
                        if machine_y <= 65:
                            machine_y = 65
                        deploy_machine ()
                elif left_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        machine_x -= (right_lenght/9)
                        if machine_x <= 65:
                            machine_x = 65
                        deploy_machine ()
                elif right_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        machine_x += (right_lenght/9)
                        if machine_x >= 515:
                            machine_x = 515
                        deploy_machine ()
                elif bot_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        machine_y += (left_lenght/9)
                        if machine_y >= 515:
                            machine_y = 515
                        deploy_machine ()
        if calibrating:
            if calibrating_right:
                command_list = get_command()
                if command_list[0] == 'arduino\n':
                    if command_list[1] == '/stopped_right\n':
                        print_command ('/move_right', 'clockwise', '1', 'python')
                        right_lenght += 1
                    if command_list[1] == '/end_right\n':
                        calibrating_right = False
                        print_command ('/move_left', 'clockwise', '10', 'python')
                        print 'Horizontal lenght ' + str(right_lenght)
            else:
                command_list = get_command()
                if command_list[0] == 'arduino\n':
                    if command_list[1] == '/stopped_left\n':
                        print_command ('/move_left', 'clockwise', '1', 'python')
                        left_lenght += 1
                    if command_list[1] == '/end_left\n':
                        calibrating = False
                        calibrating_right = True
                        print 'Vertical lenght ' + str(left_lenght)
                        buttons_enabled = True
                
        
        if choice == 'python':
            command_list = get_command()
            if command_list[0] == 'python\n':
                python_command_1 = command_list[1]
                python_command_2 = command_list[2]
                python_command_3 = command_list[3]
                if python_command_1 == '/move_right\n':
                    if python_command_2 == 'clockwise\n':
                        movement = int(python_command_3)
                    else:
                        movement = movement * -1
                    machine_x += movement
                    if machine_x >= 515:
                        print_command ('/end_right', '', '', 'arduino')
                    else:
                        print_command ('/stopped_right', '', '', 'arduino')
                if python_command_1 == '/move_left\n':
                    if python_command_2 == 'clockwise\n':
                        movement = int(python_command_3)
                    else:
                        movement = movement * -1
                    machine_y += movement
                    if machine_y >= 515:
                        print_command ('/end_left', '', '', 'arduino')
                    else:
                        print_command ('/stopped_left', '', '', 'arduino')
                
        pygame.display.update ()
        
        
        

#try:

main ()
#except:
    
    
