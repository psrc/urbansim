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
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from opus_gui.config.xmlmodelview.opusdataview import OpusDataView
from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.config.managerbase.clonenode_ui import Ui_CloneNodeGui

import random

class CloneNodeGui(QDialog, Ui_CloneNodeGui):
    def __init__(self, opusXMLAction_xxx, fl, clone, parentNode, model):
        QDialog.__init__(self, opusXMLAction_xxx.mainwindow, fl)
        self.setupUi(self)
        self.opusXMLAction_xxx = opusXMLAction_xxx
        self.clone = clone
        self.parentNode = parentNode
        self.model = model

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

