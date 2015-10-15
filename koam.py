#!/usr/bin/python2

import sys
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamView(QTabWidget):

    def __init__(self, parent = None): 
        QTabWidget.__init__(self, parent)
        self.tabs = {}

    def add(self, name): 
        self.tabs[name] = QTextBrowser() 
        self.addTab(self.tabs[name], name)
        font = QFont("Monospace")
        font.setPointSize(8)
        self.tabs[name].setCurrentFont(font)

    def update(self, name, message):
        if name not in self.tabs:
            self.add(name)
        self.tabs[name].append(message)

    def closeEvent(self, event):
        self.proc.close()
        event.accept()

class KoamProcess(QProcess):
    
    def __init__(self, controller): 
        QProcess.__init__(self)
        self.controller = controller
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)
        self.finished.connect(self.reportFinished)
        self.stateChanged.connect(self.reportState)
        self.error.connect(self.reportError)

    def reportError(self, err):
        print "Got err: " + str(err)

    def reportState(self, state):
        print "Got state: " + str(state)

    def reportFinished(self, err, status):
        print "Got fin: " + str(err) + ", " + str(status)

    def run(self, command, arguments):
        self.start(command, arguments)
        self.waitForStarted()

    def close(self):
        self.terminate()
        self.waitForFinished(1000)
        
    def out(self):
        for line in str(self.readAllStandardOutput()).splitlines():
            self.controller.out(line)

    def err(self):
        self.controller.err(str(QString.fromLocal8Bit(self.readAllStandardError())))

class KoamController(QObject):
    
    def __init__(self):
        QObject.__init__(self)

    def run(self, argv):
        self.app = QApplication(argv)
        self.view = KoamView()
        self.proc = KoamProcess(self)
        self.view.proc = self
        self.view.show()
        self.proc.run("oam-status", ["rawnet"] + argv[1:])
        self.view.update("Summary", "oam-status " + " ".join(["rawnet"] + argv[1:]))
        sys.exit(self.app.exec_())
        
    def stop(self):
        print "STOP!"

    def close(self):
        print "CLOSE!"
        self.proc.close()

    def out(self, msg):
        fields = json.loads(msg)
        print "controller fields=" + str(fields)
        self.view.update(fields['Host'], msg[8:])
        self.view.update("Summary", msg)

    def err(self, msg):
        self.view.update("Error Log", msg)

if __name__ == "__main__":
    KoamController().run(sys.argv)

