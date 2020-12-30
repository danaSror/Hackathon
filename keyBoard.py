import sys
import termios
import atexit
from select import select

class Keyboard:

    def __init__(self):  
        self.new_terminal_settings = termios.tcgetattr(sys.stdin.fileno())
        self.old_terminal_settings  = termios.tcgetattr(sys.stdin.fileno())

        self.new_terminal_settings[3] = (self.new_terminal_settings[3] & ~termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self.new_terminal_settings)

        atexit.register(self.set_terminal_to_normal) # reset, exit

    # Change the terminal to normal
    def set_terminal_to_normal(self):
        termios.tcsetattr(sys.stdin.fileno(), termios.TCSAFLUSH, self.old_terminal_settings)

    # When char press on keyboard
    def get_char(self):
        s = ''
        return sys.stdin.read(1)


    def get_arrow(self):
        # return the value when the key is press is an arrow
        # 0-up | 1-right | 2-down | 3-left
        c = sys.stdin.read(3)[2]
        vals = [65, 67, 66, 68]
        return vals.index(ord(c.decode('utf-8')))


    def is_press(self):
        # return if key press or not
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []