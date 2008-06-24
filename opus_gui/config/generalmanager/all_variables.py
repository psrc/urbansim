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

        # For now, disable the save button until we implement the write in the model...
        self.saveChanges.setEnabled(False)

        header = ["Name","Dataset","Use","Source","Definition"]
        #tabledata = [("test_var",
        #              "Foo",
        #              "Bar",
        #              "Weeee",
        #              "This is a really long test line just to show what happens when the line wraps around inside of the table view TEST TEST TEST TEST"),
        #             ("test_var2",
        #              "Foo2",
        #              "Bar2",
        #              "Weeee2",
        #              "This is a really long test line just to show what happens when the line wraps around inside of the table view TEST TEST TEST TEST2")]
        tabledata = []
        # Grab the general section...
        tree = self.mainwindow.toolboxStuff.generalManagerTree
        dbxml = tree.model.index(0,0,QModelIndex()).parent()
        all_variables_list = tree.model.findElementIndexByName("all_variables",dbxml,True)
        for all_variables in all_variables_list:
            # Should just be one all_variables section
            if all_variables.isValid():
                # Now we have to loop through all the variables and create the data grid for the display
                tsindexlist = tree.model.findElementIndexByType("variable_definition",all_variables,True)
                for tsindex in tsindexlist:
                    if tsindex.isValid():
                        # Now we have a valid variable, we fill in the set for display
                        tsitem = tsindex.internalPointer()
                        tsnode = tsitem.node()
                        if tsnode.isElement():
                            tselement = tsnode.toElement()
                            tselement_text = ""
                            if tselement.hasChildNodes():
                                classchildren = tselement.childNodes()
                                for x in xrange(0,classchildren.count(),1):
                                    if classchildren.item(x).isText():
                                        #print "Found some text in the classification element"
                                        tselement_text = classchildren.item(x).nodeValue()
                            tslist = [tselement.tagName(),
                                      tselement.attribute(QString("dataset")),
                                      tselement.attribute(QString("use")),
                                      tselement.attribute(QString("source")),
                                      tselement_text]
                            tstuple = tuple(tslist)
                            tabledata.append(tstuple)
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

