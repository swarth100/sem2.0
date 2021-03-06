import pygame, sys
from pygame.locals import *

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

choice = 1

machine_x = 65
machine_y = 65
right_lenght = 0
left_lenght = 0
max_right = 450
max_left = 450

up_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 5, 40, 40], 0)
left_arrow = pygame.draw.rect(screen, [0, 0, 255], [5, 280, 40, 40], 0)
right_arrow = pygame.draw.rect(screen, [0, 0, 255], [555, 280, 40, 40], 0)
bot_arrow = pygame.draw.rect(screen, [0, 0, 255], [280, 555, 40, 40], 0)

chess_positions = []

#CAMBIARE LA PORTA COM A SECONDA DI DOVE SI TROVI ARDUINO!!!
try:
    import serial
    arduino = serial.Serial("COM9", 9600)
    choice = 0
except:
    python = open('arduino_file.txt', 'w')
    python.close() 
    choice = 1   

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
        if programm == '0':
            nothing = True
            arduino_command_1 = arduino.readline()
            arduino_command_2 = arduino.readline()
            arduino_command_3 = arduino.readline()
            return [programm, arduino_command_1, arduino_command_2, arduino_command_3]
    except:
        python = open('arduino_file.txt', 'r')
        programm = python.readline()
        if programm == '0':
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
        arduino.write(str(programm))
        arduino.write(str(command))
        arduino.write(str(second_command))
        arduino.write(str(third_command))
    except:
        python = open('arduino_file.txt', 'w')
        python.write(programm + '\n')
        python.write(command + '\n')
        python.write(second_command + '\n')
        python.write(third_command)
        python.close() 

def deploy_machine ():
    global machine_x, machine_y, right_lenght, left_lenght
    chessboard_background ()
    pygame.draw.rect(screen, [255, 0, 0] ,[(machine_x)*450/right_lenght + 9, 50 , 2, 500], 0)
    pygame.draw.rect(screen, [255, 0, 0] ,[50, (machine_y)*450/left_lenght + 9 , 500, 2], 0)
    pygame.draw.rect(screen, [0, 0, 0] ,[(machine_x)*450/right_lenght, (machine_y)*450/left_lenght , 20, 20], 0)
    pygame.display.update ()
    
def elaborate_arduino ():
    global machine_x, machine_y, right_lenght, left_lenght
    if choice == 1:
        command_list = get_command()
        if command_list[0] == '0':
            python_command_1 = command_list[1]
            python_command_2 = command_list[2]
            python_command_3 = command_list[3]
            if python_command_1 == '0':
                movement = int(python_command_3)
                if python_command_2 == '0':
                    movement = int(python_command_3)
                else:
                    movement = movement * -1
                machine_x += movement
                if machine_x >= 65 + max_right:
                    print_command ('2', '', '', '0')
                elif machine_x <= 65:
                    print_command (4, '', '', 0)
                else:
                    print_command (6, '', '', 0)
            if python_command_1 == '/move_left\n':
                movement = int(python_command_3)
                if python_command_2 == 'clockwise\n':
                    movement = int(python_command_3)
                else:
                    movement = movement * -1
                machine_y += movement
                if machine_y >= 65 + max_left:
                    print_command (3, '', '', 0)
                elif machine_y <= 65:
                    print_command (5, '', '', 0)
                else:
                    print_command (7, '', '', 0)

def elaborate_chess_positions (x_lenght, y_lenght):
    global chess_positions
    for i in range (0, 10):
        row_list = []
        for j in range (0, 10):
            row_list.append([((x_lenght/9) *j), ((y_lenght/9)*i)])
        chess_positions.append(row_list)
        
        
    
def main ():
    import pygame
    
    global screen, arduino, python, choice, machine_x, machine_y, right_lenght, left_lenght, max_right, max_left
    global up_arrow, left_arrow, right_arrow, bot_arrow, chess_positions
    
    moving_right = False 
    moving_left = False
    calibrating = True
    buttons_enabled = False
    calibrating_right = True
    
    chessboard_background ()
    
    print_command (0, 0, '1', 1)
    right_lenght += 1
    
    #chee_positions = [[(prima fila)[x, y], [x2, y2], ...], [(seconda_fila)[x, y], [x1, y1], ...]]
    chess_positions = []
    current_position = [0, 0]
    
    while True:
        if not calibrating:
            deploy_machine ()
        command = get_command ()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit ()
            if event.type == MOUSEBUTTONDOWN:
                command_list = get_command()
                (pos_x, pos_y) = pygame.mouse.get_pos()
                if up_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        print command_list
                        if current_position[1] >= 1:
                            current_position[1] -= 1
                            print_command (1, 1, '0', 1)
                            elaborate_arduino ()
                            if command_list[1] != '5':
                                try:
                                    movement = chess_positions[current_position[0]][current_position[1] + 1][0] - chess_positions[current_position[0]][current_position[1]][0]
                                except:
                                    movement = chess_positions[current_position[0]][current_position[1]][0] - chess_positions[current_position[0]][current_position[1] - 1][0]
                                print_command (1, 1, str(movement), 1)
                                elaborate_arduino ()
                        deploy_machine ()
                elif left_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        print command_list
                        if current_position[0] >= 1:
                            current_position[0] -= 1
                            print_command (0, 1, '0', 1)
                            elaborate_arduino ()
                            if command_list[1] != '4':
                                try:
                                    movement = chess_positions[current_position[0] + 1][current_position[1]][1] - chess_positions[current_position[0]][current_position[1]][1]
                                except:
                                    movement = chess_positions[current_position[0]][current_position[1]][1] - chess_positions[current_position[0] - 1][current_position[1]][1]
                                print_command (0, 1, str(movement), 1)
                                elaborate_arduino ()
                        deploy_machine ()
                elif right_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        print command_list
                        if current_position[0] <= 8:
                            current_position[0] += 1
                            print_command (0, 0, '0', 1)
                            elaborate_arduino ()
                            if command_list[1] != '2':
                                try:
                                    movement = chess_positions[current_position[0] + 1][current_position[1]][1] - chess_positions[current_position[0]][current_position[1]][1]
                                except:
                                    movement = chess_positions[current_position[0]][current_position[1]][1] - chess_positions[current_position[0] - 1][current_position[1]][1]
                                print_command (0, 0, str(movement), 1)
                                elaborate_arduino ()
                        deploy_machine ()
                elif bot_arrow.collidepoint (pos_x, pos_y):
                    if buttons_enabled:
                        print command_list
                        if current_position[1] <= 8:
                            current_position[1] += 1
                            print_command (1, 0, '0', 1)
                            elaborate_arduino ()
                            if command_list[1] != '3':
                                try:
                                    movement = chess_positions[current_position[0]][current_position[1] + 1][0] - chess_positions[current_position[0]][current_position[1]][0]
                                except:
                                    movement = chess_positions[current_position[0]][current_position[1]][0] - chess_positions[current_position[0]][current_position[1] - 1][0]
                                print_command (1, 0, str(movement), 1)
                                elaborate_arduino ()
                        deploy_machine ()
        if calibrating:
            if calibrating_right:
                command_list = get_command()
                if command_list[0] == 0:
                    if command_list[1] == '6':
                        print_command (0, 0, '1', 1)
                        right_lenght += 1
                    if command_list[1] == '2':
                        calibrating_right = False
                        print_command (1, 0, '1', 1)
                        left_lenght += 1
                        print 'Horizontal lenght ' + str(right_lenght)
                        max_right = right_lenght
            else:
                command_list = get_command()
                if command_list[0] == 0:
                    if command_list[1] == 7:
                        print_command (1, 0, '1', 1)
                        left_lenght += 1
                    if command_list[1] == 3:
                        calibrating = False
                        calibrating_right = True
                        print 'Vertical lenght ' + str(left_lenght)
                        buttons_enabled = True
                        elaborate_chess_positions (right_lenght, left_lenght)
                        print_command (0, 1, str(right_lenght), 1)
                        elaborate_arduino ()
                        print_command (1, 1, str(left_lenght), 1)
                        elaborate_arduino ()
                        max_left = left_lenght
                        
        elaborate_arduino ()
                
        pygame.display.update ()
        
        
        

#try:

main ()
#except:
    
    
