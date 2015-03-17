# INFO: #
# NOT TESTED YET
# ===================================



import os, sys, zipfile, zlib, win32api, win32con

class Memory(object):
    def __init__(self, path):
        self.path = path
        
    def get_last_updates(self, folder_type):
        updates_dict = {}
        for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                last_update = os.stat(file_path).st_mtime
                updates_dict[os.path.join(root.lstrip('{}/{}'.format(self.path, folder_type)), file_name)] = last_update
        return updates_dict
    
    def get_files(self, folder_type, files_list):
        try:
            os.remove(self.path+'/files_to_server.zip') # Removal - Just in case
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                print 'ERROR', error
                raise
        archive = zipfile.ZipFile(self.path+'/files_to_server.zip', 'w', compression = zipfile.ZIP_DEFLATED) # Creation
        for file_path in files_list:
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_path), file_path) # Writing
        archive.close()
        archive = open(self.path+'/files_to_server.zip', 'rb') # Reading raw data
        raw_data = archive.read()
        archive.close()
        try:
            os.remove(self.path+'/files_to_server.zip') # Removal
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                print 'ERROR', error
                raise
        return raw_data

    def update_files(self, folder_type, raw_data): 
        try:
            os.remove(self.path+'/updated_files.zip') # Removal - Just in case
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                print 'ERROR', error
                raise
        updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'w', compression = zipfile.ZIP_DEFLATED) # Creation
        updated_files.close()
        updated_files = open('{}/updated_files.zip'.format(self.path), 'wb') # Writing
        updated_files.write(raw_data)
        updated_files.close()
        updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r') # Extracting
        updated_files.extract_all('{}/{}'.format(self.path, folder_type))
        updated_files.close()
        try:
            os.remove(self.path+'/updated_files.zip') # Removal
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                print 'ERROR', error
                raise

    def delete_files(self, folder_type, files_list):
        for file_name in files_list:
            try:
                os.remove('{}/{}/{}'.format(self.path, folder_type, file_name))
            except WindowsError, error:
                if error.errno == 2:
                    continue
                else:
                    print 'ERROR', error
                    raise # Shouldn't get here...
'''
Exciting. Satisfying. Period.
.
'''
