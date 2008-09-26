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
from opus_gui.config.xmltree.opusxmltree import OpusXMLTree
from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.config.xmltree.opusxmlaction import OpusXMLAction


class DatabaseConfigXMLTree(OpusXMLTree):
    def __init__(self, toolboxbase, xmlType, parentWidget, addTree=True):
        OpusXMLTree.__init__(self, toolboxbase, xmlType, parentWidget, addTree)
        
    def addTree(self):
        self.model = DatabaseConfigXMLModel(self, self.toolboxbase.doc, self.mainwindow,
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
        
        
        
class DatabaseConfigXMLModel(OpusDataModel):
    def __init__(self, parentTree, document, mainwindow, configFile, xmlType, editable, addIcons=True):
        OpusDataModel.__init__(self, parentTree, document, mainwindow, configFile, xmlType, editable, addIcons)
        
    def flags(self, index):
        default_flags = super(DatabaseConfigXMLModel, self).flags(index);
        if index.isValid() and self.editable and index.column()==0:
            return default_flags & ~Qt.ItemIsEditable
        else: return default_flags