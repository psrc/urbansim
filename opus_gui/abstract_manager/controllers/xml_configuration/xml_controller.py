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

from copy import deepcopy

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QAction

from opus_gui.main.controllers.mainwindow import get_db_connection_names

from opus_gui.abstract_manager.views.xml_view import XmlView
from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.abstract_manager.models.xml_item_delegate import XmlItemDelegate
from opus_gui.abstract_manager.controllers.xml_configuration.renamedialog \
    import RenameDialog

# List node types that are removable (which also makes them rename-able)
_REMOVABLE_NODE_TYPES = (
    "dictionary", "selectable_list", "list", "tool_file", "tool_config",
    "tool_set", "param_template", "model", "submodel", "source_data",
    "batch_visualization", "indicator_batch", "indicator",
    "indicator_result", "scenario"
)

class XmlController(object):

    '''
    Controller class for XML Trees.
    Also servers as a factory for creating XmlModel, XmlView and XmlItemDelegate
    '''

    def __init__(self, manager):
        '''
        @param manager (AbstractManager): Manager for this XmlController.
        The XmlController will attach itself to manger.base_widget on
        initialization.
        '''
        self.manager = manager

        self.project = self.manager.project

        self.xml_root = manager.xml_root

        self.model = None
        self.view = None
        self.delegate = None

        # initialize the controller
        self.setupModelViewDelegate()
        self.view.setItemDelegate(self.delegate)

        # Get the db_connection_names from the application main window
        try:
            db_connections = get_db_connection_names()
            self.view.known_db_connection_names = db_connections
        except AttributeError:
            # main_window was not set correctly on the application object
            pass

        self.view.setModel(self.model)

        # Expand nodes that defaults to open
        self.view.openDefaultItems()

        # Add the XML tree view to the parent
        self.manager.base_widget.layout().addWidget(self.view)

        # Hook up to the popup menu request
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self.view,
                        SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.processCustomMenu)

        # Actions for common menu choices
        i = self.model.removeIcon
        t = 'Remove'
        cb = self.removeSelectedNode
        self.actRemoveSelected = self.createAction(i, t, cb)

        i = self.model.makeEditableIcon
        t = 'Make node local'
        cb = self.makeSelectedNodeEditable
        self.actMakeEditable = self.createAction(i, t, cb)

        i = self.model.cloneIcon
        t = 'Duplicate'
        cb = self.cloneSelectedNode
        self.actCloneNode = self.createAction(i, t, cb)

        i = self.model.makeEditableIcon
        t = 'Rename'
        cb = self.renameSelectedNode
        self.actRenameNode = self.createAction(i, t, cb)

    def setupModelViewDelegate(self):
        '''
        Initialize and bind the Model, View and Delegate for this controller.

        This method is called before any initialization of the widgets.
        Subclasses that wish to use their own model, view and delegate
        should initialize them in this method.
        '''
        self.model = XmlModel(self.xml_root, self.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def createAction(self, icon, text, callback):
        '''
        Convenience method to create actions.
        @param icon (QIcon): Icon to use for the action
        @param text (String): Action label
        @param callback (function(None)): callback function to call
        @return: the created action (QAction)
        '''
        action = QAction(icon, text, self.view)
        QObject.connect(action, SIGNAL('triggered()'), callback)
        return action

    def rebuild_tree(self):
        ''' Rebuild the model tree '''
        if self.model:
            self.model.rebuild_tree()

    def close(self):
        '''
        Closes the controller and removes it from the parent if it is not empty.
        @return: True if the controller was removed, False if it is dirty
        '''
        self.view.hide()
        self.manager.base_widget.layout().removeWidget(self.view)
        return True

    def selectedItem(self):
        '''
        Get the currently selected item in the controller's view.
        @return: the selected item (XmlItem) or None if none is selected
        '''
        index = self.selectedIndex()
        if not index:
            return None
        return index.internalPointer()

    def selectedIndex(self):
        '''
        Get the index for the currently selected item in the controller's view.
        @return: the index (QModelIndex) for the selected item or None
        '''
        index = self.view.currentIndex()
        if index.isValid():
            return index
        return None

    def hasSelectedItem(self):
        '''
        Tests if the controller's view has a selected item or not.
        @return: True if there is a selected item, False otherwise
        '''
        return self.selectedIndex() is not None

    def processCustomMenu(self, position):
        '''
        Abstract method for creating a context sensitive popup menu.
        @param position (QPoint) point of request for the popupmenu.
        '''
        raise RuntimeError('Method processCustomMenu not implemented')

    def removeSelectedNode(self):
        ''' Removes the selected item from the model. '''
        if not self.hasSelectedItem():
            return
        index = self.selectedIndex()
        self.model.removeRow(index.row(), self.model.parent(index))
        self.view.clearSelection()

    def renameSelectedNode(self):
        ''' Opens a dialog box for changing the node name. '''
        if not self.hasSelectedItem():
            return
        item = self.selectedItem()
        renamer = lambda x: self._change_item_tag(item, x)
        RenameDialog(item.node.tag, renamer, self.view).show()

    def _change_item_tag(self, item, new_tag):
        '''
        Change the tag for a given node by removing and reinserting the node.
        This assures that inherited nodes 'shines through' as they should when
        an overriding node is renamed.
        @param item (XmlItem): item to change tag for
        @param new_tag (String): the new tag value
        @return: True if the tag was changed, False otherwise
        '''
        print 'RENAMING %s to "%s"' %(item.node.tag, new_tag)
        # TODO prevent renaming tag to the same name as an inherited
        # node in the same list

        # Clone the node, remove it from the model and reinsert it
        node = deepcopy(item.node)
        node.tag = str(new_tag)
        item_row = item.row()
        parent_index = self.model.index_for_item(item.parent_item)
        self.model.removeRow(item_row, parent_index)
        self.model.insertRow(item_row, parent_index, node)

        return False

    def cloneSelectedNode(self):
        ''' Clones the selected item using the CloneNode Gui. '''
        if not self.hasSelectedItem():
            return
        index = self.selectedIndex()
        item = self.selectedItem()

        # Clone the node with a new name and let the user rename it
        cloned_node = deepcopy(item.node)

        cloned_node.tag = cloned_node.tag + '_copy'

        # Insert the cloned node into the tree and ask the user to rename it
        if self.model.insertSibling(cloned_node, index) is True:
            index_of_clone = self.model.last_inserted_index
            # Select the new clone for visual clue
            self.view.setCurrentIndex(index_of_clone)
            cloned_item = index_of_clone.internalPointer()
            renamer = lambda x: self._change_item_tag(cloned_item, x)
            RenameDialog(cloned_node.tag, renamer, self.view).show()

    def makeSelectedNodeEditable(self):
        '''
        Copies the selected node to this project and strips the inhertied flag
        from all it's immidiate parents and all it's child nodes.
        '''
        if not self.hasSelectedItem():
            return
        self.model.makeItemEditable(self.selectedItem())

    def selectItemAt(self, point):
        '''
        Select the item at "point" to visualize which item we are working on and
        making the item accessible through self.selectedItem().

        @param point (QPoint): coordinates for where to get the item.
        @return: The selected item if the point was valid, None otherwise
        '''
        index = self.view.indexAt(point)
        if not index.isValid or index.column() != 0:
            return None
        self.view.setCurrentIndex(index)
        return index.internalPointer()

    def addDefaultMenuItems(self, node, menu):
        '''
        Append a list of menu items that is common for all nodes regardless of
        which manager they are in.
        @param node (Element): node to inspect
        @param menu (QMenu): menu to append actions to
        '''
        added_actions = []

        # Inherited nodes can be made local
        if node.get('inherited'):
            added_actions.append(self.actMakeEditable)
        if node.get('copyable') == 'True' or \
            node.get('type') in _REMOVABLE_NODE_TYPES:
            added_actions.append(self.actCloneNode)
        # Only allow local nodes to be renamed
        if node.get('type') in _REMOVABLE_NODE_TYPES and not node.get('inherited'):
            added_actions.append(self.actRenameNode)
            added_actions.append(self.actRemoveSelected)

        # Separate from other items
        if added_actions and not menu.isEmpty():
            menu.addSeparator()

        [menu.addAction(action) for action in added_actions]
