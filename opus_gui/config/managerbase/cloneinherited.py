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
from opus_gui.config.managerbase.cloneinherited_ui import Ui_CloneInheritedGui

import random

class CloneInheritedGui(QDialog, Ui_CloneInheritedGui):
    def __init__(self, opusXMLAction_xxx, fl, model, clone):
        QDialog.__init__(self, opusXMLAction_xxx.mainwindow, fl)
        self.setupUi(self)
        self.opusXMLAction_xxx = opusXMLAction_xxx
        self.model = model
        # Since we are referencing the main model we want to now make it
        # read-only while traversing it...
        self.model.editable = False;
        # Add in the base XML for user to select the drop point
        self.vboxlayout = QVBoxLayout(self.xmlBox)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = OpusDataView(self.xmlBox)
        self.delegate = OpusDataDelegate(self.view)
        self.view.setItemDelegate(self.delegate)
        self.view.setModel(self.model)
        self.view.openDefaultItems()
        self.view.setAnimated(True)
        self.view.setColumnWidth(0,200)
        self.view.setColumnWidth(1,50)
        self.view.setMinimumHeight(200)
        self.vboxlayout.addWidget(self.view)

    def on_createXML_released(self):
        # Clone the node and drop it in...
        item = self.view.currentIndex().internalPointer()
        domNode = item.node()
        if domNode.isNull():
            return
        # Handle ElementNodes
        if domNode.isElement():
            domElement = domNode.toElement()
            if domElement.isNull():
                return
            print domElement.tagName()
            # Here we can drop the clone into the model at the right spot
            parentIndex = self.view.currentIndex()
            self.model.insertRow(self.model.rowCount(parentIndex),
                                 parentIndex,
                                 self.clone)
            self.model.emit(SIGNAL("layoutChanged()"))
        # Since we are referencing the main model we want to now make it
        # editable again...
        self.model.editable = True;
        self.close()

    def on_cancelXML_released(self):
        # Close things up...
        # Since we are referencing the main model we want to now make it
        # editable again...
        self.model.editable = True;
        self.close()

