# UrbanSim software. Copyright (C) 1998-2007 University of Washington
# 
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
# 


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# QGIS bindings for mapping functions
from qgis.core import *
from qgis.gui import *

# General system includes
import sys,string


# Main map class for all map related tools...
class MapBase(object):
    def __init__(self, parent):
        self.parent = parent

        # create map canvas
        self.canvas = QgsMapCanvas(self.parent.widgetMap)
        self.canvas.setCanvasColor(Qt.yellow)
        self.canvas.enableAntiAliasing(True)
        self.canvas.useQImageToRender(False)
        self.canvas.show()
        self.canvas.parentWin = parent
        debugString = QString("Finished Loading Canvas...")
        self.parent.statusbar.showMessage(debugString)

        # lay our widgets out in the main window
        self.layout = QVBoxLayout(self.parent.widgetMap)
        self.layout.addWidget(self.canvas)

        # Link in the map tools
        QObject.connect(self.parent.mpActionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        QObject.connect(self.parent.mpActionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        QObject.connect(self.parent.mpActionPan, SIGNAL("triggered()"), self.pan)

        # Map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.parent.mpActionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False)
        self.toolZoomIn.setAction(self.parent.mpActionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True)
        self.toolZoomOut.setAction(self.parent.mpActionZoomOut)

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
            self.parent.statusbar.showMessage(debugString)
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
