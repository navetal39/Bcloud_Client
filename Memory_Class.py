# INFO: #
# ===================================

'''
To Do:
EVERYTHING
'''

import os, sys, zipfile, zlib

class Memory(object):
    def __init__(self, path):
        self.path = path

    def get_last_updates(self, folder_type):
        updates_dict = {}
        for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                last_update = os.stat(file_path).st_mtime
                updates_dict[file_path] = last_update
        return updates_dict
    
    def get_files(self, folder_type, files_list):
       archive = zipfile.ZipFile(self.path+'/files_to_server', 'w', compression = zipfile.ZIP_DEFLATED)
        for file_path in files_list:
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_path), file_path)
        archive.close()
        archive = open(self.path+'/files_to_server', 'rb')
        raw_data = archive.read()
        archive.close()
        return raw_data

    def update_files(self, folder_type, raw_data):
        updated_files = open('{}/updated_files.zip'.format(self.path), 'wb')
        updated_files.write(raw_data)
        updated_files.close()
        updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r')
        updated_files.extract_all('{}/{}'.format(self.path, folder_type))
        updated_files.close()

    def delete_files(self, folder_type, files_list):
        for path in files:
            try:
                os.remove('{}/{}/{}'.format(self.path, folder_type, file_name))
            except WindowsError, error:
                if error.errno == 2:
                    continue
                else:
                    raise # Shouldn't get here...
'''
Exciting. Satisfying. Period.
.
'''
