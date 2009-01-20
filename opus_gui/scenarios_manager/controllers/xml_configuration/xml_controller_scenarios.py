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

from xml.etree.cElementTree import Element

from PyQt4.QtCore import QString, QFileInfo, SIGNAL
from PyQt4.QtGui import QIcon, QMenu, QCursor

from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate
from opus_gui.scenarios_manager.models.xml_model_scenarios import XmlModel_Scenarios


class XmlController_Scenarios(XmlController):

    def __init__(self, manager):
        ''' See XmlController.__init__ for documentation '''
        XmlController.__init__(self, manager)

        i, t, c = (self.model.makeEditableIcon, 'Add Model...', self.addModel)
        self.actAddModel = self.createAction(i, t, c)

        i, t, c = (self.model.acceptIcon, 'Run This Scenario', self.runScenario)
        self.actRunScenario = self.createAction(i, t, c)

        i, t, c = (self.model.arrowUpIcon, "Move Up", self.moveNodeUp)
        self.actMoveNodeUp = self.createAction(i, t, c)

        i, t, c = (self.model.arrowDownIcon, "Move Down", self.moveNodeDown)
        self.actMoveNodeDown = self.createAction(i, t, c)

        # CK - what's this? Removing for now...
#        self.actOpenXMLFile = self.createAction(self.calendarIcon,"Open XML File", self.openXMLFile)
#        self.actEditXMLFileGlobal = self.createAction(self.calendarIcon,"Edit XML File Global", self.editXMLFileGlobal)
#        self.actEditXMLFileLocal = self.createAction(self.calendarIcon,"Edit XML File Local", self.editXMLFileLocal)

        self.validate_models_to_run_list()

    def _get_available_models(self):
        '''
        Get a list of names for available models in the project
        @return list of all models names in this project ([String])
        '''
        # Get all model specifications
        model_system_node = self.manager.project\
            .find('model_manager/model_system')
        return [node.tag for node in (model_system_node or [])
                if node.get('type') == 'model']

    def setupModelViewDelegate(self):
        ''' See XmlModel for documentation '''
        # Use the scenarios model
        self.model = XmlModel_Scenarios(self.xml_root, self.manager.project)
        self.view = XmlView(self.manager.base_widget)
        self.delegate = XmlItemDelegate(self.view)

    def runScenario(self):
        ''' Run the selected scenario. '''
        assert self.hasSelectedItem()
        scenario_node = self.selectedItem().node

        newModel = OpusModel(self.manager, self.manager.project.xml_config,
                             scenario_node.tag)
        self.manager.addNewSimulationElement(newModel)

    def moveNodeUp(self):
        ''' Move the selected node up one step '''
        assert self.hasSelectedItem()
        self.view.setCurrentIndex(self.model.moveUp(self.selectedIndex()))

    def moveNodeDown(self):
        ''' Move the selected node down one step '''
        assert self.hasSelectedItem()
        self.view.setCurrentIndex(self.model.moveDown(self.selectedIndex()))

    def processCustomMenu(self, point):
        ''' See XmlController for documentation '''
        item = self.selectItemAt(point)
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
            available_models = self._get_available_models()
            for model in available_models:
                cb = lambda x=model: self.addModel(self.selectedIndex(), x)
                action = self.createAction(self.model.addIcon, model, cb)
                models_menu.addAction(action)
            menu.addMenu(models_menu)

        self.addDefaultMenuItems(node, menu)

        if not menu.isEmpty():
            menu.exec_(QCursor.pos())


    def addModel(self, models_to_run_list_index, model_name):
        '''
        Add a model to a models_to_run list.
        @param scenario_index (QModelIndex): index of the list to insert under
        @param models_name (String): name of model to add
        '''
        model_node = Element(model_name, {'choices': 'Run|Skip',
                                          'type': 'model_choice'})
        model_node.text = 'Run'
        last_row_num = self.model.rowCount(models_to_run_list_index)
        self.model.insertRow(last_row_num, models_to_run_list_index, model_node)


    def validate_models_to_run_list(self, display_warning = False):
        '''
        Check each model in the models to run list to be present in the
        model configuration tab.

        The method tags the XmlItems that have missing models with an
        additional attribute named "is_missing_model" with a value of True
        for all items that represents missing models.

        @param display_warning (boolean): If True, a popup warning
        with the missing models is displayed. No warning is displayed if all
        models are present.
        @return: True if all models are present, False otherwise.
        '''
        # TODO implement this
        return True
        # fetch list of project scenarios
#
#        scenarios_node = self.xml_root
#        return [node.tag for node in (model_system_node or [])
#                if node.get('type') == 'model']
#
#        scenarios = [node.tag for node in ]
#        xml = self.xml
#        manager_root = xml.manager_root()
#        scenarios = [child for child in
#                     xml.children(manager_root) if
#                     xml.get_attrib('type', child) == 'scenario']
#        # fetch list of model names
#        existing_model_names = [model.tagName() for model in
#                                xml.children('/model_manager/model_system') if
#                                xml.get_attrib('type', model) == 'model']
#        # validate existence of models in models_to_run lists
#        for scenario in scenarios:
#            models_to_run_section = xml.get('models_to_run', scenario)
#            if not models_to_run_section:
#                continue # no models_to_run section
#            models_to_run = xml.children(models_to_run_section)
#            if not models_to_run:
#                continue # no models in models_to_run
#            missing_models = []
#            for model in models_to_run:
#                # compare by tagName (model name)
#                if not model.tagName() in existing_model_names:
#                    # set missing model flag
#                    item = xml._item_for_element(model)
#                    if item:
#                        item.is_missing_model = True
#                    missing_models.append(model)
#                else:
#                    # clear missing model flag
#                    item = xml._item_for_element(model)
#                    if item:
#                        item.is_missing_model = False
#            # handle result of the validation
#            if missing_models:
#                if display_warning:
#                    msg = ("The following models are listed to run, but they are "
#                           "not part of this (or any inherited) project.\n")
#                    for model in missing_models:
#                        msg = msg + '    %s\n' %model.tagName()
#                        item = xml._item_for_element(model)
#                    QMessageBox.error(self, 'Error - Missing models', msg)
#                return False
#            else:
#                return True

# Could not find anything that uses this -- commenting out for now.

#    def openXMLFile(self):
#        ''' NO DOCUMENTATION '''
#        assert self.hasSelectedItem()
#        node = self.selectedItem().node
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
