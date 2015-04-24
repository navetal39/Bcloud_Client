# INFO: #
# ===================================

'''
To Do:
1) Installation GUI?
2) GUI?
3) Think of a better name for the server class
4) Figure out why some file types won't be sent (i.e. pictures)
'''

import os, sys, socket, time, win32api, win32con
from Config import *
from RECURRING_FUNCTIONS import *
from Server_Class import Server
from Memory_Class import Memory
from crypto import do_hash

# Constants: #
BAD_CHARS = ("\\", '/', ':', '*', '?', '"', '<', '>', '|')
MIN_LENGTH = 4
MAX_LENGTH = 32

def check(data):
    ''' Checks if the data (username/password) are valid
    '''
    if len(data) < MIN_LENGTH:
        return False
    if len(data) >= MAX_LENGTH:
        return False
    for char in BAD_CHARS:
        if char in data:
            return False
    return True
    

def sync(server, username, password, initial = False):
    ''' All sync phases in one method
    '''
    status = server.connect(username, password)
    if status == 'SCS':
        print 'Connected'
        server.sync('public', initial)
        print 'Synchronized public folder'
        server.sync('private', initial)
        print 'Synchronized private folder'
        server.disconnect()
        print 'Disconnected'
    else:
        print "Didn't manage to connect (maybe wrong password or username)... :/"
        run() # Try again...

def prepare_folders(path):
    ''' Makes sure all the necesary folders exists
    '''
    if os.path.exists(path):
        if not os.path.exists(path+'/Bcloud'):
            os.makedirs(path+'/Bcloud')
        if not os.path.exists(path+'/Bcloud/private'):
            os.makedirs(path+'/Bcloud/private')
        if not os.path.exists(path+'/Bcloud/public'):
            os.makedirs(path+'/Bcloud/public')
    else:
        raise
    
def run():
    print 'Welcome to Bcloud!'

    global FOLDERS_LOCATION
    global TIME_BETWEEN_SYNCS
    if TIME_BETWEEN_SYNCS < 10:
        TIME_BETWEEN_SYNCS = 10
    prepare_folders(FOLDERS_LOCATION) # Creates the main and 2 sub-folders
    ACTUAL_FOLDERS_LOCATION = FOLDERS_LOCATION + '/Bcloud' # For easier access to the 2 sub-folders

    # Inputs:
    while True:
        username = raw_input('Username: ')
        if check(username):
            break
        else:
            print 'ERROR! {} is not a valid username!'.format(username)
    while True:
        password = raw_input('Password: ')
        if check(password):
            password = do_hash(password)
            break
        else:
            print 'ERROR! {} is not a valid password!'.format(password)

    memory = Memory(ACTUAL_FOLDERS_LOCATION) # Creates the object that'll help accessing the memory
    print 'memory set up'
    server = Server(SYNC_IP, SYNC_PORT, memory) # Create the object that'll be responsible for the synchronization
    print 'Initial synchronization...'
    sync(server, username, password, True) # Initial synchronization
    while True:
        time.sleep(TIME_BETWEEN_SYNCS)
        # raw_input('-----------------Enter to sync-----------------') # Used for testing
        sync(server, username, password) # Timed synchronization

'''
Exciting. Satisfying. Period.
.
'''
