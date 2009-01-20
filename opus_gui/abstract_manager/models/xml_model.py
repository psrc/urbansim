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
import copy

from PyQt4.QtCore import Qt, QVariant, SIGNAL, QModelIndex, QAbstractItemModel
from PyQt4.QtCore import QString
from PyQt4.QtGui import QColor, QIcon, QStyle, QMessageBox
from PyQt4.Qt import qApp # For generating platform specific icons

from opus_gui.main.controllers.opus_project import DummyProject
from opus_gui.abstract_manager.models.xml_item import XmlItem

# What node types we want checkboxes for
_CHECKBOX_NODE_TYPES = ('model_choice', 'table', 'dataset', 'variable')

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
        self._root_item.rebuild()

        # Reference to loaded project.
        # if none is given we use a dummy project
        if project is None:
            project = DummyProject()
        self.project = project

        # Dirty flag for keeping track of edits...
        self.dirty = False

        # Column headers
        self._headers = ['Name', 'Value']

        # Index of the last inserted item
        self.last_inserted_index = None

        # load and bind all icons
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.addIcon = QIcon(":/Images/Images/add.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.arrowDownIcon = QIcon(":/Images/Images/arrow_down.png")
        self.arrowUpIcon = QIcon(":/Images/Images/arrow_up.png")
        self.variableLibraryIcon = QIcon(":/Images/Images/book_edit.png")
        self.bulletIcon = QIcon(":/Images/Images/bullet_black.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.carIcon = QIcon(":/Images/Images/car.png")
        self.chartBarIcon = QIcon(":/Images/Images/chart_bar.png")
        self.chartLineIcon = QIcon(":/Images/Images/chart_line.png")
        self.chartOrgIcon = QIcon(":/Images/Images/chart_organisation.png")
        self.cogBlueIcon = QIcon(":/Images/Images/cog_blue.png")
        self.cogIcon = QIcon(":/Images/Images/cog.png")
        self.databaseIcon = QIcon(":/Images/Images/database.png")
        self.databaseLinkIcon = QIcon(":/Images/Images/database_link.png")
        self.databaseTableIcon = QIcon(":/Images/Images/database_table.png")
        self.executeIcon = QIcon(":/Images/Images/table_go.png")
        self.errorIcon = QIcon(":/Images/Images/error.png")
        self.exclamationIcon = QIcon(":/Images/Images/exclamation.png")
        self.fieldIcon = QIcon(":/Images/Images/field.png")
        self.folderDatabaseIcon = QIcon(":/Images/Images/folder_database.png")
        self.folderIcon = QIcon(":/Images/Images/folder.png")
        self.layersIcon = QIcon(":/Images/Images/layers.png")
        self.lockIcon = QIcon(":/Images/Images/lock.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")
        self.mapGoIcon = QIcon(":/Images/Images/map_go.png")
        self.mapIcon = QIcon(":/Images/Images/map.png")
        self.missingModelIcon = QIcon(':/Images/Images/cog_missing.png')
        self.pageWhiteIcon = QIcon(":/Images/Images/page_white.png")
        self.pythonBatchIcon = QIcon(":/Images/Images/python_batch.png")
        self.pythonScriptIcon = QIcon(":/Images/Images/python_script.png")
        self.pythonTypeIcon = QIcon(":/Images/Images/python_type.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.tableGoIcon = QIcon(":/Images/Images/table_go.png")
        self.tableIcon = QIcon(":/Images/Images/table.png")
        self.tableLightningIcon = QIcon(":/Images/Images/table_lightning.png")
        self.tableMultipleIcon = QIcon(":/Images/Images/table_multiple.png")
        self.toolConfigIcon = QIcon(":/Images/Images/wrench.png")
        self.toolFileIcon = QIcon(":/Images/Images/wrench_orange.png")
        self.toolSetIcon = QIcon(":/Images/Images/folder_wrench.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")

        self.folderIcon = QIcon()
        self.bookmarkIcon = QIcon()

        stdPixMap = qApp.style().standardPixmap
        self.bookmarkIcon.addPixmap(stdPixMap(QStyle.SP_FileIcon))
        self.folderIcon.addPixmap(stdPixMap(QStyle.SP_DirClosedIcon),
                                  QIcon.Normal, QIcon.Off)

    def iconFromType(self, type_):
        '''
        Map a type to an icon
        @param type_ (String): type to find icon for
        @return the icon for this type (QIcon) or QVariant()
        '''
        typeMap = {"":self.bulletIcon,
                   "all_source_data":self.folderIcon,
                   "boolean":self.pythonTypeIcon,
                   "cacheConfig":self.databaseLinkIcon,
                   "category":self.bulletIcon,
                   "checkbox":self.bulletIcon,
                   "class":self.pythonTypeIcon,
                   "dataset":self.folderDatabaseIcon,
                   "dictionary":self.pythonScriptIcon,
                   "dir_path":self.folderIcon,
                   "directory":self.pythonTypeIcon,
                   "file":self.pageWhiteIcon,
                   "float":self.fieldIcon,
                   "group":self.folderIcon,
                   "indicator":self.tableIcon,
                   "indicator_group":self.folderIcon,
                   "indicator_library":self.folderIcon,
                   "indicator_result":self.mapGoIcon,
                   "integer":self.fieldIcon,
                   "list":self.pythonTypeIcon,
                   "model":self.cogIcon,
                   "model_choice":self.cogIcon,
                   "model_systems":self.bulletIcon,
                   "model_template_library":self.bulletIcon,
                   "password":self.lockIcon,
                   "path":self.folderDatabaseIcon,
                   "scenario":self.chartOrgIcon,
                   "selectable_list":self.folderIcon,
                   "source_data":self.databaseIcon,
                   "string":self.fieldIcon,
                   "submodel":self.cogBlueIcon,
                   "table":self.tableIcon,
                   "tool_config":self.toolConfigIcon,
                   "tool_file":self.toolFileIcon,
                   "tool_group":self.toolSetIcon,
                   "tool_library":self.bulletIcon,
                   "tool_set":self.toolSetIcon,
                   "tool_sets":self.bulletIcon,
                   "tuple":self.pythonTypeIcon,
                   "unicode":self.fieldIcon }
        if type_ != "defValue" and type_ in typeMap:
            return typeMap[type_]
        else:
            return QVariant()

    def _item_node_path(self, item):
        '''
        Resolve the full node path for a given item.
        @param item (XmlItem): item to resolve path for
        @return: the resolved absolut path for the node or ''
        '''
        if item.parent_item is None:
            return item.node.tag + '/'
        path_before_this_item = self._item_node_path(item.parent_item)
        return path_before_this_item + item.node.tag + '/'

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
        Convenience method to remove a node.
        @param node (Element): Node to remove.
        '''
        index = self.index_for_node(node)
        row = index.row()
        parent_index = self.parent(index)
        self.removeRow(row, parent_index)

    def removeRow(self, row, parent_index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        # Make sure we have a valid parent_index
        if parent_index == QModelIndex():
            parent_item = self._root_item
        else:
            parent_item = parent_index.internalPointer()

        # Validate the row number
        if row < 0 or row > len(parent_item.child_items):
            return False

        child_item = parent_item.child_item(row)

        # TODO -- The way inheritance is dealt with is maybe not the
        # most elegant solution but it works. It's the way things were done
        # before the refactoring. The procedure is this:
        # First we remove the node from the project tree.
        # Then we get a new XML configuration by writing out the project
        # in it's current state to a temporary file and reading it back.
        # If the reloaded project tree contains this node -- we check if it was
        # inherited and if so insert a copy of it into the project tree.

        # Get the path for this node to enable inheritance lookup later
        path_to_removed_node = self._item_node_path(child_item)

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.beginRemoveRows(parent_index, row, row)
        child_item.suicide()
        self.endRemoveRows()
        self.emit(SIGNAL("layoutChanged()"))

        # Check if this node was inherited by reloading the XML tree from disk
        # and looking up the old node path in the loaded tree.
        reloaded_tree = self.project.get_reloaded_xml_tree()
        lookup_node = reloaded_tree.find(path_to_removed_node)

        # If the reloaded tree contains a node in the previous path, and that
        # node was inherited we need to insert that one again.
        if lookup_node is not None and lookup_node.get('inherited'):
            lookup_node = copy.deepcopy(lookup_node)
            self.insertRow(row, parent_index, lookup_node, False)
            # Throw away the temporary tree
            del reloaded_tree

        self.project.dirty = True
        return True

    def data(self, index, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return QVariant()

        node = index.internalPointer().node

        # Foreground Coloring
        if role == Qt.ForegroundRole:
            if node.get('inherited'):
                return QVariant(QColor(Qt.blue))
            return QVariant() # = default color

        # Display
        elif role == Qt.DisplayRole:
            if index.column() == 0:
                return QVariant(node.tag)
            elif index.column() == 1:
                if node.get('type') == "password":
                    return QVariant(QString("*********"))
                elif node.get('type') in _CHECKBOX_NODE_TYPES:
                    return QVariant()
                elif node.text:
                    return QVariant(node.text.strip())
                return QVariant()

        # Icons
        elif role == Qt.DecorationRole:
            if index.column() == 0:
                return QVariant(self.iconFromType(node.get('type')))

        # Checkboxes
        elif role == Qt.CheckStateRole:
            if index.column() == 1:
                if node.get('type') in _CHECKBOX_NODE_TYPES:
                    # this is based on that the first one of the two options is
                    # the 'yes - do it' option and the other one is skip
                    # TODO -- update this when we have type="selectable"
                    choices = node.get("choices").split('|')
                    if node.text.strip() == choices[0]:
                        return QVariant(Qt.Checked)
                    return QVariant(Qt.Unchecked)

        # Unhandled index/role
        return QVariant()

    def index_for_item(self, item):
        '''
        Looks up a QModelIndex() for a given item.
        Use this rather than index_for_node whenever possible since this is
        uses the parents of items and is much more efficient.
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
        This is done to keep inherited nodes always in the tree in case
        this node's tag was changed.
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
        Return the index for a given node.
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

    def add_node_to_path(self, node_path, node):
        '''
        Insert a node into the model at the given path. The path is relative to
        model root.

        Example usage:
         If you have a XmlModel instance handling <my_tree>, and want to insert
         a new node at 'my_tree/foo/bar/<new node>', you call:
         xml_model_instance.add_node_to_path('foo/bar/', node)

        Note that paths are resolved based on ElementTree.find(), which means
        that path ambiguity is ignored. If this is a problem, use
        XmlModel.add_child_node() instead.

        @param node_path (String): where to insert node (relative to model root)
        @param node (Element): node to insert
        @return: True if the node was inserted
        '''
        # Locate the node's index
        parent_node = self._root_node.find(node_path)
        if parent_node is None:
            raise RuntimeError('Warning: XmlModel.add_node_to_path: Could not '
            'add node because the path "%s" could not be resolved to a node '
            'relative to the instance root node "%s".'
            % (node_path, self._root_node.tag))

        parent_item = self.item_for_node(parent_node)
        if parent_item is None:
            msg = ('Warning: XmlModel.add_node: Could not add node because the '
                   'node "%s" is not in this tree.'
                   % parent_node.tag)
            return (False, msg)

        parent_index = self.index_for_item(parent_item)
        if parent_index is not None:
            self.insertRow(0, parent_index, node)
            return True
        else:
            raise RuntimeError('Warning: XmlModel.add_node: Unexpected error '
                               'when locating the internal index for parent '
                               'node "%s"' % parent_node.tag)

    def flags(self, index):
        ''' PyQt API Method -- See the PyQt documentation for a description '''
        if not index.isValid():
            return None

        node = index.internalPointer().node

        # Inherited nodes
        if node.get('inherited'):
            # Special case: checkbox items are still 'clickable' when inherited
            if node.get('type') in _CHECKBOX_NODE_TYPES:
                return (Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                        Qt.ItemIsUserCheckable)
            # General case for inherited items
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable

        # Set flags on a per column basis
        if index.column() == 0:
            return Qt.ItemIsEnabled | Qt.ItemIsSelectable
        elif index.column() == 1:
            if node.get('type') in _CHECKBOX_NODE_TYPES:
                return (Qt.ItemIsEnabled | Qt.ItemIsSelectable |
                        Qt.ItemIsUserCheckable)
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

        # only allow editing in second column
        if index.column() != 1:
            return False

        # user clicking on a checkbox
        if role == Qt.CheckStateRole and \
            node.get('type') in _CHECKBOX_NODE_TYPES:
            # ask the users if they want to make inherited nodes local first
            if item.is_inherited():
                title = 'Editing inherited node'
                msg = ("'%s' is inherited from a parent project. \n\n"
                       "Do you want to make this node part of this project "
                       "so that you can edit it?" % node.tag)
                b = (QMessageBox.Yes, QMessageBox.No)
                ans = QMessageBox.question(None, title, msg, *b)
                if ans == QMessageBox.Yes:
                    self.makeItemEditable(item)
                else:
                    return False
                del title, msg, b, ans # Clean up namespace

            choices = [c.strip() for c in node.get("choices").split('|')]
            if value.toInt()[0] == Qt.Checked:
                value = QVariant(choices[0])
            else:
                value = QVariant(choices[1])

        # convert the value to a string and set the nodes text value
        value = value.toString()
        changed_value = node.text != value
        if changed_value:
            node.text = str(value) # Element doesn't play that well with QString
            self.project.dirty = True
            s = SIGNAL("dataChanged(const QModelIndex &, const QModelIndex &)")
            self.emit(s, index, index)
        return True

    def makeItemEditable(self, item):
        # Strip the inherited attribute down the tree
        # Stripping downwards operates on nodes so that we won't miss any
        # invisible nodes. Upwards works on items because we might not always
        # have information about a node's parent.
        self._stripAttributeDown('inherited', item.node)
        self._stripAttributeUp('inherited', item)

    def insertRow(self, row, parent_index, node, node_is_local = True):
        '''
        PyQt API Method -- See the PyQt documentation for a description
        @param row (int): row to insert into. If row is -1 the last row is used
        @param parent_index (QModelIndex): index of parent item
        @param node (Element): node to insert
        @param node_is_local (bool): If True, the inserted item is made editable
        @return: True if the sibling was inserted, False otherwise
        '''
        if row < 0 or row > self.rowCount(parent_index):
            return False

        self.emit(SIGNAL("layoutAboutToBeChanged()"))
        self.beginInsertRows(parent_index, row, row)

        # Get a correct parent_item
        if parent_index == QModelIndex():
            parent_item = self._root_item
        else:
            parent_item = parent_index.internalPointer()

        # Insert the node, put it in an item and rebuild the tree
        parent_node = parent_item.node
        parent_node.insert(row, node)
        new_item = XmlItem(node, parent_item)
        new_item.rebuild()
        parent_item.child_items.insert(row, new_item)
        self.endInsertRows()
        self.emit(SIGNAL("layoutChanged()"))

        if node_is_local:
            item = parent_item.child_item(row)
            self.makeItemEditable(item)
            self.project.dirty = True

        # Store the last inserted index for access by XmlViews
        self.last_inserted_index = self.index(row, 0, parent_index)
        return True

    def insertSibling(self, node, sibling_index):
        '''
        Create and insert an item at the same level as another item.
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
        if parent_item is self._root_item:
            return QModelIndex()
        return self.createIndex(parent_item.row(), 0, parent_item)

    def moveUp(self, index):
        '''
        Moves the specified item up one step
        @param index (QModelIndex): index for the item to move
        @return index (QModelIndex): index of the new position
        '''
        if not index.isValid() or index.row() == 0:
            return index

        parent_item = self.parent(index).internalPointer()
        row = index.row()
        this_item = parent_item.child_items.pop(row)
        above_item = parent_item.child_items.pop(row - 1)
        parent_item.child_items.insert(row - 1, this_item)
        parent_item.child_items.insert(row, above_item)
        self.makeItemEditable(this_item)
        self.makeItemEditable(above_item)
        self.emit(SIGNAL('layoutChanged()'))
        self.project.dirty = True
        return self.index(row - 1, 0, self.parent(index))

    def moveDown(self, index):
        '''
        Moves the specified item down one step
        @param index (QModelIndex): index for the item to move
        @return index (QModelIndex): index of the new position
        '''
        if not index.isValid() or \
            index.row() >= (self.rowCount(self.parent(index)) - 1):
            return index

        parent_item = self.parent(index).internalPointer()
        row = index.row()
        this_item = parent_item.child_items.pop(row)
        below_item = parent_item.child_items.pop(row)
        parent_item.child_items.insert(row, below_item)
        parent_item.child_items.insert(row + 1, this_item)
        self.makeItemEditable(this_item)
        self.makeItemEditable(below_item)
        self.emit(SIGNAL('layoutChanged()'))
        self.project.dirty = True
        return self.index(row + 1, 0, self.parent(index))

    def _stripAttributeDown(self, attribute, parent_node):
        '''
        Remove all occurrences of an attribute from parent_item and for all
        nodes in it's subtree. Operate on nodes to not restrict to only
        stripping the attribute for nodes that are visible in the tree.
        @param attribute (String): attribute to remove
        @param parent_node (Element): Node to start removing from
        '''
        if parent_node.get(attribute):
            del parent_node.attrib[attribute]
            self.project.dirty = True
        # Strip (recursively) from all child nodes
        map(lambda x: self._stripAttributeDown(attribute, x),
            parent_node.getchildren())

    def _stripAttributeUp(self, attribute, parent_item):
        '''
        Remove all occurrences of an attribute from parent_item and upwards.
        Only direct parents are affected, not their subnodes.
        @param attribute (String): attribute to remove
        @param parent_item (XmlItem): Item to start removing from
        '''
        node = parent_item.node
        if node.get(attribute):
            del node.attrib[attribute]
            self.project.dirty = True
        if parent_item.parent_item:
            self._stripAttributeUp(attribute, parent_item.parent_item)

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
