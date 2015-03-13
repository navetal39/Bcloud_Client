# INFO: #
# NOT TESTED YET
# ===================================



import os, sys, zipfile, zlib, win32api, win32con

class Memory(object):
    def __init__(self, path):
        self.path = path

        try:
            os.remove(self.path+'/files_to_server.zip')
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                raise
        try:
            os.remove(self.path+'/updated_files.zip')
        except WindowsError, error:
            if error.errno == 2:
                pass
            else:
                raise
            
        temp_archive = zipfile.ZipFile(self.path+'/files_to_server.zip', 'w', compression = zipfile.ZIP_DEFLATED)
        temp_archive.close()
        temp_archive = zipfile.ZipFile(self.path+'/updated_files.zip', 'w', compression = zipfile.ZIP_DEFLATED)
        temp_archive.close()
        
        win32api.SetFileAttributes(self.path+'/files_to_server.zip', win32con.FILE_ATTRIBUTE_HIDDEN)
        win32api.SetFileAttributes(self.path+'/updated_files.zip', win32con.FILE_ATTRIBUTE_HIDDEN)

    def get_last_updates(self, folder_type):
        updates_dict = {}
        for root, dirs, files in os.walk('{}/{}'.format(self.path, folder_type)):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                last_update = os.stat(file_path).st_mtime
                updates_dict[file_path] = last_update
        return updates_dict
    
    def get_files(self, folder_type, files_list):
        archive = zipfile.ZipFile(self.path+'/files_to_server.zip', 'w', compression = zipfile.ZIP_DEFLATED)
        for file_path in files_list:
            archive.write('{path}/{folder}/{fil}'.format(path = self.path, folder = folder_type, fil = file_path), file_path)
        archive.close()
        archive = open(self.path+'/files_to_server.zip', 'rb')
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
