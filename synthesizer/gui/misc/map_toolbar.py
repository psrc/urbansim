# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import sys, os

from regionTool import *
from pointSelectTool import *


qgis_prefix = "C:\qgis"

class Toolbar(QToolBar):
    def __init__(self, canvas, layer, parent=None):
        super(Toolbar, self).__init__(parent)

        self.canvas = canvas
        self.layer = layer

        self.mpActionZoomIn = QAction(self.canvas)
        self.mpActionZoomIn.setIcon(QIcon("./images/viewmag+.png"))
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")
        self.mpActionZoomIn.setToolTip("Zoom In")

        self.mpActionZoomOut = QAction(self.canvas)
        self.mpActionZoomOut.setIcon(QIcon("./images/viewmag-.png"))
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")
        self.mpActionZoomOut.setToolTip("Zoom Out")

        self.mpActionZoomFull = QAction(self.canvas)
        self.mpActionZoomFull.setIcon(QIcon("./images/viewmagfit.png"))
        self.mpActionZoomFull.setObjectName("mpActionZoomFull")
        self.mpActionZoomFull.setToolTip("Zoom Fit")

        self.mpActionPan = QAction(self.canvas)
        self.mpActionPan.setIcon(QIcon("./images/pan.png"))
        self.mpActionPan.setObjectName("mpActionPan")
        self.mpActionPan.setToolTip("Pan")

        self.mpActionSelect = QAction(self.canvas)
        self.mpActionSelect.setIcon(QIcon("./images/highlight.png"))
        self.mpActionSelect.setObjectName("mpActionSelect")
        self.mpActionSelect.setToolTip("Select")

        self.mpActionClickSelect = QAction(self.canvas)
        self.mpActionClickSelect.setIcon(QIcon("./images/highlight.png"))
        self.mpActionClickSelect.setObjectName("mpActionClickSelect")
        self.mpActionClickSelect.setToolTip("Select")


        # create a little toolbar
        self.addAction(self.mpActionZoomIn);
        self.addAction(self.mpActionZoomOut);
        self.addAction(self.mpActionZoomFull);
        self.addAction(self.mpActionPan);
        self.addAction(self.mpActionClickSelect);
        self.addAction(self.mpActionSelect);
        # create the map tools
        self.toolClickSelect = ClickTool(self.canvas)
        self.toolClickSelect.setAction(self.mpActionClickSelect)
        self.toolSelect = regionTool(self.canvas)
        self.toolSelect.setAction(self.mpActionSelect)
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.mpActionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomIn.setAction(self.mpActionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        self.toolZoomOut.setAction(self.mpActionZoomOut)

        # create the actions behaviours
        self.connect(self.mpActionZoomIn, SIGNAL("triggered()"), self.zoomIn)
        self.connect(self.mpActionZoomOut, SIGNAL("triggered()"), self.zoomOut)
        self.connect(self.mpActionZoomFull, SIGNAL("triggered()"), self.zoomFull)
        self.connect(self.mpActionPan, SIGNAL("triggered()"), self.pan)
        self.connect(self.mpActionSelect, SIGNAL("triggered()"), self.select)
        self.connect(self.mpActionClickSelect, SIGNAL("triggered()"), self.clickSelect)
        self.connect(self.toolSelect.o, SIGNAL("finished()"), self.doneRectangle)
        self.connect(self.toolClickSelect.o, SIGNAL("finished()"), self.donePointSelect)

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def zoomFull(self):
        self.canvas.zoomFullExtent()

    def pan(self):
        self.canvas.setMapTool(self.toolPan)

    def select(self):
        self.canvas.setMapTool(self.toolSelect)
        self.toolSelect.canvas.setCursor(self.toolSelect.cursor)

    def clickSelect(self):
        self.canvas.setMapTool(self.toolClickSelect)
        self.toolSelect.canvas.setCursor(self.toolClickSelect.cursor)

    def donePointSelect(self):
        provider = self.layer.getDataProvider()
        allAttrs = provider.allAttributesList()
        renderer = self.layer.renderer()
        self.layer.select(self.toolClickSelect.bb, False)
        provider.select(allAttrs, self.toolClickSelect.bb, True, True)
        feat = QgsFeature()
        provider.getNextFeature(feat)
        attrMap = feat.attributeMap()
        self.emit(SIGNAL("currentGeoChanged"), provider, feat)

    def doneRectangle(self):
        provider = self.layer.getDataProvider()
        allAttrs = provider.allAttributesList()
        self.layer.select(self.toolSelect.bb, False)
        provider.select(allAttrs, self.toolSelect.bb, True, True)
        feat = QgsFeature()

        while provider.getNextFeature(feat):
            attrMap = feat.attributeMap()
            if feat.geometry().wkbType() == QGis.WKBPoint:
                transform = self.canvas.getCoordinateTransform()
                devicepoint = transform.transform(feat.geometry().asPoint())
                #print devicepoint.x(), devicepoint.y()
                dummy = ""
            for (i, attr) in attrMap.iteritems():
                if i == 0:
                    dummy = '"%s"' % attr.toString().trimmed()
                else:
                    dummy += ',"%s"' % attr.toString().trimmed()
            #print "Field Values: " + dummy, feat.featureId()

    def hideDragTool(self):
        self.mpActionSelect.setVisible(False)

    def hideSelectTool(self):
        self.mpActionClickSelect.setVisible(False)

    def activateClickSelectTool(self):
        pass



def main():
    app = QApplication(sys.argv)
    QgsApplication.setPrefixPath(qgis_prefix, True)
    QgsApplication.initQgis()


    Toolbar.show()
    app.exec_()

    QgsApplication.exitQgis()


if __name__ == "__main__":
    main()

