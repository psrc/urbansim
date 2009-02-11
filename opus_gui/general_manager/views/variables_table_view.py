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

from PyQt4.QtGui import QTableView
from PyQt4.QtCore import Qt, SIGNAL

from opus_gui.general_manager.models.variables_table_model import VariablesTableModel

class VariablesTableView(QTableView):
    def __init__(self, parent_widget):
        QTableView.__init__(self, parent_widget)

        self.setSelectionBehavior(self.SelectRows)
        self.setSelectionMode(self.NoSelection)
       
        self.setSortingEnabled(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()

        self.setWordWrap(False)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

    def setModel(self, model):
        # Override default setModel so that we can hook up some callbacks
        def resize_to_fit():
            self.resizeRowsToContents()
            self.resizeColumnsToContents()
        self.connect(model, SIGNAL('layoutChanged()'), resize_to_fit)
        QTableView.setModel(self, model)
        resize_to_fit() # initial resize
 

