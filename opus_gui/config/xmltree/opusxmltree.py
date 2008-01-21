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

from opus_gui.config.xmlmodelview.opusdatamodel import OpusDataModel
from opus_gui.config.xmlmodelview.opusdatadelegate import OpusDataDelegate
from opus_gui.config.xmltree.opusxmlaction import OpusXMLAction

class OpusXMLTree(object):
  def __init__(self, parent,xmlType,parentWidget):    
    self.addTree(parent,xmlType,parentWidget)

  def addTree(self, parent,xmlType,parentWidget):
    #parent is a toolboxBase object
    self.parent = parent.parent
    self.parentTool = parent
    self.xmlType = xmlType
    self.parentWidget = parentWidget
    self.groupBox = QGroupBox(self.parent)
    self.groupBoxLayout = QVBoxLayout(self.groupBox)
    self.model = OpusDataModel(self,self.parentTool.doc, self.parent,
                               self.parentTool.configFile, self.xmlType, True)
    self.view = QTreeView(self.parent)
    self.delegate = OpusDataDelegate(self.view)
    self.view.setItemDelegate(self.delegate)
    self.view.setModel(self.model)
    self.view.expandAll()
    self.view.setAnimated(True)
    self.view.setColumnWidth(0,200)
    self.view.setColumnWidth(1,50)
    self.view.setMinimumHeight(200)
    
    self.groupBoxLayout.addWidget(self.view)
    self.groupBox.setTitle(QFileInfo(self.parentTool.xml_file).filePath())
    self.parentWidget.addWidget(self.groupBox)
    
    # Hook up to the mousePressEvent and pressed
    self.view.setContextMenuPolicy(Qt.CustomContextMenu)
    self.xmlAction = OpusXMLAction(self)

  def removeTree(self):
    if not self.model.dirty:
      self.groupBox.hide()
      self.parentWidget.removeWidget(self.groupBox)
      return True
    else:
      return False
