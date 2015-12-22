#!/usr/bin/python

import sys
import logging

from PyQt4.QtCore import *

class KoamCommand(QProcess):
    """ A simple one-shot command - runs, we collect all the output from the
        process and make it all available when the process has exited. The result
        signal is emitted with the exitCode of the process (and the hostname of the server
        it was run on).
    """

    # ident (hostname), exitCode
    result = pyqtSignal('QString', int)

    def __init__(self, ident, cmd, argv):
        QProcess.__init__(self)
        self.ident = ident
        self.cmd = cmd
        self.argv = argv
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)
        self.finish.connect(self.fin)
        self.logger = logging.getLogger("koam.command." + ident)
        self.output = []

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
            self.logger.log(logging.DEBUG, "calling terminate for %s %s", self.cmd, str(self.argv))
            self.terminate()
            self.waitForFinished(1000)
        else:
            self.logger.log(logging.ERROR, "%s %s was not running", self.cmd, str(self.argv))

    def out(self):
        for line in str(self.readAllStandardOutput()).splitlines():
            self.logger.log(logging.DEBUG, "output: %s", line)
            if sys.version_info > (3,0):
                self.output.append(line[2:-3]) # remove leading/trailing garbage
            else:
                self.output.append(line)

    def err(self):
        msg = str(self.readAllStandardError())
        self.logger.log(logging.ERROR, "error from %s %s: %s", self.cmd, str(self.argv), msg)
        self.output.append(msg)

    def fin(self, exitCode, exitStatus):
        self.logger.log(logging.INFO, "finish signalled from %s %s: %d %s",
                        self.cmd, str(self.argv), exitCode, str(exitStatus))
        self.result.emit(self.ident, exitCode)
