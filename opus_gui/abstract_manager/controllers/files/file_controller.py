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
from PyQt4.QtCore import Qt, QStringList, QDir, QObject, SIGNAL
from PyQt4.QtGui import QTreeView, QDirModel

class FileController(object):
    def __init__(self, toolboxbase, controller_type,opusDataPath, parentWidget, listen_to_menu = True):
        self.controller_type = controller_type

        self.addTree(toolboxbase,opusDataPath,parentWidget)

        self.currentColumn = None
        self.currentIndex = None
        self.classification = ""

        if listen_to_menu:
            QObject.connect(self.treeview,
                            SIGNAL("customContextMenuRequested(const QPoint &)"),
                            self.processCustomMenu)


    def addTree(self, toolboxbase,opusDataPath,parentWidget):
        self.mainwindow = toolboxbase.mainwindow
        self.toolboxBase = toolboxbase
        self.containerWidget = parentWidget
        self.opusDataPath = opusDataPath

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

        self.containerWidget.addWidget(self.treeview)

        # Hook up to the mousePressEvent and pressed
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)

    def removeTree(self):
        self.treeview.hide()
        self.containerWidget.removeWidget(self.treeview)
        return True


    def processCustomMenu(self, position):
        raise Exception('Method processCustomMenu is not implemented')
