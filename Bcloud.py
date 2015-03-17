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
global FOLDERS_LOCATION
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

    while True: #Folders set-up
        try:
            FOLDERS_LOCATION = raw_input('Enter the location of the Bcloud folder: ')
            prepare_folders(FOLDERS_LOCATION)
        except:
            pass
        else:
            FOLDERS_LOCATION += '/Bcloud'
            break

    
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
        # time.sleep(TIME_BETWEEN_SYNCS)
        #for i in xrange(20):
        #    print 20 - i
        #    time.sleep(1)
        raw_input()
        sync(server, username, password)
    

'''
Exciting. Satisfying. Period.
.
'''
