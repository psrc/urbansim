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


from PyQt4.QtCore import QString, QFileInfo, SIGNAL
from PyQt4.QtGui import QIcon, QMenu, QCursor

from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.abstract_manager.controllers.xml_configuration.clonenode import CloneNodeGui
from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlView
from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlItemDelegate
from opus_gui.scenarios_manager.models.xml_model_scenarios import XmlModel_Scenarios

class XmlController_Scenarios(XmlController):
    
    def __init__(self, toolboxbase, parentWidget):
        XmlController.__init__(self, toolboxbase = toolboxbase,
                               xml_type = 'scenario_manager',
                               parentWidget = parentWidget)

        self.currentColumn = None
        self.currentIndex = None

        self.addIcon = QIcon(":/Images/Images/add.png")
        self.arrowUpIcon = QIcon(":/Images/Images/arrow_up.png")
        self.arrowDownIcon = QIcon(":/Images/Images/arrow_down.png")
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        self.actAddModel = self.createAction(self.makeEditableIcon,"Add Model...",self.addModel)
        self.actRemoveModel = self.createAction(self.removeIcon,"Remove This Model",self.removeNode)
        self.actRunModel = self.createAction(self.acceptIcon,"Run This Scenario",self.runModel)
        self.actOpenXMLFile = self.createAction(self.calendarIcon,"Open XML File",self.openXMLFile)
        self.actEditXMLFileGlobal = self.createAction(self.calendarIcon,"Edit XML File Global",self.editXMLFileGlobal)
        self.actEditXMLFileLocal = self.createAction(self.calendarIcon,"Edit XML File Local",self.editXMLFileLocal)
        self.actMakeEditable = self.createAction(self.makeEditableIcon,"Add to current project",self.makeEditableAction)
        self.actRemoveNode = self.createAction(self.removeIcon,"Remove node from current project",self.removeNode)
        self.actCloneNode = self.createAction(self.cloneIcon,"Copy Node",self.cloneNode)
        self.actMoveNodeUp = self.createAction(self.arrowUpIcon,"Move Model Up",self.moveNodeUp)
        self.actMoveNodeDown = self.createAction(self.arrowDownIcon,"Move Model Down",self.moveNodeDown)

        self.xml_helper = ResultsManagerXMLHelper(self.toolboxbase)
        self.validate_models_to_run_list()


    def setupModelViewDelegate(self):
        '''switch out the model'''
        self.model = XmlModel_Scenarios(self, self.toolboxbase.doc, self.mainwindow,
              self.toolboxbase.configFile, self.xmlType, True)
        self.view = XmlView(self.mainwindow)
        self.delegate = XmlItemDelegate(self.view)


    def checkIsDirty(self):
        if (self.toolboxbase.resultsManagerTree and self.toolboxbase.resultsManagerTree.model.isDirty()) or \
               (self.toolboxbase.modelManagerTree and self.toolboxbase.modelManagerTree.model.isDirty()) or \
               (self.toolboxbase.runManagerTree and self.toolboxbase.runManagerTree.model.isDirty()) or \
               (self.toolboxbase.dataManagerTree and self.toolboxbase.dataManagerTree.model.isDirty()) or \
               (self.toolboxbase.dataManagerDBSTree and self.toolboxbase.dataManagerDBSTree.model.isDirty()) or \
               (self.toolboxbase.generalManagerTree and self.toolboxbase.generalManagerTree.model.isDirty()):
            return True
        else:
            return False

    def runModel(self):
        '''Run the selected model'''
        # Update the XMLConfiguration copy of the XML tree before running the model
        self.toolboxbase.updateOpusXMLTree()
        modelToRun = self.currentIndex.internalPointer().node().nodeName()
        # Add the model to the run Q
        newModel = OpusModel(self,
                             self.toolboxbase.xml_file,
                             modelToRun)
        self.mainwindow.scenariosManagerBase.addNewSimulationElement(model = newModel)

    def openXMLFile(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.toolboxbase.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
        self.toolboxbase.openXMLTree(newFile.absoluteFilePath())


    def editXMLFileLocal(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.toolboxbase.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))

        # To test QScintilla
        if self.mainwindow.editorStuff:
            #print "Loading into qscintilla..."
            # Now an individual tab
            from opus_gui.util.editorbase import EditorTab
            fileName = newFile.absoluteFilePath()
            x = EditorTab(self.mainwindow, QString(fileName))

    def editXMLFileGlobal(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.toolboxbase.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))

        # To test QScintilla
        if self.mainwindow.editorStuff:
            #print "Loading into qscintilla..."
            # Start with the base tab
            fileName = newFile.absoluteFilePath()
            self.mainwindow.editorStuff.clear()
            try:
                f = open(fileName,'r')
            except:
                return
            for l in f.readlines():
                self.mainwindow.editorStuff.append(l)
            f.close()
            self.mainwindow.editorStatusLabel.setText(QString(fileName))

    def removeNode(self):
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.validate_models_to_run_list()
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def moveNodeUp(self):
        self.currentIndex.model().moveUp(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def moveNodeDown(self):
        self.currentIndex.model().moveDown(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNode(self):
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        window = CloneNodeGui(self, clone,parentIndex,model)
        window.show()
        self.validate_models_to_run_list()

    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        self.currentIndex.model().makeEditable(thisNode)
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def processCustomMenu(self, position):
        if self.view.indexAt(position).isValid() and \
               self.view.indexAt(position).column() == 0:
            self.currentColumn = self.view.indexAt(position).column()
            self.currentIndex = self.view.indexAt(position)
            # select the scenario in the list to highlight it
            self.view.setCurrentIndex(self.view.indexAt(position))
            parentElement = None
            parentIndex = self.currentIndex.model().parent(self.currentIndex)
            if parentIndex and parentIndex.isValid():
                parentNode = parentIndex.internalPointer().node()
                parentElement = parentNode.toElement()
            item = self.currentIndex.internalPointer()
            domElement = item.node().toElement()
            if domElement.isNull():
                return

            # create and populate menu based on the node element
            menu = QMenu(self.mainwindow)
            if domElement.attribute(QString("executable")) == QString("True"):
                menu.addAction(self.actRunModel)
            elif domElement.attribute(QString("type")) == QString("file"):
                menu.addAction(self.actOpenXMLFile)
                menu.addSeparator()
                menu.addAction(self.actEditXMLFileGlobal)
                menu.addAction(self.actEditXMLFileLocal)

            elif domElement.attribute(QString("type")) == "model_choice":
                menu.addAction(self.actRemoveModel)
                menu.addAction(self.actMoveNodeUp)
                menu.addAction(self.actMoveNodeDown)

            elif domElement.attribute("config_name") == QString("models"):
                # decide which scenario to add models to
                scenario_index = self.currentIndex

                # build a submenu with models
                models_submenu = QMenu(menu)
                models_submenu.setTitle('Add model to run')
                available_models = self.getAvailableModels()
                for model in available_models:
                    callback = lambda x=model: self.addModel(scenario_index, x)
                    models_submenu.addAction(self.createAction(self.addIcon,
                                                               model, callback))
                menu.addMenu(models_submenu)

            if menu:
                # Last minute chance to add items that all menus should have
                if domElement.hasAttribute(QString("inherited")):
                    # Tack on a make editable if the node is inherited
                    menu.addSeparator()
                    menu.addAction(self.actMakeEditable)
                else:
                    if domElement.hasAttribute(QString("copyable")) and \
                           domElement.attribute(QString("copyable")) == QString("True"):
                        menu.addSeparator()
                        menu.addAction(self.actCloneNode)
                    if domElement and (not domElement.isNull()) and \
                           domElement.hasAttribute(QString("type")) and \
                           ((domElement.attribute(QString("type")) == QString("dictionary")) or \
                            (domElement.attribute(QString("type")) == QString("selectable_list")) or \
                            (domElement.attribute(QString("type")) == QString("list"))):
                        menu.addSeparator()
                        menu.addAction(self.actRemoveNode)
            # Check if the menu has any elements before exec is called
            if not menu.isEmpty():
                menu.exec_(QCursor.pos())
        return

    def getAvailableModels(self):
        ''' return a list of names for available models in the project'''
        from opus_gui.results_manager.xml_helper_methods import elementsByAttributeValue

        model_elements = []
        available_model_names = []

        elements = elementsByAttributeValue(domDocument=self.toolboxbase.doc, attribute='type', value='model')
        model_elements = [e[0] for e in elements]
        # if the xml file is old, it might have some models defined as part of
        # the 'default_model_configuration' -- include those when populating the
        # menu. Should we drop this support?
        def_models = self.xml.get('model_manager/default_models') or \
            self.xml.get('model_manager/default_model_configurations')  
        if def_models is not None:
            def_model_names = [e.tagName() for e in self.xml.children(def_models)]
            available_model_names.extend(def_model_names)

        model_names = [e.tagName() for e in model_elements]
        available_model_names.extend(model_names)

        return available_model_names

    def addModel(self, scenario_index, model_name):
        spawn = self.model.domDocument.createElement(model_name)
        spawn_text = self.model.domDocument.createTextNode('Run')
        spawn.appendChild(spawn_text)
        spawn.setAttribute('choices', 'Run|Skip')
        spawn.setAttribute('type', 'model_choice')
        # insert as first child to scenario
        self.model.insertRow(0, scenario_index, spawn)

    def validate_models_to_run_list(self, display_warning = False):
        '''
            Check each model in the models to run list to be present in the
            model configuration tab. If display_warning is True, a popup warning
            with the missing models is displayed. No warning is displayed if all
            models are present.

            Returns True if all models are present, False otherwise.
        '''
        # fetch list of project scenarios
        xml = self.xml
        manager_root = xml.manager_root()
        scenarios = [child for child in
                     xml.children(manager_root) if
                     xml.get_attrib('type', child) == 'scenario']
        # fetch list of model names
        existing_model_names = [model.tagName() for model in
                                xml.children('/model_manager/model_system') if
                                xml.get_attrib('type', model) == 'model']
        # validate existence of models in models_to_run lists
        for scenario in scenarios:
            models_to_run_section = xml.get('models_to_run', scenario)
            if not models_to_run_section:
                continue # no models_to_run section
            models_to_run = xml.children(models_to_run_section)
            if not models_to_run:
                continue # no models in models_to_run
            missing_models = []
            for model in models_to_run:
                # compare by tagName (model name)
                if not model.tagName() in existing_model_names:
                    # set missing model flag
                    item = xml._item_for_element(model)
                    if item:
                        item.is_missing_model = True
                    missing_models.append(model)
                else:
                    # clear missing model flag
                    item = xml._item_for_element(model)
                    if item:
                        item.is_missing_model = False
            # handle result of the validation
            if missing_models:
                if display_warning:
                    msg = ("The following models are listed to run, but they are "
                           "not part of this (or any inherited) project.\n")
                    for model in missing_models:
                        msg = msg + '    %s\n' %model.tagName()
                        item = xml._item_for_element(model)
                    MessageBox.error(mainwindow = self.mainwindow,
                                      text = "There are missing models.",
                                      detailed_text = msg)

                return False
            else:
                return True
