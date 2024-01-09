# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt5.QtCore import QVariant, Qt

from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists
from opus_gui.util.icon_library import IconLibrary

class XmlModel_Models(XmlModel):

    def __init__(self, model_root_node, project = None, parent_widget = None):
        XmlModel.__init__(self, model_root_node, project, parent_widget)

    def data(self, index, role):
        ''' PyQt API Method -- see PyQt for documentation '''

        if not index.isValid():
            return QVariant()

        node = index.internalPointer().node

        if node is None:
            return QVariant()

        # only override displaying of left column
        if index.column() != 0:
            return XmlModel.data(self, index, role)

        # give some nodes special icons
        if role == Qt.DecorationRole:
            if node.tag in ['structure', 'specification']:

                if node.getparent().tag == 'model':
                    return QVariant(IconLibrary.icon('folder_development'))

                elif node.getparent().tag == 'structure':
                    return QVariant(IconLibrary.icon('method'))

                elif node.getparent().tag == 'specification' and node.tag != 'submodel':
                    # assume it's a submodel group
                    return QVariant(IconLibrary.icon('folder_development'))

        # fall back on default
        return XmlModel.data(self, index, role)

#    def add_model_node(self, model_node):
#        '''
#        Appends a node representing a model to the project's list of models.
#        This method is a callback from the 'Add model from template' - dialogs
#        @param model_node (Element) node representing the model
#        '''
#        model_system_node = self.root_node.find('model_system')
#        model_system_node.append(model_node)
#        self.rebuild_tree()

    def removeRow(self, row, parent_index):
        ''' Override the default removeRow to catch updates to models. '''
        # Catch the events where we alter the list of available models and
        # notify interested objects
        node = self.index(row, 0, parent_index).internalPointer().node
        notify = False
        if node is not None and node.tag == 'model':
            notify = True
        XmlModel.removeRow(self, row, parent_index)
        if notify:
            update_models_to_run_lists()

    def insertRow(self, row, parent_index, node, reinserting = False):
        ''' Override the default insertRow to catch updates to models. '''
        # Catch the events where we alter the list of available models and
        # notify interested objects
        XmlModel.insertRow(self, row, parent_index, node, reinserting)
        if node.tag == 'model':
            update_models_to_run_lists()
