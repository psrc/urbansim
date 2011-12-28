# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# TODO rename methods to follow OPUS code conventions

from copy import deepcopy

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QCursor, QMenu

from opus_gui.abstract_manager.views.xml_view import XmlView
from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.abstract_manager.models.xml_item_delegate import XmlItemDelegate
from opus_gui.abstract_manager.controllers.xml_configuration.renamedialog import RenameDialog
from opus_gui.util.convenience import create_qt_action

# List node types that are removable (which also makes them rename-able)
_REMOVABLE_NODE_TYPES = (
    "dictionary", "selectable_list", "list", "tool", "tool_config",
    "tool_set", "param_template", "model", "submodel", "source_data",
    "batch_visualization", "indicator_batch", "indicator",
    "indicator_result", "scenario", 'tool_file', 'tool_library', 'tool_group',
    'class', 'param', None, "models_to_run", "integer"
)

class XmlController(object):

    '''
    Controller class for XML Trees.
    '''

    def __init__(self, manager):
        '''
        @param manager (AbstractManager) The parent manager for this XmlController
        The XmlController will attach itself to manger.base_widget on initialization.
        '''
        self.manager = manager
        self.project = self.manager.project
        self.xml_root = manager.xml_root
        self.model = None
        self.view = None
        self.delegate = None

        self.add_model_view_delegate()
        self.view.setItemDelegate(self.delegate)
        self.view.setModel(self.model)
        self.view.openDefaultItems()
        self.manager.base_widget.layout().addWidget(self.view)
        self.view.setContextMenuPolicy(Qt.CustomContextMenu)
        QObject.connect(self.view,
                        SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.process_custom_menu)

        # Actions for common menu choices
        # Note that revert and delete are the same action, but we want to present them differently
        # to show that deleting an inherited node (reverting) will keep the node around
        self.act_remove_selected = self.create_action('delete', 'Delete', self.remove_selected_node)
        self.act_revert = self.create_action('revert', 'Revert to inherited value', self.remove_selected_node)
        self.act_make_editable = self.create_action('make_editable', 'Make node local', self.make_selected_editable)
        self.act_clone_node = self.create_action('clone', 'Duplicate', self.clone_selected_node)
        self.act_rename_node = self.create_action('rename', 'Rename', self.rename_selected_node)

    def add_model_view_delegate(self):
        '''
        Initialize and bind the Model, View and Delegate for this controller.

        This method is called before any initialization of the widgets.
        Subclasses that wish to use their own model, view and/or delegate
        should override this method and initialize their own widgets.
        '''
        self.model = XmlModel(self.xml_root, self.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def create_action(self, icon_name, text, callback):
        return create_qt_action(icon_name, text, callback, self.view)

    def rebuild_tree(self):
        ''' Rebuild the model tree '''
        if self.model:
            self.model.rebuild_tree()

    # CK: TODO This is a method left from before the refactoring in december, don't know
    # if it's needed/used
    def close(self):
        '''
        Closes the controller and removes it from the parent if it is not empty.
        @return: True. Previous behavior was to return False if self.model was
        dirty. This is no longer done as dirty checks have been moved.
        '''
        self.view.hide()
        self.manager.base_widget.layout().removeWidget(self.view)
        return True

    def selected_item(self):
        '''
        Get the currently selected item in the controller's view.
        @return: the selected item (XmlItem) or None if no item is selected.
        '''
        index = self.selected_index()
        return index.internalPointer() if index else None

    def selected_index(self):
        '''
        Get the index for the currently selected item in the controller's view.
        @return: the index (QModelIndex) for the selected item or None
        '''
        index = self.view.currentIndex()
        if index.isValid():
            return index
        return None

    def has_selected_item(self):
        '''
        Tests if the controller's view has a selected item or not.
        @return: True if there is a selected item, otherwise False.
        '''
        return self.selected_index() is not None

    def process_custom_menu(self, position):
        '''
        Default method for creating a context sensitive popup menu.
        Calls self.add_custom_menu_items_for_node() to populate the menu
        with context-specific menu items.
        @param position (QPoint) point of request for the popupmenu.
        '''
        item = self.select_item_at(position)
        assert item is not None
        node = item.node
        
        menu = QMenu(self.view)
        if item is self.model.root_item():
            self.add_default_menu_items_for_widget(menu)
        elif not self.add_custom_menu_items_for_node(node, menu):
            if not menu.isEmpty():
                menu.addSeparator()
            self.add_default_menu_items_for_node(node, menu)
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())


    def set_project_dirty(self):
        if self.project:
            self.project.dirty = True


    def remove_selected_node(self):
        ''' Removes the selected item from the model. '''
        if not self.has_selected_item():
            return
        index = self.selected_index()
        self.model.removeRow(index.row(), self.model.parent(index))
        self.view.clearSelection()
        self.set_project_dirty()

    # CK: this is a helper function for the clone_node method, but maybe its general enough to be
    # promoted to a higher abstraction layer?
    def _get_unique_name_like_node(self, node):
        '''
        Search sibling items with the same tag to find a name that is guaranteed to be unique.
        First it tries to insert the item with it's current name. If that fails it appends
        _copy to the name and tries again. Subsequent tries have _copyX appended to them where
        X is a number from 1 ->
        @param node (Element) the item holding the node to find a new name for
        @return (String) a unique name for the new node.
        '''
        base_name = node.get('name')
        # Get all the names that currently exist in the same level
        if node.getparent() is None: # no parent = no siblings
            return base_name
        sibling_nodes = node.getparent().getchildren()
        taken_names = [n.get('name') for n in sibling_nodes]
        if base_name not in taken_names:
            return base_name

        try_name = 'Copy of %s' % base_name
        copy_number = 0
        while try_name in taken_names:
            copy_number += 1
            try_name = 'Copy %d of %s' % (copy_number, base_name)
        return try_name

    def clone_selected_node(self):
        ''' Clone the selected node and insert it as a sibling with a unique name '''
        if not self.has_selected_item():
            return
        index = self.selected_index()
        item = self.selected_item()

        cloned_node = deepcopy(item.node)
        cloned_node.set('name', self._get_unique_name_like_node(item.node))

        # Insert the cloned node into the tree
        if self.model.insert_sibling(cloned_node, index) is not None:
            index_of_clone = self.model.last_inserted_index
            # Select the new clone if it was inserted
            if index_of_clone is not None:
                self.view.setCurrentIndex(index_of_clone)
            self.set_project_dirty()

    def rename_selected_node(self):
        ''' Opens a dialog box for changing the node name. '''
        if not self.has_selected_item():
            return
        item = self.selected_item()
        node = item.node
        taken_names = [n.get('name') for n in node.getparent().getchildren() if not n is node]
        dialog = RenameDialog(node.get('name'), taken_names, self.view)
        if dialog.exec_() == dialog.Accepted:
            node.set('name', dialog.accepted_name)
            self.set_project_dirty()

    def make_selected_editable(self):
        '''
        Copies the selected node to this project and strips the inhertied flag
        from all it's immidiate parents and all it's child nodes.
        '''
        if not self.has_selected_item():
            return
        self.model.make_item_local(self.selected_item())

    def select_item_at(self, point):
        '''
        Select the item at "point" to visualize which item we are working on and
        making the item accessible through self.selected_item().
        If the point is invalid, the currently selected item, if any, is deselected,
        and the root item is returned.

        @param point (QPoint): coordinates for where to get the item.
        @return: The selected item if the point was valid, None otherwise
        '''
        index = self.view.indexAt(point)
        if not index.isValid or index.column() != 0: # only allow right-clicking on left side nodes
            index = self.view.rootIndex()
            item = self.model.root_item()
        else:
            item = index.internalPointer()
        self.view.setCurrentIndex(index)
        
        assert item is not None
        return item
    
    def add_custom_menu_items_for_node(self, node, menu):
        '''
        Append a list of menu items specific to a manager.
        Supposed to be overridden.
        @param node (Element): node to inspect
        @param menu (QMenu): menu to append actions to
        @return: True if no default menu items should be inserted
        '''
        pass

    def add_default_menu_items_for_node(self, node, menu):
        '''
        Append a list of menu items that is common for all nodes regardless of
        which manager they are in.
        @param node (Element): node to inspect
        @param menu (QMenu): menu to append actions to
        '''
        added_actions = []

        # Inherited nodes can be made local
        if node.get('inherited'):
            added_actions.append(self.act_make_editable)
        # nodes that do not have a 'name' attribute are special nodes that should not be copyable
        # for example; <expression_library>, <model_manager> etc..
        if node.get('name') is not None: # or node.get('copyable') == 'True':
            added_actions.append(self.act_clone_node)
        # named nodes that are not inherited can be renamed
        if node.get('name') is not None and not node.get('inherited'):
            added_actions.append(self.act_rename_node)
        if self.project and self.project.is_shadowing(node):
            added_actions.append(self.act_revert)
        elif node.get('type') in _REMOVABLE_NODE_TYPES and not node.get('inherited'):
            added_actions.append(self.act_remove_selected)

        # Separate from other items
        if added_actions and not menu.isEmpty():
            menu.addSeparator()
        map(lambda x: menu.addAction(x), added_actions)
        # [menu.addAction(action) for action in added_actions]
        
    def add_default_menu_items_for_widget(self, menu):
        pass
