#!/usr/bin/python

import sys
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamController(QObject):
    
    def __init__(self, argv):
        QObject.__init__(self)
        self.app = QApplication(argv)
        self.win = KoamMainWindow(self)
        self.proc = KoamProcess(self, "oam-status", ["rawnet"] + argv[1:])

    def startProc(self):
        self.win.msg("Running")
        self.proc.run() # default on/off?
        
    def run(self):
        self.startProc()
        return self.app.exec_()
        
    def close(self):
        self.proc.close()

    def out(self, msg):
        try:
            fields = json.loads(msg)
            self.win.view.update("All", fields)
            self.win.view.update(fields['Host'], fields)
        except ValueError:
            self.err("ValueError exception for: " + msg)
        except:
            self.err("Unexpected exception for: " + msg + ", " + sys.exc_info()[0])

    def err(self, msg):
        self.win.view.message("Error Log", msg)