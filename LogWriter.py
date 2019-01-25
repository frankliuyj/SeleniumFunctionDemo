# -*- coding: UTF-8 -*-

import time


class LogFileWriter(object):

    def __init__(self, path='./', mode='w'):
        fname = path + time.strftime("%d-%b-%Y-%H-%M-%S.log", time.localtime())
        self.log = open(fname, mode)

    def log_write(self, logInfo):
        self.log.write(logInfo)

    def log_close(self):
        self.log.close()