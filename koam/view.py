#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import koam

class KoamView(QTabWidget):

    SUMMARY_TAB = 'All'

    def __init__(self, parent = None): 
        QTabWidget.__init__(self, parent)
        self.setTabPosition(QTabWidget.West)
        self.tabs = {}
        self.index = {}
        self.progress = koam.KoamProgress()
        self.addTab(self.progress, "Progress")
        self.add(self.SUMMARY_TAB)

    def add(self, name): 
        self.tabs[name] = koam.KoamHost(name)
        self.tabs[name].setHeader(koam.KoamStatus.header())
        self.index[name] = self.addTab(self.tabs[name], name)

    def remove(self, name):
        self.removeTab(self.index[name])
        del self.index[name]
        del self.tabs[name]

    def update(self, name, message):
        self.message(name, koam.KoamStatus.layout(message))
        if name != self.SUMMARY_TAB:
            self.progress.update(name, koam.KoamStatus.merges(message))

    def message(self, topic, msg):
        if topic not in self.tabs:
            self.add(topic)
        self.tabs[topic].add(msg)
