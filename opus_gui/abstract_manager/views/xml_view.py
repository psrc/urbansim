# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtGui import QTreeView
from PyQt4.QtCore import QModelIndex

class XmlView(QTreeView):

    '''
    TreeView for viewing XML data.
    '''

    STANDARD_COLUMN_WIDTH_NODES = 250
    STANDARD_COLUMN_WIDTH_DATA  = 50

    def __init__(self, parent_widget):
        '''
        Tree view for displaying data in a XmlModel
        @param parent_widget (QWidget): Parent widget
        '''
        QTreeView.__init__(self, parent_widget)

        self.setAnimated(True)
        self.setMinimumHeight(200)

    def _expand_subnodes(self, item):
        '''
        Recursively expands all items under (and including) a given index.
        Items are expanded only if "setexpanded" set to "True".
        @param item (XmlItem): the item to (maybe) expand along with subnodes
        '''
        index = self.model().index_for_item(item)
        if item.node.get('setexpanded') == 'True':
            self.expand(index)
        for child_item in item.child_items:
            self._expand_subnodes(child_item)

    def openDefaultItems(self):
        ''' Expand all items that default to expanded and refresh the width'''
        # Expand all items at the root level
        self._expand_subnodes(self.model().root_item())
        self.setColumnWidth(0, self.STANDARD_COLUMN_WIDTH_NODES)
        self.setColumnWidth(1, self.STANDARD_COLUMN_WIDTH_DATA)

