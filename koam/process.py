#!/usr/bin/python

import sys
import logging

from PyQt4.QtCore import *

class KoamProcess(QProcess):
    """ A monitoring process - typically a long living remote process. The
    process can be stopped (paused) and restarted, but will always be run
    again as the same command and arguments.
    """
    
    def __init__(self, controller, ident, cmd, argv): 
        QProcess.__init__(self)
        self.controller = controller
        self.ident = ident
        self.cmd = cmd
        self.argv = argv
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)
        self.logger = logging.getLogger("koam.process")

    def run(self):
        self.logger.log(logging.INFO, "running: %s %s", self.cmd, str(self.argv))
        if self.state() == QProcess.NotRunning:
            self.start(self.cmd, self.argv)
            self.waitForStarted()
        else:
            self.logger.log(logging.ERROR, "%s %s was running", self.cmd, str(self.argv))

    def close(self):
        self.logger.log(logging.INFO, "close event for %s %s", self.cmd, str(self.argv))
        if self.state() != QProcess.NotRunning:
            self.write("# shutdown hint\n");
            self.logger.log(logging.DEBUG, "calling terminate for %s %s", self.cmd, str(self.argv))
            self.terminate()
            self.waitForFinished(1000)
        else:
            self.logger.log(logging.ERROR, "%s %s was not running", self.cmd, str(self.argv))

    def out(self):
        for line in str(self.readAllStandardOutput()).splitlines():
            self.logger.log(logging.DEBUG, "output: %s", line)
            if sys.version_info > (3,0):
                self.controller.out(self.ident, line[2:-3]) # remove leading/trailing garbage
            else:
                self.controller.out(self.ident, line)

    def err(self):
        msg = str(self.readAllStandardError())
        self.logger.log(logging.ERROR, "error from %s %s: %s", self.cmd, str(self.argv), msg)
        self.controller.err(self.ident, msg)
