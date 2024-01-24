# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_gui.main.controllers.instance_handlers import get_db_connection_names

import copy

from lxml.etree import Element, SubElement

# PyQt5 includes for python bindings to QT
from PyQt5.QtCore  import  Qt, QRegExp, QObject, pyqtSignal, QSize, pyqtSlot
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, QVBoxLayout, QFileDialog, QDialog, QHBoxLayout, QPushButton, QFrame, QComboBox

from opus_gui.data_manager.views.ui_configuretool import Ui_ConfigureToolGui

import random

class ConfigureToolGui(QDialog, Ui_ConfigureToolGui):
    def __init__(self, tool_library_node, callback, parent_widget = None):
        QDialog.__init__(self, parent_widget)
        self.setupUi(self)

        self.tool_library_node = tool_library_node
        self.callback = callback

        self.vars = {}
        # To test... add some dummy vars
        self.vboxlayout = QVBoxLayout(self.variableBox)
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.test_widget = []
        self.hboxlayout = []
        self.test_text = []
        self.test_text_type = []
        self.test_line = []

        self.tool_nodes = {}
        for tool_group_node in tool_library_node:
            for tool_file_node in tool_group_node:
                self.tool_nodes[tool_file_node.get('name')] = tool_file_node
                self.comboBox.addItem(tool_file_node.get('name'))

        # Now we hook up to the user selecting the type desired
        #QObject.connect(self.comboBox, pyqtSignal("currentIndexChanged(int)"),
        #                self.toolTypeSelected)
        self.comboBox.currentIndexChanged.connect(self.toolTypeSelected)

        self.tooltypearray = []
        self.typeSelection = None
        self.setWindowTitle(("Add and configure tool..."))

    @pyqtSlot()
    def on_createConfig_clicked(self):
        toolname = str(self.test_line[0].text())
        if(len(toolname) < 1):
            self.test_line[0].setText('must specify configuration name')
            self.test_line[0].selectAll()
            self.test_line[0].setFocus()
            return

        newNode = Element('tool_config', {'name': toolname})
        newChild = SubElement(newNode, 'tool_hook', {'hidden': 'True', })
        newChild.text = str(self.typeSelection)

        # for key,val in self.vars.iteritems():
        for x in range(1,len(self.test_text)):
            #self.vars[self.test_text[x].text()] = self.test_line[x].text()
            if type(self.test_line[x]) == QComboBox:
                key = self.test_text[x].text()
                val = self.test_line[x].currentText()
            else:
                key = self.test_text[x].text()
                val = self.test_line[x].text()
            typeVal = self.test_text_type[x].text().remove(QRegExp("[\(\)]"))
            SubElement(newNode, str(key)).text = str(val)
        self.callback(newNode)
        self.close()

    @pyqtSlot()
    def on_cancelConfig_clicked(self):
        #print "cancel pressed"
        self.close()

    def toolTypeSelected(self, index):
        #print "Got a new selection"
        #print self.comboBox.itemText(index)

        self.typeSelection = str(self.comboBox.itemText(index))
        for testw in self.test_widget:
            self.vboxlayout.removeWidget(testw)
            testw.hide()
        self.tooltypearray = []
        self.test_widget = []
        self.test_text = []
        self.test_line = []

        # The tool_config will always have tool_config name
        self.tooltypearray.append(["Tool Config Name","tool_config",""])

        # Now look up the selected connection type and present to the user...
        # First we start at the tool_library
        tool_name = str(self.typeSelection)
        tool_node = self.tool_nodes[tool_name]
        for param_node in tool_node.find('params'):
            type_val = param_node.get('param_type')
            default_val = param_node.text or ''
            self.tooltypearray.append([param_node.get('name'), type_val, default_val])

        for i, param in enumerate(self.tooltypearray):
            # print "Key: %s , Val: %s" % (param[0],param[1])
            paramName = str(param[0] or '').strip()
            type_val = str(param[1] or '').strip()
            default_val = str(param[2] or '').strip()

            if (i==0):
                widgetTemp = QFrame(self.variableBox)
                widgetTemp.setFrameStyle(QFrame.Panel | QFrame.Raised)
                widgetTemp.setLineWidth(2)
            else:
                widgetTemp = QWidget(self.variableBox)
            widgetTemp.setObjectName(("test_widget").append((i)))
            self.test_widget.append(widgetTemp)
            hlayout = QHBoxLayout(widgetTemp)
            self.hboxlayout.append(hlayout)
            hlayout.setContentsMargins(4, 4, 4, 4)
            hlayout.setSpacing(4)
            hlayout.setObjectName(("hboxlayout").append((i)))
            test_text = QLabel(widgetTemp)
            self.test_text.append(test_text)
            test_text.setObjectName(("test_text").append((i)))
            if type_val == "Required":
                palette = test_text.palette()
                palette.setColor(QPalette.WindowText,Qt.red)
                test_text.setPalette(palette)
            test_text.setText(paramName)
            test_text_type = QLabel(widgetTemp)
            self.test_text_type.append(test_text_type)
            test_text_type.setObjectName(("test_text_type").append((i)))
            paramName = type_val
            test_text_type.setText(("(").append(paramName).append((")")))
            hlayout.addWidget(test_text)
            hlayout.addWidget(test_text_type)
            if type_val == 'db_connection_hook':
                test_line = QComboBox(widgetTemp)
                db_connection_choices = get_db_connection_names()
                for i in db_connection_choices:
                    test_line.addItem((i))
                self.test_line.append(test_line)
                test_line.setEnabled(True)
                test_line.setMinimumSize(QSize(200,0))
                test_line.setObjectName(("test_line").append((i)))
            else:
                test_line = QLineEdit(widgetTemp)
                self.test_line.append(test_line)
                test_line.setEnabled(True)
                test_line.setMinimumSize(QSize(200,0))
                test_line.setObjectName(("test_line").append((i)))
#            test_line = QLineEdit(widgetTemp)
#            self.test_line.append(test_line)
#            test_line.setEnabled(True)
#            test_line.setMinimumSize(QSize(200,0))
#            test_line.setObjectName(("test_line").append((i)))
#            test_line.setText((""))
            hlayout.addWidget(test_line)
            self.vboxlayout.addWidget(widgetTemp)
