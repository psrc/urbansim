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

class XmlItem(object):
    '''
    Item container for XML nodes to be used in XmlModel.
    '''
    def __init__(self, node, parent_item):
        '''
        @param node (ElementTree.Element): node to represent
        @param parent_node (ElementTree.Element): parent node
        '''
        assert node is not None
        self.node = node                      # Connection to ElementTree
        self.parent_item = parent_item        # Parent item
        self.child_items = []                 # child items (only visible nodes)

    def visible(self):
        '''
        Get the visible state for this item
        @return: True if node is visible, False otherwise
        '''
        return self.node.get('hidden').lower() == 'true'

    def is_inherited(self):
        '''
        Get the inheritance state for this item
        @return: True if node is inherited, False otherwise
        '''
        return self.node.get('inherited') is not None

    def row(self):
        '''
        Get the which row this item is in
        @return: row number (int)
        '''
        if self.parent_item is None or not self in self.parent_item.child_items:
            return 0
        return self.parent_item.child_items.index(self)

    def rebuild(self):
        ''' Refreshes this XmlItem's list of child_items. '''
        self.child_items = [XmlItem(node, self) for node in self.node
                            if not node.get('hidden') == 'True']
        map(lambda x: x.rebuild(), self.child_items)

    def child_item(self, row):
        '''
        Get a reference to the child item in a given row.
        @param row (int): row to get child item from
        @return: the item (XmlItem) at given row or None
        '''
        try:
            return self.child_items[row]
        except IndexError, ex:
            return None

    def suicide(self):
        ''' Remove the item from it's parent and the node from the XML '''
        self.parent_item.child_items.remove(self)
        self.parent_item.node.remove(self.node)
