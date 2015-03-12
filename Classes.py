# INFO: #
# ===================================

import os, sys, socket
from COM import *
from RECURRING_FUNCTIONS import *

class Server(object):
    def __init__(self, ip, port):
        ''' This method will run every time you boot up the module.
        '''
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket()
    
    def __str__(self):
        return "ip: {ip}; port: {port}".format(ip=self.server_ip, port=self.server_port)
    
    def __repr__(self):
        return "################\nThe main server is (or at least should be) listening on:\nIP address: {ip}\nTCP port: {port}\n################".format(ip=self.server_ip, port=self.server_port)

    def connect(self, username, password):
        self.sock.connect((self.server_ip, self.server_port))
        message = "AUT|{}|{}".format(username, password)
        secure_send(self.sock, message)
        response = secure_recv(self.sock)
        response_parts = response.split('|')
        flag = response_parts[0]; response_parts.remove(flag)
        if response_parts == message.split('|'):
            return flag
        else:
            return 'WTF'
        
    def disconnect(self):
        self.MAIN_SOCKET.close()

    def get_last_updates(self, folder_type):
        message = "LUD|"+folder_type
        secure_send(self.sock, message)
        file_content = file_recv(self.sock)
        lines = file_content.split('\n')
        updates_dict = {}
        for line in lines:
            pair = line.split(':')
            updates_dict[pair[0]] = pair[1]
        return updates_dict

    def update_updates_info(self, folder_type, updates_dict):
        new_data = ''
        for key in updates_dict.keys():
            new_data += '{}:{}\n'.format(key, updates_dict[key])
        message = 'NUD|'+folder_type
        secure_send(self.sock, message)
        response = secure_recv(self.sock)
        response_parts = response.split('|')
        flag = response_parts[0]; response_parts.remove(flag)
        if flag == 'ACK' and response_parts == message.split('|'):
            secure_file_send(new_data)
            final_response = secure_recv(self.sock)
            final_response_parts = final_response.split('|')
            final_flag = final_response_parts[0]; final_response_parts.remove(final_flag)
            if final_response_parts = message.split('|'):
                return final_flag
            else:
                raise # Shouldn't get here...
        else:
            raise # Shouldn't get here...

        def sync_with_server(self):
            pass
        
'''
Exciting. Satisfying. Period.
.
'''
