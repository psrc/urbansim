# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from PyQt4 import QtGui, Qt, QtCore
from opus_gui.general_manager.views.ui_dependency_viewer import Ui_DependencyViewer

class DependencyViewer(QtGui.QDialog, Ui_DependencyViewer):

    def __init__(self, parent_window):
        flags = QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowMaximizeButtonHint
        QtGui.QDialog.__init__(self, parent_window, flags)
        self.setupUi(self)
        self.setModal(True)  #TODO: this shouldn't be necessary, but without it the window is unresponsive

    def show_error_message(self):
        self.lbl_error.setVisible(True)
        self.scrollArea.setVisible(False)

    def show_graph(self, file_path, name):
        self.lbl_error.setVisible(False)
        self.scrollArea.setVisible(True)
        self.setWindowTitle("Dependency graph of %s" % name)
        self.image_file = file_path
        pix = QtGui.QPixmap.fromImage(QtGui.QImage(file_path))
        self.label.setPixmap(pix)
        self.scrollAreaWidgetContents.setMinimumSize(pix.width(), pix.height())
        self.label.setMinimumSize(pix.width(), pix.height())
        rect = Qt.QApplication.desktop().screenGeometry(self)
        self.resize(min(rect.width(), pix.width() + 35), min(rect.height(), pix.height() + 80))
        self.update()

    def on_closeWindow_released(self):
        self.close()
        os.remove(self.image_file)
