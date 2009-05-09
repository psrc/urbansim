# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from lxml.etree import Element

from PyQt4.QtGui import QMenu, QCursor

from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate
from opus_gui.scenarios_manager.models.xml_model_scenarios import XmlModel_Scenarios
from opus_gui.models_manager.models_manager import get_model_names
from opus_gui.scenarios_manager.scenario_manager import update_models_to_run_lists
from opus_gui.util.icon_library import IconLibrary


class XmlController_Scenarios(XmlController):

    def __init__(self, manager):
        ''' See XmlController.__init__ for documentation '''
        XmlController.__init__(self, manager)

        self.actAddModel = self.create_action('make_editable', 'Add Model', self.addModel)
        self.actRunScenario = self.create_action('accept', 'Run This Scenario', self.runScenario)
        self.actMoveNodeUp = self.create_action('arrow_up', "Move Up", self.moveNodeUp)
        self.actMoveNodeDown = self.create_action('arrow_down', "Move Down", self.moveNodeDown)

        # CK - what's this? Removing for now...
#        self.actOpenXMLFile = self.create_action(self.calendarIcon,"Open XML File", self.openXMLFile)
#        self.actEditXMLFileGlobal = self.create_action(self.calendarIcon,"Edit XML File Global", self.editXMLFileGlobal)
#        self.actEditXMLFileLocal = self.create_action(self.calendarIcon,"Edit XML File Local", self.editXMLFileLocal)

        # validate_models_to_run_lists()

    def add_model_view_delegate(self):
        ''' See XmlModel for documentation '''
        # Use the scenarios model
        self.model = XmlModel_Scenarios(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def runScenario(self):
        ''' Run the selected scenario. '''
        assert self.has_selected_item()
        scenario_node = self.selected_item().node

        newModel = OpusModel(self.manager, self.manager.project.xml_config,
                             scenario_node.get('name'))
        self.manager.addNewSimulationElement(newModel)

    def validate_models_to_run(self):
        ''' Mark up missing models in models to run lists '''
        self.model.validate_models_to_run()

    def moveNodeUp(self):
        ''' Move the selected node up one step '''
        assert self.has_selected_item()
        self.view.setCurrentIndex(self.model.move_up(self.selected_index()))

    def moveNodeDown(self):
        ''' Move the selected node down one step '''
        assert self.has_selected_item()
        self.view.setCurrentIndex(self.model.move_down(self.selected_index()))

    def process_custom_menu(self, point):
        ''' See XmlController for documentation '''
        item = self.select_item_at(point)
        if not item:
            return
        menu = QMenu()
        node = item.node

        if node.get('executable') == 'True':
            menu.addAction(self.actRunScenario)
        elif node.get('type') == 'model_choice':
            menu.addAction(self.actMoveNodeUp)
            menu.addAction(self.actMoveNodeDown)
        elif node.get('config_name') == 'models':
            models_menu = QMenu(menu)
            models_menu.setTitle('Add model to run')
            models_menu.setIcon(IconLibrary.icon('add'))
            available_model_names = get_model_names(self.project)
            for model_name in available_model_names:
                cb = lambda x=model_name: self.addModel(self.selected_index(), x)
                action = self.create_action('model', model_name, cb)
                models_menu.addAction(action)
            menu.addMenu(models_menu)

        self.add_default_menu_items_for_node(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())

    def addModel(self, models_to_run_list_index, model_name):
        '''
        Add a model to a models_to_run list.
        @param scenario_index (QModelIndex): index of the list to insert under
        @param models_name (String): name of model to add
        '''
        model_node = Element(model_name, {'choices': 'Run|Skip', 'type': 'model_choice'})
        model_node.text = 'Run'
        last_row_num = self.model.rowCount(models_to_run_list_index)
        self.model.insertRow(last_row_num, models_to_run_list_index, model_node)
        # Validate models to run
        update_models_to_run_lists()


# Could not find anything that uses this -- commenting out for now.

#    def openXMLFile(self):
#        ''' NO DOCUMENTATION '''
#        assert self.has_selected_item()
#        node = self.selected_item().node
#        filePath = node.tag
#
#        fileInfo = QFileInfo(filePath)
#        baseInfo = QFileInfo(self.toolboxbase.xml_file)
#        baseDir = baseInfo.absolutePath()
#        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
#        self.toolboxbase.openXMLTree(newFile.absoluteFilePath())

#    def editXMLFileLocal(self):
#        ''' NO DOCUMENTATION '''
#        filePath = ""
#        if self.currentIndex.internalPointer().node().hasChildNodes():
#            children = self.currentIndex.internalPointer().node().childNodes()
#            for x in xrange(0,children.count(),1):
#                if children.item(x).isText():
#                    filePath = children.item(x).nodeValue()
#        fileInfo = QFileInfo(filePath)
#        baseInfo = QFileInfo(self.toolboxbase.xml_file)
#        baseDir = baseInfo.absolutePath()
#        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
#
#        # To test QScintilla
#        if self.mainwindow.editorStuff:
#            #print "Loading into qscintilla..."
#            # Now an individual tab
#            from opus_gui.util.editorbase import EditorTab
#            fileName = newFile.absoluteFilePath()
#            x = EditorTab(self.mainwindow, QString(fileName))
#
#    def editXMLFileGlobal(self):
#        ''' NO DOCUMENTATION '''
#        filePath = ""
#        if self.currentIndex.internalPointer().node().hasChildNodes():
#            children = self.currentIndex.internalPointer().node().childNodes()
#            for x in xrange(0,children.count(),1):
#                if children.item(x).isText():
#                    filePath = children.item(x).nodeValue()
#        fileInfo = QFileInfo(filePath)
#        baseInfo = QFileInfo(self.toolboxbase.xml_file)
#        baseDir = baseInfo.absolutePath()
#        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
#
#        # To test QScintilla
#        if self.mainwindow.editorStuff:
#            #print "Loading into qscintilla..."
#            # Start with the base tab
#            fileName = newFile.absoluteFilePath()
#            self.mainwindow.editorStuff.clear()
#            try:
#                f = open(fileName,'r')
#            except:
#                return
#            for l in f.readlines():
#                self.mainwindow.editorStuff.append(l)
#            f.close()
#            self.mainwindow.editorStatusLabel.setText(QString(fileName))
