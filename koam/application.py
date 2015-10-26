#!/usr/bin/python

import koam
from PyQt4.QtGui import QApplication

class KoamApplication(QApplication):
    
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.controller = koam.KoamController(argv)
        self.koamwidget = koam.KoamWidget(self.controller)
        self.toplevel = koam.KoamMainWindow(self.koamwidget, self.controller)
        self.controller.setWidget(self.koamwidget)
        
    def run(self):
        self.controller.startProc()
        return self.exec_()
