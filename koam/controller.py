#!/usr/bin/python

import sys
import logging
import json
import koam

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamController(QObject):

    DISABLE_PASS_QUERY = [ '-o', 'BatchMode=yes']
    REMOTE_CMD = 'oam-status rawloop & read ; kill $!'
    
    def __init__(self):
        QObject.__init__(self)
        self.proc = {}
        self.logger = logging.getLogger("koam.controller")
        self.checker = koam.KoamCheckHost(self)
        #koam.KoamObserver.connect_add(self.add)
        koam.KoamObserver.connect_rem(self.remove)

    def add(self, server):
        if server not in self.proc:
            self.logger.log(logging.INFO, "adding: %s ", server)
            self.proc[server] = koam.KoamProcess(self, server,
                                                 "ssh", self.DISABLE_PASS_QUERY + [server, self.REMOTE_CMD])
            self.logger.log(logging.INFO, "starting: %s ", server)
            self.proc[server].run()
        else:
            self.logger.log(logging.ERROR, "not adding: %s - already present", server)

    def remove(self, server):
        if server in self.proc:
            self.logger.log(logging.INFO, "removing: %s ", server)
            self.proc[server].close()
            del self.proc[server]
        else:
            self.logger.log(logging.ERROR, "not removing: %s - not present", server)

    def setWidget(self, widget):
        self.win = widget
        
    def stopAll(self):
        for server in self.proc:
            self.logger.log(logging.INFO, "stopping: %s ", server)
            self.proc[server].close()

    def startAll(self):
        for server in self.proc:
            self.logger.log(logging.INFO, "starting: %s ", server)
            self.proc[server].run()

    def out(self, ident, msg):
        self.logger.log(logging.DEBUG, "output: %s - %s", ident, msg)
        try:
            fields = json.loads(msg)
            self.win.view.update("All", fields)
            self.win.view.update(fields['Host'], fields)
        except ValueError:
            self.err(ident, "ValueError exception for: " + msg)
        except:
            self.err(ident, "Unexpected exception for: " + str(msg) +
                     ", " + str(sys.exc_info()[0]) + ", " + str(sys.exc_info()))

    def err(self, ident, msg):
        self.logger.log(logging.ERROR, "error: %s - %s", ident, msg)
        self.win.view.message("Error Log", msg)
