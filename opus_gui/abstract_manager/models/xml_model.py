# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import Qt, QVariant, SIGNAL, QModelIndex, QAbstractItemModel
from PyQt4.QtCore import QString
from PyQt4.QtGui import QColor, QIcon, QStyle, QMessageBox
from PyQt4.Qt import qApp # For platform specific icons
from opus_gui.util.icon_library import IconLibrary

from opus_gui.abstract_manager.models.xml_item import XmlItem
from opus_gui.main.controllers.instance_handlers import update_mainwindow_savestate

# What node types we want checkboxes for
# _CHECKBOX_NODE_TYPES = ('selectable')

class XmlModel(QAbstractItemModel):

    '''
        A data model for a XML tree.
        The model exposes a subset of the entire XML tree containing only
        XML nodes that do not have the attribute "hidden" set to "True".
    '''

    def __init__(self, model_root_node, project = None, parent_widget = None):
        '''
        @param model_root_node (ElementTree.Element): Root node for this model
        @param project (OpusProject): Loaded project file
        @param parent_widget (QObject): Parent object for this ItemModel
        '''
        QAbstractItemModel.__init__(self, parent_widget)

        # Root element
        self._root_node = model_root_node

        # Root for the subtree of visible items
        self._root_item = XmlItem(self._root_node, None)

        # Rebuild the (whole) tree of visible items
        self.rebuild_tree()

        # Optional reference to loaded project for inheritance handling.
        self.project = project

        # NOTE: when setting the dirty flag, make sure to use self.dirty rather than
        # self.__dirty.
        self.__dirty = False

        # Column headers
        self._headers = ['Name', 'Value']

        # Index of the last inserted item
        self.last_inserted_index = None

        # use platform specific folder and file icons
        self.folderIcon = QIcon()
        self.fileIcon = QIcon()
        std_icon = qApp.style().standardPixmap
        self.fileIcon.addPixmap(std_icon(QStyle.SP_FileIcon))
        self.folderIcon.addPixmap(std_icon(QStyle.SP_DirClosedIcon), QIcon.Normal, QIcon.Off)

    def __is_dirty(self):
        return self.__dirty

    def __set_dirty(self, dirty):
        self.__dirty = dirty
        if self.project is not None:
            self.project.dirty = True
    dirty = property(__is_dirty, __set_dirty)

    def columnCount(self, parent):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        return len(self._headers)

    def rebuild_tree(self):
        ''' Rebuilds the tree from the underlying XML structure '''
        self._root_item.rebuild()
        self.emit(SIGNAL('layoutChanged()'))

    def rowCount(self, parent_index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not parent_index.isValid():
            item = self._root_item
        else:
            item = parent_index.internalPointer()
        return len(item.child_items)

    def remove_node(self, node):
        '''
        Convenience method to remove a node without bothering with the internal model representation
        @param node (Element): Node to remove.
        '''
        index = self.index_for_node(node)
        row = index.row()
        parent_index = self.parent(index)
        self.removeRow(row, parent_index)

    def removeRow(self, row, parent_index):
        '''
        Removes an object from the data model
        @param row (int) row number to remove
        @param parent_index (QModelIndex) index of parent element
        '''
        # Make sure we have a valid parent_index
        if parent_index == QModelIndex():
            parent_item = self._root_item
        else:
            parent_item = parent_index.internalPointer()
        # Validate the row number
        if row < 0 or row > len(parent_item.child_items):
            return False
        child_item = parent_item.child_item(row)

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.beginRemoveRows(parent_index, row, row)
        # remove the child item from it's parent's list of children
        child_item.parent_item.child_items.remove(child_item)
        # handle inheritance if we are dealing with a project
        reinserted_node = None
        if self.project is None:
            child_item.node.getparent().remove(child_item.node)
        else:
            reinserted_node = self.project.delete_node(child_item.node)
        self.endRemoveRows()
        self.emit(SIGNAL("layoutChanged()"))

        if reinserted_node is not None:
            self.insertRow(row, parent_index, reinserted_node, reinserting = True)
        self.dirty = True
        return True
    
    def _get_node_name(self, node):
        if node.get('type') == 'selectable':
            return node.get('return_value') or node.get('name') or node.tag
        return node.get('name') or node.tag
    
    def _get_node_text(self, node):
        if node.get('type') == "password":
            return "*********"
        # hide the text value for checkable nodes
        elif node.tag == 'selectable' or node.get('type') == 'boolean':
            return ""
        elif node.text:
            return node.text.strip()
        return ""

    def _get_item_children_text(self, item):
        l = list(self._get_node_name(child.node) for child in item.child_items)
        return ', '.join(l)

    def data(self, index, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return QVariant()

        item = index.internalPointer()
        node = item.node

        # Foreground Coloring
        if role == Qt.ForegroundRole:
            if node.get('inherited'):
                return QVariant(QColor(Qt.darkBlue))
            return QVariant() # = default color

        # Display
        elif role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant(self._get_node_name(node))
            elif index.column() == 1:
                return QVariant(self._get_node_text(node))
        elif role == Qt.ToolTipRole:
            # don't need to worry about inheritance when there is no project
            if not self.project:
                return QVariant()
            
            if index.column() == 0:
                value = self._get_node_text(node)
                if value:
                    value = 'Value: %s\n' % value
                else:
                    value = self._get_item_children_text(item)
                    if value:
                        value = 'Children: %s\n' % value
                
                inheritance = ''
                if node.get('inherited'):
                    inheritance = 'Inherited value from file: %s' % node.get('inherited')
                elif self.project.is_shadowing(node):
                    prototype_node = self.project.get_prototype_node(node)
                    inheritance = 'Original value defined in file: %s' % prototype_node.get('inherited')
                else:
                    inheritance = 'Value is defined in this file.'
                text = 'Name: %s\n%s%s' % (self._get_node_name(node), value, inheritance)
                return QVariant(text)
            elif index.column() == 1:
                return QVariant(self._get_node_text(node))

#        elif role == Qt.FontRole:
#            if index.column() == 0:
#                if node.tag == 'model':
#                    font = QFont()
#                    font.setPointSize(14)
#                    return QVariant(font)

# CK: Experimenting with making shadowing nodes bold to differentiate them from local nodes
#        elif role == Qt.FontRole:
#            f = QFont()
#            if self.project is not None:
#                f.setBold(self.project.is_shadowing(node))
#            return QVariant(f)

        # Icons
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                return QVariant(IconLibrary.icon_for_type(node.tag))

        # Checkboxes
        elif role == Qt.CheckStateRole and index.column() == 1:
            if node.tag == 'selectable' or node.get('type') == 'boolean':
                return QVariant(Qt.Checked if (node.text.strip() == 'True') else Qt.Unchecked)

        # Unhandled index/role
        return QVariant()

    def index_for_item(self, item):
        '''
        Looks up a QModelIndex() for a given item.
        @param item (XmlItem): item to find in the model
        @return: The index (QModelIndex) for the given item.
        '''
        if item is self._root_item:
            return QModelIndex()
        parent_index = self.index_for_item(item.parent_item)
        return self.index(item.row(), 0, parent_index)

    def update_node(self, node):
        '''
        Refreshes the node by removing it and reinserting it.
        '''
        item = self.item_for_node(node)
        if item is None:
            return
        parent_index = self.index_for_item(item.parent_item)
        if parent_index is None:
            return
        row = item.row()
        self.removeRow(row, parent_index)
        self.insertRow(row, parent_index, node)

    # CK: This is a pretty ineffective method of finding the node <-> item mapping.
    # A dictionary mapping would be better.
    def _item_for_node(self, parent_item, node):
        '''
        Depth first search for the XmlItem containing a given node.
        @param parent_item (XmlItem): parent of nodes to scan.
        @param node (Element): the node to locate
        @return: the found node (Element) if found, None otherwise
        '''
        for child_item in parent_item.child_items:
            if child_item.node is node:
                return child_item
            found_item = self._item_for_node(child_item, node)
            if found_item is not None:
                return found_item
        return None

    def item_for_node(self, node):
        '''
        Return the item for a given node.
        @param node (Element): The node to locate.
        @return: The item containing the given node (XmlItem) or None
        '''
        return self._item_for_node(self._root_item, node)

    def index_for_node(self, node):
        '''
        Return the qt index for a given node.
        @param node (Element): The node to locate.
        @return: The item containing the given node (XmlItem) or None
        '''
        item = self._item_for_node(self._root_item, node)
        return self.index_for_item(item)

    def add_node(self, parent_node, node):
        '''
        Adds a child node (may contain a subtree) to a given parent node and
        updates the model.

        For efficient insertion of entire trees; first construct the subtree to
        insert using ElementTree, and then call this method once with the root
        node for it.

        @param parent_node (Element): parent node
        @param node (Element): node to insert
        '''
        parent_item = self.item_for_node(parent_node)
        parent_index = self.index_for_item(parent_item)
        self.insertRow(0, parent_index, node)
        if self.project:
            self.project.dirty = True

    # TODO update comments to xml 2.0
    def insert_node(self, node, parent_node):
        '''
        Insert a node into the XML and into the model.
        This method automatically finds the qt index for the parent index so that the item can be
        inserted.
        @param node (Element): node to insert
        @param parent_node (Element): Parent node to append @node
        @return: True if the node was inserted
        '''
        parent_item = self.item_for_node(parent_node)
        if parent_item is None:
            msg = ('Tried to insert a node under <%s>, but that node is not in this XmlModel' %
                   parent_node.tag)
            return (False, msg)

        parent_index = self.index_for_item(parent_item)
        if parent_index is not None:
            self.insertRow(0, parent_index, node)
            self.project.dirty = True
            return (True, 'OK')
        else:
            msg = ('Tried to insert a node under <%s>, but could not find its index.' %
                   parent_node.tag)
            return (False, msg)

    def flags(self, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return None

        node = index.internalPointer().node

        is_checkbox_node = node.tag == 'selectable' or node.get('type') == 'boolean'

        # Inherited nodes
        if node.get('inherited'):
            # inherited nodes are generally only selectable and enabled, with the exception
            # of checkboxes that are clickable even when they are inherited
            if is_checkbox_node:
                return (Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # Set flags on a per column basis
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        elif index.column() == 1:
            if is_checkbox_node:
                return (Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable)
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

        # Unhandled index
        return QVariant()

    def headerData(self, section, orientation, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self._headers[section])
        else:
            return QVariant()

    def index(self, row, column, parent_index = QModelIndex()):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        if not parent_index.isValid():
            parent_item = self._root_item
        else:
            parent_item = parent_index.internalPointer()

        child_item = parent_item.child_item(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        else:
            return QModelIndex()

    def setData(self, index, value, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return False

        item = index.internalPointer()
        node = item.node

        is_checkbox_node = node.tag == 'selectable' or node.get('type') == 'boolean'

        # only allow editing in second column
        if index.column() != 1:
            return False

        # user clicking on a checkbox
        if role == Qt.CheckStateRole and is_checkbox_node:
            # ask the users if they want to make inherited nodes local first
            if node.get('inherited'):
                title = 'Editing inherited node'
                msg = ("'%s' is inherited from a parent project. \n\n"
                       "Do you want to make this node part of this project "
                       "so that you can edit it?" % node.get('name') or node.tag)
                b = (QMessageBox.Yes, QMessageBox.No)
                ans = QMessageBox.question(None, title, msg, *b)
                if ans == QMessageBox.Yes:
                    self.make_item_local(item)
                else:
                    return False
                del title, msg, b, ans # Clean up namespace
            if value.toInt()[0] == Qt.Checked:
                value = QVariant('True')
            else:
                value = QVariant('False')

        # convert the value to a string and set the nodes text value
        value = value.toString()
        changed_value = node.text != value
        if changed_value:
            node.text = str(value) # avoid QString's in the xml
            self.dirty = True
            s = SIGNAL("dataChanged(const QModelIndex &, const QModelIndex &)")
            self.emit(s, index, index)
        return True

    def make_item_local(self, item):
        if not self.project: return
        self.project.make_local(item.node)

    def insertRow(self, row, parent_index, node, reinserting = False):
        '''
        Insert a row into the data model
        @param row (int): row to insert into.
        @param parent_index (QModelIndex): index of parent item
        @param node (Element): node to insert
        @param reinserting (bool): if True; assume that the project has already reinserted the node
        and just insert it into the internal model. Also skip making it local after inserting.
        @return: True if the sibling was inserted, False otherwise
        '''
        if row < 0 or row > self.rowCount(parent_index):
            return False

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.beginInsertRows(parent_index, row, row)

        # Get a valid parent_item
        if parent_index == QModelIndex():
            parent_item = self._root_item
        else:
            parent_item = parent_index.internalPointer()
        parent_node = parent_item.node

        if self.project is None: # no inheritance simple insert into tree
            parent_node.insert(row, node)
        else:
            # when dealing with a project and inheritance we have two cases --
            # either insertRow is inserting a node that already exists in the project
            # (reinserting is True) or we are inserting a new node.
            if not reinserting:
                inserted_node = self.project.insert_node(node, parent_node, row)
                if inserted_node is None:
                    # raise RuntimeError('Could not insert node into model')
                    print 'WARNING: Could not insert %s:%s' % (node.tag, node.get('name'))
                    return False
                self.project.make_local(inserted_node)
            else:
                inserted_node = node

        new_item = XmlItem(inserted_node, parent_item)
        new_item.rebuild()
        parent_item.child_items.insert(row, new_item)
        self.endInsertRows()
        self.emit(SIGNAL("layoutChanged()"))

        # If the item was created we store it so that XmlViews can access it
        self.last_inserted_index = self.index(row, 0, parent_index) if new_item else None
        update_mainwindow_savestate()
        return True

    def insert_sibling(self, node, sibling_index):
        '''
        Create and insert a sibling node.
        @param node (Element): node for the new item
        @param sibling_index (QModelIndex): index for the sibling item
        @return: True if the sibling was inserted, False otherwise
        '''
        parent_index = self.parent(sibling_index)
        return self.insertRow(sibling_index.row(), parent_index, node)

    def parent(self, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return QModelIndex()
        parent_item = index.internalPointer().parent_item
        parent_node = index.internalPointer().parent_item.node
        if parent_item is self._root_item:
            return QModelIndex()
        parent_ind = self.createIndex(parent_item.row(), 0, parent_item)
        parent_ind.node = parent_node
        return parent_ind

    # TODO consider doing this with lxml's insert(current index - 1) instead, the current
    # implementation gives me a headache (and I think its broken)
    def move_up(self, index, view=None):
        '''
        Moves the specified item up one step
        @param index (QModelIndex): index for the item to move
        @return index (QModelIndex): index of the new position
        '''
        if not index.isValid() or index.row() == 0:
            return index
        parent_item = self.parent(index).internalPointer()
        row = index.row()
        if view:
            this_item_expanded = view.isExpanded(self.index(row, 0, self.parent(index)))
            above_item_expanded = view.isExpanded(self.index(row-1, 0, self.parent(index)))
        this_item = parent_item.child_items.pop(row)
        above_item = parent_item.child_items.pop(row - 1)
        parent_item.child_items.insert(row - 1, this_item)
        parent_item.child_items.insert(row, above_item)
        self.make_item_local(this_item)
        self.make_item_local(above_item)
        self.emit(SIGNAL('layoutChanged()'))
        self.dirty = True
        if view:
            view.setExpanded(self.index(row, 0, self.parent(index)), above_item_expanded)
            view.setExpanded(self.index(row-1, 0, self.parent(index)), this_item_expanded)
        return self.index(row - 1, 0, self.parent(index))

    def move_down(self, index, view=None):
        '''
        Moves the specified item down one step
        @param index (QModelIndex): index for the item to move
        @return index (QModelIndex): index of the new position
        '''
        if not index.isValid() or index.row() >= (self.rowCount(self.parent(index)) - 1):
            return index

        parent_item = self.parent(index).internalPointer()
        row = index.row()
        if view:
            this_item_expanded = view.isExpanded(self.index(row, 0, self.parent(index)))
            below_item_expanded = view.isExpanded(self.index(row+1, 0, self.parent(index)))
        this_item = parent_item.child_items.pop(row)
        below_item = parent_item.child_items.pop(row)
        parent_item.child_items.insert(row, below_item)
        parent_item.child_items.insert(row + 1, this_item)
        self.make_item_local(this_item)
        self.make_item_local(below_item)
        self.emit(SIGNAL('layoutChanged()'))
        self.dirty = True
        if view:
            view.setExpanded(self.index(row+1, 0, self.parent(index)), this_item_expanded)
            view.setExpanded(self.index(row, 0, self.parent(index)), below_item_expanded)
        return self.index(row + 1, 0, self.parent(index))

    def root_node(self):
        '''
        Get a reference to this model's root node
        @return: The models root node (Element)
        '''
        return self._root_node

    def root_item(self):
        '''
        Get a reference to this model's root item
        @return: The models root item (XmlItem)
        '''
        return self._root_item
