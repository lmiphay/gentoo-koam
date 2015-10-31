#!/usr/bin/python

import os
import koam

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamWidget(QWidget):

    def __init__(self, controller, parent=None):
        QWidget.__init__(self, parent)
        self.controller = controller
        self.layout = QVBoxLayout(self)
        self.toolbar = koam.KoamToolbar(self, controller)
        self.view = koam.KoamView()
        self.statusbar = QStatusBar()
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.view)
        self.layout.addWidget(self.statusbar)
        self.setLayout(self.layout)
        self.msg("Startup")

    def closeEvent(self, event):
        self.controller.stopAll()
        event.accept()

    def msg(self, text):
        self.statusbar.showMessage(text)
