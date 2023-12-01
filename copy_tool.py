# -*- coding: utf-8 -*-
"""
@Description    : Click to select one feature and copy the wkt to paste-board automatically.
@Author         : Zisheng Yu
@Date           : 2023-12-01
"""

from datetime import datetime

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QApplication, QMessageBox

from qgis.core import *
from qgis.gui import *

from . import resources


class CopyTool(QgsMapToolIdentifyFeature):

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.layer = self.iface.activeLayer()
        QgsMapToolIdentifyFeature.__init__(self, self.canvas, self.layer)
        self.iface.currentLayerChanged.connect(self.active_changed)
        self.cursor = QCursor(QPixmap(":/icons/quick_copy_cursor.png"), 1, 1)

    def active_changed(self, layer):
        self.layer.removeSelection()
        if isinstance(layer, QgsVectorLayer) and layer.isSpatial():
            self.layer = layer
            self.setLayer(self.layer)

    def activate(self):
        self.canvas.setCursor(self.cursor)

    def canvasPressEvent(self, event):
        clipboard = QApplication.clipboard()
        identified_features = self.identify(event.x(), event.y(), [self.layer], QgsMapToolIdentify.TopDownAll)
        self.layer.selectByIds([f.mFeature.id() for f in identified_features], QgsVectorLayer.SetSelection)
        selected_features = self.layer.selectedFeatures()
        if selected_features is not None and len(selected_features) != 0:
            clipboard.setText(f'{selected_features[0].geometry().asWkt()}')
            self.iface.messageBar().pushMessage("[QuickCopy] Feature selected and wkt copied. ({})".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            clipboard.setText("[QuickCopy] No feature selected.")
            self.iface.messageBar().pushMessage("[QuickCopy] No feature selected. ({})".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def deactivate(self):
        self.layer.removeSelection()
