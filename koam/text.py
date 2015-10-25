#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamText(QTextBrowser):

    def __init__(self, parent = None):
        QTextBrowser.__init__(self, parent)
        self.setCurrentFont(koam.KoamFont())
        self.setContextMenuPolicy(Qt.CustomContextMenu);
        self.customContextMenuRequested.connect(self.rightMenu)

    def rightMenu(self, pos):
        menu = QMenu()
        clearAction = menu.addAction("Clear")
        clearAction.triggered.connect(self.clear)
        menu.exec_(self.mapToGlobal(pos))
