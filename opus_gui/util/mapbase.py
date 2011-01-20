# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString, Qt, QFileInfo, QObject, SIGNAL
from PyQt4.QtGui import QVBoxLayout

# QGIS bindings for mapping functions
# CK: avoid star imports
from qgis.core import *
from qgis.gui import *

# General system includes
import sys,string


# Main map class for all map related tools...
class MapBase(object):
    def __init__(self, mainwindow):
        self.mainwindow = mainwindow

        # create map canvas
        self.canvas = QgsMapCanvas(self.mainwindow.widgetMap)
        self.canvas.setCanvasColor(Qt.yellow)
        self.canvas.enableAntiAliasing(True)
        self.canvas.useQImageToRender(False)
        self.canvas.show()
        self.canvas.parentWin = mainwindow
        debugString = QString("Finished Loading Canvas...")
        self.mainwindow.statusbar.showMessage(debugString)

        # lay our widgets out in the main window
        self.layout = QVBoxLayout(self.mainwindow.widgetMap)
        self.layout.addWidget(self.canvas)

        # Link in the map tools
        QObject.connect(self.mainwindow.mpActionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        QObject.connect(self.mainwindow.mpActionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        QObject.connect(self.mainwindow.mpActionPan, SIGNAL("triggered()"), self.pan)

        # Map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.mainwindow.mpActionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)
        self.toolZoomIn.setAction(self.mainwindow.mpActionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)
        self.toolZoomOut.setAction(self.mainwindow.mpActionZoomOut)

        ##### Lets test out a simple map
        self.layers = []
        f = "data/st99_d00.shp"
        f_string = QString(f)
        info = QFileInfo(QString(f))

        # create layer
        layer = QgsVectorLayer(QString(f), info.completeBaseName(), "ogr")

        if not layer.isValid():
            # Deal with the error
            debugString = QString("Error Loading Layer...")
            self.mainwindow.statusbar.showMessage(debugString)
            return
        QgsMapLayerRegistry.instance().addMapLayer(layer)

        # set extent to the extent of our layer
        self.canvas.setExtent(layer.extent())

        # Set the transparency for the layer
        #layer.setTransparency(190)

        # set the map canvas layer set
        cl = QgsMapCanvasLayer(layer)
        self.layers.insert(0,cl)
        self.canvas.setLayerSet(self.layers)

    # Signal handeler for zoom in button
    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    # Signal handeler for zoom out button
    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    # Signal handeler for pan button
    def pan(self):
        self.canvas.setMapTool(self.toolPan)
