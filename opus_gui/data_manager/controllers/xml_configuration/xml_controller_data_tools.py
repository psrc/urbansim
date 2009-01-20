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
from opus_gui.main.controllers.mainwindow import get_mainwindow_instance

import os,tempfile

from PyQt4.QtCore import QString, Qt, QFileInfo, QObject, SIGNAL, QFile, QIODevice
from PyQt4.QtGui import QIcon, QAction, QMenu, QCursor, QFileDialog
from PyQt4.QtXml import QDomDocument

from xml.etree.cElementTree import Element, SubElement, ElementTree

from opus_gui.data_manager.run.run_tool import OpusTool, RunToolThread
import opus_gui.util.documentationbase
from opus_gui.data_manager.controllers.dialogs.configuretool import ConfigureToolGui
from opus_gui.data_manager.controllers.dialogs.executetool import ExecuteToolGui

from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.data_manager.controllers.dialogs.executetoolset import ExecuteToolSetGui

class XmlController_DataTools(XmlController):
    def __init__(self, manager):
        XmlController.__init__(self, manager)

        self.actExecToolFile = self.createAction(self.model.executeIcon,"Execute Tool...", self.execToolFile)
        self.actExecToolConfig = self.createAction(self.model.executeIcon,"Execute Tool...", self.execToolFile)
        self.actAddToolFile = self.createAction(self.model.addIcon,"Add Tool to Library", self.addToolFile)
        self.actAddRequiredStringParam = self.createAction(self.model.addIcon,"Add Required String Parameter",self.addRequiredStringParam)
        self.actAddRequiredDirParam = self.createAction(self.model.addIcon,"Add Required Directory Parameter",self.addRequiredDirParam)
        self.actAddRequiredFileParam = self.createAction(self.model.addIcon,"Add Required File Parameter",self.addRequiredFileParam)
        self.actAddOptionalStringParam = self.createAction(self.model.addIcon,"Add Optional String Parameter",self.addOptionalStringParam)
        self.actAddOptionalDirParam = self.createAction(self.model.addIcon,"Add Optional Directory Parameter",self.addOptionalDirParam)
        self.actAddOptionalFileParam = self.createAction(self.model.addIcon,"Add Optional File Parameter",self.addOptionalFileParam)
        self.actAddNewToolSet = self.createAction(self.model.addIcon,"Add New Tool Set",self.addNewToolSet)
        self.actNewConfig = self.createAction(self.model.addIcon,"Add Tool to Tool Set",self.newConfig)
        self.actOpenDocumentation = self.createAction(self.model.calendarIcon,"Open Documentation",self.openDocumentation)
        self.actMoveNodeUp = self.createAction(self.model.arrowUpIcon,"Move Up",self.moveNodeUp)
        self.actMoveNodeDown = self.createAction(self.model.arrowDownIcon,"Move Down",self.moveNodeDown)
        self.actExecBatch = self.createAction(self.model.executeIcon,"Execute Tool Set",self.execBatch)
        self.actExportXMLToFile = self.createAction(self.model.cloneIcon,"Export XML Node To File",self.exportXMLToFile)
        self.actImportXMLFromFile = self.createAction(self.model.cloneIcon,"Import XML Node From File",self.importXMLFromFile)

    def addToolFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        toolname = 'Tool_Name_Rename_Me'
        filename = 'File_Name_Rename_Me'
        tool_node = Element(toolname, {'type':'tool_file'})
        SubElement(tool_node, "name", {'type':'tool_name'}).text = filename
        SubElement(tool_node, "param", {'type':'param_template'})

        self.model.insertRow(0, self.selectedIndex(), tool_node)

    def newToolParam(self, toolType, choices):
        ''' NO DOCUMENTATION '''
        param_node = Element("New_Param_Rename_Me")

        attributes = {'type': "string", 'choices': "Required|Optional"}
        SubElement(param_node, 'required', attributes).text = choices

        SubElement(param_node, 'type', {'type': "string"}).text = toolType
        SubElement(param_node, 'default', {'type': toolType }).text = ""
        return param_node

    def addRequiredStringParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        req_node = self.newToolParam("string", "Required")
        self.model.insertSibling(req_node, self.selectedIndex())

    def addRequiredDirParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        newNode = self.newToolParam("dir_path", "Required")
        self.model.insertSibling(newNode, self.selectedIndex())

    def addRequiredFileParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        newNode = self.newToolParam("file_path", "Required")
        self.model.insertSibling(newNode, self.selectedIndex())

    def addOptionalStringParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        newNode = self.newToolParam("string", "Optional")
        self.model.insertSibling(newNode, self.selectedIndex())

    def addOptionalDirParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        newNode = self.newToolParam("dir_path", "Optional")
        self.model.insertSibling(newNode, self.selectedIndex())

    def addOptionalFileParam(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        newNode = self.newToolParam("dir_path", "Optional")
        self.model.insertSibling(newNode, self.selectedIndex())

    def addNewToolSet(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        # First add the dummy toolset shell
        toolset_node = Element('Rename_Me', {'type': "tool_set"})
        self.model.insertRow(0, self.selectedIndex(), toolset_node)

    def newConfig(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        index = self.selectedIndex()
        tool_set_node = self.selectedItem().node
        tool_library_node = self.xml_root.find('Tool_Library')
        callback = \
            lambda node: self.model.insertRow(0, self.model.parent(index), node)
        window = ConfigureToolGui(tool_library_node, callback, self.view)
        window.setModal(True)
        window.show()

    def moveNodeUp(self):
        ''' NO DOCUMENTATION '''
        # TODO connect directly to lambda
        assert self.hasSelectedItem()
        new_index = self.model.moveUp(self.selectedIndex())
        self.view.setCurrentIndex(new_index)

    def moveNodeDown(self):
        ''' NO DOCUMENTATION '''
        # TODO connect directly to lambda
        assert self.hasSelectedItem()
        new_index = self.model.moveDown(self.selectedIndex())
        self.view.setCurrentIndex(new_index)

    def openDocumentation(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        filePath = self.selectedItem().node.text
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.toolboxbase.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
        fileName = newFile.absoluteFilePath().trimmed()
        x = util.documentationbase.DocumentationTab(self.mainwindow,
                                                    QString(fileName))

    def execToolFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        # Open up a GUI element and populate with variable's
        window = ExecuteToolGui(self.manager.base_widget,
                                self.selectedItem().node,
                                self.xml_root.find('Tool_Library'))
        window.setModal(True)
        window.show()

# CK: Could not find anything that uses this --
# note that there's a duplicate in ExecuteToolGui that IS used

#    def execToolConfigGen(self, tool_node):
#        ''' NO DOCUMENTATION '''
#        library = self.model.root_node().find('Tool_Library')
#
#        tool_hook = configNode.elementsByTagName(QString("tool_hook")).item(0)
#        tool_name = QString("")
#        if tool_hook.hasChildNodes():
#            children = tool_hook.childNodes()
#            for x in xrange(0,children.count(),1):
#                if children.item(x).isText():
#                    tool_name = children.item(x).nodeValue()
#        # This will be in the Tool_Library
#        tool_path = library.toElement().elementsByTagName("tool_path").item(0)
#        tool_file = library.toElement().elementsByTagName(tool_name).item(0)
#
#        # First find the tool path text...
#        if tool_path.hasChildNodes():
#            children = tool_path.childNodes()
#            for x in xrange(0,children.count(),1):
#                if children.item(x).isText():
#                    toolPath = children.item(x).nodeValue()
#        # Next if the tool_file has a tool_name we grab it
#        filePath = ""
#        if tool_file.hasChildNodes():
#            children = tool_file.childNodes()
#            for x in xrange(0,children.count(),1):
#                if children.item(x).isElement():
#                    thisElement = children.item(x).toElement()
#                    if thisElement.hasAttribute(QString("type")) and \
#                           (thisElement.attribute(QString("type")) == QString("tool_name")):
#                        if thisElement.hasChildNodes():
#                            children2 = thisElement.childNodes()
#                            for x2 in xrange(0,children2.count(),1):
#                                if children2.item(x2).isText():
#                                    filePath = children2.item(x2).nodeValue()
#        importPath = QString(toolPath).append(QString(".")).append(QString(filePath))
#        #print "New import ", importPath
#
#        #Now loop and build up the parameters...
#        params = {}
#        childNodes = configNode.childNodes()
#        for x in xrange(0,childNodes.count(),1):
#            thisElement = childNodes.item(x)
#            thisElementText = QString("")
#            if thisElement.hasChildNodes():
#                children = thisElement.childNodes()
#                for x in xrange(0,children.count(),1):
#                    if children.item(x).isText():
#                        thisElementText = children.item(x).nodeValue()
#            params[thisElement.toElement().tagName()] = thisElementText
#
#        x = OpusTool(self.mainwindow,importPath,params)
#        y = RunToolThread(self.mainwindow,x)
#        y.run()

    def toolFinished(self, success):
        ''' NO DOCUMENTATION '''
        print "Tool Finished Signal Recieved - %s" % (success)

# CK: Couldn't find anything that uses this

#    def execToolConfig(self):
#        ''' NO DOCUMENTATION '''
#        # First find the tool that this config refers to...
#        configNode = self.currentIndex.internalPointer().node().toElement()
#        #library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
#        self.execToolConfigGen(configNode)

# CK: Couldn't find anything that uses this

    def execBatch(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        batchNode = self.selectedItem().node
        # TODO Update XML to only have lowercase names
        library = self.model.root_node().find('Tool_Library')
        childNodes = batchNode.childNodes()
        tool_hooks = []
        # tool_hooks = [x.text for x in batchNode.findall('.//*') if
        #               x.get('type') == 'tool_library_ref']
        for thisNode in batchNode:
            for newNode in thisNode:
                if newNode.get('type') == 'tool_library_ref':
                    tool_hooks.append(newNode.text)

        tool_hook_to_tool_name_dict = {}
        for tool_hook in tool_hooks:
            # find the tag named as the hook (somewhere?) in lib
            tool_file = library.find('.//%s' %tool_hook)
            name = tool_file.find('name')
            tool_hook_to_tool_name_dict[tool_file] = name.text

        flgs = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        wndow = ExecuteToolSetGui(get_mainwindow_instance(), flgs, childNodes,
                                  tool_hook_to_tool_name_dict)
        wndow.show()

# CK: Moved to XmlController
#    def cloneNode(self):
#        ''' NO DOCUMENTATION '''
#        #print "cloneNode Pressed"
#        clone = self.currentIndex.internalPointer().domNode.cloneNode()
#        parentIndex = self.currentIndex.model().parent(self.currentIndex)
#        model = self.currentIndex.model()
#        window = CloneNodeGui(self, clone, parentIndex, model)
#        window.show()

# CK: Moved to XmlController as removeSelectedNode
#    def removeNode(self):
#        ''' NO DOCUMENTATION '''
#        #print "Remove Node Pressed"
#        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
#                                            self.currentIndex.model().parent(self.currentIndex))
#        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

# CK: Moved to XmlController as makeSelectedNodeEditable
#    def makeEditableAction(self):
#        ''' NO DOCUMENTATION '''
#        thisNode = self.currentIndex.internalPointer().node()
#        self.currentIndex.model().makeEditable(thisNode)
#        # Finally we refresh the tree to indicate that there has been a change
#        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))


    def exportXMLToFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        # TODO clean this up maybe?

        # Ask the user where they want to save the file to
        start_dir = ''
        opus_home = os.environ.get('OPUS_HOME')
        if opus_home:
            start_dir_test = os.path.join(opus_home, 'project_configs')
            if start_dir_test:
                start_dir = start_dir_test
        configDialog = QFileDialog()
        filter_str = QString("*.xml")
        fd = configDialog.getSaveFileName(self.manager.base_widget,
                                          QString("Save As..."),
                                          QString(start_dir), filter_str)
        # Check for cancel
        if len(fd) == 0:
            return
        fileNameInfo = QFileInfo(QString(fd))
        fileName = fileNameInfo.fileName().trimmed()
        fileNamePath = fileNameInfo.absolutePath().trimmed()
        saveName = os.path.join(str(fileNamePath),str(fileName))

        # proper root node for XmlConfiguration
        root_node = Element('opus_project')
        root_node.append(self.selectedItem().node)

        # Write out the file
        ElementTree(root_node).write(saveName)

    def importXMLFromFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        # print "importXMLFromFile"
        # First, prompt the user for the filename to read in
        start_dir = ''
        opus_home = os.environ.get('OPUS_HOME')
        if opus_home:
            start_dir_test = os.path.join(opus_home, 'project_configs')
            if start_dir_test:
                start_dir = start_dir_test
        configDialog = QFileDialog()
        filter_str = QString("*.xml")
        fd = configDialog.getOpenFileName(self.manager.base_widget,
                                          "Please select an xml file to import...",
                                          start_dir, filter_str)
        # Check for cancel
        if len(fd) == 0:
            return
        fileName = QString(fd)
        fileNameInfo = QFileInfo(QString(fd))
        fileNameInfoBaseName = fileNameInfo.completeBaseName()
        fileNameInfoName = fileNameInfo.fileName().trimmed()
        fileNameInfoPath = fileNameInfo.absolutePath().trimmed()

        # Pass that in to create a new XMLConfiguration
        xml_config = XMLConfiguration(str(fileNameInfoName),str(fileNameInfoPath))

        xml_node = xml_config.full_tree.getroot()
        if len(xml_node) == 0:
            raise ValueError('Loading tool from XML file failed. '
                             'No tool definition found')
        xml_node = xml_node[0]

        # Insert it into the parent node from where the user clicked
        self.model.insertSibling(xml_node, self.selectedIndex())


    def processCustomMenu(self, position):
        ''' See XmlConfig.processCustomMenu for documentation '''
        item = self.selectItemAt(position)
        if not item:
            return

        node = item.node

        menu = QMenu(self.view)
        if node.get('type') == "tool_file":
            menu.addAction(self.actExecToolFile)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)
        elif node.get('type') == "tool_group":
            menu.addAction(self.actAddToolFile)
        elif node.get('type') == "param_template":
            menu.addAction(self.actAddRequiredStringParam)
            menu.addAction(self.actAddRequiredDirParam)
            menu.addAction(self.actAddRequiredFileParam)
            menu.addAction(self.actAddOptionalStringParam)
            menu.addAction(self.actAddOptionalDirParam)
            menu.addAction(self.actAddOptionalFileParam)
        elif node.get('type') == "tool_config":
            menu.addAction(self.actExecToolConfig)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)
        elif node.get('type') == "tool_sets":
            menu.addAction(self.actAddNewToolSet)
        elif node.get('type') == "tool_set":
            menu.addAction(self.actExecBatch)
            menu.addSeparator()
            menu.addAction(self.actNewConfig)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)
        elif node.get('type') == "documentation_path":
            menu.addAction(self.actOpenDocumentation)
            menu.addSeparator()
            menu.addAction(self.actCloneNode)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)

        if not menu: # don't build a menu for this node
            return

        # Default menu items
        self.addDefaultMenuItems(node, menu)

        # Now add the export and import methods
        menu.addSeparator()
        menu.addAction(self.actExportXMLToFile)
        menu.addAction(self.actImportXMLFromFile)

        # Check if the menu has any elements before exec is called
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

