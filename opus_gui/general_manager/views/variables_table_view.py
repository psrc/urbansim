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
from PyQt4.QtCore import Qt

class VariablesTableView(QTableView):
    def __init__(self, pick_mode = True, parent_widget = None):
        '''
        Initialize the view to one of two modes,
        pick_mode = use check boxes for selecting variables
        normal mode = use standard selection mode for selecting variables
        '''
        QTableView.__init__(self, parent_widget)
        self.pick_mode = pick_mode

        self.setSelectionBehavior(self.SelectRows)

        if pick_mode:
            self.setSelectionMode(self.NoSelection)
        else:
            self.setSelectionMode(self.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Visual settings
        self.setSortingEnabled(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.verticalHeader().hide()
        self.setWordWrap(False)

    def setModel(self, model):
        ''' Override of setModel() to make some visual tweaking '''
        # self.connect(model, SIGNAL('layoutChanged()'), self._resize_to_fit)
        QTableView.setModel(self, model)

        for col in (0, 3, 4): # compress the short columns
            self.resizeColumnToContents(col)

        # make the name column twice as big as the dataset column
        self.setColumnWidth(1, self.columnWidth(2) * 2)
        self.setColumnHidden(0, not self.pick_mode)
