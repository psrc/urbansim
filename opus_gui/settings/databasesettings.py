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

# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from opus_gui.config.xmltree.opusxmltree import OpusXMLTree
import os

from opus_core.misc import directory_path_from_opus_path
from xml.etree.cElementTree import ElementTree, tostring
import StringIO


# UI specific includes
from databasesettings_ui import Ui_databaseConfigEditor
from opus_gui.settings.databasesettingsview import *



############ APR Added 082908 as example of using OpusXMLTree for database XML editing
from databasesettingsedit_ui import Ui_DatabaseSettingsEditGui
from opus_gui.config.xmltree.opusxmltree import OpusXMLTree

class DatabaseSettingsEditGui(QDialog, Ui_DatabaseSettingsEditGui):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow

        settings_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        self.database_server_configuration_file = os.path.join(settings_directory, 'database_server_configurations.xml')
        self.configFile = QFile(self.database_server_configuration_file)
        self.doc = QDomDocument()
        self.doc.setContent(self.configFile)
        self.databaseSettingsEditTree = OpusXMLTree(self,"database_server_configurations",
                                                    self.gridlayout)

    def on_saveChanges_released(self):
        #print "save pressed"
        indentSize = 2
        self.configFile.close()
        self.configFile.open(QIODevice.ReadWrite | QIODevice.Truncate)
        out = QTextStream(self.configFile)
        self.doc.save(out, indentSize)
        self.close()

    def on_cancelWindow_released(self):
        #print "cancel pressed"
        self.configFile.close()
        self.close()
############ APR Added 082908 as example of using OpusXMLTree for database XML editing



class UrbansimDatabaseSettingsGUI(QDialog, Ui_databaseConfigEditor):
    def __init__(self, mainwindow, fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.databaseSettingsDataView = DatabaseSettingsDataView(self)
        self.databaseSettingsDataView.setGeometry(QRect(20,20,361,211))
        self.databaseSettingsDataView.setObjectName("databaseSettingsTreeView")
        self.mainwindow = mainwindow
        
        settings_directory = os.path.join(os.environ['OPUS_HOME'], 'settings')
        self.database_server_configuration_file = os.path.join(settings_directory, 'database_server_configurations.xml')
        qf = QFile(self.database_server_configuration_file)
        self.database_server_configuration_doc = QDomDocument()
        self.database_server_configuration_doc.setContent(qf)
        self.databaseSettingsDataModel = DatabaseSettingsDataModel(self.database_server_configuration_doc, \
                                  self, self.database_server_configuration_file, \
                                  "", True)
        
        self.databaseSettingsDataView.setModel(self.databaseSettingsDataModel)
        self.databaseSettingsDataView.openDefaultItems()
                                  
                                  
        #hook up the buttons
        
 
    def _saveDatabaseConnectionSettings_(self):
        str_io = StringIO.StringIO(self.database_server_configuration_doc.toString(2))
        etree = ElementTree(file=str_io)
        etree.write(self.database_server_configuration_doc)
        str_io.close()
        
    def accepted(self):
        self._saveDatabaseConnectionSettings_()
        self.done()
        
