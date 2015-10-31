#!/usr/bin/python

import os
import koam

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamMainWindow(QMainWindow):

    def __init__(self, koamwidget, controller, parent=None):
        QMainWindow.__init__(self, parent)
        self.setCentralWidget(koamwidget)
        self.controller = controller
        koamwidget.msg("Startup")
        self.resize(850,256)
        self.setWindowTitle("koam on " + os.uname()[1])
        self.show()

    def closeEvent(self, event):
        self.controller.stopAll()
        event.accept()
