# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import koam

class KoamPlasmoid(plasmascript.Applet):

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.setHasConfigurationInterface(False)
        self.setAspectRatioMode(Plasma.IgnoreAspectRatio)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)
        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)
        self.controller = koam.KoamController()
        self.koamwidget = koam.KoamWidget(self.controller)
        self.koamGraphicsWidget = self.scene().addWidget(self.koamwidget)
        self.controller.setWidget(self.koamwidget)
        self.layout.addItem(self.koamGraphicsWidget)
        self.applet.setLayout(self.layout)
        self.resize(850, 256)

def CreateApplet(parent):
    return KoamPlasmoid(parent)
