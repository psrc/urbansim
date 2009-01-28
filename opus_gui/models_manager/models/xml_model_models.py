#
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

from PyQt4.QtCore import QVariant, QString, Qt, QModelIndex, SIGNAL
from PyQt4.QtGui import QColor

from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists

class XmlModel_Models(XmlModel):

    def __init__(self, model_root_node, project = None, parent_widget = None):
        XmlModel.__init__(self, model_root_node, project, parent_widget)

    def data(self, index, role):
        ''' PyQt API Method -- see PyQt for documentation '''

        if not index.isValid():
            return QVariant()

        node = index.internalPointer().node

        # only override displaying of left column
        if index.column() != 0:
            return XmlModel.data(self, index, role)

        if role == Qt.DisplayRole:
            if node.get('type') == 'model_system':
                # Nicer name
                return QVariant('Models')

            elif node.get('type') == 'model':
                return QVariant(node.tag)

            elif node.get('type') == 'configuration':
                # Nicer name
                return QVariant('Estimation Configuration')

        elif role == Qt.ForegroundRole:
            if node.get('type') == 'configuration':
                return QVariant(Qt.darkMagenta)

        # fall back on default
        return XmlModel.data(self, index, role)

    def add_model_node(self, model_node):
        '''
        Appends a node representing a model to the project's list of models.
        This method is a callback from the 'Add model from template' - dialogs
        @param model_node (Element) node representing the model
        '''
        model_system_node = self.root_node.find('model_system')
        model_system_node.append(model_node)
        self.rebuild_tree()

    def removeRow(self, row, parent_index):
        '''
        Override the default removeRow to also update the models_to_run
        lists.
        '''
        # Whenever we delete a model, we need to also reverify the list of
        # models to run for all the scenarios that might been using it
        # As long as we have the models names as their node tags, we don't need
        # to do anything special for renaming nodes.
        XmlModel.removeRow(self, row, parent_index)
        update_models_to_run_lists()
