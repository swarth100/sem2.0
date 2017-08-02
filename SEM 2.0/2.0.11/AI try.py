import subprocess, time

engine = subprocess.Popen(
    'C:\Python27\stockfish-5-win\stockfish-5-win\Windows\stockfish_14053109_32bit',
    universal_newlines=True,
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
)

def put(command):
    print('\nyou:\n\t'+command)
    engine.stdin.write(command+'\n')

def get():
    # using the 'isready' command (engine has to answer 'readyok')
    # to indicate current last line of stdout
    engine.stdin.write('isready\n')
    print('\nengine:')
    while True:
        text = engine.stdout.readline().strip()
        if text == 'readyok':
            break
        if text !='':
            print('\t'+text)

get()
put('uci')
get()
put('setoption name Hash value 128')
get()
put('ucinewgame')
get()
put('position startpos moves e2e4 e7e5 f2f4')
get()
put('go infinite')
time.sleep(3)
get()
put('stop')
get()
put('quit')
time.sleep(10)