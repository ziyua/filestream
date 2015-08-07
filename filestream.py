#!/usr/bin/python
# -*- coding: gb2312 -*-

import fileinput
import os


class FileStream:

    def __init__(self, filename, cutsize=2048):
        self.filename = filename
        self.cutsize = cutsize  # 2048 byte
        self.size = os.path.getsize(self.filename)
        self.file = fileinput.input(filename)
        self.Buff = ''
        self.fileStream = self._filestream()

    def cuttimes(self):
        if self.lastsize() == 0:
            return self.size / self.cutsize
        elif self.lastsize() >= 0:
            return self.size / self.cutsize + 1

    def lastsize(self):
        return self.size % self.cutsize

    def _bytestream(self):
        for line in self.file:
            for byte in line:
                yield byte

    def _filestream(self):
        bytestream = self._bytestream()
        for k in range(self.size):
            byte = bytestream.next()
            self.Buff += byte
            if len(self.Buff) == self.cutsize:
                data = self.Buff
                self.Buff = ''
                yield data
        else:
            if len(self.Buff) != 0:
                data = self.Buff
                self.Buff = ''
                yield data

    def getstream(self):
        # have not more content, return <type 'None'>.
        try:
            content = self.fileStream.next()
        except StopIteration:
            self.file.close()
            return
        else:
            return content

if __name__ == '__main__':
    fs = FileStream('1.txt', 1024)
    print fs.cuttimes()
    print fs.lastsize()
    while 1:
        fby = fs.getstream()
        if fby is not None:
            print '--------'
            print fby, len(fby)
        else:
            break
