import sqlite3
import os
import errno
from time import time
from utils import *

class Index:
    
    MAX_RESULTS = 50
    
    def __init__(self):
        data_dir = os.path.join(get_proj_root(), "data")
        try:
            os.makedirs(data_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        self.con =  sqlite3.connect(os.path.join(data_dir, 'index.sqlite'))
        self.cursor = self.con.cursor()
    
    def start_db(self):
        # Fetch all table names to determine if the table is created
        self.cursor.execute('SELECT name FROM sqlite_master WHERE type= "table"')
        tables = self.cursor.fetchall()
        
        if len(tables) == 0:
            print(4)
            self.cursor.execute("CREATE TABLE IF NOT EXISTS search(name text, path text, type integer, rank integer)")
            self.cursor.execute("CREATE INDEX filename_index ON search(name)")
            self.index()
    
    def rank(self, path):
        root = os.path.expanduser("~")
        if path.find(root) != -1:
            return 1
        return 0    
        

    def index(self):
        '''This function save the paths of the files and directories in the database.'''
        print(2)
        start_time = time()
        print("Indexing...")
        paths = get_search_paths()
        for path in paths:
            for (dirpath, dirnames, filenames) in os.walk(path):
                for dirname in dirnames:
                    try:
                        rank = self.rank(dirpath)
                        self.cursor.execute("INSERT INTO search(name, path, type, rank) VALUES('%s', '%s', '%i', '%i')" % \
                                            (dirname, dirpath, ItemType.directory, rank))
                    except BaseException:
                        print('Error: unable to index:', dirpath)
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    try:
                        rank = self.rank(filepath)
                        self.cursor.execute("INSERT INTO search(name, path, type, rank) VALUES('%s', '%s', '%i', '%i')" % \
                                            (filename, filepath, ItemType.file, rank))
                    except BaseException:
                        print('Error: unable to index:', filepath)
        
        print('Indexing took %.3f secs.' % (time() - start_time))               
        self.con.commit()
    
    def splat(self, names):
        '''This function unpacks the elements from the list 'names' and returns them.'''
        elements = []
        
        for row in names:
            name, = row
            elements.append(name)
        return elements
            
        
    
    def run_search(self, command, query):
        '''This function returns the path to the files and directories that exist in the database.'''         
        data = []
            
        if command == Command.directory:
            self.cursor.execute("SELECT path FROM search WHERE name LIKE '%s' and type = %d ORDER BY rank DESC LIMIT '%i'" % (query, ItemType.directory, self.MAX_RESULTS))
            data.append(self.splat(self.cursor.fetchall()))
        
        elif command == Command.file:
            self.cursor.execute("SELECT path FROM search WHERE name LIKE '%s' and type = %d ORDER BY rank DESC LIMIT '%i'" % (query, ItemType.file, self.MAX_RESULTS))
            data.append(self.splat(self.cursor.fetchall()))
        
        elif command == Command.all:
            self.cursor.execute("SELECT path FROM search WHERE name LIKE '%s' ORDER BY rank DESC LIMIT '%i' " % (query, self.MAX_RESULTS))
            data.append(self.splat(self.cursor.fetchall()))
        return data