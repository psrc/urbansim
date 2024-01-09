# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE



# PyQt5 includes for python bindings to QT
from PyQt5.QtCore import Qt, QDir, QObject, pyqtSignal
from PyQt5.QtWidgets import QTreeView, QDirModel

class FileController(object):
    def __init__(self, manager, opusDataPath, parentWidget, listen_to_menu = True):

        self.addTree(opusDataPath, parentWidget)

        self.currentColumn = None
        self.currentIndex = None
        self.classification = ""

        self.manager = manager
        if listen_to_menu:
            QObject.connect(self.treeview,
                            pyqtSignal("customContextMenuRequested(const QPoint &)"),
                            self.process_custom_menu)


    def addTree(self, opusDataPath, parentWidget):
        self.containerWidget = parentWidget
        self.opusDataPath = opusDataPath

        self.treeview = QTreeView()
        filters = []
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

        self.containerWidget.layout().addWidget(self.treeview)

        # Hook up to the mousePressEvent and pressed
        self.treeview.setContextMenuPolicy(Qt.CustomContextMenu)

    def close(self):
        self.treeview.hide()
        self.containerWidget.layout().removeWidget(self.treeview)
        return True


    def process_custom_menu(self, position):
        raise Exception('Method processCustomMenu is not implemented')
