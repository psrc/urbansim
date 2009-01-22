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

from xml.etree.cElementTree import ElementTree

from PyQt4.QtGui import QDialog, QTreeView
from opus_gui.abstract_manager.models.xml_model import XmlModel
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate
from opus_gui.abstract_manager.views.xml_view import XmlView
import os

from opus_gui.main.views.ui_databasesettingsedit import Ui_DatabaseSettingsEditGui

class DatabaseSettingsEditGui(QDialog, Ui_DatabaseSettingsEditGui):
    def __init__(self, parent_widget):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        settings_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        self._config_filename = \
            os.path.join(settings_directory,
                         'database_server_configurations.xml')
        try:
            self.xml_root = ElementTree(file=self._config_filename).getroot()
            self.tree_view = XmlView(self)
            self.tree_view.setModel(XmlModel(self.xml_root))
            self.tree_view.setItemDelegate(XmlItemDelegate(self.tree_view))
            self.tree_view.openDefaultItems()
            self.gridlayout.addWidget(self.tree_view)

        except IOError, ex:
            print str(ex)
            self.xml_root = None
            self._config_filename = ''
            self.configFile = None

    def on_saveChanges_released(self):
        try:
            ElementTree(self.xml_root).write(self._config_filename)
        finally:
            self.close()

    def on_cancelWindow_released(self):
        self.close()

