# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
import re
from lxml.etree import ElementTree

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtWidgets, QtCore

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.util import common_dialogs
from opus_gui.main.controllers.xml_configuration.database_config_xml_controller import XmlController_DatabaseConfig

from opus_gui.main.views.ui_databasesettingsedit import Ui_DatabaseSettingsEditGui
from opus_core.database_management.configurations.database_server_configuration import DatabaseServerConfiguration
from opus_core import paths

class DatabaseSettingsEditGui(QDialog, Ui_DatabaseSettingsEditGui):
    project = None
    
    def __init__(self, parent_widget):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)
        
        desc = '\n'.join(('%(PROTOCOL_TAG)s: Database protocol. Double-click and hold to see the available options.',
                          '%(HOST_NAME_TAG)s: Host name (and database name for Postgres).',
                          '    * Postgres: Use the format "host_name/database_name" (without quotes).',
                          '          - Leave host_name empty to connect to localhost.',
                          '          - Leave database_name empty (but retain the slash) to connect',
                          '            to the default database for the database user.',
                          '    * Other protocols: Enter the host name only.',
                          '%(USER_NAME_TAG)s: Database user name',
                          '%(PASSWORD_TAG)s: Database password',
                          '',
                          'To add a new database configuration, please edit',
                          '%(conf_file_path)s'
                          )
                         )
        desc = QtWidgets.QApplication.translate("DatabaseSettingsEditGui", desc, None, QtWidgets.QApplication.UnicodeUTF8)
        desc = str(desc) % dict([(n, eval('DatabaseServerConfiguration.%s'%n)) for n in dir(DatabaseServerConfiguration) if re.match('.*_TAG$', n)] +
                                    [('conf_file_path', DatabaseServerConfiguration.get_default_configuration_file_path())])
        desc = QtCore.(desc)
        
        self.description.setText(desc)

        self._config_filename = DatabaseServerConfiguration.get_default_configuration_file_path()

        try:
            self.xml_root = ElementTree(file=self._config_filename).getroot()
            self.base_widget = self.variableBox
            self.xml_controller = XmlController_DatabaseConfig(self)
            # Turns out that Qt Garbage collects the model (and delegate) if we don't explicitly
            # bind it to a Python object in addition to using the PyQt .setModel() method.

            self.tree_view = self.xml_controller.view
            return

        except IOError as ex:
            MessageBox.error(mainwindow = self,
                          text = 'Could not initialize Database Settings',
                          detailed_text = str(ex))
            self.xml_root = None
            self._config_filename = ''
            self.configFile = None

    def on_buttonBox_accepted(self):
        try:
            ElementTree(self.xml_root).write(self._config_filename, pretty_print=True, with_tail=False)
        except IOError as ex:
            MessageBox.error(self,
                          text = 'A disk error occured when saving the ' +
                          'settings.',
                          detailed_text = str(ex))
        except Exception as ex:
            MessageBox.error(mainwindow = self,
                          text = 'An unknown error occured when saving ' +
                          'your changes.',
                          detailed_text = str(ex))
        finally:
            self.close()

    def on_buttonBox_rejected(self):
        # If there are any changes to the data, ask the user to save them
        if self.tree_view.model().dirty:
            question = 'Do you want to save your changes before closing?'
            user_answer = common_dialogs.save_before_close(question)
            if user_answer == common_dialogs.YES:
                self.on_buttonBox_accepted()
            elif user_answer == common_dialogs.NO:
                pass
            else:
                return # Cancel
        self.close()
