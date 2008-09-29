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
from PyQt4.QtCore import QString, Qt, QRegExp, QObject, SIGNAL, QSize
from PyQt4.QtGui import QPalette, QLabel, QWidget, QLineEdit, QVBoxLayout, QFileDialog, QDialog, QHBoxLayout, QPushButton


from opus_gui.data_manager.views.configuretool_ui import Ui_ConfigureToolGui

import random

class ConfigureToolGui(QDialog, Ui_ConfigureToolGui):
    def __init__(self, xml_controller, fl):
        QDialog.__init__(self, xml_controller.mainwindow, fl)
        self.setupUi(self)
        self.xml_controller = xml_controller
        self.model = xml_controller.currentIndex.model()
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
        templates_root = self.model.xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        if templates_root.hasChildNodes():
            # These are tool groups
            groups = templates_root.childNodes()
            for x in xrange(0,groups.count(),1):
                if groups.item(x).isElement():
                    group = groups.item(x).toElement()
                    if group and group.hasChildNodes():
                        # These are tools within a group
                        tools = group.childNodes()
                        for x in xrange(0,tools.count(),1):
                            if tools.item(x).isElement():
                                tool = tools.item(x).toElement()
                                if tool.attribute(QString("type")) == QString("tool_file"):
                                    # We have a template... add it to the list
                                    self.comboBox.addItem(tool.tagName())
        # Now we hook up to the user selecting the type desired
        QObject.connect(self.comboBox, SIGNAL("currentIndexChanged(int)"),
                        self.toolTypeSelected)
        self.tooltypearray = []
        self.typeSelection = None

    def on_createConfig_released(self):
        #print "create pressed"

        # Need to create something that looks like this:
        #<opus_database_to_sql_config type="tool_config">
        #  <tool_hook type="tool_library_ref">opus_database_to_sql_tool</tool_hook>
        #  <sql_db_name type="string">mytestdb</sql_db_name>
        #  <opus_data_directory type="string" />
        #  <opus_data_year type="string">ALL</opus_data_year>
        #  <opus_table_name type="string">ALL</opus_table_name>
        #</opus_database_to_sql_config>
        
        toolname = self.test_line[0].text()
        # First is the connection node with the connection name
        newNode = self.xml_controller.currentIndex.model().domDocument.createElement(toolname)
        newNode.setAttribute(QString("type"),QString("tool_config"))
        # Add the tool hook back in
        newChild = self.xml_controller.currentIndex.model().domDocument.createElement(QString("tool_hook"))
        newChild.setAttribute(QString("type"),QString("tool_library_ref"))
        newText = self.xml_controller.currentIndex.model().domDocument.createTextNode(self.typeSelection)
        newChild.appendChild(newText)
        newNode.appendChild(newChild)
        # for key,val in self.vars.iteritems():
        for x in xrange(1,len(self.test_text)):
            #self.vars[self.test_text[x].text()] = self.test_line[x].text()
            key = self.test_text[x].text()
            val = self.test_line[x].text()
            typeVal = self.test_text_type[x].text().remove(QRegExp("[\(\)]"))
            # print "Key: %s , Val: %s" % (key,val)
            # Next we add each of the child nodes with the user defined values
            newChild = self.xml_controller.currentIndex.model().domDocument.createElement(key)
            newChild.setAttribute(QString("type"),typeVal)
            newText = self.xml_controller.currentIndex.model().domDocument.createTextNode(val)
            newChild.appendChild(newText)
            newNode.appendChild(newChild)
        self.xml_controller.currentIndex.model().insertRow(self.xml_controller.currentIndex.model().rowCount(self.xml_controller.currentIndex),
                                                   self.xml_controller.currentIndex,
                                                   newNode)
        self.xml_controller.currentIndex.model().emit(SIGNAL("layoutChanged()"))
        self.close()

    def on_cancelConfig_released(self):
        #print "cancel pressed"
        self.close()

    def toolTypeSelected(self,index):
        #print "Got a new selection"
        #print self.comboBox.itemText(index)

        self.typeSelection = self.comboBox.itemText(index)
        for testw in self.test_widget:
            self.vboxlayout.removeWidget(testw)
            testw.hide()
        del self.tooltypearray[:]
        del self.test_widget[:]
        del self.test_text[:]
        del self.test_line[:]

        # The tool_config will always have tool_config name
        self.tooltypearray.append([QString("Tool Config Name"),QString("tool_config"),QString("")])

        # Now look up the selected connection type and present to the user...
        # First we start at the Tool_Library
        templates_root = self.model.xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        if templates_root and templates_root.hasChildNodes():
            # These are tool groups
            groups = templates_root.childNodes()
            for x in xrange(0,groups.count(),1):
                if groups.item(x).isElement():
                    group = groups.item(x).toElement()
                    if group and group.hasChildNodes():
                        # These are tools within a group
                        tools = group.childNodes()
                        for x in xrange(0,tools.count(),1):
                            if tools.item(x).isElement():
                                tool = tools.item(x).toElement()
                                foundOurTool = False
                                if tool.hasAttribute(QString("type")) and \
                                       (tool.attribute(QString("type")) == QString("tool_file")):
                                    if tool.tagName() == self.comboBox.itemText(index):
                                        foundOurTool = True
                                if foundOurTool:
                                    tool_file = tool.childNodes()
                                    for xx in xrange(0,tool_file.count(),1):
                                        if tool_file.item(xx).isElement():
                                            tool_file_child = tool_file.item(xx).toElement()
                                            # Find the name element and compare
                                            if tool_file_child.hasAttribute(QString("type")) and \
                                                   (tool_file_child.attribute(QString("type")) == QString("param_template")):
                                                if tool_file_child.hasChildNodes():
                                                    params = tool_file_child.childNodes()
                                                    # Here we loop through the params
                                                    for xxx in xrange(0,params.count(),1):
                                                        if params.item(xxx).isElement():
                                                            param = params.item(xxx).toElement()
            
                                                            tagName = param.tagName()
                                                            typeName = QString('')
                                                            nodeVal = QString('')
                                                            # Now we look inside to find the discriptions of the params
                                                            if param.hasChildNodes():
                                                                desc = param.childNodes()
                                                                # Here we loop through the desc's
                                                                for xxxx in xrange(0,desc.count(),1):
                                                                    if desc.item(xxxx).isElement():
                                                                        desc_el = desc.item(xxxx).toElement()
                                                                        if desc_el.tagName() == QString('type'):
                                                                            # We have a type
                                                                            if desc_el.hasChildNodes():
                                                                                textSearch = desc_el.childNodes()
                                                                                for xxxxx in xrange(0,textSearch.count(),1):
                                                                                    if textSearch.item(xxxxx).isText():
                                                                                        typeName = textSearch.item(xxxxx).nodeValue()
                                                                        if desc_el.tagName() == QString('default'):
                                                                            if desc_el.hasChildNodes():
                                                                                textSearch = desc_el.childNodes()
                                                                                for xxxxx in xrange(0,textSearch.count(),1):
                                                                                    if textSearch.item(xxxxx).isText():
                                                                                        nodeVal = textSearch.item(xxxxx).nodeValue()
                                                            self.tooltypearray.append([tagName,typeName,nodeVal])
        for i,param in enumerate(self.tooltypearray):
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
