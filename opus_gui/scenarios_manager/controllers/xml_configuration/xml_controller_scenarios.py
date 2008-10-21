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
from PyQt4.QtCore import QString, Qt, QFileInfo, QObject, SIGNAL
from PyQt4.QtGui import QIcon, QAction, QMenu, QCursor, QKeySequence

from opus_gui.scenarios_manager.run.run_simulation import OpusModel
from opus_gui.abstract_manager.controllers.xml_configuration.clonenode import CloneNodeGui

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController

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
        self.modelIcon = QIcon(":/Images/Images/cog.png")

        self.actAddModel = self.createAction(self.addIcon,"Add Model...",self.addModel)
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
        #print "Test - ", newFile.absoluteFilePath()
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
            import opus_gui.util.editorbase
            fileName = newFile.absoluteFilePath()
            x = util.editorbase.EditorTab(self.mainwindow, QString(fileName))

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
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def moveNodeUp(self):
        #print "Move Up Pressed"
        self.currentIndex.model().moveUp(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def moveNodeDown(self):
        #print "Move Down Pressed"
        self.currentIndex.model().moveDown(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parentIndex,model)
        window.setModal(True)
        window.show()

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
            parentElement = None
            parentIndex = self.currentIndex.model().parent(self.currentIndex)
            if parentIndex and parentIndex.isValid():
                parentNode = parentIndex.internalPointer().node()
                parentElement = parentNode.toElement()
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return

                self.menu = QMenu(self.mainwindow)
                if domElement.attribute(QString("executable")) == QString("True"):
                    self.menu.addAction(self.actRunModel)
                elif domElement.attribute(QString("type")) == QString("file"):
                    self.menu.addAction(self.actOpenXMLFile)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actEditXMLFileGlobal)
                    self.menu.addAction(self.actEditXMLFileLocal)
                elif domElement.attribute(QString("type")) == QString("model_choice"):
                    self.menu.addAction(self.actRemoveModel)
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("config_name")) == QString("models"):
                    self.modelMenu = QMenu(QString("Add Model"), self.mainwindow)
                    self.modelMenu.setIcon(self.addIcon)
                    QObject.connect(self.modelMenu, SIGNAL('aboutToShow()'), self.aboutToShowModelMenu)
                    self.menu.addMenu(self.modelMenu)
                if self.menu:
                    # Last minute chance to add items that all menus should have
                    if domElement.hasAttribute(QString("inherited")):
                        # Tack on a make editable if the node is inherited
                        self.menu.addSeparator()
                        self.menu.addAction(self.actMakeEditable)
                    else:
                        if domElement.hasAttribute(QString("copyable")) and \
                               domElement.attribute(QString("copyable")) == QString("True"):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actCloneNode)
                        if domElement and (not domElement.isNull()) and \
                               domElement.hasAttribute(QString("type")) and \
                               ((domElement.attribute(QString("type")) == QString("dictionary")) or \
                                (domElement.attribute(QString("type")) == QString("selectable_list")) or \
                                (domElement.attribute(QString("type")) == QString("list"))):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return
    
    def aboutToShowModelMenu(self):
        models = self.getAvailableModels()
        for model in models:
            action = QAction(self.modelIcon, model, self.mainwindow)
            callback = lambda model_name=model: self.addModel(model_name)
            QObject.connect(action, SIGNAL("triggered()"), callback)
            self.modelMenu.addAction(action)

    def getAvailableModels(self):
        from opus_gui.results_manager.xml_helper_methods import elementsByAttributeValue
        model_elements = elementsByAttributeValue(domDocument=self.toolboxbase.doc, attribute='type', value='model')
        available_models = []
        for model in model_elements:
            model_name = model[1].nodeName()
            available_models.append(model_name)
        return available_models

    def addModel(self, model_name):
        # Add a model to the models_to_run list from the model_system
        
#        new_model = self.toolboxbase.doc.createElement(model_name)
#        new_model.setAttribute(QString("choices"),QString("Run|Skip"))
#        new_model.setAttribute(QString("type"),QString("model"))
#        x = self.toolboxbase.doc.elementsByTagName(QString("models_to_run"))
#        x.item(0).appendChild(new_model)
        
        from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
        helper = ResultsManagerXMLHelper(self.toolboxbase)
        head_node_args = {"choices":"Run|Skip", "type":"model",'value':'Run'}
        helper._add_new_xml_tree(head_node_name=model_name, 
                                 head_node_args=head_node_args, 
                                 parent_name='models_to_run',
                                 xml_tree = self.toolboxbase.runManagerTree)



