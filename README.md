# #SEM2.0
A fully automated electromagnetic chessboard. <br>
You can play chess on our laptop and the pieces get moved for you on the board. <br>

## Arduino

We used an Arduino Uno Board with 2 Stepper Motors and a Electromagnet. <br>
The actual chessboard was made out of wood with a few lego components. <br>
Chess pieces were handmade and fitted with a neodymium magnet underneath.

[![#SEM2.0 VIDEO](http://imgur.com/R7D9JGt.png)](https://vimeo.com/140035967)

## Python

### Dependencies
- `PySerial`: Allows us to communicate to the Ardduino board via a serial port.
- `PyGame`: Used to render all graphical components onto the screen.
- `Stockfish`: Used as the main Chess Engine.
- `PyChess`: Used to validate moves executed by human players.
- `Python 2.7`: As the PyChess packages were only available for 2.7 we could not upgrade to Python 3.

### The Program

The main program is written in Python 2.7 and uses Pygame as a Graphic's Engine. <br>
Version `2.0.12-Works` has all dependencies disabled and solely relies on Python 2.7 and Pygame to be installed. <br>
Version `2.0.12` will instead require PySerial, PyChess and the Stockfish API.

![#SEM2.0 Home View](http://imgur.com/pljwsBh.gif)

![#SEM2.0 Chess View](http://imgur.com/3R1Fge1.gif)

![#SEM2.0 Options View](http://imgur.com/PE0clPs.gif)
