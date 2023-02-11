import os
import sys
from enum import Enum
from enum import IntEnum

class Test(Enum):
    '''Test by searching local project directory'''
    local = "local"
    '''Test by searching from the disk root (this will be slow!)'''
    root = "root"
    '''Disable testing, will get the user's home directory as search path'''
    off = "off"

TEST = Test.root

class Command(Enum):
    file = "file"
    directory = "directory"
    all = "all"

class ItemType(IntEnum):
    directory = 0
    file = 1

def get_proj_root():
    '''Returns the root path for the project (e.g. containing src, test, etc.)'''
    # Gets the root directory assuming search.py will be within src
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def get_root():
    path = sys.executable
    while os.path.split(path)[1]:
        path = os.path.split(path)[0]
    return path

def get_search_paths():
    '''Returns the root directory to search from'''
    if TEST == Test.local:
        return os.sep.join([get_proj_root(), "test", "test-fs"])
    elif TEST == Test.root:
        return [get_root(), 'E:\\\\']
    elif TEST == Test.off:
        # This will return the user's home directory (e.g. C:\\Users\name on
        # Windows and /Users/name on macOS.)
        return os.path.expanduser("~")
    else:
        raise Exception("Invalid testing option.")

def get_command():
    '''This function ask the user a command'''
    while True:
        command = input("Enter a valid command or 'q' to exit the program: ")
        
        if command == 'q' or command == 'Q':
            return 'q', None
        
        command_split = command.split(' ')
        command_str = command_split[0]
        del command_split[0]
        query = ' '.join(command_split)
        try:
            command = Command(command_str)
            break
        except ValueError:
            print("Incorrect command: %s" % command_str)
    
    return command, query    




