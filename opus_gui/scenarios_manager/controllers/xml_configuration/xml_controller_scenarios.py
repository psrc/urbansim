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
from PyQt4.QtGui import QIcon, QAction, QMenu, QCursor

from opus_gui.scenarios_manager.run.opusrunmodel import OpusModel
from opus_gui.abstract_manager.controllers.xml_configuration.clonenode import CloneNodeGui

from opus_gui.abstract_manager.controllers.xml_configuration.xml_controller import XmlController

class XmlController_Scenarios(XmlController):
    def __init__(self, toolboxbase, parentWidget, addTree = True, listen_to_menu = True): 
        XmlController.__init__(self, toolboxbase = toolboxbase, xml_type = 'scenario_manager', parentWidget = parentWidget, addTree = addTree, listen_to_menu = listen_to_menu) 
        

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

        self.actAddModel = QAction(self.addIcon,
                                   "Add Model...",
                                   self.mainwindow)
        QObject.connect(self.actAddModel,
                        SIGNAL("triggered()"),
                        self.addModel)

        self.actRemoveModel = QAction(self.removeIcon,
                                   "Remove This Model",
                                   self.mainwindow)
        QObject.connect(self.actRemoveModel,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actRunModel = QAction(self.acceptIcon,
                                   "Run This Scenario",
                                   self.mainwindow)
        QObject.connect(self.actRunModel,
                        SIGNAL("triggered()"),
                        self.runModel)

        self.actOpenXMLFile = QAction(self.calendarIcon,
                                      "Open XML File",
                                      self.mainwindow)
        QObject.connect(self.actOpenXMLFile,
                        SIGNAL("triggered()"),
                        self.openXMLFile)

        self.actEditXMLFileGlobal = QAction(self.calendarIcon,
                                            "Edit XML File Global",
                                            self.mainwindow)
        QObject.connect(self.actEditXMLFileGlobal,
                        SIGNAL("triggered()"),
                        self.editXMLFileGlobal)

        self.actEditXMLFileLocal = QAction(self.calendarIcon,
                                           "Edit XML File Local",
                                           self.mainwindow)
        QObject.connect(self.actEditXMLFileLocal,
                        SIGNAL("triggered()"),
                        self.editXMLFileLocal)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                    "Add to current project",
                                    self.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove node from current project",
                                     self.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Copy Node",
                                    self.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actMoveNodeUp = QAction(self.arrowUpIcon,
                                     "Move Model Up",
                                     self.mainwindow)
        QObject.connect(self.actMoveNodeUp,
                        SIGNAL("triggered()"),
                        self.moveNodeUp)

        self.actMoveNodeDown = QAction(self.arrowDownIcon,
                                       "Move Model Down",
                                       self.mainwindow)
        QObject.connect(self.actMoveNodeDown,
                        SIGNAL("triggered()"),
                        self.moveNodeDown)

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
                elif domElement.attribute(QString("type")) == QString("model"):
                    self.menu.addAction(self.actRemoveModel)
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("config_name")) == QString("models"):
                    self.modelMenu = QMenu(QString("Add Model"), self.mainwindow)
                    self.modelMenu.setIcon(self.addIcon)
                    self.modelMenu.addAction(QString("models go here"))
                    self.menu.addMenu(self.modelMenu)
                    #self.menu.addAction(self.actAddModel)

                if self.menu:
                    # Last minute chance to add items that all menues should have
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
# Jesse working:
    def addModel(self):
        # Add a model to the models_to_run list from the model_system
        print "Not implemented yet"
#        self.getListOfModels()
#    def getListOfModels(self):
#        '''
#        Returns a list of the names of models available in the
#        model_system section of the model manager
#        '''
#        model_system = self.mainwindow.toolboxBase.modelManagerTree.model.domDocument.elementsByTagName(QString("model_system"))
#        print model_system
#        for i in range(0, model_system.count()):
#            print i
##        configFile = QFile(database_server_configuration_file)
##        doc = QDomDocument()
##        doc.setContent(configFile)
##
##        list_of_db_connections = []
##        for i in range(0, doc.documentElement().childNodes().length()):
##            db_connection_name = doc.documentElement().childNodes().item(i).nodeName()
##            if db_connection_name != '#comment':
##                list_of_db_connections.append(str(db_connection_name))
##        return list_of_db_connections        

