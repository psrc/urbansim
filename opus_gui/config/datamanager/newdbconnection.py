# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from opus_gui.config.datamanager.newdbconnection_ui import Ui_NewDbConnectionGui

import random

class NewDbConnectionGui(QDialog, Ui_NewDbConnectionGui):
    def __init__(self, parent, fl):
        QDialog.__init__(self, parent.mainwindow, fl)
        self.setupUi(self)
        self.parent = parent
        self.model = parent.currentIndex.model()
        self.vars = {}
        # To test... add some dummy vars
        self.vboxlayout = QVBoxLayout(self.variableBox)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.test_widget = []
        self.hboxlayout = []
        self.test_text = []
        self.test_line = []
        # First find the available database connection templates to fill in types
        templates_root = self.model.xmlRoot.toElement().elementsByTagName(QString("database_templates")).item(0)
        if templates_root.hasChildNodes():
            children = templates_root.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).toElement().attribute(QString("type")) == QString("db_template"):
                    # We have a template... add it to the list
                    self.comboBox.addItem(children.item(x).toElement().tagName())
        # Now we hook up to the user selecting the type desired
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"),
                        self.databaseTypeSelected)
        self.dbtypearray = []
    
    def on_createConfig_released(self):
        print "create pressed - Need to add the config to the XML here..."
        for x in xrange(0,len(self.test_text)):
            self.vars[self.test_text[x].text()] = self.test_line[x].text()
        for key,val in self.vars.iteritems():
            print "Key: %s , Val: %s" % (key,val)
        self.close()

    def on_cancelConfig_released(self):
        print "cancel pressed"
        self.close()

    def databaseTypeSelected(self,index):
        #print "Got a new selection"
        for testw in self.test_widget:
            self.vboxlayout.removeWidget(testw)
            testw.hide()
        # Now look up the selected connection type and present to the user...
        templates_root = self.model.xmlRoot.toElement().elementsByTagName(QString("database_templates")).item(0)
        if templates_root.hasChildNodes():
            children = templates_root.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).toElement().tagName() == self.comboBox.itemText(index):
                    if children.item(x).hasChildNodes():
                        children2 = children.item(x).childNodes()
                        for y in xrange(0,children2.count(),1):
                            # We have a parameter... need to get tag name and text node value
                            tagName = children2.item(y).toElement().tagName()
                            nodeVal = QString('')
                            if children2.item(y).hasChildNodes():
                                children3 = children2.item(y).childNodes()
                                for z in xrange(0,children3.count(),1):
                                    if children3.item(z).isText():
                                        nodeVal = children3.item(z).nodeValue()
                            self.dbtypearray.append([tagName,nodeVal])
        for param in self.dbtypearray:
            #print "Key: %s , Val: %s" % (param[0],param[1])
            widgetTemp = QWidget(self.variableBox)
            widgetTemp.setObjectName(QString("test_widget").append(str(param[0])))
            self.test_widget.append(widgetTemp)
            hlayout = QHBoxLayout(widgetTemp)
            self.hboxlayout.append(hlayout)
            hlayout.setMargin(4)
            hlayout.setSpacing(4)
            hlayout.setObjectName(QString("hboxlayout").append(str(param[0])))
            test_text = QLabel(widgetTemp)
            self.test_text.append(test_text)
            test_text.setObjectName(QString("test1_text").append(str(param[0])))
            paramName = QString(str(param[0]))
            if param[1].trimmed() == QString("Required"):
                palette = test_text.palette()
                palette.setColor(QPalette.WindowText,Qt.red)
                test_text.setPalette(palette)
            test_text.setText(paramName)
            hlayout.addWidget(test_text)
            test_line = QLineEdit(widgetTemp)
            self.test_line.append(test_line)
            test_line.setEnabled(True)
            test_line.setMinimumSize(QSize(200,0))
            test_line.setObjectName(QString("test_line").append(str(param[0])))
            test_line.setText(QString(""))
            hlayout.addWidget(test_line)
            self.vboxlayout.addWidget(widgetTemp)
        
