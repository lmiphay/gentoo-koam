#!/usr/bin/python

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamFont(QFont):
    
    def __init__(self): 
        QFont.__init__(self, "Monospace", 8)
