import os
from sys import platform
from time import time
from utils import *
from index import *
import threading

class Search:
    
    MAX_RESULTS = 50
    
    def __init__(self):
        self.index = Index()
    
    def print_paths(self, data):
        '''This method prints the paths to the files and directories that the method
        run_search() found.'''
        for paths in data:
            for path in paths:
                print(path)
    
    def prepare(self):
        '''Prepares for the search to happen'''
        self.index.start_db()
        self.start_search()
        
    
    def start_search(self):
        command, query = get_command()
        while command != 'q':
            start_time = time()
            self.print_paths(self.index.run_search(command, query.replace("*", "%")))
            print('Search took %.3f secs.' % (time() - start_time))
            command, query = get_command()

