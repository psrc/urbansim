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


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QString

class XmlItem(object):
    '''
    Represents an Item in the Manager Tree models.
    '''
    def __init__(self, domDocument, node, parentOpusDataItem):
        self.domDocument = domDocument
        self.domNode = node
        self.parentOpusDataItem = parentOpusDataItem
        self.childItems = []

    def initAsRootItem(self):
        '''
        Add this Item to the tree and iterate through it's children and add any 
        non-hidden child nodes
        '''
        for x in xrange(0, self.domNode.childNodes().count(), 1):
            child_node = self.domNode.childNodes().item(x).toElement()
            # do not add nodes (or subtrees) that should be hidden
            if not child_node.isNull() and \
                child_node.attribute('hidden').toLower() != QString('true'):
                child_item = XmlItem(self.domDocument, child_node, self)
                self.childItems.append(child_item)
                # descend into childs subtree
                child_item.initAsRootItem()

    def refresh(self):
        ''' Re-adds all the children nodes of this Item '''
        self.childItems = []
        self.initAsRootItem()

    def node(self):
        ''' 
        Get a reference to the internal domNode for this Item
        @return: (QDomNode) A reference to the internal domNode
         '''
        return self.domNode

    def parent(self):
        ''' 
        Get a reference to this item's parent.
        @return: parent item (XmlItem) or None
        '''
        return self.parentOpusDataItem

    def child(self, row):
        '''
        Get a reference to the item at a given row
        @param: row (int) which item row
        @return: the item (XmlItem) at the row or None
        '''
        try:
            return self.childItems[row]
        except IndexError:
            return None
#        tryToFind = i+1
#        foundSoFar = 0
#        for x in xrange(0, self.domNode.childNodes().count(), 1):
#            current = self.domNode.childNodes().item(x)
#            if current.isElement() and not \
#                current.toElement().attribute('hidden').toLower() == QString('true'):
#                # We found one
#                foundSoFar = foundSoFar + 1
#            if foundSoFar == tryToFind:
#                # We have the one we are looking for
#                childNode = self.domNode.childNodes().item(x)
#                childItem = XmlItem(self.domDocument, childNode, i , self)
#                self.childItems.append(childItem)
#                return childItem


    def row(self):
        ''' 
        Get the row number for this Item.
        @return: (int) row number of this Item.
        '''
        if self.parentOpusDataItem:
            try:
                index = self.parentOpusDataItem.childItems.index(self)
            except:
                index = 0
            return index
        else:
            return 0

    def numChildren(self):
        '''
        Get the number of child nodes for this Item.
        @return: Number of child nodes (int)
        '''
        return len(self.childItems)

    def lastChild(self):
        '''
        Get a reference to the child in the last row.
        @return The last child item (XmlItem) or None
        '''
        if len(self.childItems) > 0:
            return self.childItems[-1]
        else:
            return None
