import serial
import pygame

pygame.init()
pygame.display.set_caption('ARDUINO-PROJECT')
screen = pygame.display.set_mode([1000, 600])
screen.fill ([255, 255, 255])

arduino = serial.Serial(
    port='COM9',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
choice = 'arduino'
command = 0
verse = 0
author = 2
arduino_command = 0
ending_command = 0

print 'Press 1 and then ENTER to rotate dx motor clockwise'
print 'Now add light to photoresistor A0'
print 'The motor will stop and change direction, it stores the max dx lenght'

def arduino_print():
    global command, verse
    arduino.write('0')
    arduino.write(str(command))
    arduino.write(str(verse))

def arduino_read ():
    global arduino_command, author, ending_command
    serial_lenght = arduino.inWaiting()
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
            arduino_print()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            command = 0
            verse = 0
        #elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            #command = 1
            #verse = 0
    if author == '1':
        if arduino_command == '4':
            if ending_command == '0':
                command = 0
                verse = 1
                arduino_print()
                author = ''
                arduino_command = ''
                ending_command = ''
            elif ending_command == '1':
                command = 0
                verse = 0
                author = ''
                arduino_command = ''
                ending_command = ''
                arduino_print()
    arduino_read ()
    pygame.display.update ()


