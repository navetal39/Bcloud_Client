# INFO: #
# ===================================

'''
To Do:
1) Installation GUI?
2) GUI?
'''

import os, sys, socket, time
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
    server.connect(username, password)
    print 'Connected'
    server.sync('public', initial)
    print 'Synchronized public folder'
    server.sync('private', initial)
    print 'Synchronized private folder'
    server.disconnect()
    print 'Disconnected'
    
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

    
    server = Server(SYNC_IP, SYNC_PORT)
    print 'Initial synchronization...'
    sync(server, username, password, True)
    while True:
        time.sleep(TIME_BETWEEN_SYNCS)
        sync(server, username, password)
    

'''
Exciting. Satisfying. Period.
.
'''
