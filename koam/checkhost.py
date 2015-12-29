#!/usr/bin/python

import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamCheckHost(QObject):
    """ Run a remote oam-checkconfig against the requested servers.
        If the check passes, then call 'add' on the controller to start monitoring
        that server. If the check fails, then error log the failure (and monitoring
        is not started).
    """

    def __init__(self, controller):
        QObject.__init__(self)
        self.controller = controller
        self.logger = logging.getLogger("koam.check.host")
        koam.KoamObserver.connect_add(self.add)
        self.runner = {}

    def add(self, server):
        self.logger.log(logging.INFO, "check host %s", server)
        self.runner[server] = koam.KoamCommand(server, 'ssh',
                                               koam.KoamController.DISABLE_PASS_QUERY +
                                               [str(server), 'oam-checkconfig', '-e'])
        self.runner[server].result.connect(self.fin)
        self.runner[server].run()
        self.logger.log(logging.INFO, "check started for %s", server)

    def fin(self, server, exitCode):
        if exitCode == 0:
            self.logger.log(logging.INFO, "check passed: %s had %d failures", server, exitCode)
            self.controller.add(server)
        else:
            self.logger.log(logging.ERROR, "check failed: %s had %d failures", server, exitCode)
            self.controller.err(server, 'check host failed' + str(self.runner[server].output))
        del self.runner[server]
        self.logger.log(logging.INFO, "check complete for %s", server)
