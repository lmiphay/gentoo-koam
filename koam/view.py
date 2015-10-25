#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamView(QTabWidget):

    def __init__(self, parent = None): 
        QTabWidget.__init__(self, parent)
        self.tabs = {}

    def add(self, name): 
        self.tabs[name] = koam.KoamHost()
        self.tabs[name].setHeader(koam.KoamStatus.header())
        self.addTab(self.tabs[name], name)

    def update(self, name, message):
        self.message(name, koam.KoamStatus.layout(message))

    def message(self, topic, msg):
        if topic not in self.tabs:
            self.add(topic)
        self.tabs[topic].add(msg)
