# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5 import QtWidgets, QtCore
from lxml import etree
from opus_gui.util.convenience import get_unique_name
from opus_gui.models_manager.models.submodel_structure_item import SubmodelStructureItem


class SubmodelStructureEditorTree(QtWidgets.QTreeWidget):

    '''
    Custom Tree Widget that has some convenience methods and supports drag and drop assignments of
    equations to nests.
    '''

    def __init__(self, parent_widget = None):
        QtWidgets.QTreeWidget.__init__(self, parent_widget)
        self._root_node = None
        self.setAcceptDrops(True)

    def set_root_node(self, root_node):
        self._root_node = root_node

    def create_structure_node(self, structure_type):
        ''' create and insert a new tag of structure_type (<nest> or <equation>).
        Accepted values for structure_type are "nest" and "equation" '''
        if structure_type not in ['nest', 'equation']:
            raise ValueError("Don't know how to create a structure node for '%s'" %structure_type)
        # get a unique name for the structure node
        taken_names = [node.get('name') for node in self._root_node.findall(structure_type)]
        name = get_unique_name('new %s' % structure_type, taken_names)
        # create the node with a <variable_list> child node
        attrib = {'name': name, '%s_id' % structure_type: '-2'}
        structure_node = etree.SubElement(self._root_node, structure_type, attrib)
        item = SubmodelStructureItem(structure_node, editable=True, parent_widget=self)
        if structure_type == 'equation':
            etree.SubElement(structure_node, 'variable_list', {'type': 'variable_list'})
        # and insert the item
        self.addTopLevelItem(item)
        self.emit(QtCore.pyqtSignal('structure_changed'))

    def delete_struct_item(self, item):
        ''' deletes the given item from the tree and the XML '''
        node = item._node
        if item.parent():
            index = item.parent().indexOfChild(item)
            item.parent().takeChild(index)
        else:
            index = self.indexOfTopLevelItem(item)
            self.takeTopLevelItem(index)
        node.getparent().remove(node)
        self.emit(QtCore.pyqtSignal('structure_changed'))

    def mousePressEvent(self, event):
        QtWidgets.QTreeWidget.mousePressEvent(self, event)
        # start drags when the left mouse button is pressed
        if event.buttons() == QtCore.Qt.LeftButton:
            mime = QtCore.QMimeData() # the data object to be passed with the event
            # monkey patch the mime object to avoid converting the Python object to QBytes...
            item = self.itemAt(event.pos())
            if item is None:
                return
            mime.dragged_item = item
            drag = QtWidgets.QDrag(self)
            drag.setMimeData(mime)
            # prompt the submode editor to rebuild the structure when the drop was made
            if drag.start(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction:
                # item._node.getparent().remove(item._node)
                self.emit(QtCore.pyqtSignal('structure_changed'))

    def _target_and_source_from_event(self, event):
        ''' convenience to get the target and source item from an event '''
        target_item = self.itemAt(event.pos())
        source_item = event.mimeData().dragged_item
        return (target_item, source_item)

    def dragEnterEvent(self, event):
        # event must be accepted by enter and move in order to be dropped
        event.accept()

    def dragMoveEvent(self, event):
        target_item, source_item = self._target_and_source_from_event(event)
        # if source_item is None we are not dragging anything droppable -- so reject it
        # if target_item is None, we are dropping something in the "white area" of the widget
        # and if target_item is not None we are dropping on another item
        if source_item is None:
            event.ignore()
        elif target_item is None or target_item._node.tag == 'nest':
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        target_item, source_item = self._target_and_source_from_event(event)
        if target_item is source_item:
            event.ignore()
            return
        # if the item is dropped in the "white area" of the widget the target_item will be None
        if target_item is None:
            target_node = self._root_node
        else:
            target_node = target_item._node

        target_node.append(source_item._node)
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()
