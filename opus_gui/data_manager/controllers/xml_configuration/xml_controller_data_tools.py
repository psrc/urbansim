# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import os

from xml.etree.cElementTree import Element, SubElement, ElementTree
from PyQt4.QtCore import QString
from PyQt4.QtGui import QMenu, QCursor, QFileDialog

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.data_manager.data_manager_functions import get_tool_node_by_name, get_tool_library_node
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.data_manager.controllers.dialogs.configuretool import ConfigureToolGui
from opus_gui.data_manager.controllers.dialogs.executetool import ExecuteToolGui
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.data_manager.controllers.dialogs.executetoolset import ExecuteToolSetGui


class XmlController_DataTools(XmlController):
    def __init__(self, manager):
        XmlController.__init__(self, manager)

        # Show dialog to execute/config tools
        self.actExecToolFile = self.createAction(self.model.executeIcon,"Execute Tool...", self.execToolFile)
        self.actExecToolConfig = self.createAction(self.model.executeIcon,"Execute Tool...", self.execToolConfig)

        # Adding tools, groups, sets and configurations
        self.actAddToolFile = self.createAction(self.model.addIcon,"Add Tool", self.addToolFile)
        self.actAddToolGroup = self.createAction(self.model.addIcon,"Create Tool Group", self.addNewToolGroup)
        self.actAddNewToolSet = self.createAction(self.model.addIcon,"Create Tool Set",self.addNewToolSet)
        self.actNewConfig = self.createAction(self.model.addIcon,"Add New Tool Configuration",self.newConfig)

        self.actOpenDocumentation = self.createAction(self.model.calendarIcon,"Open Documentation",self.openDocumentation)

        # moving tools up and down
        self.actMoveNodeUp = self.createAction(self.model.arrowUpIcon,"Move Up",self.moveNodeUp)
        self.actMoveNodeDown = self.createAction(self.model.arrowDownIcon,"Move Down",self.moveNodeDown)
        self.actExecBatch = self.createAction(self.model.executeIcon,"Execute Tool Set",self.execBatch)
        self.actExportXMLToFile = self.createAction(self.model.cloneIcon,"Export XML Node To File",self.exportXMLToFile)
        self.actImportXMLFromFile = self.createAction(self.model.cloneIcon,"Import XML Node From File",self.importXMLFromFile)

        # Batch create 'add ... parameter' actions
        self.add_parameter_actions = []
        parameter_types = {'String': 'string', # Description, attribute value
                           'Directory': 'dir_path',
                           'File': 'file_path'}
        for required in (True, False):
            for type_name, type_value in parameter_types.items():
                req_text = "Required" if required else "Optional"
                label = "Create %s %s parameter" % (req_text, type_name)
                act = self._create_add_param_action(label, type_value, required)
                self.add_parameter_actions.append(act)

    def _create_add_param_action(self, label, type_name, required = False):
        '''
        Creates and returns a new action for creating a parameter node.
        The parameter node will have the attribute 'type' set to type_name
        and, if required is True, the attribute "required" will be "Required"
        (if required is False, attribute "required" will be "Optional")
        @param label (str) text to show on the menu
        @param type_name (str) the parameters type
        @param required (boolean) whether the param is required or not
        @return the created action or None
        '''
        # Make a node and a callback and use them to assemble the action
        node = Element("Unnamed_Parameter")
        attributes = {'type': "string", 'choices': "Required|Optional"}
        choice = "Required" if required else "Optional"
        SubElement(node, 'required', attributes).text = choice
        SubElement(node, 'type', {'type': "string"}).text = str(type_name)
        SubElement(node, 'default', {'type': str(type_name) }).text = ""
        def action():
            self.model.insertRow(0, self.selectedIndex(), node)
            self.view.expand(self.selectedIndex())
        return self.createAction(self.model.addIcon, label, action)

    def addToolFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        toolname = 'Unnamed_Tool_Name'
        filename = 'Unnamed_File_Name'
        tool_node = Element(toolname, {'type':'tool_file'})
        SubElement(tool_node, "name", {'type':'tool_name'}).text = filename
        SubElement(tool_node, "params", {'type':'param_template'})

        self.model.insertRow(0, self.selectedIndex(), tool_node)

    def addNewToolSet(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        # First add the dummy toolset shell
        toolset_node = Element('Unnamed_Tool_Set', {'type': "tool_set"})
        self.model.insertRow(0, self.selectedIndex(), toolset_node)

    def addNewToolGroup(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        # First add the dummy toolset shell
        node = Element('Unnamed_Tool_Group', {'type': "tool_group",
                                     'setexpanded':'True'})
        self.model.insertRow(0, self.selectedIndex(), node)

    def newConfig(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()
        index = self.selectedIndex()
        tool_library_node = get_tool_library_node(self.project)
        callback = \
            lambda node: self.model.insertRow(0, index, node)
        window = ConfigureToolGui(tool_library_node, callback, self.view)
        window.setModal(True)
        window.show()

    # CK: is it desirable to move tool nodes?
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
        print 'Documentation for tools is disabled.'
        return # disabled for now
#        assert self.hasSelectedItem()
#        filePath = self.selectedItem().node.text
#        fileInfo = QFileInfo(filePath)
#        baseInfo = QFileInfo(self.toolboxbase.xml_file)
#        baseDir = baseInfo.absolutePath()
#        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
#        fileName = newFile.absoluteFilePath().trimmed()
#        x = util.documentationbase.DocumentationTab(self.mainwindow,
#                                                    QString(fileName))

    def execToolFile(self):
        '''
        Show a dialog box that lets the user configure and execute a
        tool.
        '''
        assert self.hasSelectedItem()

        tool_lib_node = get_tool_library_node(self.project)
        window = ExecuteToolGui(parent_widget = self.manager.base_widget,
                                tool_node = self.selectedItem().node,
                                tool_library_node = tool_lib_node)
        window.setModal(True)
        window.show()

    def execToolConfig(self):
        '''
        Show the dialog box for executing a "tool config"
        A tool config is has a pointer to an existing tool (a "tool hook") but
        can provide an alternative configuration.
        '''
        assert self.hasSelectedItem()

        # CK: Not sure that this does the right thing. From what I understand,
        # this will run the tool with the configuration as it is specified in
        # the tool library. The configuration that is specified in the selected
        # 'tool config' is ignored.

        # First we need to get the hooked node that we want to run
        node = self.selectedItem().node
        hooked_tool_name = node.find('tool_hook').text
        hooked_tool_node = get_tool_node_by_name(hooked_tool_name)
        if hooked_tool_node is None:
            MessageBox.error(mainwindow = self.view,
                text = 'Invalid tool hook',
                detailed_text = ('This tool config points to a tool named "%s" '
                    'but there is no tool with that name in this project.' %
                    hooked_tool_name))
            return

        hooked_tool_node = get_tool_node_by_name(hooked_tool_name)

        # Open up a GUI element and populate with variable's
        tool_lib_node = get_tool_library_node(self.project)
        window = ExecuteToolGui(parent_widget = self.manager.base_widget,
                                tool_node = hooked_tool_node,
                                tool_library_node = tool_lib_node)
        window.setModal(True)
        window.show()

    # ?
    def toolFinished(self, success):
        ''' NO DOCUMENTATION '''
        print "Tool Finished Signal Recieved - %s" % (success)

    def execBatch(self):
        ''' Present a dialog to execute a set of tool configurations '''
        assert self.hasSelectedItem()
        # Node representing the set to execute
        tool_set_node = self.selectedItem().node

        # map tool config nodes in set -> name of the hooked node
        tool_config_to_tool_name = {}
        tool_config_nodes = tool_set_node[:]
        for tool_config_node in tool_config_nodes:
            hook_node = tool_config_node.find('tool_hook')
            hooked_tool_name = str(tool_hook_node.text or '').strip()
            hooked_tool_node = get_tool_node_by_name(hooked_tool_name)
            # just map the name of the tool (name is the filename)
            tool_file_name = str(hooked_tool_node.find('name').text).strip()
            tool_config_to_tool_name[tool_config_node] = tool_file_name

        ExecuteToolSetGui(get_mainwindow_instance(),
            config_nodes,
            config_to_filenames).show()

    def exportXMLToFile(self):
        ''' NO DOCUMENTATION '''
        assert self.hasSelectedItem()

        # Ask the users where they want to save the file
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

        # Tool files are the "actual" tools
        if node.get('type') == "tool_file":
            menu.addAction(self.actExecToolFile)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)

        # "Tool library is a collection of tool groups
        elif node.get('type') == "tool_library":
            menu.addAction(self.actAddToolGroup)

        # Tool groups are groups of "tool files"
        elif node.get('type') == "tool_group":
            menu.addAction(self.actAddToolFile)

        # Param Template is the parameter node for the tools -- where
        # users can build up a list of parameters that gets passed to the
        # tool function
        elif node.get('type') == "param_template":
            map(menu.addAction, self.add_parameter_actions)

        # A "tool config" is an alternative configuration for a tool that can be
        # put in a Tool Set
        elif node.get('type') == "tool_config":
            menu.addAction(self.actExecToolConfig)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)

        # "Tool sets" is a collection of multiple tool sets
        elif node.get('type') == "tool_sets":
            menu.addAction(self.actAddNewToolSet)

        # A Tool set is a collection of (alternative) configurations for
        # existing tools.
        elif node.get('type') == "tool_set":
            menu.addAction(self.actExecBatch)
            menu.addSeparator()
            menu.addAction(self.actNewConfig)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)

        # ?
        elif node.get('type') == "documentation_path":
            menu.addAction(self.actOpenDocumentation)
            menu.addSeparator()
            menu.addAction(self.actCloneNode)
            menu.addSeparator()
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)

        # Default menu items
        self.addDefaultMenuItems(node, menu)

        # Now add the export and import methods
        menu.addSeparator()
        menu.addAction(self.actExportXMLToFile)
        menu.addAction(self.actImportXMLFromFile)

        # Check if the menu has any elements before exec is called
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

