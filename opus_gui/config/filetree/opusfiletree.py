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

from opus_gui.config.filetree.opusfileaction import OpusFileAction

class OpusFileTree(object):
    def __init__(self, toolboxbase, opusDataPath, parentWidget):
        self.addTree(toolboxbase,opusDataPath,parentWidget)


    def addTree(self, toolboxbase,opusDataPath,parentWidget):
        self.mainwindow = toolboxbase.mainwindow
        self.toolboxBase = toolboxbase
        self.containerWidget = parentWidget
        self.opusDataPath = opusDataPath

        self.groupBox = QGroupBox(self.mainwindow)
        self.groupBoxLayout = QVBoxLayout(self.groupBox)

        self.treeview = QTreeView(self.mainwindow)
        filters = QStringList()
        filters.append("*.*")
        #filters.append("*.py")
        #filters.append("*.shp")
        #filters.append("*.tif")
        self.model = QDirModel(filters, QDir.Files|QDir.AllDirs|QDir.NoDotAndDotDot, QDir.Name)
        self.treeview.setModel(self.model)
        if self.opusDataPath:
            self.treeview.setRootIndex(self.model.index(self.opusDataPath))
        self.treeview.setColumnWidth(0,200)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.groupBoxLayout.addWidget(self.treeview)
        #self.groupBox.setTitle(QFileInfo(self.toolboxbase.xml_file).filePath())
        self.containerWidget.addWidget(self.groupBox)

        # Hook up to the mousePressEvent and pressed
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)
        self.xmlAction = OpusFileAction(self)

    def removeTree(self):
        self.groupBox.hide()
        self.containerWidget.removeWidget(self.groupBox)
        return True
