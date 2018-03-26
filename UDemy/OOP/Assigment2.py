#!/usr/bin/env python

import abc
from datetime import datetime

class WriteFile(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def write(self):
        return

    def __init__(self, filename):
        self.filename = filename

    def write_line(self, string):
        fh = open(self.filename, 'a')
        fh.write(string + "\n")
        fh.close()


class LogFile(WriteFile):
    def write(self, string):
        dt_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.write_line('{0}   {1}'.format(dt_str, string))


class DelimFile(WriteFile):
    def __init__(self, file, delim):
        super(DelimFile, self).__init__(file)
        self.delim = delim

    def write(self, list):
        line = self.delim.join(list)
        self.write_line(line)


log = LogFile('somelog.txt')
c = DelimFile('file.csv', ',')

log.write('Some random message')
log.write('Some other random message')

c.write(['a', 'b', 'c', 'd'])
c.write(['1', '2', '3', '4'])
