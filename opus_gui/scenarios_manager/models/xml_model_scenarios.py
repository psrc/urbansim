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

class XmlModel_Scenarios(XmlModel):

    def __init__(self, model_root_node, project = None, parent_widget = None):
        ''' See XmlModel.__init__ for documentation '''
        XmlModel.__init__(self, model_root_node, project, parent_widget)

    def data(self, index, role):
        ''' PyQt API Method -- See the PyQt documentation for a description '''

        # Handle special drawing of missing models
        item = index.internalPointer()
        if not hasattr(item, 'is_missing_model') or not item.is_missing_model:
            # Not a missing model -- use default data handler
            return XmlModel.data(self, index, role)

        # Colorize item
        if role == Qt.ForegroundRole and index.column() == 1:
            return QVariant(QColor(Qt.red))
        # Give it a special icon
        elif role == Qt.DecorationRole and index.column() == 0:
            return QVariant(self.missingModelIcon)
        # Add a small information string next to it's checkbox
        elif role == Qt.DisplayRole and index.column() == 1:
            return QVariant("(cannot find model)")

        # Other data properties are handled by the default data() method
        return XmlModel.data(self, index, role)
