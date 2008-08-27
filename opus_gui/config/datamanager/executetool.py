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

from opus_gui.config.datamanager.executetool_ui import Ui_ExecuteToolGui
from opus_gui.util.xmlhelper import *
from opus_gui.run.tool.opusruntool import *

import random,time

class FileDialogSignal(QWidget):
    def __init__(self, parent=None, typeName=None, param=None):
        QWidget.__init__(self, parent)
        self.o = QObject()
        self.param = param
        self.type = typeName
        #print "FileDialogSignal created..."

    def updateParam(self,param):
        self.param = param

    def updateParam(self,typeName):
        self.type = typeName

    def relayButtonSignal(self):
        #print "relayButtonSignal"
        self.o.emit(SIGNAL("buttonPressed(PyQt_PyObject,PyQt_PyObject)"),self.type,self.param)
        



class ExecuteToolGui(QDialog, Ui_ExecuteToolGui):
    def __init__(self,mainwindow,model,currentElement,execToolConfigGen,fl):
        QDialog.__init__(self, mainwindow, fl)
        self.setupUi(self)
        self.mainwindow = mainwindow
        self.model = model
        # Grab the tool we are interested in...
        self.currentElement = currentElement
        #self.execToolConfigGen = execToolConfigGen
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
        self.test_line_delegates = []
        self.test_line_buttons = []

        # Decide if we have a tool_file or tool_config
        # If we have a too_file, then we need to traverse the XML and create a temporary
        # config to be used.
        # If we have a config we just extract the params and create the GUI elements
        self.tooltypearray = []
        if self.currentElement.hasAttribute(QString('type')) and \
           self.currentElement.attribute(QString('type')) == QString('tool_file'):
            self.typeSelection = self.currentElement.tagName()
            
            #Jesse
            #getting tool_name
            child_nodes = self.currentElement.childNodes()
            self.tool_name = getNodeText(child_nodes.item(0))
            
            self.presentToolFileGUI()
        else:
            # We assume config
            typeSelections = getChildElementsText(self.currentElement,
                                                  [QString('tool_hook')],
                                                  True,False)
            self.typeSelection = typeSelections[QString('tool_hook')]
            #self.typeSelection = getElementText(self.currentElement.elementsByTagName(QString("tool_hook")).item(0))
            
            #Jesse
            #getting tool_name
            tool_names = getElementsByType(self.model.domDocument, 'tool_name', True, True)
            for i in tool_names:
                if getNodeText(i) == self.typeSelection:
                    self.tool_name = getNodeText(i)
            
            self.presentToolConfigGUI()
            
        #Setting tool title:
        self.tool_title = self.model.domDocument.createTextNode(self.typeSelection).data()

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
        print "Main Window Prio - %s" % (str(self.mainwindow.thread().priority()))
        self.execTool.setEnabled(False)
        self.textEdit.clear()
        self.progressBar.setValue(0)
        
        #toolname = self.test_line[0].text()
        # First is the connection node with the connection name
        newNode = self.model.domDocument.createElement(QString("temp_config"))
        newNode.setAttribute(QString("type"),QString("tool_config"))
        # Add the tool hook back in
        newChild = self.model.domDocument.createElement(QString("tool_hook"))
        newChild.setAttribute(QString("type"),QString("tool_library_ref"))
        newText = self.model.domDocument.createTextNode(self.typeSelection)
        newChild.appendChild(newText)
        newNode.appendChild(newChild)
        # for key,val in self.vars.iteritems():
        for x in xrange(0,len(self.test_text)):
            #self.vars[self.test_text[x].text()] = self.test_line[x].text()
            key = self.test_text[x].text()
            val = self.test_line[x].text()
            typeVal = self.test_text_type[x].text().remove(QRegExp("[\(\)]"))
            #print "Key: %s , Val: %s" % (key,val)
            # Next we add each of the child nodes with the user defined values
            newChild = self.model.domDocument.createElement(key)
            newChild.setAttribute(QString("type"),typeVal)
            newText = self.model.domDocument.createTextNode(val)
            newChild.appendChild(newText)
            newNode.appendChild(newChild)
        self.execToolConfigGen(newNode)
        #self.close()

    def on_cancelExec_released(self):
        #print "cancel pressed"
        self.close()

    def fillInToolTypeArrayFromToolFile(self,qDomNodeList):
        for xx in xrange(0,qDomNodeList.count(),1):
            if qDomNodeList.item(xx).isElement():
                tool_file_child = qDomNodeList.item(xx).toElement()
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

        
    def fillInToolTypeArrayFromToolConfig(self,toolConfigElement):
        # Loop through children and build up the params
        if toolConfigElement and not toolConfigElement.isNull() and \
               toolConfigElement.hasChildNodes():
            children = toolConfigElement.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isElement() and \
                       children.item(x).toElement().hasAttribute(QString('type')) and \
                       children.item(x).toElement().attribute(QString('type')) != QString('tool_library_ref'):
                    child = children.item(x).toElement()
                    tagName = child.tagName()
                    typeName = child.attribute(QString('type'))
                    nodeVal = getElementText(child)
                    self.tooltypearray.append([tagName,typeName,nodeVal])


    def createGUIElements(self):
        for i,param in enumerate(self.tooltypearray):
            # print "Key: %s , Val: %s" % (param[0],param[1])
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
        tool_path_elements = getElementsByType(self.model.domDocument, 'tool_path', True, True)
        for i in tool_path_elements:
            try:
                tool_path = getElementText(i)
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
            fd = editor_file.getOpenFileName(self.mainwindow,QString("Please select a file..."),
                                             line.text())
        else:
            fd = editor_file.getExistingDirectory(self.mainwindow,QString("Please select a directory..."),
                                                  line.text())
        # Check for cancel
        if len(fd) != 0:
            fileName = QString(fd)
            line.setText(fileName)

    
    def presentToolFileGUI(self):
        #print "Got a new selection"
        #print self.comboBox.itemText(index)

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
                                    if tool.tagName() == self.typeSelection:
                                        foundOurTool = True
                                if foundOurTool:
                                    tool_file = tool.childNodes()
                                    self.fillInToolTypeArrayFromToolFile(tool_file)
        self.createGUIElements()

    def presentToolConfigGUI(self):
        #print "Got a new selection"

        # First, fillInToolTypeArrayFromToolConfig
        self.fillInToolTypeArrayFromToolConfig(self.currentElement)
        self.createGUIElements()

    def toolFinishedFromThread(self,success):
        #print "toolFinishedFromThread - %s" % (success)
        if success:
            self.progressBar.setValue(100)
        self.execTool.setEnabled(True)

    def toolLogPingFromThread(self,log):
        #print "toolLogPingFromThread - %s" % (log)
        self.textEdit.insertPlainText(log)
        
    def toolProgressPingFromThread(self,progress):
        #print "toolProgressPingFromThread - %s" % (progress)
        self.progressBar.setValue(progress)
        
    def execToolConfigGen(self,configNode,statusElement=None,progressElement=None):
        library = self.model.xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        tool_hook = configNode.elementsByTagName(QString("tool_hook")).item(0)
        tool_name = QString("")
        if tool_hook.hasChildNodes():
            children = tool_hook.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    tool_name = children.item(x).nodeValue()
        # This will be in the Tool_Library
        tool_path = library.toElement().elementsByTagName("tool_path").item(0)
        tool_file = library.toElement().elementsByTagName(tool_name).item(0)
        
        # First find the tool path text...
        if tool_path.hasChildNodes():
            children = tool_path.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    toolPath = children.item(x).nodeValue()
        # Next if the tool_file has a tool_name we grab it
        filePath = ""
        if tool_file.hasChildNodes():
            children = tool_file.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isElement():
                    thisElement = children.item(x).toElement()
                    if thisElement.hasAttribute(QString("type")) and \
                           (thisElement.attribute(QString("type")) == QString("tool_name")):
                        if thisElement.hasChildNodes():
                            children2 = thisElement.childNodes()
                            for x2 in xrange(0,children2.count(),1):
                                if children2.item(x2).isText():
                                    filePath = children2.item(x2).nodeValue()
        importPath = QString(toolPath).append(QString(".")).append(QString(filePath))
        print "New import ", importPath

        #Now loop and build up the parameters...
        params = {}
        childNodes = configNode.childNodes()
        for x in xrange(0,childNodes.count(),1):
            thisElement = childNodes.item(x)
            thisElementText = QString("")
            if thisElement.hasChildNodes():
                children = thisElement.childNodes()
                for x in xrange(0,children.count(),1):
                    if children.item(x).isText():
                        thisElementText = children.item(x).nodeValue()
            params[thisElement.toElement().tagName()] = thisElementText

        x = OpusTool(self.mainwindow,importPath,params)
        y = RunToolThread(self.mainwindow,x)
        QObject.connect(y, SIGNAL("toolFinished(PyQt_PyObject)"),
                        self.toolFinishedFromThread)
        QObject.connect(y, SIGNAL("toolProgressPing(PyQt_PyObject)"),
                        self.toolProgressPingFromThread)
        QObject.connect(y, SIGNAL("toolLogPing(PyQt_PyObject)"),
                        self.toolLogPingFromThread)
        y.start()
