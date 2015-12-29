#!/usr/bin/python

import logging
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamAddServer(QLineEdit):

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent)
        self.logger = logging.getLogger("koam.add.server")
        self.setPlaceholderText('Enter new server name(s) (space separated hostnames)')
        self.returnPressed.connect(self.add)

    def add(self):
        self.logger.log(logging.INFO, "adding server(s): %s", self.text())
        for server in str(self.text()).split():
            self.logger.log(logging.INFO, "adding server: %s", server)
            koam.KoamObserver.add_server(server)
        self.clear()
