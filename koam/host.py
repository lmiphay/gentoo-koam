#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamHost(QWidget):
    
    def __init__(self, parent = None): 
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.header = QLabel()
        self.header.setFont(KoamFont())
        self.logmsg = KoamText()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.logmsg)
        self.setLayout(self.layout)

    def setHeader(self, hdr):
        self.header.setText(hdr)

    def add(self, msg):
        self.logmsg.append(msg)