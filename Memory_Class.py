# INFO: #
# NOT TESTED YET
# ===================================



import os, sys, zipfile, zlib, win32api, win32con

class Memory(object):
    def __init__(self, path):
        '''sets up a memory object
        '''
        self.path = path

    def ensure_existance(self, folder_type):
        ''' Ensures the existance of the main folders, in case a user tries to delete them.
        '''
        folder = self.path + '/' + folder_type
        if not os.path.exists(folder):
            os.makedirs(folder)
    
    def get_last_updates(self, folder_type):
        ''' Gets the last updates info of a specific folder
        '''
        self.ensure_existance(folder_type)
        
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
        ''' Compresses, then returns the compressed content of a list of files from a given folder type
        '''
        self.ensure_existance(folder_type)
        
        try:
            os.remove(self.path+'/files_to_server.zip') # Removal - Just in case the temporary file wasen't removed properly.
        except WindowsError, error:
            if error.errno == 2: # The file does not exist - All is good
                pass
            else:
                print 'ERROR', error
                raise
        print 'gfl: removed zip'
        archive = zipfile.ZipFile(self.path+'/files_to_server.zip', 'w', compression = zipfile.ZIP_DEFLATED) # Creation
        print 'gfl: created zip'
        for file_path in files_list:
            print 'gfl: Adding {} to zip'.format(file_path)
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_path), file_path) # Writing using the given, relative path, not the full one
        print 'gfl: finished writing'
        archive.close()
        print 'gfl: closed zip'
        # Opening the zip file now as a normal file in order to read it as a bytestream.
        archive = open(self.path+'/files_to_server.zip', 'rb') # Reading raw data
        print 'gfl: reading from zip'
        raw_data = archive.read()
        print 'gfl: got raw data'
        archive.close()
        print 'gfl: finished reading'
        try:
            os.remove(self.path+'/files_to_server.zip') # Removal of the temp file
        except WindowsError, error:
            if error.errno == 2: # If, somehow, it does not exist anymore, then it's all good. (It's just me being lazy and copy-pasting and now I'm too scared to change the code...
                pass
            else:
                print 'ERROR', error
                raise
        print 'gfl: returning raw data'
        return raw_data

    def update_files(self, folder_type, raw_data):
        ''' Gets a compressed archive, then extracts it into a given folder type.
        '''
        self.ensure_existance(folder_type)
        
        try:
            os.remove(self.path+'/updated_files.zip') # Removal - Just in case it wasen't removed properly.
        except WindowsError, error:
            if error.errno == 2: # If it does not exist - all is good!
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
        # Openning the archive as a normal file in order to read it's content as a bytestream
        updated_files = zipfile.ZipFile('{}/updated_files.zip'.format(self.path), 'r') # Extracting
        print 'upd: opened zip'
        updated_files.extractall('{}/{}'.format(self.path, folder_type))
        print 'upd: extracted'
        updated_files.close()
        try:
            os.remove(self.path+'/updated_files.zip') # Removal of temp file
        except WindowsError, error:
            if error.errno == 2: # If, somehow, it does not exist anymore, then it's all good. (It's just me being lazy and copy-pasting and now I'm too scared to change the code...
                pass
            else:
                print 'ERROR', error
                raise

    def delete_files(self, folder_type, files_list):
        ''' Deletes the files who's paths are given from the given folder type.
        '''
        self.ensure_existance(folder_type)
        
        for file_name in files_list:
            try:
                os.remove('{}/{}/{}'.format(self.path, folder_type, file_name))
                print 'del: removed {}/{}/{}'.format(self.path, folder_type, file_name)
            except WindowsError, error:
                if error.errno == 2: # The file was somehow removed already
                    continue
                else:
                    print 'ERROR', error
                    raise # Shouldn't get here...
'''
Exciting. Satisfying. Period.
.
'''
