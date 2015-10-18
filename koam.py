#!/usr/bin/python

import sys
import os
import json

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamFont(QFont):
    
    def __init__(self): 
        QFont.__init__(self, "Monospace", 8)

class KoamStatus:

    ORDER = [ 'Host', 'Date', 'OAM Begin', 'OAM End',
              'Merges Made', 'Total Merges',
              'OAM Last Cmd', 'emerge' ]
    
    @staticmethod
    def header():
        return (" " + KoamStatus.layout(dict(zip(KoamStatus.ORDER, KoamStatus.ORDER)))).replace("Merges Made Total Merges ", " Merges ")
    
    @staticmethod
    def layout(msg):
        KoamStatus.tidyup(msg)
        return "%(Host)-8s %(Date)-8s %(OAM Begin)9s %(OAM End)9s %(Merges Made)3s %(Total Merges)3s %(OAM Last Cmd)-25s %(emerge)s" % msg

    @staticmethod
    def removedate(date, timestamp):
        return timestamp[len(date)+1:] if timestamp.startswith(date) else timestamp
    
    @staticmethod
    def tidyup(msg):
        msg['OAM Begin'] = KoamStatus.removedate(msg['Date'], msg['OAM Begin'])
        msg['OAM End'] = KoamStatus.removedate(msg['Date'], msg['OAM End'])
        msg['OAM Last Cmd'] = msg['OAM Last Cmd'][:25]
        msg['emerge'] = msg['emerge'][:45]
        return msg

class KoamText(QTextBrowser):

    def __init__(self, parent = None):
        QTextBrowser.__init__(self, parent)
        self.setCurrentFont(KoamFont())
        self.setContextMenuPolicy(Qt.CustomContextMenu);
        self.customContextMenuRequested.connect(self.rightMenu)

    def rightMenu(self, pos):
        menu = QMenu()
        clearAction = menu.addAction("Clear")
        clearAction.triggered.connect(self.clear)
        menu.exec_(self.mapToGlobal(pos))

class KoamHost(QWidget):
    
    def __init__(self, parent = None): 
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.header = QLabel()
        self.header.setFont(KoamFont())
        self.logmsg = KoamText()
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.logmsg)
        self.setLayout(self.layout)

    def setHeader(self, hdr):
        self.header.setText(hdr)

    def add(self, msg):
        self.logmsg.append(msg)

class KoamView(QTabWidget):

    def __init__(self, parent = None): 
        QTabWidget.__init__(self, parent)
        self.tabs = {}

    def add(self, name): 
        self.tabs[name] = KoamHost()
        self.tabs[name].setHeader(KoamStatus.header())
        self.addTab(self.tabs[name], name)

    def update(self, name, message):
        if name not in self.tabs:
            self.add(name)
        self.tabs[name].add(KoamStatus.layout(message))

class KoamProcess(QProcess):
    
    def __init__(self, controller): 
        QProcess.__init__(self)
        self.controller = controller
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)

    def run(self, command, arguments):
        self.start(command, arguments)
        self.waitForStarted()

    def close(self):
        self.terminate()
        self.waitForFinished(1000)
        
    def out(self):
        for line in str(self.readAllStandardOutput()).splitlines():
            if sys.version_info > (3,0):
                self.controller.out(line[2:-3]) # remove leading/trailing garbage
            else:
                self.controller.out(line)

    def err(self):
        self.controller.err(self.readAllStandardError())

class KoamMainWindow(QMainWindow):

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.view = KoamView()
        self.setCentralWidget(self.view)
        self.statusBar().showMessage("Starting")
        self.resize(850,256)
        self.setWindowTitle("koam on " + os.uname()[1])
        self.show()

    def closeEvent(self, event):
        self.controller.close()
        event.accept()

class KoamController(QObject):
    
    def __init__(self):
        QObject.__init__(self)

    def run(self, argv):
        self.app = QApplication(argv)
        self.win = KoamMainWindow(self)
        self.proc = KoamProcess(self)
        self.proc.run("oam-status", ["rawnet"] + argv[1:])
        sys.exit(self.app.exec_())
        
    def close(self):
        self.proc.close()

    def out(self, msg):
        fields = json.loads(msg)
        self.win.view.update("Summary", fields)
        self.win.view.update(fields['Host'], fields)

    def err(self, msg):
        self.view.update("Error Log", msg)

if __name__ == "__main__":
    KoamController().run(sys.argv)

