from PyQt5.QtWidgets import QAction

from .code import *

def classFactory(iface):
    return MinimalCheckPlugin(iface)


class  MinimalCheckPlugin:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        self.action = QAction('Check!', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        del self.action

    def run(self):
        check()
