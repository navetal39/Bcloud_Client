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
from Server_Class import Server
from Memory_Class import Memory

# Constants: #
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

def prepare_folders(path):
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
    prepare_folders(FOLDERS_LOCATION)
    FOLDERS_LOCATION += '/Bcloud'

    
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
    print 'memory set up'
    server = Server(SYNC_IP, SYNC_PORT, memory)
    print 'Initial synchronization...'
    sync(server, username, password, True)
    while True:
        # time.sleep(TIME_BETWEEN_SYNCS)
        #for i in xrange(20):
        #    print 20 - i
        #    time.sleep(1)
        raw_input()
        sync(server, username, password)
    
run()

raw_input('')
'''
Exciting. Satisfying. Period.
.
'''
