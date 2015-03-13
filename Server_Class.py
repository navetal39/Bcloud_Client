# INFO: #
# ===================================

'''
To Do:
1) Think about what to do if the server doesn't manage to send the files to the client
'''

import socket
from COM import *
from RECURRING_FUNCTIONS import *
from Memory_Class import Memory

class Server(object):
    def __init__(self, ip, port):
        ''' This method will run every time you boot up the module.
        '''
        self.server_ip = ip
        self.server_port = port
        self.sock = socket.socket()
        self.memory = Memory()
    
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

    def update_updates_info(self, folder_type):
        updates_dict = self.memory.get_last_updates(folder_type)
        new_data = ''
        for key in updates_dict.keys():
            new_data += '{}:{}\n'.format(key, updates_dict[key])
        if new_data == '': # In case the folder is now empty
            new_data = 'EMPTY' # Sending an empty string can lead to some problems...
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
            if final_response_parts == message.split('|'):
                return final_flag
            else:
                raise # Shouldn't get here...
        else:
            raise # Shouldn't get here...

    def compare_updates(self, folder_type, first_time):
        updates_dict = self.memory.get_last_updates(folder_type)
        server_updates_dict = self.get_last_updates(folder_type)
        
        compared = set()
        to_send, to_recv, to_delete = [], [], []
        for key in updates_dict.keys():
            if key in server_updates_dict.keys(): # Both client and server have the file
                dif = updates_dict[key]-server_updates_dict[key]
                if dif > 0: # Our version is the most up-to-date
                    to_send.append(key)
                elif dif <0: # The server's version is the most up-to-date
                    to_recv.append(key)
                else: # Both versions are up-to-date
                    continue
            else: # The server doesn't have the file
                if first_time: # The file was removed on a previous run on another machine
                    to_delete.append(key)
                else: # A new file that was created during this run
                    to_send.append(key)
            compared.add(key)
            
        for key in server_updates_dict.keys():
            if key in compared: # Already did this one
                continue
            else: # We don't have this file
                to_recv.append(key)

    def stringify(self, l):
        l_str = ''
        for item in l:
            l_str+='<>{}'.format(item)
        if len(l_str):
            l_str.lstrip('<>')
        return l_str
        
    def sync(self, folder_type, first_time = False):
        to_send, to_recv, to_delete = self.compare_updates(self, folder_type, first_time)
        
        if len(to_send)+len(to_recv)+len(to_delete): # If there's something that needs to update
            to_send_str = self.stringify(to_send)
            to_recv_str = self.stringify(to_recv)
            to_delete_str = self.stringify(to_delete)
            long_ass_message = "{}|{}|{}|".format(folder_type, to_recv_str, to_send_str)
            if not first_time:
                long_ass_message += to_delete_str

            
            secure_send(self.sock, 'SYN')
            response = secure_recv(self.sock)
            if response == 'ACK|SYN':
                secure_file_send(self.sock, long_ass_message)
            else:
                raise # Shouldn't get here...

            # Synchronization phases:
            while True:
                phase = secure_recv(self.sock, 3)
                if phase == 'UPD': # Server is updating it's files
                    files_for_server = self.memory.get_files(folder_type, to_send)
                    secure_file_send(files_for_server)
                elif phase == 'SND': # Server is ready to send files here
                    secure_send(self.sock, 'ACK|SND')
                    data = secure_file_recv(self.sock)
                    self.memory.update_files(folder_type, data)
                elif phase == 'SNF': # Server didn't manage to give us our files
                    pass # SEE TO DO LIST
                elif phase == 'DEL': # Server is ready to delete files on it's end
                    secure_send(self.sock, 'ACK|DEL')
                elif phase == 'FIN': # Server finished it's part
                    break
                else:
                    raise # Shouldn't get here

            if first_time: # Deleting files on our end.
                self.memory.delete_files(folder_type, to_delete)

            self.update_updates_info(folder_type)

                            
            

            
            
'''
Exciting. Satisfying. Period.
.
'''
