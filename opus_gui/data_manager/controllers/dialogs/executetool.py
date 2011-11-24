# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml.etree import Element, SubElement

from PyQt4.QtCore import QString, Qt, QRegExp, QObject, SIGNAL, QSize, pyqtSlot, QVariant
from PyQt4.QtGui import QPalette, QLabel, QWidget, QLineEdit, QVBoxLayout, QFileDialog, QDialog, QHBoxLayout, QPushButton, QComboBox, QMessageBox, QCheckBox

from opus_gui.data_manager.views.ui_executetool import Ui_ExecuteToolGui
from opus_gui.data_manager.run.run_tool import RunToolThread, OpusTool
from opus_gui.main.controllers.instance_handlers import get_db_connection_names
from opus_gui.data_manager.data_manager_functions import get_tool_node_by_name, get_tool_library_node
from PyQt4 import QtGui

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

    def __init__(self, parent_widget, tool_node, tool_config, tool_library_node, model, params = {}):
        ''' optional params:
                tool_path - path to tools, element of data_manager'''
        window_flags = (Qt.WindowTitleHint |
                        Qt.WindowSystemMenuHint |
                        Qt.WindowMaximizeButtonHint)
        QDialog.__init__(self, parent_widget, window_flags)
        self.setupUi(self)

        # Grab the tool we are interested in...
        self.tool_node = tool_node
        self.tool_config = tool_config
        self.tool_library_node = tool_library_node

        self.vars = {}
        self.model = model

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
        # If we have a tool, then we need to traverse the XML and create a temporary
        # config to be used.
        # If we have a config we just extract the params and create the GUI elements

        self.tooltypearray = []
        assert tool_node.tag == 'tool'

        self.module_name = tool_node.find('class_module').text
        self.tool_name = tool_node.get('name')

        if tool_config is None: self.presentToolFileGUI()
        else: self.presentToolConfigGUI()

        self.setWindowTitle(self.tool_name.replace('_', ' '))
        
        self.execTool.setFocus()

    def get_params(self):
        # self.test_text contains the parameter name  (stored as a QLabel instance)
        # self.test_line contains the editor (QLineEdit or QComboBox) for the parameter value
        # self.test_text_type contains the value for the type attribute (QLineEdit)
        params = {}
        for i in range(0, len(self.test_text)):

            param_name = str(self.test_text[i].text())
            if type(self.test_line[i]) == QComboBox:
                param_value = str(self.test_line[i].currentText())
            elif type(self.test_line[i]) == QCheckBox:
                param_value = self.test_line[i].isChecked()
            else:
                param_value = str(self.test_line[i].text())
            type_value = self.test_text_type[i].text().remove(QRegExp("[\(\)]"))
            type_value = str(type_value)

            params[param_name] = param_value
        return params

    @pyqtSlot()
    def on_saveBack_clicked(self):
        params = self.get_params()
        param_nodes = self.tool_node.find('params')
        for param_node in param_nodes.iterchildren():
            old_text = self.model._get_node_text(param_node)
            new_text = str(params[param_node.get('name')])
            if old_text != new_text:
                item = self.model.item_for_node(param_node)
                index = self.model.index_for_item(item)
                self.model.project.make_local(param_node)
                self.model.setData(index.sibling(index.row(),1), QVariant(new_text), Qt.EditRole)
        
    @pyqtSlot()
    def on_execTool_clicked(self):
        self.execTool.setEnabled(False)
        self.textEdit.clear()
        self.progressBar.setValue(0)

        params = self.get_params()

        tool_hook = self.tool_name
        # look in all groups for the tool_name -- NOTE this requires the tool
        # to be uniquely named regardless of which group it's in or this code
        # will execute the wrong tool.
        tool_node = get_tool_node_by_name(self.tool_library_node, tool_hook)
        if tool_node is None:
            QMessageBox.warning(None, 'Invalid tool hook',
                                'Could not find a tool named %s' %tool_hook)
            return

        tool_path = self.optional_params['tool_path']
        import_path = tool_path + '.' + self.module_name

        opus_tool = OpusTool(import_path, params)
        run_tool_thread = RunToolThread(opus_tool)
        QObject.connect(run_tool_thread, SIGNAL("toolFinished(PyQt_PyObject)"),
                        self.toolFinishedFromThread)
        QObject.connect(run_tool_thread, SIGNAL("toolProgressPing(PyQt_PyObject)"),
                        self.toolProgressPingFromThread)
        QObject.connect(run_tool_thread, SIGNAL("toolLogPing(PyQt_PyObject)"),
                        self.toolLogPingFromThread)
        run_tool_thread.start()

    @pyqtSlot()
    def on_cancelExec_clicked(self):
        self.close()

    def fillInToolTypeArrayFromToolFile(self):
        # Find params subnode
        param_nodes = self.tool_node.find('params')
        for param_node in param_nodes:
            name = param_node.get('name')
            type_ = param_node.get('param_type') or ''
            default_value = param_node.text or ''
            self.tooltypearray.append([name, type_, default_value])

    def fillInToolTypeArrayFromToolConfig(self):
        ''' NO DOCUMENTATION '''
        for child in self.tool_node.find('params'):
            name = child.get('name')
            type_ = child.get('param_type') or ''
            default_value = child.text or ''
            if self.tool_config.find(name) is not None: 
                default_value = self.tool_config.find(name).text

            self.tooltypearray.append([name, type_, default_value])

    def createGUIElements(self):
        ''' Build the GUI based on the parameters for the tool '''
        for i, param in enumerate(self.tooltypearray):
            # print 'creatgui element %d, %s' %(i, param)
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
            test_text.setMaximumSize(test_text.sizeHint())
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
            elif param[1] == 'boolean':
                test_line = QCheckBox(widgetTemp)
                self.test_line.append(test_line)
                checked = (param[2].lower() == 'true')
                test_line.setChecked(checked)
                test_line.setEnabled(True)
                test_line.setMaximumSize(QSize(test_line.sizeHint()))
                test_line.setObjectName(QString("test_line").append(QString(i)))
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
                                self.on_pbnSelect_clicked)
                QObject.connect(pbnSelect, SIGNAL("clicked()"), pbnSelectDelegate.relayButtonSignal)
                self.test_line_delegates.append(pbnSelectDelegate)
                self.test_line_buttons.append(pbnSelect)
                hlayout.addWidget(pbnSelect)
            self.vboxlayout.addWidget(widgetTemp)
            self.adjustSize()
        # Jesse adding help text from opusHelp
        tool_path = self.optional_params.get('tool_path','')
        try:
            exec_stmt = 'from %s.%s import opusHelp' % (tool_path, self.module_name)
            exec exec_stmt
            help = QString(opusHelp())
            self.toolhelpEdit.insertPlainText(help)
        except Exception, e:
            help = 'could not find opusHelp function in tool module'
            self.toolhelpEdit.insertPlainText(help)

    @pyqtSlot()
    def on_pbnSelect_clicked(self,typeName,line):
        #print "on_pbnSelect_clicked recieved"
        editor_file = QFileDialog()
        filter_str = QString("*.*")
        editor_file.setFilter(filter_str)
        editor_file.setAcceptMode(QFileDialog.AcceptOpen)
        if typeName == QString("file_path"):
            fd = editor_file.getOpenFileName(self,QString("Please select a file..."),
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
        # print 'Filling in type array from tool config'
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
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertPlainText(log)
        self.textEdit.moveCursor(QtGui.QTextCursor.End)

    def toolProgressPingFromThread(self,progress):
        #print "toolProgressPingFromThread - %s" % (progress)
        self.progressBar.setValue(progress)
