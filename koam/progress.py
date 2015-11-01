#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamProgress(QWidget):
    
    def __init__(self, parent = None): 
        QWidget.__init__(self, parent)
        self.layout = QFormLayout()
        self.host = {}
        self.setLayout(self.layout)

    def add(self, server):
        self.host[server] = QProgressBar()
        self.host[server].setMinimum(0)
        self.host[server].setFormat("%v / %m merges")
        self.layout.addRow(server, self.host[server])
 
    def update(self, server, merges):
        if server not in self.host:
            self.add(server)
        if merges[0] <= merges[1]:
            self.host[server].setValue(merges[0])
        else:
            self.host[server].setValue(merges[1])
        self.host[server].setMaximum(merges[1])
        self.host[server].setToolTip(str(merges[0]) + " out of " + str(merges[1]) + " merges")
        
