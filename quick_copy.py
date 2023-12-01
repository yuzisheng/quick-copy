# -*- coding: utf-8 -*-
"""
@Description    : Click to select one feature and copy the wkt to paste-board automatically.
@Author         : Zisheng Yu
@Date           : 2023-12-01
"""

from os import path

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction

from . import resources
from .copy_tool import CopyTool


class QuickCopy:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = path.dirname(__file__)
        self.action = None
        self.mapTool = None

    def initGui(self):
        self.action = QAction("QuickCopy", self.iface.mainWindow())
        self.action.setIcon(QIcon(":/icons/quick_copy_cursor.png"))
        self.action.setWhatsThis("QuickCopy")
        self.iface.addPluginToMenu("QuickCopy", self.action)
        self.iface.addToolBarIcon(self.action)
        self.action.triggered.connect(self.run)
        self.mapTool = CopyTool(self.iface)

    def unload(self):
        self.iface.removeToolBarIcon(self.action)
        self.iface.removePluginMenu("QuickCopy", self.action)
        self.action.deleteLater()
        if self.iface.mapCanvas().mapTool() == self.mapTool:
            self.iface.mapCanvas().unsetMapTool(self.mapTool)
        del self.mapTool

    def run(self):
        self.iface.mapCanvas().setMapTool(self.mapTool)
