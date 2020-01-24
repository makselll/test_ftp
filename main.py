import json
import os
import ftplib
from threading import Thread


class MyThread(Thread):
    def __init__ (self, file_name, root, number_of_thread):
        """Init of Thread"""
        Thread.__init__(self)
        self.number_of_thread = number_of_thread
        self.file_name = file_name
        # login to ftp server
        self.ftp = ftplib.FTP(
            config[ 'settings_for_ftp' ][ 'host' ],
            config[ 'settings_for_ftp' ][ 'username' ],
            config[ 'settings_for_ftp' ][ 'password' ]
            )
        # setup encoding
        self.ftp.encoding = 'utf-8'
        # change home directory to directory 'path_to_copy_on_server'
        try:
            self.ftp.cwd(config[ 'settings_for_files' ][ 'path_to_copy_on_server' ])
        # if directory not found, creating new directory and change directory
        except ftplib.error_perm:
            self.ftp.mkd(config[ 'settings_for_files' ][ 'path_to_copy_on_server' ])
            self.ftp.cwd(config[ 'settings_for_files' ][ 'path_to_copy_on_server' ])
        self. full_file_name = os.path.join(root, file_name)

    def run(self):
        """Starting thread"""
        ftpresponse = self.ftp.storbinary("STOR %s" % self.file_name, open(self.full_file_name, 'rb'))
        print(self.number_of_thread, self.file_name, ftpresponse[ 4: ])
        self.ftp.quit()


def create_threads():
    """Creating threads"""
    for root, dirs, files in os.walk(config[ 'settings_for_files' ][ 'path_to_files' ]):
        number_of_thread = 0
        for file_name in files:
            number_of_thread += 1
            my_thread = MyThread(file_name, root, number_of_thread)
            my_thread.start()


if __name__ == "__main__":
    with open('config.json') as json_file:
        config = json.load(json_file)
    create_threads()
