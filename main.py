import json
import ftplib
import threading
from threading import Thread


class MyThread(Thread):
    def __init__ (self, file_name, path_from, path_to, number_of_thread):
        """Init of Thread"""
        Thread.__init__(self)
        self.number_of_thread = number_of_thread
        self.file_name = file_name
        self.path_from = path_from
        self.path_to = path_to
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
            self.ftp.cwd(self.path_to)
        # if directory not found, creating new directory and change directory
        except ftplib.error_perm:
            self.ftp.mkd(self.path_to)
            self.ftp.cwd(self.path_to)

    def run(self):
        """Starting thread"""
        threadLimiter.acquire()
        try:
            ftpresponse = self.ftp.storbinary("STOR %s" % self.file_name, open(self.path_from, 'rb'))
            print(self.number_of_thread, self.file_name, ftpresponse[ 4: ])
            self.ftp.quit()
        finally:
            threadLimiter.release()


def create_threads():
    """Creating threads"""
    number_of_thread = 0
    for file_name in config[ 'settings_for_files' ]:
        number_of_thread += 1
        path_from = config[ 'settings_for_files' ][file_name]['path_from']
        path_to = config[ 'settings_for_files' ][file_name]['path_to']
        my_thread = MyThread(file_name, path_from, path_to,  number_of_thread)
        my_thread.start()


if __name__ == "__main__":
    with open('config.json') as json_file:
        config = json.load(json_file)
    threadLimiter = threading.BoundedSemaphore(int(config[ 'settings_for_threads' ][ 'number_of_threads' ]))
    create_threads()
