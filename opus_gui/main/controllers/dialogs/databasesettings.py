# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from xml.etree.cElementTree import ElementTree

from PyQt4.QtGui import QDialog, QMessageBox

from opus_gui.main.controllers.dialogs.message_box import MessageBox
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
            root = ElementTree(file=self._config_filename).getroot()
            view = XmlView(self)
            model = XmlModel(root)
            delegate = XmlItemDelegate(view)
            view.setModel(model)
            view._model = model # HACK this is necessary so that Qt don't GC the model object
            view._delegate = delegate # Same as above
            view.setItemDelegate(delegate)
            view.openDefaultItems()

            self.gridlayout.addWidget(view)

            self.tree_view = view
            self.xml_root = root
            return

        except IOError, ex:
            MessageBox.error(mainwindow = self,
                          text = 'Could not initialize Database Settings',
                          detailed_text = str(ex))
            self.xml_root = None
            self._config_filename = ''
            self.configFile = None

    def on_buttonBox_accepted(self):
        try:
            ElementTree(self.xml_root).write(self._config_filename)
        except IOError, ex:
            MessageBox.error(self,
                          text = 'A disk error occured when saving the ' +
                          'settings.',
                          detailed_text = str(ex))
        except Exception, ex:
            MessageBox.error(mainwindow = self,
                          text = 'An unknown error occured when saving ' +
                          'your changes.',
                          detailed_text = str(ex))
        finally:
            self.close()

    def on_buttonBox_rejected(self):
        # If there are any changes to the data, ask the user to save them
        if self.tree_view.model().dirty:
            question = ('Changes have been made to the settings.\n'
                        'Do you want to save or discard those changes?')
            buttons = (QMessageBox.Discard, QMessageBox.Save, QMessageBox.Cancel)
            doSave = QMessageBox.question(self, "Warning", question, *buttons)
            if doSave == QMessageBox.Save:
                self.on_buttonBox_accepted()
            elif doSave == QMessageBox.Discard:
                self.close()
            else:
                return # Cancel
        self.close()
