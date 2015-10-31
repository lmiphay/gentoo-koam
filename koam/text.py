#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamText(QTextBrowser):

    def __init__(self, name, parent = None):
        QTextBrowser.__init__(self, parent)
        self.name = name
        self.setCurrentFont(koam.KoamFont())
        self.setContextMenuPolicy(Qt.CustomContextMenu);
        self.customContextMenuRequested.connect(self.rightMenu)

    def rightMenu(self, pos):
        menu = QMenu()
        clearAction = menu.addAction("Clear")
        clearAction.triggered.connect(self.clear)
        removeAction = menu.addAction("Remove")
        removeAction.triggered.connect(self.remove)
        menu.exec_(self.mapToGlobal(pos))

    def remove(self):
        koam.KoamObserver.rem_server(self.name)
