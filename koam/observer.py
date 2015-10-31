#!/usr/bin/python

import sys
import logging
import koam

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class KoamObserver(QObject):

     attach = pyqtSignal('QString')
     remove = pyqtSignal('QString')
     
     def __init__(self):
          QObject.__init__(self)
          self.logger = logging.getLogger("koam.observer")
         
     @pyqtSlot('QString')
     def log_add(self, name):
          self.logger.log(logging.INFO, "adding server %s", name)
        
     @pyqtSlot('QString')
     def log_rem(self, name):
          self.logger.log(logging.INFO, "removing server %s", name)

     @staticmethod
     def connect_add(method):
          _BROKER.attach.connect(method)
         
     @staticmethod
     def disconnect_add(method):
          _BROKER.attach.disconnect(method)

     @staticmethod
     def connect_rem(method):
          _BROKER.remove.connect(method)
         
     @staticmethod
     def disconnect_rem(method):
          _BROKER.remove.disconnect(method)

     @staticmethod
     def add_server(name):
          _BROKER.attach.emit(name)

     @staticmethod
     def rem_server(name):
          _BROKER.remove.emit(name)
         
     def startup(self):
          self.connect_add(self.log_add)
          self.connect_rem(self.log_rem)
         
     def shutdown(self):
          self.disconnect_add(self.log_add)
          self.disconnect_rem(self.log_rem)
        
_BROKER = KoamObserver()
_BROKER.startup()
