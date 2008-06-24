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

from opus_gui.config.xmlmodelview.opusallvariablestablemodel import OpusAllVariablesTableModel
from opus_gui.config.generalmanager.all_variables_ui import Ui_AllVariablesGui

import random

class AllVariablesGui(QDialog, Ui_AllVariablesGui):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow
        #Add a default table
        tv = QTableView()
        tv.setSortingEnabled(True)
        header = ["Name","Dataset","Use","Source","Definition"]
        tabledata = [("test_var",
                      "Foo",
                      "Bar",
                      "Weeee",
                      "This is a really long test line just to show what happens when the line wraps around inside of the table view TEST TEST TEST TEST")]
        tm = OpusAllVariablesTableModel(tabledata, header, self) 
        tv.setModel(tm)
        tv.horizontalHeader().setStretchLastSection(True)
        tv.setTextElideMode(Qt.ElideNone)
        self.gridlayout.addWidget(tv)
        
    def on_saveChanges_released(self):
        print "save pressed"

        self.close()

    def on_cancelWindow_released(self):
        print "cancel pressed"
        self.close()

