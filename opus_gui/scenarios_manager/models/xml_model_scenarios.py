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
from PyQt4.QtGui import QColor, QIcon

from opus_gui.abstract_manager.models.xml_model import XmlModel

class XmlModel_Scenarios(XmlModel):

    def __init__(self, parentTree, document, mainwindow, configFile, xmlType,
                 editable, addIcons=True):
        XmlModel.__init__(self, parentTree, document, mainwindow, configFile,
                          xmlType, editable, addIcons)

    def data(self, index, role):
        # override the data method to enable custom icons for missing models

        item = index.internalPointer()
        if not hasattr(item, 'is_missing_model') or \
            item.is_missing_model == False:
            # we don't need special handling if there's no missing model
            return XmlModel.data(self, index, role)

        # Override display for missing models
        if role == Qt.ForegroundRole and index.column() == 1:
            return QVariant(QColor(Qt.red))
        elif role == Qt.DecorationRole and index.column() == 0:
            return QVariant(self.missingModelIcon)
        elif role == Qt.DisplayRole and index.column() == 1:
            # add (missing model) next to check box
            return QVariant("(missing model)")
        
        # fall back on default
        return XmlModel.data(self, index, role)
