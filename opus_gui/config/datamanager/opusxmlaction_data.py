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
from PyQt4.QtXml import *

from opus_gui.run.tool.opusruntool import *
import opus_gui.util.documentationbase
from opus_gui.config.datamanager.configuretool import ConfigureToolGui
from opus_gui.config.datamanager.executetool import ExecuteToolGui
from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui
from opus_gui.config.managerbase.clonenode import CloneNodeGui
from opus_core.configurations.xml_configuration import XMLConfiguration

import os,tempfile

class OpusXMLAction_Data(object):
    def __init__(self, opusXMLAction):
        self.opusXMLAction = opusXMLAction
        self.mainwindow = opusXMLAction.mainwindow
        self.xmlTreeObject = opusXMLAction.xmlTreeObject

        self.currentColumn = None
        self.currentIndex = None

        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        self.addIcon = QIcon(":/Images/Images/add.png")
        self.arrowUpIcon = QIcon(":/Images/Images/arrow_up.png")
        self.arrowDownIcon = QIcon(":/Images/Images/arrow_down.png")
        self.executeIcon = QIcon(":/Images/Images/table_go.png")
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")
        
        self.actExecToolFile = QAction(self.executeIcon,
                                       "Execute Tool...",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecToolFile,
                        SIGNAL("triggered()"),
                        self.execToolFile)

        self.actExecToolConfig = QAction(self.executeIcon,
                                           "Execute Tool...",
                                           self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecToolConfig,
                        SIGNAL("triggered()"),
                        self.execToolFile)

        self.actAddToolFile = QAction(self.addIcon,
                                        "Add Tool to Library",
                                        self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddToolFile,
                        SIGNAL("triggered()"),
                        self.addToolFile)

        self.actAddRequiredStringParam = QAction(self.addIcon,
                                                 "Add Required String Parameter",
                                                 self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddRequiredStringParam,
                        SIGNAL("triggered()"),
                        self.addRequiredStringParam)

        self.actAddRequiredDirParam = QAction(self.addIcon,
                                              "Add Required Directory Parameter",
                                              self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddRequiredDirParam,
                        SIGNAL("triggered()"),
                        self.addRequiredDirParam)
        
        self.actAddRequiredFileParam = QAction(self.addIcon,
                                               "Add Required File Parameter",
                                               self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddRequiredFileParam,
                        SIGNAL("triggered()"),
                        self.addRequiredFileParam)
        
        self.actAddOptionalStringParam = QAction(self.addIcon,
                                                 "Add Optional String Parameter",
                                                 self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddOptionalStringParam,
                        SIGNAL("triggered()"),
                        self.addOptionalStringParam)

        self.actAddOptionalDirParam = QAction(self.addIcon,
                                              "Add Optional Directory Parameter",
                                              self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddOptionalDirParam,
                        SIGNAL("triggered()"),
                        self.addOptionalDirParam)

        self.actAddOptionalFileParam = QAction(self.addIcon,
                                               "Add Optional File Parameter",
                                               self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddOptionalFileParam,
                        SIGNAL("triggered()"),
                        self.addOptionalFileParam)

        self.actAddNewToolSet = QAction(self.addIcon,
                                        "Add New Tool Set",
                                        self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddNewToolSet,
                        SIGNAL("triggered()"),
                        self.addNewToolSet)

        self.actNewConfig = QAction(self.addIcon,
                                     "Add Tool to Tool Set",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actNewConfig,
                        SIGNAL("triggered()"),
                        self.newConfig)

        self.actCloneBatch = QAction(self.cloneIcon,
                                     "Clone Tool Set",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneBatch,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actCloneTool = QAction(self.cloneIcon,
                                      "Clone Tool",
                                      self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneTool,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actOpenDocumentation = QAction(self.calendarIcon,
                                            "Open Documentation",
                                            self.xmlTreeObject.mainwindow)
        QObject.connect(self.actOpenDocumentation,
                        SIGNAL("triggered()"),
                        self.openDocumentation)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove node from current project",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actMoveNodeUp = QAction(self.arrowUpIcon,
                                     "Move Up",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMoveNodeUp,
                        SIGNAL("triggered()"),
                        self.moveNodeUp)

        self.actMoveNodeDown = QAction(self.arrowDownIcon,
                                       "Move Down",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMoveNodeDown,
                        SIGNAL("triggered()"),
                        self.moveNodeDown)

        #jesse testing
        self.actExecBatch = QAction(self.executeIcon,
                                      "Execute Tool Set",
                                      self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecBatch,
                        SIGNAL("triggered()"),
                        self.execBatch)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                       "Add to current project",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Copy Node",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actExportXMLToFile = QAction(self.cloneIcon,
                                          "Export XML Node To File",
                                          self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExportXMLToFile,
                        SIGNAL("triggered()"),
                        self.exportXMLToFile)

        self.actImportXMLFromFile = QAction(self.cloneIcon,
                                            "Import XML Node From File",
                                            self.xmlTreeObject.mainwindow)
        QObject.connect(self.actImportXMLFromFile,
                        SIGNAL("triggered()"),
                        self.importXMLFromFile)


    def addToolFile(self):
        #print "Add Tool Pressed"
        # First add the dummy tool shell
        newNode = self.currentIndex.model().domDocument.createElement(QString("Tool_Name_Rename_Me"))
        newNode.setAttribute(QString("type"),QString("tool_file"))
        # Now add the name field
        newName = self.currentIndex.model().domDocument.createElement(QString("name"))
        newName.setAttribute(QString("type"),QString("tool_name"))
        newNameText = self.currentIndex.model().domDocument.createTextNode(QString("File_Name_Rename_Me"))
        newName.appendChild(newNameText)
        # Next the empty params section
        newParams = self.currentIndex.model().domDocument.createElement(QString("params"))
        newParams.setAttribute(QString("type"),QString("param_template"))
        newNode.appendChild(newName)
        newNode.appendChild(newParams)
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))


    def newToolParam(self,toolType,choices):
        newParam = self.currentIndex.model().domDocument.createElement(QString("New_Param_Rename_Me"))

        newNodeRequired = self.currentIndex.model().domDocument.createElement(QString("required"))
        newNodeRequired.setAttribute(QString("type"),QString("string"))
        newNodeRequired.setAttribute(QString("choices"),QString("Required|Optional"))
        newTextRequired = self.currentIndex.model().domDocument.createTextNode(choices)
        newNodeRequired.appendChild(newTextRequired)

        newNodeType = self.currentIndex.model().domDocument.createElement(QString("type"))
        newNodeType.setAttribute(QString("type"),QString("string"))
        #newNode.setAttribute(QString("choices"),QString("string"))
        newTextType = self.currentIndex.model().domDocument.createTextNode(toolType)
        newNodeType.appendChild(newTextType)

        newNodeDefault = self.currentIndex.model().domDocument.createElement(QString("default"))
        newNodeDefault.setAttribute(QString("type"),toolType)
        newTextDefault = self.currentIndex.model().domDocument.createTextNode("")
        newNodeDefault.appendChild(newTextDefault)

        newParam.appendChild(newNodeRequired)
        newParam.appendChild(newNodeType)
        newParam.appendChild(newNodeDefault)

        return newParam

    def addRequiredStringParam(self):
        newNode = self.newToolParam(QString("string"), QString("Required"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addRequiredDirParam(self):
        newNode = self.newToolParam(QString("dir_path"), QString("Required"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addRequiredFileParam(self):
        newNode = self.newToolParam(QString("file_path"), QString("Required"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addOptionalStringParam(self):
        newNode = self.newToolParam(QString("string"), QString("Optional"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addOptionalDirParam(self):
        newNode = self.newToolParam(QString("dir_path"), QString("Optional"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addOptionalFileParam(self):
        newNode = self.newToolParam(QString("file_path"), QString("Optional"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def addNewToolSet(self):
        # First add the dummy toolset shell
        newNode = self.currentIndex.model().domDocument.createElement(QString("Rename_Me"))
        newNode.setAttribute(QString("type"),QString("tool_set"))
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def newConfig(self):
        #print "newConfig Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = ConfigureToolGui(self,flags)
        window.setModal(True)
        window.show()
        # Connect to a signal when the GUI collects the vars to add the element

    def moveNodeUp(self):
        #print "Move Up Pressed"
        self.currentIndex.model().moveUp(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def moveNodeDown(self):
        #print "Move Down Pressed"
        self.currentIndex.model().moveDown(self.currentIndex)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def openDocumentation(self):
        #print "Open Documentation Pressed"
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.xmlTreeObject.toolboxbase.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
        fileName = newFile.absoluteFilePath().trimmed()
        x = util.documentationbase.DocumentationTab(self.xmlTreeObject.mainwindow,
                                                    QString(fileName))


    def execToolFile(self):
        #print "Exec Tool Pressed"
        # Open up a GUI element and populate with variable's
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = ExecuteToolGui(self.mainwindow,self.currentIndex.model(),
                                self.currentIndex.internalPointer().node().toElement(),
                                self.execToolConfigGen,flags)
        tool_title = window.tool_title.replace('_', ' ')
        tool_title2 = str(tool_title).title()
        window.setWindowTitle(tool_title2)
        window.setModal(True)
        window.show()
        

    def execToolConfigGen(self,configNode,statusElement=None,progressElement=None):
        library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
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
        #print "New import ", importPath

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

        x = OpusTool(self.xmlTreeObject.mainwindow,importPath,params)
        y = RunToolThread(self.xmlTreeObject.mainwindow,x)
        y.run()

    def toolFinished(self, success):
        print "Tool Finished Signal Recieved - %s" % (success)
    
    def execToolConfig(self):
        # First find the tool that this config refers to...
        configNode = self.currentIndex.internalPointer().node().toElement()
        #library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        self.execToolConfigGen(configNode)
        
    def execBatch(self):
        #print "Execute batch pressed..."
        batchNode = self.currentIndex.internalPointer().node().toElement()
        #library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        childNodes = batchNode.childNodes()
        for x in xrange(0,childNodes.count(),1):
            thisNode = childNodes.item(x)
            if thisNode.isElement():
                thisElement = thisNode.toElement()
                if thisElement.hasAttribute(QString("type")) and \
                       (thisElement.attribute(QString("type")) == QString("tool_config")):
                    #self.execToolConfigGen(thisElement)
                    flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
                    window = ExecuteToolGui(self.mainwindow,self.currentIndex.model(),
                                            thisElement,
                                            self.execToolConfigGen,flags)
                    tool_title = window.tool_title.replace('_', ' ')
                    tool_title2 = str(tool_title).title()
                    window.setWindowTitle(tool_title2)
                    window.setModal(True)
                    window.show()

    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parentIndex,model)
        window.setModal(True)
        window.show()

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        self.currentIndex.model().makeEditable(thisNode)
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def exportXMLToFile(self):
        #print "exportXMLToFile"
        # First we grab a copy of the XML
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        # Ask the user where they want to save the file to
        start_dir = ''
        opus_home = os.environ.get('OPUS_HOME')
        if opus_home:
            start_dir_test = os.path.join(opus_home, 'project_configs')
            if start_dir_test:
                start_dir = start_dir_test
        configDialog = QFileDialog()
        filter_str = QString("*.xml")
        fd = configDialog.getSaveFileName(self.mainwindow,QString("Save As..."),
                                          QString(start_dir), filter_str)
        # Check for cancel
        if len(fd) == 0:
            return
        fileName = QString(fd)
        fileNameInfo = QFileInfo(QString(fd))
        fileName = fileNameInfo.fileName().trimmed()
        fileNamePath = fileNameInfo.absolutePath().trimmed()

        # Now create a dummyfile to make XMLConfiguration happy to start...
        [tempFile,tempFilePath] = tempfile.mkstemp()
        tempFileNameInfo = QFileInfo(QString(tempFilePath))
        tempFileName = tempFileNameInfo.fileName().trimmed()
        tempFileNamePath = tempFileNameInfo.absolutePath().trimmed()
        # We have to write out some dummy data for XMLConfig to be happy
        tempFile = QFile(tempFilePath)
        if tempFile:
            tempFile.open(QIODevice.ReadWrite)
            tempFile.write("<opus_project></opus_project>")
            tempFile.close()

        # Then create an XMLConfiguration based on that file
        newXMLTree = XMLConfiguration(str(tempFileName),str(tempFileNamePath))

        # Create a dom document to use as a temp space for the clone before writing out
        newDomDoc = QDomDocument()
        # Once again, we have to have opus_project for XMLConfig to be happy
        rootElement = newDomDoc.createElement("opus_project")
        newDomDoc.appendChild(rootElement)
        newElement = newDomDoc.importNode(clone,True)
        rootElement.appendChild(newElement)
        # Finally, write out the clone to the file via XMLConfiguration
        indentSize = 2
        newXMLTree.update(str(newDomDoc.toString(indentSize)))
        saveName = os.path.join(str(fileNamePath),str(fileName))
        newXMLTree.save_as(saveName)


    def importXMLFromFile(self):
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
        fd = configDialog.getOpenFileName(self.mainwindow,QString("Please select an xml file to import..."),
                                          QString(start_dir), filter_str)
        # Check for cancel
        if len(fd) == 0:
            return
        fileName = QString(fd)
        fileNameInfo = QFileInfo(QString(fd))
        fileNameInfoBaseName = fileNameInfo.completeBaseName()
        fileNameInfoName = fileNameInfo.fileName().trimmed()
        fileNameInfoPath = fileNameInfo.absolutePath().trimmed()

        # Pass that in to create a new XMLConfiguration
        newXMLTree = XMLConfiguration(str(fileNameInfoName),str(fileNameInfoPath))
        
        # Get the tree from XMLConfiguration
        [tempFile,tempFilePath] = tempfile.mkstemp()
        newXMLTree.full_tree.write(tempFilePath)
        configFileTemp = QFile(tempFilePath)
        configFileTemp.open(QIODevice.ReadWrite)
        newDoc = QDomDocument()
        newDoc.setContent(configFileTemp)

        # Now get the first node under opus_project
        xmlRoot = newDoc.elementsByTagName(QString("opus_project")).item(0)
        if xmlRoot.isNull():
            #Need to add an error here
            print "null xmlRoot"
            return
        newNodeToCopy = xmlRoot.firstChild()
        if newNodeToCopy.isNull():
            #Need to add an error here
            print "null newNodeToCopy"
            return

        # Need to get a copy of the node from one doc to the next
        newNode = self.currentIndex.model().domDocument.importNode(newNodeToCopy,True)

        # Insert it into the parent node from where the user clicked
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
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

                self.menu = QMenu(self.xmlTreeObject.mainwindow)
                if domElement.attribute(QString("type")) == QString("tool_file"):
                    self.menu.addAction(self.actExecToolFile)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actCloneTool)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("type")) == QString("tool_group"):
                    self.menu.addAction(self.actAddToolFile)
                elif domElement.attribute(QString("type")) == QString("param_template"):
                    self.menu.addAction(self.actAddRequiredStringParam)
                    self.menu.addAction(self.actAddRequiredDirParam)
                    self.menu.addAction(self.actAddRequiredFileParam)
                    self.menu.addAction(self.actAddOptionalStringParam)
                    self.menu.addAction(self.actAddOptionalDirParam)
                    self.menu.addAction(self.actAddOptionalFileParam)
                elif domElement.attribute(QString("type")) == QString("tool_config"):
                    self.menu.addAction(self.actExecToolConfig)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("type")) == QString("tool_sets"):
                    self.menu.addAction(self.actAddNewToolSet)
                elif domElement.attribute(QString("type")) == QString("tool_set"):
                    self.menu.addAction(self.actExecBatch)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actNewConfig)
                    self.menu.addAction(self.actCloneBatch)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("type")) == QString("documentation_path"):
                    self.menu.addAction(self.actOpenDocumentation)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actCloneNode)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)

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
                                (domElement.attribute(QString("type")) == QString("list")) or \
                                (domElement.attribute(QString("type")) == QString("tool_file")) or \
                                (domElement.attribute(QString("type")) == QString("tool_config")) or \
                                (domElement.attribute(QString("type")) == QString("tool_set")) or \
                                (domElement.attribute(QString("type")) == QString("param_template"))):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                    # Now add the export and import methods
                    self.menu.addSeparator()
                    self.menu.addAction(self.actExportXMLToFile)
                    self.menu.addAction(self.actImportXMLFromFile)
                    
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return

