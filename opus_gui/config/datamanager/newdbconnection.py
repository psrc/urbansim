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
        self.test_text_type = []
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
        # print "create pressed - Need to add the config to the XML here..."
        databasename = self.test_line[0].text()
        # First is the connection node with the connection name
        newNode = self.parent.currentIndex.model().domDocument.createElement(databasename)
        newNode.setAttribute(QString("type"),QString("db_connection"))
        # for key,val in self.vars.iteritems():
        for x in xrange(1,len(self.test_text)):
            #self.vars[self.test_text[x].text()] = self.test_line[x].text()
            key = self.test_text[x].text()
            val = self.test_line[x].text()
            typeVal = self.test_text_type[x].text().remove(QRegExp("[\(\)]"))
            # print "Key: %s , Val: %s" % (key,val)
            # Next we add each of the child nodes with the user defined values
            newChild = self.parent.currentIndex.model().domDocument.createElement(key)
            newChild.setAttribute(QString("type"),typeVal)
            newText = self.parent.currentIndex.model().domDocument.createTextNode(val)
            newChild.appendChild(newText)
            newNode.appendChild(newChild)
        self.parent.currentIndex.model().insertRow(self.parent.currentIndex.model().rowCount(self.parent.currentIndex),
                                                   self.parent.currentIndex,
                                                   newNode)
        self.parent.currentIndex.model().emit(SIGNAL("layoutChanged()"))
        self.close()

    def on_cancelConfig_released(self):
        # print "cancel pressed"
        self.close()

    def databaseTypeSelected(self,index):
        # print "Got a new selection"
        for testw in self.test_widget:
            self.vboxlayout.removeWidget(testw)
            testw.hide()
        del self.dbtypearray[:]
        del self.test_widget[:]
        del self.test_text[:]
        del self.test_line[:]
        # The database connection will always have a tagname
        self.dbtypearray.append([QString("Database Connection Name"),QString("db_connection"),QString("")])
        # Now look up the selected connection type and present to the user...
        templates_root = self.model.xmlRoot.toElement().elementsByTagName(QString("database_templates")).item(0)
        if templates_root and templates_root.hasChildNodes():
            children = templates_root.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).toElement().tagName() == self.comboBox.itemText(index):
                    if children.item(x).hasChildNodes():
                        children2 = children.item(x).childNodes()
                        for y in xrange(0,children2.count(),1):
                            # We have a parameter... need to get tag name and text node value
                            tagName = children2.item(y).toElement().tagName()
                            typeName = QString('')
                            typeName = children2.item(y).toElement().attribute(QString("type"))
                            nodeVal = QString('')
                            if children2.item(y).hasChildNodes():
                                children3 = children2.item(y).childNodes()
                                for z in xrange(0,children3.count(),1):
                                    if children3.item(z).isText():
                                        nodeVal = children3.item(z).nodeValue()
                            self.dbtypearray.append([tagName,typeName,nodeVal])
        for i,param in enumerate(self.dbtypearray):
            # print "Key: %s , Val: %s" % (param[0],param[1])
            if (i==0):
                widgetTemp = QFrame(self.variableBox)
                widgetTemp.setFrameStyle(QFrame.Panel | QFrame.Raised)
                widgetTemp.setLineWidth(2)
            else:
                widgetTemp = QWidget(self.variableBox)
            widgetTemp.setObjectName(QString("test_widget").append(QString(i)))
            self.test_widget.append(widgetTemp)
            hlayout = QHBoxLayout(widgetTemp)
            self.hboxlayout.append(hlayout)
            hlayout.setMargin(4)
            hlayout.setSpacing(4)
            hlayout.setObjectName(QString("hboxlayout").append(QString(i)))
            test_text = QLabel(widgetTemp)
            self.test_text.append(test_text)
            test_text.setObjectName(QString("test_text").append(QString(i)))
            paramName = param[0].trimmed()
            if param[2].trimmed() == QString("Required"):
                palette = test_text.palette()
                palette.setColor(QPalette.WindowText,Qt.red)
                test_text.setPalette(palette)
            test_text.setText(paramName)
            test_text_type = QLabel(widgetTemp)
            self.test_text_type.append(test_text_type)
            test_text_type.setObjectName(QString("test_text_type").append(QString(i)))
            paramName = param[1].trimmed()
            test_text_type.setText(QString("(").append(paramName).append(QString(")")))
            hlayout.addWidget(test_text)
            hlayout.addWidget(test_text_type)
            test_line = QLineEdit(widgetTemp)
            self.test_line.append(test_line)
            test_line.setEnabled(True)
            test_line.setMinimumSize(QSize(200,0))
            test_line.setObjectName(QString("test_line").append(QString(i)))
            test_line.setText(QString(""))
            hlayout.addWidget(test_line)
            self.vboxlayout.addWidget(widgetTemp)

