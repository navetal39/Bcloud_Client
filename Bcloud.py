# INFO: #
# ===================================

'''
To Do:
1) Installation GUI?
2) GUI?
3) Think of a better name for the server class
'''

import os, sys, socket, time, win32api, win32con
from COM import *
from RECURRING_FUNCTIONS import *
from Server_Class import Server
from Memory_Class import Memory

# Constants: #
FOLDERS_LOCATION = 'C:/Users/user/Bcloud'
TIME_BETWEEN_SYNCS = 900 # 900 sec = 1/4 h
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
        print "Didn't manage to connect... :/"
        run() # Try again...
    
def run():
    print 'Welcome to Bcloud!'
    
    while True:
        username = raw_input('Username: ')
        if check(username):
            break
        else:
            print 'ERROR! {} is not a valid username!'.format(username)
    while True:
        password = raw_input('Password: ')
        if check(password):
            break
        else:
            print 'ERROR! {} is not a valid password!'.format(password)

    memory = Memory(FOLDERS_LOCATION)
    server = Server(SYNC_IP, SYNC_PORT, memory)
    print 'Initial synchronization...'
    sync(server, username, password, True)
    while True:
        time.sleep(TIME_BETWEEN_SYNCS)
        sync(server, username, password)
    

'''
Exciting. Satisfying. Period.
.
'''
