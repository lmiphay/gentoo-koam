#!/usr/bin/python

import sys

from PyQt4.QtCore import *

class KoamProcess(QProcess):
    
    def __init__(self, controller, cmd, argv): 
        QProcess.__init__(self)
        self.controller = controller
        self.cmd = cmd
        self.argv = argv
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)

    def run(self):
        self.start(self.cmd, self.argv)
        self.waitForStarted()

    def close(self):
        self.terminate()
        self.waitForFinished(1000)
        
    def out(self):
        for line in str(self.readAllStandardOutput()).splitlines():
            if sys.version_info > (3,0):
                self.controller.out(line[2:-3]) # remove leading/trailing garbage
            else:
                self.controller.out(line)

    def err(self):
        self.controller.err(self.readAllStandardError())
