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

from xml.etree.cElementTree import Element, SubElement

from PyQt4.QtCore import QString, Qt, QRegExp, QObject, SIGNAL, QSize
from PyQt4.QtGui import QPalette, QLabel, QWidget, QLineEdit, QVBoxLayout, QFileDialog, QDialog, QHBoxLayout, QPushButton, QComboBox, QMessageBox

from opus_gui.data_manager.views.ui_executetool import Ui_ExecuteToolGui
from opus_gui.data_manager.run.run_tool import RunToolThread, OpusTool
from opus_gui.main.controllers.instance_handlers import get_db_connection_names

class FileDialogSignal(QWidget):
    ''' NO DOCUMENTATION '''

    def __init__(self, parent=None, typeName=None, param=None):
        ''' NO DOCUMENTATION '''
        QWidget.__init__(self, parent)
        self.o = QObject()
        self.param = param
        self.type = typeName

    def updateParam(self,param):
        ''' NO DOCUMENTATION '''
        self.param = param

    def updateType(self,typeName):
        ''' NO DOCUMENTATION '''
        self.type = typeName

    def relayButtonSignal(self):
        ''' NO DOCUMENTATION '''
        #print "relayButtonSignal"
        self.o.emit(SIGNAL("buttonPressed(PyQt_PyObject,PyQt_PyObject)"),self.type,self.param)

class ExecuteToolGui(QDialog, Ui_ExecuteToolGui):

    def __init__(self, parent_widget, tool_node, tool_library_node, params = {}):
        ''' NO DOCUMENTATION '''
        window_flags = (Qt.WindowTitleHint |
                        Qt.WindowSystemMenuHint |
                        Qt.WindowMaximizeButtonHint)
        QDialog.__init__(self, parent_widget, window_flags)
        self.setupUi(self)

        # Grab the tool we are interested in...
        self.tool_node = tool_node
        self.tool_library_node = tool_library_node

        self.vars = {}

        self.optional_params = params

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
        self.test_line_delegates = []
        self.test_line_buttons = []

        # Decide if we have a tool_file or tool_config
        # If we have a too_file, then we need to traverse the XML and create a temporary
        # config to be used.
        # If we have a config we just extract the params and create the GUI elements

        # Note about conversion from QtXml to ElementTree
        # The code below is an interpretation of the original codes intent --
        # TODO test that this does what it's supposed to do
        self.tooltypearray = []
        if tool_node.get('type') == 'tool_file':
            self.type_selection = self.tool_node.tag
            self.tool_name = tool_node.find('name').text
            self.presentToolFileGUI()
        else:
            tool_hook_node = tool_node.find('tool_hook')
            # tag name of the 'hooked' tool
            self.type_selection = tool_hook_node.text
            # Find the 'hooked' tool and get it's <name>
            for tool in self.tool_library_node[:]:
                if tool.tag == self.type_selection:
                    self.tool_name = tool.find('name').text
                    break
            print('ExecuteToolGui: Could not find tool for tool_hook "%s"'
                  % self.type_selection)
            self.tool_name = ''
            self.presentToolConfigGUI()

        self.setWindowTitle(self.type_selection.replace('_', ' '))

    def on_execTool_released(self):
        #print "create pressed"

        # Need to create something that looks like this:
        #<opus_database_to_sql_config type="tool_config">
        #  <tool_hook type="tool_library_ref">opus_database_to_sql_tool</tool_hook>
        #  <sql_db_name type="string">mytestdb</sql_db_name>
        #  <opus_data_directory type="string" />
        #  <opus_data_year type="string">ALL</opus_data_year>
        #  <opus_table_name type="string">ALL</opus_table_name>
        #</opus_database_to_sql_config>
        #print "Main Window Prio - %s" % (str(self.mainwindow.thread().priority()))
        self.execTool.setEnabled(False)
        self.textEdit.clear()
        self.progressBar.setValue(0)

        # self.test_text contains the parameter name  (stored as a QLabel instance)
        # self.test_line contains the editor (QLineEdit or QComboBox) for the parameter value
        # self.test_text_type contains the value for the type attribute (QLineEdit)
        # for each parameter; construct a XML node in the following format
        #  <parameter-name type="type-value"> parameter-value </parameter-name>

        tmp_config_node = Element('temp_config', {'type': 'tool_config'})
        SubElement(tmp_config_node, 'tool_hook',
                   {'type': 'tool_library_ref'}).text = self.type_selection
        for i in range(0, len(self.test_text)):
            param_name = str(self.test_text[i].text())
            if type(self.test_line[i]) == QComboBox:
                param_value = str(self.test_line[i].currentText())
            else:
                param_value = str(self.test_line[i].text())
            type_value = self.test_text_type[i].text().remove(QRegExp("[\(\)]"))
            type_value = str(type_value)
            SubElement(tmp_config_node, param_name,
                       {'type': type_value}).text = param_value

        self.execToolConfigGen(tmp_config_node)

    def on_cancelExec_released(self):
        #print "cancel pressed"
        self.close()

    def fillInToolTypeArrayFromToolFile(self):
        # Find params subnode
        param_nodes = self.tool_node.find('params') or []
        for param_node in param_nodes:
            type_ = param_node.find('type').text or ''
            default_value = param_node.find('default').text or ''
            self.tooltypearray.append([param_node.tag, type_, default_value])

    def fillInToolTypeArrayFromToolConfig(self):
        ''' NO DOCUMENTATION '''
        for child in self.tool_node.find('params'):
            if not child.get('type') == 'tool_library_ref':
                print 'adding parameter %s (%s): %s' %(child.tag, child.get('type'), child.text)
                self.tooltypearray.append([child.tag,
                                           child.get('type'),
                                           child.text])

    def createGUIElements(self):
        ''' Build the GUI based on the parameters for the tool '''
        for i, param in enumerate(self.tooltypearray):
            print 'creatgui element %d, %s' %(i, param)
            #Swap in the passed params if they exist... loop through each passed
            #param and see if it matches... if so swap it in
            if self.optional_params.has_key(str(param[0])):
                param[2] = self.optional_params[str(param[0])]
            #print "Key: %s , Val: %s" % (param[0],param[1])
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
            paramName = param[0].strip()
            if param[2].strip() == "Required":
                palette = test_text.palette()
                palette.setColor(QPalette.WindowText,Qt.red)
                test_text.setPalette(palette)
            test_text.setText(paramName)
            test_text_type = QLabel(widgetTemp)
            self.test_text_type.append(test_text_type)
            test_text_type.setObjectName(QString("test_text_type").append(QString(i)))
            paramName = param[1].strip()
            test_text_type.setText(QString("(").append(paramName).append(QString(")")))
            hlayout.addWidget(test_text)
            hlayout.addWidget(test_text_type)
            if param[1] == 'db_connection_hook':
                test_line = QComboBox(widgetTemp)
                db_connection_choices = get_db_connection_names()
                for i in db_connection_choices:
                    test_line.addItem(QString(i))
                self.test_line.append(test_line)
                test_line.setEnabled(True)
                test_line.setMinimumSize(QSize(200,0))
                test_line.setObjectName(QString("test_line").append(QString(i)))
                index = test_line.findText(param[2], Qt.MatchExactly)
                test_line.setCurrentIndex(index)
            else:
                test_line = QLineEdit(widgetTemp)
                self.test_line.append(test_line)
                test_line.setEnabled(True)
                test_line.setMinimumSize(QSize(200,0))
                test_line.setObjectName(QString("test_line").append(QString(i)))
                test_line.setText(QString(param[2]))
            hlayout.addWidget(test_line)
            # If we have a dir_path or file_path add a select button
            if (paramName == QString('dir_path')) or (paramName == QString('file_path')):
                pbnSelect = QPushButton(widgetTemp)
                pbnSelect.setObjectName(QString('pbnSelect').append(QString(i)))
                pbnSelect.setText(QString("Select..."))
                pbnSelectDelegate = FileDialogSignal(typeName=paramName,param=test_line)
                QObject.connect(pbnSelectDelegate.o, SIGNAL("buttonPressed(PyQt_PyObject,PyQt_PyObject)"),
                                self.on_pbnSelect_released)
                QObject.connect(pbnSelect, SIGNAL("released()"), pbnSelectDelegate.relayButtonSignal)
                self.test_line_delegates.append(pbnSelectDelegate)
                self.test_line_buttons.append(pbnSelect)
                hlayout.addWidget(pbnSelect)
            self.vboxlayout.addWidget(widgetTemp)
            self.adjustSize()
        # Jesse adding help text from opusHelp
        tool_path_node = self.tool_library_node.find('tool_path')
        tool_path = tool_path_node.text if tool_path_node is not None else ''
        try:
            exec_stmt = 'from %s.%s import opusHelp' % (tool_path, self.tool_name)
            exec exec_stmt
            help = QString(opusHelp())
            self.toolhelpEdit.insertPlainText(help)
        except:
            help = 'could not find opusHelp function in tool module'
            self.toolhelpEdit.insertPlainText(help)

    def on_pbnSelect_released(self,typeName,line):
        #print "on_pbnSelect_released recieved"
        editor_file = QFileDialog()
        filter_str = QString("*.*")
        editor_file.setFilter(filter_str)
        editor_file.setAcceptMode(QFileDialog.AcceptOpen)
        if typeName == QString("file_path"):
            fd = editor_file.getOpenFileName(self, self.QString("Please select a file..."),
                                             line.text())
        else:
            fd = editor_file.getExistingDirectory(self,QString("Please select a directory..."),
                                                  line.text())
        # Check for cancel
        if len(fd) != 0:
            fileName = QString(fd)
            line.setText(fileName)

    def presentToolFileGUI(self):
        #print "Got a new selection"
        #print self.comboBox.itemText(index)
        self.fillInToolTypeArrayFromToolFile()
        self.createGUIElements()

    def presentToolConfigGUI(self):
        # First, fillInToolTypeArrayFromToolConfig
        print 'Filling in type array from tool config'
        self.fillInToolTypeArrayFromToolConfig()
        self.createGUIElements()

    def toolFinishedFromThread(self,success):
        #print "toolFinishedFromThread - %s" % (success)
        if success:
            self.progressBar.setValue(100)
        self.execTool.setEnabled(True)
        self.cancelExec.setText(QString('Close'))

    def toolLogPingFromThread(self,log):
        #print "toolLogPingFromThread - %s" % (log)
        self.textEdit.insertPlainText(log)

    def toolProgressPingFromThread(self,progress):
        #print "toolProgressPingFromThread - %s" % (progress)
        self.progressBar.setValue(progress)

    def execToolConfigGen(self,config_node,statusElement=None,progressElement=None):
        # CK: This is only called from on_execTool_released() where the
        # config_node is generated from values in the GUI dialog.
        # Is it possible to remove that intermediate step and just run the
        # OpusTool directly?
        tool_hook = config_node.find('tool_hook').text
        # look in all groups for the tool_name -- NOTE this requires the tool
        # to be uniquely named regardless of which group it's in or this code
        # will execute the wrong tool.
        for tool_group_node in self.tool_library_node:
            tool_node = tool_group_node.find(tool_hook)
            if tool_node is not None:
                break
        if tool_node is None:
            QMessageBox.warning(None, 'Invalid tool hook',
                                'Could not find a tool named %s' %tool_hook)
            return
        tool_file = tool_node.find('name').text
        tool_path = self.tool_library_node.find('tool_path').text
        import_path = tool_path + '.' + tool_file
        params = dict((node.tag, node.text) for node in config_node)

        opus_tool = OpusTool(import_path, params)
        run_tool_thread = RunToolThread(opus_tool)
        QObject.connect(run_tool_thread, SIGNAL("toolFinished(PyQt_PyObject)"),
                        self.toolFinishedFromThread)
        QObject.connect(run_tool_thread, SIGNAL("toolProgressPing(PyQt_PyObject)"),
                        self.toolProgressPingFromThread)
        QObject.connect(run_tool_thread, SIGNAL("toolLogPing(PyQt_PyObject)"),
                        self.toolLogPingFromThread)
        run_tool_thread.start()
