import curses
import os
import sys
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import Terminal256Formatter
#from pygments.formatters import BBCodeFormatter

lexer = get_lexer_by_name("javascript", stripall=True)
formatter = Terminal256Formatter(cssclass="source")

screen = curses.initscr()
curses.start_color()
curses.use_default_colors()

forground = 0
background = curses.COLORS - 1
print curses.COLORS

curses.init_pair(1, forground, background)

reset_char = '\x1b[39;49;00m'


def print_escaped(x, y, formatted_string):

    forground = 0
    background = curses.COLORS - 1


    screen.move(0,0)
    tokens = re.split("(\x1b\[[^m]+m)", formatted_string)
    #tokens = re.split("(\x1b)", formatted_string)
    for token in tokens:
        if (re.match("^\x1b\[39;49;00m", token) or re.match("^\x1b\[39m", token)):
            screen.attroff(curses.color_pair(1));
            screen.addstr(repr(token))
        elif re.match("^\x1b", token):
            screen.addstr(repr(token) + " ")
            color_tokens = token.split(";");
            #color = re.sub("[^0-9]", "", color_tokens[2]);
            background = background - 20;
            forground = forground + 20;
            i = 0;
            for color in color_tokens:
                screen.addstr(str(i) + " " +  color + " ");
                i = i + 1
            #curses.init_pair(1,int(color),background)
            screen.attron(curses.color_pair(1))
        else:
            screen.addstr(token);
    #print 'ls\r\n\x1b[00m\x1b[01;31mexamplefile.zip\x1b[00m\r\n\x1b[01;31m'


ESCAPE_CHAR = '\x1b'
START_SEQUENCE = '['
PARAM_SEPERATOR = ';'
END_COMMAND = 'm'

RESET = 0
BOLD = 1
FAINT = 2
ITALIC = 3
UNDERLINE_SINGLE = 4
BLINK_SLOW = 5
BLINK_RAPID = 6
INVERSE = 7
CONCEAL = 8
CROSSED_OUT = 9
DEFAULT_FONT = 10
#FONTS 11 - 20, IGNORE for now
UNDERLINE_DOUBLE = 21
NORMAL_INTENSITY = 23

SET_FORGROUND_BLACK = 30
SET_FORGROUND_RED = 31
SET_FORGROUND_GREEN = 32
SET_FORGROUND_YELLOW = 33
SET_FORGROUND_BLUE = 34
SET_FORGROUND_MAGENETA = 35
SET_FORGROUND_CYAN = 36
SET_FORGROUND_GRAY = 37
SET_FORGROUND_EXTENDED = 38

SET_BACKGROUND_BLACK = 40
SET_BACKGROUND_RED = 41
SET_BACKGROUND_GREEN = 42
SET_BACKGROUND_YELLOW = 43
SET_BACKGROUND_BLUE = 44
SET_BACKGROUND_MAGENETA = 45
SET_BACKGROUND_CYAN = 46
SET_BACKGROUND_GRAY = 47
SET_BACKGROUND_EXTENDED = 48

def set_forground_black(token):
    screen.addstr('[BLACKFG]')


commands = {
        SET_FORGROUND_BLACK : set_forground_black
}


#
# In an escape sequence we can help
#

def escape_located(string):
    done = False
    i = 0
    while not done:
        c = string[i]
        i = i + 1;
        if( c == START_SEQUENCE ):
            screen.addstr('[bracket]')
            #read_command(string[i:])
        done = True
    return i

#
# Reads the commands from the escape sequence
#   params are seperated by ';' and ended with 'm'
#
def read_command(string):
    done = False
    i = 0
    command = ""
    while not done:
        c = string[i]
        i = i + 1;
        #Act on this command and read next
        if(c == PARAM_SEPERATOR):
            i = i + commands[int(command)](string[i:])
            i = i + read_command(string[i:])
        #Act on this command and finish up
        elif(c == END_COMMAND):
            i = i + commands[int(command)](string[i:])
            done = True;
            return i
        else:
            command = command + c

#def do_command(command_code):


def print_escaped(formatted_string):
    screen.move(0,0)
    done = False
    i = 0
    while not done:
        c = formatted_string[i];
        i = i + 1;
        if ( c == ESCAPE_CHAR ):
            screen.addstr('[escape char]')
            i = i + escape_located(formatted_string[i:])
        else :
            screen.addstr(c);
        if ( i >= len(formatted_string)): done = True


string = ""
while True:
    result = highlight(string, lexer, formatter)
    print_escaped(result)
    c = screen.getkey()
    string += c;

curses.endwin()




