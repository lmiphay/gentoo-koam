#!/usr/bin/python2

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamWidget(QTabWidget):

    def __init__(self, parent = None): 
        QTabWidget.__init__(self, parent)
        self.tabs = {}

    def addHost(self, name): 
        self.tabs[name] = QTextBrowser() 
        self.addTab(self.tabs[name], name)

    def updateHost(self, message):
        name = message.split()[0]
        self.tabs[name].append(message)

    def closeEvent(self, event):
        self.proc.close()
        event.accept()

class MusshProcess(QProcess):
    
    def __init__(self, parent = None): 
        QProcess.__init__(self, parent)
        self.readyReadStandardOutput.connect(self.addStdout)
        self.readyReadStandardError.connect(self.addStderr)
        self.finished.connect(self.stop)

    def start(self, command, arguments):
        self.start(command, arguments)

    def close(self):
        self.terminate()
        self.waitForFinished(1000)
        
    def addStdout(self):
        self.widget.updateHost(QString.fromLocal8Bit(self.readAllStandardOutput()))

    def addStderr(self):
        self.widget.updateHost(QString.fromLocal8Bit(self.readAllStandardError()))

class KoamController:
    
    def __init__(self, args): 
        self.app = QApplication(args)
        self.view = KoamWidget()
        self.model = MusshProcess()
    
        self.view.proc = self.model
        self.model.widget = self.view

        self.hosts = ""
        for i in args:
            self.view.addHost(i)
            self.hosts += i + " "

    def run(self):
        self.view.show()
        self.model.start("oam-mussh", self.hosts)
    
        sys.exit(self.app.exec_())
        
if __name__ == "__main__":
    KoamController(sys.argv).run()

