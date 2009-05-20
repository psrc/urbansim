# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import QVariant, Qt
from PyQt4.QtGui import QColor

from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.models_manager.models_manager import get_model_names
from opus_gui.util.icon_library import IconLibrary

class XmlModel_Scenarios(XmlModel):

    def __init__(self, model_root_node, project = None, parent_widget = None):
        ''' See XmlModel.__init__ for documentation '''
        XmlModel.__init__(self, model_root_node, project, parent_widget)
        self.missing_models = set()

    def data(self, index, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        # Handle special drawing of missing models
        node = index.internalPointer().node
        if node.tag != 'model' or node.get('name') not in self.missing_models:
            # Not a missing model -- use default data handler
            return XmlModel.data(self, index, role)

        # Missing models get a colored description label and a special icon
        if index.column() == 1:
            if role == Qt.ForegroundRole:
                return QVariant(QColor(Qt.red))
            elif role == Qt.DisplayRole:
                return QVariant("(no such model)")
        # Give it a special icon
        elif role == Qt.DecorationRole and index.column() == 0:
            return QVariant(IconLibrary.icon('missing_model'))

        # Other data properties are handled by the default data() method
        return XmlModel.data(self, index, role)

    def validate_models_to_run(self):
        '''
        Goes through all scenarios in the XmlController and makes sure that
        the models in their 'models_to_run' list actually is present in the
        project.
        '''
        model_names = get_model_names(self.project)
        self.missing_models = set()
        scenarios_nodes = self._root_node.findall('scenario')
        for scenario_node in scenarios_nodes:
            models_to_run_lists = [node for node in scenario_node.findall('selectable') if
                                   node.get('name') == 'models_to_run']
            # validate all models to run lists of this scenario
            for mtr_list in models_to_run_lists:
                for model_name in mtr_list:
                    if not model_name in model_names:
                        self.missing_models.add(model_name)

#    def rebuild_tree(self):
#        ''' Do a little magic to place inherited scenarios under their parents '''
#        XmlModel.rebuild_tree(self)
#        child_item_nodes = dict((i,i.node) for i in self._root_item.child_items if
#                                i.node.tag == 'scenario')
#        for item, node in child_item_nodes.items():
#                scenario_parent_node = node.find('parent')
#                if scenario_parent_node is None:
#                    continue
#                scenario_parent_node = self._root_node.find(scenario_parent_node.text.strip())
#                self.insert_node(node, scenario_parent_node)




