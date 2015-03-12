# INFO: #
# ===================================

'''
To Do:
EVERYTHING
'''

import os, sys, zipfile, zlib

class Memory(object):
    def __init__(self, root):
        self.root = root

    def get_last_updates(self, folder_type):
        pass
    
    def get_files(self, folder_type, files_list):
       pass

    def update_files(self, folder_type, raw_data):
        pass

    def delete_files(self, folder_type, files_list):
        for path in files:
            try:
                os.remove('{}/{}/{}'.format(self.root, folder_type, file_name))
            except WindowsError, error:
                if error.errno == 2:
                    continue
                else:
                    raise # Shouldn't get here...
'''
Exciting. Satisfying. Period.
.
'''
