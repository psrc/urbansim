# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QDialog, QVBoxLayout

from opus_gui.abstract_manager.views.xml_view import XmlView
from opus_gui.abstract_manager.models.xml_item_delegate import XmlItemDelegate
from opus_gui.abstract_manager.views.ui_cloneinherited import Ui_CloneInheritedGui


class CloneInheritedGui(QDialog, Ui_CloneInheritedGui):
    def __init__(self, xml_controller, fl, model, clone):
        QDialog.__init__(self, xml_controller.mainwindow, fl)
        self.setupUi(self)
        self.xml_controller = xml_controller
        self.model = model
        # Since we are referencing the main model we want to now make it
        # read-only while traversing it...
        self.model.editable = False;
        # Add in the base XML for user to select the drop point
        self.vboxlayout = QVBoxLayout(self.xmlBox)
        self.vboxlayout.setObjectName("vboxlayout")
        self.view = XmlView(self.xmlBox)
        self.delegate = XmlItemDelegate(self.view)
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

