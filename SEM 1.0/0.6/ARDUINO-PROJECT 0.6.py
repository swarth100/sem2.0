import serial
import pygame

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

try:
    arduino = serial.Serial(
        port='COM9',\
        baudrate=9600,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE,\
        bytesize=serial.EIGHTBITS,\
            timeout=0)
except:
    print 'ERROR OPENING SERIAL!!!!'
    print 'ERROR'
    print 'ERROR'
    arduino = open('arduino.txt', 'w')
choice = 'arduino'
command = 0
verse = 0
author = 2
arduino_command = 0
ending_command = 0
position = [0, 0]
calibrating = False
calibrating_done = False
arduino_done_step = False

arduino.write('2')
arduino.write('0')
arduino.write('0')

#COMMANDS:
#Sender == Python (0):
#   0: Rotate right motor for INFINITY
#   1: Rotate right motor for ONE STEP
#   2: Rotate left motor for INFINITY
#   3: Rotate left motor for ONE STEP
#   4: Get back to 0,0
#Sender == ARDUINO (1):
#   0: A0 Photoresistor hit by right motor
#   1: A1 Photoresistor hit by right motor
#   2: Right motor DONE 1 STEP
#   3: A2 Photoresistor hit by left motor
#   4: A3 Photoresistor hit by left motor
#   5: Left motor DONE 1 STEP

print 'Calibration DEVICE!'
print 'Press 1to start Calibration then give light to A0 PHOTORESISTOR'
print 'The motor changes direction, Arduino saves its total number of turns, Arduino changes direction'
print 'Now give light to A1 PHOTORESISTOR, Arduino will stop definitely and calculate (as a mean) the total steps for each cell'
print 'Use key 2 to make arduino make one pace CLOCKWISE, Use key 3 to make one pace ANTICLOCKWISE'

def arduino_print():
    global command, verse
    arduino.write('0')
    arduino.write(str(command))
    arduino.write(str(verse))

def arduino_read ():
    global arduino_command, author, ending_command
    try:
        serial_lenght = arduino.inWaiting()
    except:
        serial_lenght = 0
    if serial_lenght >= 3:
        author = arduino.read()
        arduino_command = arduino.read()
        ending_command = arduino.read()
        if author == '0':
            arduino.write('0')
            arduino.write(arduino_command)
            arduino.write(ending_command)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit ()
        elif event.type == pygame.KEYDOWN and event.key== pygame.K_RETURN:
            #arduino_print()
            nothing = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            print '__CALIBRATING__'
            calibrating = True
            command = 0
            verse = 0
            arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            if calibrating_done:
                if position[0] <= 8:
                    if arduino_done_step:
                        print '__ONE__STEP__CLOCKWISE__'
                        position[0] += 1
                        command = 1
                        verse = 0
                        arduino_done_step = False
                        arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            if calibrating_done:
                if position[0] >= 1:
                    if arduino_done_step:
                        print '__ONE__STEP__ANTICLOCKWISE__'
                        position[0] -= 1
                        command = 1
                        verse = 1
                        arduino_done_step = False
                        arduino_print()
    if author == '1':
        if arduino_command == '0':
            if ending_command == '0':
                if calibrating:
                    command = 0
                    verse = 1
                    arduino_print()
                    calibrating = False
                else:
                    print '__HIT__A0__'
        elif arduino_command == '1':
            if ending_command == '1':
                if calibrating_done == False:
                    print '__CALIBRATING__DONE__'
                    calibrating_done = True
                    arduino_done_step = True
                else:
                    print '__HIT__A1__'
        elif arduino_command == '2':
            print '__STEP__DONE__'
            arduino_done_step = True
        author = ''
        arduino_command = ''
        ending_command = ''
    arduino_read ()
    pygame.display.update ()


