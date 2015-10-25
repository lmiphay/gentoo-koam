#!/usr/bin/python

import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamMainWindow(QMainWindow):

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.addToolBar(KoamToolbar(self, controller))
        self.view = KoamView()
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
