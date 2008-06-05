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

from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.config.xmltree.opusxmlaction import OpusXMLAction

class OpusXMLTree(object):
    def __init__(self, toolboxbase, xmlType, parentWidget):
        # This parent reference is to be removed...
        self.parent = toolboxbase.mainwindow
        self.toolboxbase = toolboxbase
        self.mainwindow = toolboxbase.mainwindow
        self.xmlType = xmlType
        self.parentWidget = parentWidget
        self.addTree()

    def addTree(self):
        self.groupBox = QGroupBox(self.mainwindow)
        self.groupBoxLayout = QVBoxLayout(self.groupBox)
        self.model = OpusDataModel(self,self.toolboxbase.doc, self.mainwindow,
                                   self.toolboxbase.configFile, self.xmlType, True)
        self.view = OpusDataView(self.mainwindow)
        self.delegate = OpusDataDelegate(self.view)
        self.view.setItemDelegate(self.delegate)
        self.view.setModel(self.model)
        # Need to traverse the whole tree and expand the nodes if they default to open
        self.view.openDefaultItems()
        self.view.setAnimated(True)
        self.view.setColumnWidth(0,200)
        self.view.setColumnWidth(1,50)
        self.view.setMinimumHeight(200)

        self.groupBoxLayout.addWidget(self.view)
        self.parentWidget.addWidget(self.groupBox)

        # Hook up to the mousePressEvent and pressed
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.xmlAction = OpusXMLAction(self)

    def removeTree(self):
        if not self.model.isDirty():
            self.groupBox.hide()
            self.parentWidget.removeWidget(self.groupBox)
            return True
        else:
            return False
