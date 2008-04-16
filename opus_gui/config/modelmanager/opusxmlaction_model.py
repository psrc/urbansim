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
from PyQt4.QtXml import *

from opus_gui.run.estimation.opusrunestimation import OpusEstimation
from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui


class OpusXMLAction_Model(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainwindow = parent.mainwindow
        self.xmlTreeObject = parent.xmlTreeObject

        self.currentColumn = None
        self.currentIndex = None

        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")

        self.actPlaceHolder = QAction(self.applicationIcon,
                                      "Placeholder",
                                      self.xmlTreeObject.parent)
        QObject.connect(self.actPlaceHolder,
                        SIGNAL("triggered()"),
                        self.placeHolderAction)

        self.actRunEstimation = QAction(self.applicationIcon,
                                        "Run Estimation",
                                        self.xmlTreeObject.parent)
        QObject.connect(self.actRunEstimation,
                        SIGNAL("triggered()"),
                        self.runEstimationAction)

        self.actCloneNode = QAction(self.applicationIcon,
                                    "Clone Down To Child",
                                    self.xmlTreeObject.parent)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNodeAction)

    def placeHolderAction(self):
        #print "placeHolderAction pressed with column = %s and item = %s" % \
        #      (self.currentColumn,
        #       self.currentIndex.internalPointer().node().toElement().tagName())
        pass

    def runEstimationAction(self):
        # First confirm that the project file needs to be saved
        # before running the estimation...
        if not self.xmlTreeObject.model.dirty:
            newEstimation = OpusEstimation(self.xmlTreeObject,
                                           self.xmlTreeObject.parentTool.xml_file)
            self.xmlTreeObject.parent.runManagerStuff.addNewEstimationRun(newEstimation)
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Save changes to project before running estimation")

    def cloneNodeAction(self):
        print "Clone Node pressed..."
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneInheritedGui(self,flags,self.xmlTreeObject.model,clone)
        window.show()

    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                if domElement.hasAttribute(QString("inherited")) and \
                       domElement.hasAttribute(QString("cloneable")) and \
                       domElement.attribute(QString("cloneable")) == QString("True"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actCloneNode)
                    self.menu.exec_(QCursor.pos())
                elif domElement.tagName() == QString("models_to_estimate"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actRunEstimation)
                    self.menu.exec_(QCursor.pos())
                else:
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actPlaceHolder)
                    self.menu.exec_(QCursor.pos())
        return


