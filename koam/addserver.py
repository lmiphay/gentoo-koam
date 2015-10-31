#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamAddServer(QLineEdit):

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setPlaceholderText('Enter new server name')
        self.returnPressed.connect(self.add)

    def add(self):
        koam.KoamObserver.add_server(self.text())
        self.clear()
