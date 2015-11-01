#!/usr/bin/python

import os
import pickle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamToolbar(QToolBar):

    KOAMDIR = os.path.expanduser('~/.koam')
    SERVERS = KOAMDIR + '/servers.pickle'

    def __init__(self, parent, controller):
        QToolBar.__init__(self, parent)
        self.controller = controller
        self.loadAct = self.makeAction('Load', 'Ctrl+L', True, self.doLoad)
        self.saveAct = self.makeAction('Save', 'Ctrl+S', True, self.doSave)
        self.stopAct = self.makeAction('Stop', 'Ctrl+P', True, self.doStop)
        self.startAct = self.makeAction('Start', 'Ctrl+T', False, self.doStart)
        self.addWidget(koam.KoamAddServer())
        self.prefs = koam.KoamPreferences()

    def doLoad(self):
        if self.prefs.load():
            self.parent().msg("Loaded")
        else:
            self.parent().msg(self.SERVERS + " not found")

    def doSave(self):
        self.prefs.save()
        self.parent().msg("Saved")

    def doStop(self):
        self.parent().msg("Paused")
        self.stopAct.setEnabled(False)
        self.startAct.setEnabled(True)
        self.controller.stopAll()

    def doStart(self):
        self.parent().msg("Running")
        self.stopAct.setEnabled(True)
        self.startAct.setEnabled(False)
        self.controller.startAll()

    def makeAction(self, text, shortcut, enabled, callback):
        act = QAction(text, self)
        act.setShortcut(shortcut)
        act.setEnabled(enabled)
        act.triggered.connect(callback)
        self.addAction(act)
        return act
