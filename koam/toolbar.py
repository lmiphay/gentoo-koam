#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamToolbar(QToolBar):

    def __init__(self, mainwin, controller):
        QToolBar.__init__(self)
        self.mainwin = mainwin
        self.controller = controller
        self.stopAct = self.makeAction('Stop', 'Ctrl+S', True, self.doStop)
        self.startAct = self.makeAction('Start', 'Ctrl+S', False, self.doStart)

    def doStop(self):
        self.mainwin.msg("Paused")
        self.stopAct.setEnabled(False)
        self.startAct.setEnabled(True)
        self.controller.close()

    def doStart(self):
        self.mainwin.msg("Running")
        self.stopAct.setEnabled(True)
        self.startAct.setEnabled(False)
        self.controller.startProc()

    def makeAction(self, text, shortcut, enabled, callback):
        act = QAction(text, self)
        act.setShortcut(shortcut)
        act.setEnabled(enabled)
        act.triggered.connect(callback)
        self.addAction(act)
        return act