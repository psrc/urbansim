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
from PyQt4.QtCore import QObject, SIGNAL, Qt

from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate


class OpusXMLController(object):
    def __init__(self, toolboxbase, xml_type, parentWidget, addTree, listen_to_menu = True):
        
        self.toolboxbase = toolboxbase
        self.mainwindow = toolboxbase.mainwindow
        self.xmlType = xml_type
        self.parentWidget = parentWidget

        if addTree:
            self.addTree(listen_to_menu = listen_to_menu)


    def addTree(self, listen_to_menu):
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
        
        if listen_to_menu:
            QObject.connect(self.view,
                            SIGNAL("customContextMenuRequested(const QPoint &)"),
                            self.processCustomMenu)

    def removeTree(self):
        if not self.model.isDirty():
            self.view.hide()
            self.parentWidget.removeWidget(self.view)
            return True
        else:
            return False


    def processCustomMenu(self, position):
        raise Exception('Method processCustomMenu is not implemented')

