# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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
from PyQt4.QtCore import Qt

from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.config.xmltree.opusxmlaction import OpusXMLAction

class OpusXMLTree(object):
    def __init__(self, toolboxbase, xmlType, parentWidget, addTree=True):
        self.toolboxbase = toolboxbase
        self.mainwindow = toolboxbase.mainwindow
        self.xmlType = xmlType
        self.parentWidget = parentWidget
        if addTree:
            self.addTree()

    def addTree(self):
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

        self.parentWidget.addWidget(self.view)
        # Hook up to the mousePressEvent and pressed
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.xmlAction = OpusXMLAction(self)

    def removeTree(self):
        if not self.model.isDirty():
            self.view.hide()
            self.parentWidget.removeWidget(self.view)
            return True
        else:
            return False
