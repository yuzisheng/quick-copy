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
        self.vector_layer = None
        if isinstance(self.iface.activeLayer(), QgsVectorLayer) and self.iface.activeLayer().isSpatial():
            self.vector_layer = self.iface.activeLayer()
        QgsMapToolIdentifyFeature.__init__(self, self.canvas, self.vector_layer)
        self.iface.currentLayerChanged.connect(self.change_layer)

    def change_layer(self, current_layer):
        if self.vector_layer:
            self.vector_layer.removeSelection()
        if isinstance(current_layer, QgsVectorLayer) and current_layer.isSpatial():
            self.vector_layer = current_layer
            self.setLayer(current_layer)
        else:
            self.vector_layer = None

    def activate(self):
        self.canvas.setCursor(QCursor(QPixmap(":/icons/quick_copy_cursor.png"), 1, 1))

    def canvasPressEvent(self, event):
        clipboard = QApplication.clipboard()
        if self.vector_layer:
            identified_features = self.identify(event.x(), event.y(), [self.vector_layer], QgsMapToolIdentify.TopDownAll)
            if len(identified_features) != 0:
                selected_feature_id = identified_features[0].mFeature.id()
                self.vector_layer.selectByIds([selected_feature_id], QgsVectorLayer.SetSelection)
                selected_feature = self.vector_layer.selectedFeatures()[0]
                clipboard.setText(f"{selected_feature.geometry().asWkt()}")
                self.iface.messageBar().pushMessage("[QuickCopy] Feature selected and wkt copied: FeatureId={}. ({})".format(selected_feature_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            else:
                clipboard.setText("[QuickCopy] No feature selected.")
                self.iface.messageBar().pushMessage("[QuickCopy] No feature selected. ({})".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        else:
            clipboard.setText("[QuickCopy] No feature selected.")
            self.iface.messageBar().pushMessage("[QuickCopy] Current layer is not a vector layer. ({})".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def deactivate(self):
        if self.vector_layer:
            self.vector_layer.removeSelection()
