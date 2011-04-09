# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from lxml.etree import Element, SubElement, ElementTree
from PyQt4.QtCore import QString, QFileInfo
from PyQt4.QtGui import QMenu, QCursor, QFileDialog
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.data_manager.data_manager_functions import *
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.data_manager.controllers.dialogs.configuretool import ConfigureToolGui
from opus_gui.data_manager.controllers.dialogs.executetool import ExecuteToolGui
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.data_manager.controllers.dialogs.executetoolset import ExecuteToolSetGui
from opus_gui.data_manager.controllers.dialogs.addparam import addParamGui
from opus_gui.abstract_manager.controllers.xml_configuration.renamedialog import RenameDialog


class XmlController_DataTools(XmlController):
    def __init__(self, manager):
        XmlController.__init__(self, manager)

        # Show dialog to execute/config tools
        self.actExecToolFile = self.create_action('execute',"Execute Tool...", self.execToolFile)
        self.actExecToolConfig = self.create_action('execute',"Execute Tool...", self.execToolConfig)

        # Adding tools, groups, sets and configurations
        self.actAddToolFile = self.create_action('add',"Add Tool", self.addToolFile)
        self.actAddToolGroup = self.create_action('add',"Create Tool Group", self.addNewToolGroup)
        self.actAddNewToolSet = self.create_action('add',"Create Tool Set",self.addNewToolSet)
        self.actNewConfig = self.create_action('add',"Add New Tool Configuration",self.newConfig)
        self.actAddParam = self.create_action('add',"Add New Param",self.addParam)
        self.actEditParam = self.create_action('rename',"Edit Param",self.editParam)

        self.actOpenDocumentation = self.create_action('calendar_view_day',"Open Documentation",self.openDocumentation)

        self.actChangeClassModule = self.create_action('rename',"Change Module Class Name",self.changeClassModule)
        self.actChangePathToTools = self.create_action('rename',"Change Path to Tools",self.changePathToTools)

        # moving tools up and down
        self.actMoveNodeUp = self.create_action('arrow_up',"Move Up",self.moveNodeUp)
        self.actMoveNodeDown = self.create_action('arrow_down',"Move Down",self.moveNodeDown)
        self.actExecBatch = self.create_action('execute',"Execute Tool Set",self.execBatch)
        self.actExportXMLToFile = self.create_action('export',"Export XML Node To File",self.exportXMLToFile)
        self.actImportXMLFromFile = self.create_action('import',"Import XML Node From File",self.importXMLFromFile)

    def addParam(self):
        assert self.has_selected_item()

        item = self.selected_item()
        node = item.node
        window = addParamGui(self.manager.base_widget, None)
        window.setModal(True)
        window.show()

        if window.exec_() == window.Accepted:
            name = str(window.nameEdit.text())
            typ = str(window.typeComboBox.currentText())
            default = str(window.defaultEdit.text())
            required = str(window.requiredComboBox.currentText())

            attributes = {'name': name, 'param_type': typ, 'required': required}
            node = Element('param', attributes)
            node.text = default
            if self.model.insertRow(0, self.selected_index(), node) == False:
                MessageBox.error(mainwindow = self.view,
                    text = 'Parameter Name Exists',
                    detailed_text = ('The parameter name to add is "%s" '
                    'but there is already a parameter with that name.' %
                    name))
                return

            self.view.expand(self.selected_index())

    def editParam(self):
        assert self.has_selected_item()

        item = self.selected_item()
        node = item.node
        window = addParamGui(self.manager.base_widget, node)
        window.setModal(True)
        window.show()

        if window.exec_() == window.Accepted:
            name = str(window.nameEdit.text())
            typ = str(window.typeComboBox.currentText())
            default = str(window.defaultEdit.text())
            required = str(window.requiredComboBox.currentText())

            self.model.make_item_local(item)
            node.set('name', name)
            node.set('param_type', typ)
            node.set('required', required)
            node.text = default

    def changeClassModule(self):
        ''' Opens a dialog box for changing the class module. '''
        assert self.has_selected_item()

        item = self.selected_item()
        node = item.node
        dialog = RenameDialog(node.text, [], self.view)
        if dialog.exec_() == dialog.Accepted:
            node.text = dialog.accepted_name
            self.model.make_item_local(item)

    def changePathToTools(self):
        ''' Opens a dialog box for changing the path to tools. '''
        assert self.has_selected_item()

        item = self.selected_item()
        node = item.node
        dialog = RenameDialog(node.text, [], self.view)
        if dialog.exec_() == dialog.Accepted:
            node.text = dialog.accepted_name
            self.model.make_item_local(item)

    def addToolFile(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()

        tool_node = Element('tool', {'name': 'unnamed_tool'})
        SubElement(tool_node, "class_module").text = 'unnamed_module'
        SubElement(tool_node, "params")

        self.model.insertRow(0, self.selected_index(), tool_node)
        self.view.expand(self.selected_index())

    def addNewToolSet(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()

        # First add the dummy toolset shell
        toolset_node = Element('tool_set', {'name': 'unnamed_tool_set'})
        self.model.insertRow(0, self.selected_index(), toolset_node)

    def addNewToolGroup(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()

        # First add the dummy toolset shell
        node = Element('tool_group', {'name': 'unnamed_tool_group',
                                     'setexpanded':'True'})
        self.model.insertRow(0, self.selected_index(), node)

    def newConfig(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()
        index = self.selected_index()
        tool_library_node = get_tool_library_node(self.project)
        callback = \
            lambda node: self.model.insertRow(0, index, node)
        window = ConfigureToolGui(tool_library_node, callback, self.view)
        window.setModal(True)
        window.show()

    def moveNodeUp(self):
        ''' NO DOCUMENTATION '''
        # TODO connect directly to lambda
        assert self.has_selected_item()
        new_index = self.model.move_up(self.selected_index(),view=self.view)
        self.view.setCurrentIndex(new_index)

    def moveNodeDown(self):
        ''' NO DOCUMENTATION '''
        # TODO connect directly to lambda
        assert self.has_selected_item()
        new_index = self.model.move_down(self.selected_index(),view=self.view)
        self.view.setCurrentIndex(new_index)

    def openDocumentation(self):
        ''' NO DOCUMENTATION '''
        print 'NOTE openDocumentation for tools is disabled for now.'
        return
#        assert self.has_selected_item()
#        filePath = self.selected_item().node.text
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
        assert self.has_selected_item()

        tool_lib_node = get_tool_library_node(self.project)
        params = {'tool_path': get_path_to_tool_modules(self.project)}

        tool_node = self.selected_item().node

        try:
            module_name = tool_node.find('class_module').text
            import_path = params['tool_path'] + '.' + module_name
            importString = "from %s import opusRun" % (import_path)
            exec(importString)
        except Exception, e:
            print e
            MessageBox.error(mainwindow = self.view,
                text = 'Invalid module name',
                detailed_text = ('This tool points to a module named "%s", ' % import_path + \
                                 'but there is no module with that name, or module returned import error: %s. ' \
                                 % formatExceptionInfo() 
                                 ))
            return

        window = ExecuteToolGui(parent_widget = self.manager.base_widget,
                                tool_node = tool_node,
                                tool_config = None,
                                tool_library_node = tool_lib_node, 
                                params=params)
        window.setModal(True)
        window.show()

    def execToolConfig(self):
        '''
        Show the dialog box for executing a "tool config"
        A tool config is has a pointer to an existing tool (a "tool hook") but
        can provide an alternative configuration.
        '''
        assert self.has_selected_item()

        # First we need to get the hooked node that we want to run
        node = self.selected_item().node
        hooked_tool_name = node.find('tool_hook').text
        hooked_tool_node = get_tool_node_by_name(self.project, hooked_tool_name)
        if hooked_tool_node is None:
            MessageBox.error(mainwindow = self.view,
                text = 'Invalid tool hook',
                detailed_text = ('This tool config points to a tool named "%s" '
                    'but there is no tool with that name in this project.' %
                    hooked_tool_name))
            return

        # Open up a GUI element and populate with variable's
        tool_lib_node = get_tool_library_node(self.project)
        params = {'tool_path': get_path_to_tool_modules(self.project)}
        window = ExecuteToolGui(parent_widget = self.manager.base_widget,
                                tool_node = hooked_tool_node,
                                tool_config = node,
                                tool_library_node = tool_lib_node,
                                params=params)
        window.setModal(True)
        window.show()

    def execBatch(self):
        ''' Present a dialog to execute a set of tool configurations '''
        assert self.has_selected_item()
        # Node representing the set to execute
        tool_set_node = self.selected_item().node

        # map tool config nodes in set -> name of the hooked node
        tool_config_to_tool_name = {}
        tool_config_nodes = tool_set_node[:]
        for tool_config_node in tool_config_nodes:
            hook_node = tool_config_node.find('tool_hook')
            hooked_tool_name = str(hook_node.text or '').strip()
            hooked_tool_node = get_tool_node_by_name(self.project, hooked_tool_name)
            module_name = hooked_tool_node.find('class_module').text
            
            try:
                module_name = hooked_tool_node.find('class_module').text
                tool_path = get_path_to_tool_modules(self.project)
                import_path = tool_path + '.' + module_name
                importString = "from %s import opusRun" % (import_path)
                exec(importString)
                tool_config_to_tool_name[tool_config_node] = import_path
            except Exception, e:
                MessageBox.error(mainwindow = self.view,
                    text = 'Invalid module name',
                    detailed_text = ('This tool points to a module named "%s", ' % import_path + \
                                     'but there is no module with that name, or module returned import error: %s. ' \
                                     % formatExceptionInfo() 
                                     ))
                return

        ExecuteToolSetGui(get_mainwindow_instance(),
            tool_config_nodes,
            tool_config_to_tool_name).show()

    def exportXMLToFile(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()

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
        import copy
        root_node.append(copy.deepcopy(self.selected_item().node))

        # Write out the file
        ElementTree(root_node).write(saveName)

    def importXMLFromFile(self):
        ''' NO DOCUMENTATION '''
        assert self.has_selected_item()
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
            raise ValueError('Loading node from XML file failed. '
                             'No node definition found')
        xml_node = xml_node[0]

        parent_node = self.selected_item().node

        allowed_parent_tags = {"tool": ["tool_group"], \
                               "class_module": ["tool"], \
                                    "path_to_tool_modules": ["tool_library"], \
                               "tool_library": ["data_manager"], \
                               "tool_group": ["tool_library"], \
                               "params": ["tool"], \
                               "param": ["params"], \
                               "tool_config": ["tool_set"], \
                               "tool_set": ["tool_sets"], \
                               "tool_sets": ["data_manager"]}
        if parent_node.tag not in allowed_parent_tags[xml_node.tag]:
            MessageBox.error(mainwindow = self.view,
                text = 'Invalid Xml insert',
                detailed_text = ('Xml insert of node of type "%s" failed.  '
                'Invalid type of parent node is "%s" - needs to be one of %s' %
                (xml_node.tag, parent_node.tag, str(allowed_parent_tags[xml_node.tag]))))
            return

        # Insert it into the parent node from where the user clicked
        name = xml_node.get('name') if xml_node.get('name') is not None else ''
        if self.model.insertRow(0, self.selected_index(), xml_node) is False:
            MessageBox.error(mainwindow = self.view,
                text = 'Xml Insert Failed',
                detailed_text = ('Xml insert of node with name "%s" failed - '
                'most likely because there is already a node with that name.' %
                name))
            return


    def process_custom_menu(self, position):
        ''' See XmlConfig.processCustomMenu for documentation '''
        item = self.select_item_at(position)

        index = self.view.indexAt(position)
        cnt = self.model.rowCount(index.parent())

        istop = index.row() == 0
        isbottom = index.row() == cnt-1
        isonly = cnt == 1

        if not item:
            return

        node = item.node
        menu = QMenu(self.view)

        # Tool files are the "actual" tools
        if node.tag == "tool":
            menu.addAction(self.actExecToolFile)
            if not isonly: menu.addSeparator()
            if not istop: menu.addAction(self.actMoveNodeUp)
            if not isbottom: menu.addAction(self.actMoveNodeDown)

        elif node.tag == "class_module":
            menu.addAction(self.actChangeClassModule)

        elif node.tag == "path_to_tool_modules":
            menu.addAction(self.actChangePathToTools)

        # "Tool library is a collection of tool groups
        elif node.tag == "tool_library":
            menu.addAction(self.actAddToolGroup)

        # Tool groups are groups of "tool files"
        elif node.tag == "tool_group":
            menu.addAction(self.actAddToolFile)
            if not isonly: menu.addSeparator()
            if not istop: menu.addAction(self.actMoveNodeUp)
            if not isbottom: menu.addAction(self.actMoveNodeDown)

        # Param Template is the parameter node for the tools -- where
        # users can build up a list of parameters that gets passed to the
        # tool function
        elif node.tag == "params":
            menu.addAction(self.actAddParam)

        elif node.tag == "param":
            menu.addAction(self.actEditParam)

        # A "tool config" is an alternative configuration for a tool that can be
        # put in a Tool Set
        elif node.tag == "tool_config":
            menu.addAction(self.actExecToolConfig)
            if not isonly: menu.addSeparator()
            if not istop: menu.addAction(self.actMoveNodeUp)
            if not isbottom: menu.addAction(self.actMoveNodeDown)

        # "Tool sets" is a collection of multiple tool sets
        elif node.tag == "tool_sets":
            menu.addAction(self.actAddNewToolSet)

        # A Tool set is a collection of (alternative) configurations for
        # existing tools.
        elif node.tag == "tool_set":
            menu.addAction(self.actExecBatch)
            menu.addSeparator()
            menu.addAction(self.actNewConfig)
            if not isonly: menu.addSeparator()
            if not istop: menu.addAction(self.actMoveNodeUp)
            if not isbottom: menu.addAction(self.actMoveNodeDown)

        elif node.tag == "documentation_path":
            menu.addAction(self.actOpenDocumentation)
            menu.addSeparator()
            menu.addAction(self.actCloneNode)

        # Default menu items
        self.add_default_menu_items_for_node(node, menu)

        # Now add the export and import methods
        menu.addSeparator()
        menu.addAction(self.actExportXMLToFile)
        menu.addAction(self.actImportXMLFromFile)

        # Check if the menu has any elements before exec is called
        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

