#!/usr/bin/python

import logging
import koam
from PyQt4.QtGui import QApplication

class KoamApplication(QApplication):
    
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.controller = koam.KoamController()
        self.koamwidget = koam.KoamWidget(self.controller)
        self.toplevel = koam.KoamMainWindow(self.koamwidget, self.controller)
        self.controller.setWidget(self.koamwidget)
        self.logger = logging.getLogger("koam.application")
        
    def run(self):
        self.logger.log(logging.INFO, "entering event loop")
        return self.exec_()
