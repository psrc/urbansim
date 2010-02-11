# PopGen 1.1 is A Synthetic Population Generator for Advanced
# Microsimulation Models of Travel Demand
# Copyright (C) 2009, Arizona State University
# See PopGen/License

#-----------------------------------------------------------
#
# Generate Random Points
#
# A QGIS plugin for generating a simple random points
# shapefile.
#
# Copyright (C) 2008  Carson Farmer
#
# EMAIL: carson.farmer (at) gmail.com
# WEB  : www.geog.uvic.ca/spar/carson
#
#-----------------------------------------------------------
#
# licensed under the terms of GNU GPL 2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
#---------------------------------------------------------------------

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from random import *
import math

class RandPoints():
    def __init__(self, Dialog):
        self.progressBar = QProgressBar()
        self.progressBar.setProperty("value",QVariant(24))
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")
        #self.gridlayout.addWidget(self.progressBar,7,0,1,1)
        self.progressBar.setValue(0)

# when 'OK' button is pressed, gather required inputs, and initiate random points generation
    def accept(self, path, hhfreqvar):
        self.progressBar.setValue(2.5)

        inlayerpath = path + '_sel' + '.shp'
        inLayer = QgsVectorLayer(inlayerpath, "SelCounties", "ogr")
        outPath = path + '_hhpoints' + '.shp'
        self.progressBar.setValue(5)
        design = "field"
        value = hhfreqvar
        minimum = 0.00
        self.progressBar.setValue(10)
        self.randomize(inLayer, outPath, minimum, design, value, self.progressBar)
        self.progressBar.setValue(100)
        #addToTOC = QMessageBox.question(self, "Random Points", "Created output point Shapefile:\n" + outPath
        #    + "\n\nWould you like to add the new layer to the TOC?", QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        #if addToTOC == QMessageBox.Yes:
        #    self.vlayer = QgsVectorLayer(outPath, unicode(outName), "ogr")
        #    QgsMapLayerRegistry.instance().addMapLayer(self.vlayer)
        self.progressBar.setValue(0)
        return outPath
# Generate list of random points
    def simpleRandom(self, n, bound, xmin, xmax, ymin, ymax):
        seed()
        points = []
        i = 1
        while i <= n:
            pGeom = QgsGeometry().fromPoint(QgsPoint(xmin + (xmax-xmin) * random(), ymin + (ymax-ymin) * random()))
            if pGeom.intersects(bound):
                points.append(pGeom)
                i = i + 1
        return points

# Get vector layer by name from TOC
    def getVectorLayerByName(self, myName):
        mc = self.iface.getMapCanvas()
        nLayers = mc.layerCount()
        for l in range(nLayers):
            layer = mc.getZpos(l)
            if layer.name() == unicode(myName):
                vlayer = QgsVectorLayer(unicode(layer.source()),  unicode(myName),  unicode(layer.getDataProvider().name()))
                if vlayer.isValid():
                    return vlayer
                else:
                    QMessageBox.information(self, "Generate Centroids", "Vector layer is not valid")

# Get map layer by name from TOC
    def getMapLayerByName(self, myName):
        mc = self.iface.getMapCanvas()
        nLayers = mc.layerCount()
        for l in range(nLayers):
            layer = mc.getZpos(l)
            if layer.name() == unicode(myName):
                if layer.isValid():
                    return layer

# Retreive the field map of a vector Layer
    def getFieldList(self, vlayer):
        fProvider = vlayer.getDataProvider()
        feat = QgsFeature()
        allAttrs = fProvider.allAttributesList()
        fProvider.select(allAttrs)
        myFields = fProvider.fields()
        return myFields


    def randomize(self, inLayer, outPath, minimum, design, value, progressBar):
        outFeat = QgsFeature()
        points = self.loopThruPolygons(inLayer, value, design, progressBar)

        fields = { 0 : QgsField("ID", QVariant.Int) }
        check = QFile(outPath)
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile(outPath):
                print "Problem"
                return
        writer = QgsVectorFileWriter(outPath, "CP1250", fields, QGis.WKBPoint, None)
        #writer = QgsVectorFileWriter(unicode(outPath), "CP1250", fields, QGis.WKBPoint, None)
        idVar = 0
        count = 70.00
        add = 30.00 / len(points)
        for i in points:
            outFeat.setGeometry(i)
            outFeat.addAttribute(0, QVariant(idVar))
            writer.addFeature(outFeat)
            idVar = idVar + 1
            count = count + add
            progressBar.setValue(count)
        del writer

#
    def loopThruPolygons(self, inLayer, numRand, design, progressBar):
        sProvider = inLayer.getDataProvider()
        sAllAttrs = sProvider.allAttributesList()
        sProvider.select(sAllAttrs)
        sFeat = QgsFeature()
        sGeom = QgsGeometry()
        sPoints = []
        if design == "field":
            for (i, attr) in sProvider.fields().iteritems():
                if (unicode(numRand) == attr.name()): index = i #get input field index
        count = 10.00
        add = 60.00 / sProvider.featureCount()
        while sProvider.getNextFeature(sFeat):
            sGeom = sFeat.geometry()
            if design == "density":
                sDistArea = QgsDistanceArea()
                value = int(round(numRand * sDistArea.measure(sGeom)))
            elif design == "field":
                sAtMap = sFeat.attributeMap()
                value = sAtMap[index].toInt()[0]
            else:
                value = numRand
            sExt = sGeom.boundingBox()
            sPoints.extend(self.simpleRandom(value, sGeom, sExt.xMin(), sExt.xMax(), sExt.yMin(), sExt.yMax()))
            count = count + add
            progressBar.setValue(count)
        return sPoints
