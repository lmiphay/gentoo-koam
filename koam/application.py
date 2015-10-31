#!/usr/bin/python

import logging
import koam
from PyQt4.QtGui import QApplication

class KoamApplication(QApplication):
    
    def __init__(self, argv):
        QApplication.__init__(self, argv)
        self.controller = koam.KoamController(argv)
        self.koamwidget = koam.KoamWidget(self.controller)
        self.toplevel = koam.KoamMainWindow(self.koamwidget, self.controller)
        self.controller.setWidget(self.koamwidget)
        self.logger = logging.getLogger("koam.application")
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
        
    def run(self):
        self.controller.startProc()
        self.logger.log(logging.INFO, "controller started")
        return self.exec_()
