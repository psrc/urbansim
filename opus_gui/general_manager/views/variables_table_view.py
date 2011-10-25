# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QTableView
from PyQt4.QtCore import Qt

class VariablesTableView(QTableView):
    def __init__(self, parent_widget = None):
        '''
        Initialize the view to one of two modes,
        pick_mode = use check boxes for selecting variables
        normal mode = use standard selection mode for selecting variables
        '''
        QTableView.__init__(self, parent_widget)

        self.setSelectionBehavior(self.SelectRows)

        self.setSelectionMode(self.ExtendedSelection)
        self.setContextMenuPolicy(Qt.CustomContextMenu)

        # Visual settings
        self.setSortingEnabled(True)
        self.horizontalHeader().setStretchLastSection(True)
        self.horizontalHeader().setSortIndicator(0, Qt.AscendingOrder)
        self.verticalHeader().hide()
        self.setWordWrap(False)
