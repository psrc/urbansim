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
from PyQt4.QtCore import QFile, QIODevice, QTextStream
from PyQt4.QtGui import QDialog
from PyQt4.QtXml import QDomDocument
from opus_gui.main.controllers.database_config_xml_controller import DatabaseConfigXMLController
import os

############ APR Added 082908 as example of using OpusXMLTree for database XML editing
from opus_gui.main.views.ui_databasesettingsedit import Ui_DatabaseSettingsEditGui

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
        self.databaseSettingsEditTree = DatabaseConfigXMLController(self,"database_server_configurations",
                                                    self.gridlayout)
        print self.doc.documentElement().tagName()

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

