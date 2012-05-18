# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.main.controllers.instance_handlers import shows_hidden

class XmlItem(object):
    '''
    Item container for XML nodes to be used in XmlModel.
    Note: The design of this class is for usage with ElementTree. Much of the functionality is
    not necessary now that XML is handled by lxml (for example, parent nodes), but it's kept
    for API compability.
    '''
    def __init__(self, node, parent_item, hidden=False):
        '''
        @param node (ElementTree.Element): node to represent
        @param parent_node (ElementTree.Element): parent node
        '''
        assert node is not None
        self.node = node                      # Connection to ElementTree
        self.parent_item = parent_item        # Parent item
        self.child_items = []                 # child items (only visible nodes)
        self.hidden = hidden

    def row(self):
        '''
        Get the which row this item is in
        @return: row number (int)
        '''
        if self.parent_item is None or not self in self.parent_item.child_items:
            return 0
        return self.parent_item.child_items.index(self)

    def rebuild(self):
        def _enumerate_child_items():
            # This routine encapsulates the logic of adding all necessary items to the tree
            # depending on whether we want to see the hidden items or not.
            
            # The helper routine _is_removed() is defined depending on if we
            # want to see the hidden items
            if shows_hidden():
                def _is_removed(hide):
                    return False
            else:
                def _is_removed(hide):
                    return hide
            
            # We hide all children if this node is hidden...
            hide_children = self.hidden
            
            # ...or if the "hidden" attribute is set accordingly
            if self.node.get('hidden') == 'Children':
                hide_children = True
            
            # shortcut, early stop:
            if _is_removed(hide_children):
                return

            for node in self.node:
                # In addition, we hide a child if the "hidden" attribute is set
                hidden = hide_children or (node.get('hidden') == 'True')
                
                # Yield the new XmlItem if necessary
                if not _is_removed(hidden):
                    yield XmlItem(node, self, hidden)
            
        ''' Refreshes this XmlItem's list of child_items. '''
        self.child_items = [i for i in _enumerate_child_items()]
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
