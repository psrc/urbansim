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

from PyQt4.QtCore import QVariant, Qt
from PyQt4.QtGui import QColor

from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.models_manager.models_manager import get_model_names

class XmlModel_Scenarios(XmlModel):

    def __init__(self, model_root_node, project = None, parent_widget = None):
        ''' See XmlModel.__init__ for documentation '''
        XmlModel.__init__(self, model_root_node, project, parent_widget)

    def data(self, index, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        # Handle special drawing of missing models
        item = index.internalPointer()
        if not hasattr(item, 'model_is_missing') or not item.model_is_missing:
            # Not a missing model -- use default data handler
            return XmlModel.data(self, index, role)

        # Handle missing models
        # Colorize item
        if role == Qt.ForegroundRole and index.column() == 1:
            return QVariant(QColor(Qt.red))
        # Give it a special icon
        elif role == Qt.DecorationRole and index.column() == 0:
            return QVariant(self.missingModelIcon)
        # Add a small information string next to it's checkbox
        elif role == Qt.DisplayRole and index.column() == 1:
            return QVariant("(no such model)")

        # Other data properties are handled by the default data() method
        return XmlModel.data(self, index, role)

    def validate_models_to_run(self):
        '''
        Goes through all scenarios in the XmlController and makes sure that
        the models in their 'models_to_run' list actually is present in the
        project.
        '''
        # Monkey-patch the items in "models to run" lists that hold invalid
        # references to models
        model_names = get_model_names(self.project)

        scenario_items = self._root_item.child_items
        for scenario_item in scenario_items:
            models_to_run_item = None
            for child_item in scenario_item.child_items:
                if child_item.node.tag == 'models_to_run':
                    models_to_run_item = child_item
                    break
            if models_to_run_item is None:
                continue # no models to run list, go to next scenario
            for model_item in models_to_run_item.child_items:
                model_item.model_is_missing = \
                    model_item.node.tag not in model_names
