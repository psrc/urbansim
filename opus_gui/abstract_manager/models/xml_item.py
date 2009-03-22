# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

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
