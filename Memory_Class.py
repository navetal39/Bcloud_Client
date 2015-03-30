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
                print 'glu: looking at file: '+file_path
                last_update = int(os.stat(file_path).st_mtime)
                print 'glu: last update: '+str(last_update)
                updates_dict[os.path.join(root[len('{}/{}'.format(self.path, folder_type)):], file_name)] = last_update
                print 'glu: updated dict'
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
        print 'gfl: removed zip'
        archive = zipfile.ZipFile(self.path+'/files_to_server.zip', 'w', compression = zipfile.ZIP_DEFLATED) # Creation
        print 'gfl: created zip'
        for file_path in files_list:
            print 'gfl: Adding {} to zip'.format(file_path)
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_path), file_path) # Writing
        print 'gfl: finished writing'
        archive.close()
        print 'gfl: closed zip'
        archive = open(self.path+'/files_to_server.zip', 'rb') # Reading raw data
        print 'gfl: reading from zip'
        raw_data = archive.read()
        print 'gfl: got raw data'
        archive.close()
        print 'gfl: finished reading'
        try:
            os.remove(self.path+'/files_to_server.zip') # Removal
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                print 'ERROR', error
                raise
        print 'gfl: returning '+raw_data
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
        print 'upd: created zip'
        updated_files = open('{}/updated_files.zip'.format(self.path), 'wb') # Writing
        print 'upd: opened zip'
        updated_files.write(raw_data)
        updated_files.close()
        print 'upd: wrote to zip'
        updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r') # Extracting
        print 'upd: opened zip'
        updated_files.extract_all('{}/{}'.format(self.path, folder_type))
        print 'upd: extracted'
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
                print 'del: removed {}/{}/{}'.format(self.path, folder_type, file_name)
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
