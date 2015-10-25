#!/usr/bin/python

import os
import koam

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamMainWindow(QMainWindow):

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.addToolBar(koam.KoamToolbar(self, controller))
        self.view = koam.KoamView()
        self.setCentralWidget(self.view)
        self.msg("Startup")
        self.resize(850,256)
        self.setWindowTitle("koam on " + os.uname()[1])
        self.show()

    def closeEvent(self, event):
        self.controller.close()
        event.accept()

    def msg(self, text):
        self.statusBar().showMessage(text)
