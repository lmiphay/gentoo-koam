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
    
    def __init__(self, controller, cmd, argv): 
        QProcess.__init__(self)
        self.controller = controller
        self.cmd = cmd
        self.argv = argv
        self.readyReadStandardOutput.connect(self.out)
        self.readyReadStandardError.connect(self.err)

    def run(self):
        self.start(self.cmd, self.argv)
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

class KoamMainWindow(QMainWindow):

    def __init__(self, controller):
        QMainWindow.__init__(self)
        self.controller = controller
        self.addToolBar(KoamToolbar(self, controller))
        self.view = KoamView()
        self.setCentralWidget(self.view)
        self.msg("Startup")
        self.resize(850,256)
        self.setWindowTitle("koam on " + os.uname()[1])
        self.show()

    def closeEvent(self, event):
        self.controller.close()
        event.accept()

    def msg(self, text):
        self.statusBar().showMessage(text)

class KoamController(QObject):
    
    def __init__(self, argv):
        QObject.__init__(self)
        self.app = QApplication(argv)
        self.win = KoamMainWindow(self)
        self.proc = KoamProcess(self, "oam-status", ["rawnet"] + argv[1:])

    def startProc(self):
        self.win.msg("Running")
        self.proc.run() # default on/off?
        
    def run(self):
        self.startProc()
        return self.app.exec_()
        
    def close(self):
        self.proc.close()

    def out(self, msg):
        try:
            fields = json.loads(msg)
            self.win.view.update("All", fields)
            self.win.view.update(fields['Host'], fields)
        except ValueError:
            self.err("ValueError exception for: " + msg)
        except:
            self.err("Unexpected exception for: " + msg + ", " + sys.exc_info()[0])

    def err(self, msg):
        self.win.view.update("Error Log", msg)

if __name__ == "__main__":
    sys.exit(KoamController(sys.argv).run())
