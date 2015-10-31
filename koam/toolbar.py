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
        self.servers = set()
        koam.KoamObserver.connect_add(self.add_handler)
        koam.KoamObserver.connect_rem(self.remove_handler)

    def doLoad(self):
        if os.path.exists(self.SERVERS):
            self.servers = pickle.load(open(self.SERVERS, 'rb'))
            self.parent().msg("Loaded")
            for server in self.servers:
                koam.KoamObserver.add_server(server)
        else:
            self.parent().msg(self.SERVERS + " not found")

    def doSave(self):
        if not os.path.isdir(self.KOAMDIR):
            os.mkdir(self.KOAMDIR)
        pickle.dump(self.servers, open(self.SERVERS, 'wb'))
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

    def add_handler(self, server):
        self.servers.add(server)

    def remove_handler(self, server):
        if server in self.servers:
            self.servers.remove(server)
