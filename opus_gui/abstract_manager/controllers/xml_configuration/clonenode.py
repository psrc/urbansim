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
from PyQt4.QtCore import SIGNAL, QString, Qt
from PyQt4.QtGui import QDialog, QMessageBox

from opus_gui.abstract_manager.views.ui_clonenode import Ui_CloneNodeGui

class CloneNodeGui(QDialog, Ui_CloneNodeGui):
    def __init__(self, xml_controller, clone, parentNode, model):
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | \
            Qt.WindowMaximizeButtonHint
        QDialog.__init__(self, xml_controller.mainwindow, flags)
        self.setupUi(self)
        self.xml_controller = xml_controller
        self.clone = clone
        self.parentNode = parentNode
        self.model = model
        self.setModal(True)

    def on_createXML_released(self):
        newNameWithSpace = self.newName.text()
        newName = newNameWithSpace.replace(QString(" "),QString("_"))
        nodeElement = self.clone.toElement()
        if not nodeElement.isNull():
            nodeElement.setTagName(newName)
            # Swap in the new name and drop in the node...
            self.model.insertRow(self.model.rowCount(self.parentNode),
                                 self.parentNode,
                                 self.clone)
            self.model.emit(SIGNAL("layoutChanged()"))
        else:
            # TODO: Send up an error
            pass
        self.close()

    def on_cancelXML_released(self):
        # Close things up...
        self.close()
        
class RenameNodeGui(CloneNodeGui):
    def __init__(self, xml_controller, node):
        CloneNodeGui.__init__(self, xml_controller, None, None, None)
        
        # check that we got a valid node
        if not node.isElement():
            QMessageBox.warning(self, 'Invalid node',
                                'Ignoring rename request for non element node.')
            self.close()
        
        # dialog is identical to clone node dialog except for some text strings
        self.label.setText('Please select a new name')
        self.createXML.setText('Rename')
        self.newName.setText(node.tagName())
        
        self.node = node
        self.xml_controller = xml_controller
        
    def on_createXML_released(self):
        # update the node tag name
        name = self.newName.text()
        name = name.replace(' ', '_')
        element = self.node.toElement()
        element.setTagName(name)
        self.xml_controller.model.emit(SIGNAL('layoutChanged()'))
        self.close()
