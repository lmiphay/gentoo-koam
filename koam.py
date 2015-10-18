#!/usr/bin/python

import sys
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
        msg['emerge'] = msg['emerge'][:30]
        return msg
 
class KoamHost(QWidget):
    
    def __init__(self, parent = None): 
        QWidget.__init__(self, parent)
        self.layout = QVBoxLayout()
        self.header = QLabel()
        self.header.setFont(KoamFont())
        self.logmsg = QTextBrowser()
        self.logmsg.setCurrentFont(KoamFont())
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

    def closeEvent(self, event):
        self.proc.close()
        event.accept()

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

class KoamController(QObject):
    
    def __init__(self):
        QObject.__init__(self)

    def run(self, argv):
        self.app = QApplication(argv)
        self.view = KoamView()
        self.proc = KoamProcess(self)
        self.view.proc = self
        self.view.resize(850,256)
        self.view.show()
        self.proc.run("oam-status", ["rawnet"] + argv[1:])
        sys.exit(self.app.exec_())
        
    def close(self):
        self.proc.close()

    def out(self, msg):
        fields = json.loads(msg)
        self.view.update("Summary", fields)
        self.view.update(fields['Host'], fields)

    def err(self, msg):
        self.view.update("Error Log", msg)

if __name__ == "__main__":
    KoamController().run(sys.argv)

