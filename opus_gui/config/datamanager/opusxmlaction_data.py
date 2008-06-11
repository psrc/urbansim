# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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
from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui
from opus_gui.config.managerbase.clonenode import CloneNodeGui

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
        
#        self.actExecToolFile = QAction(self.calendarIcon,
#                                         "Exec Tool (TESTING)",
#                                         self.xmlTreeObject.mainwindow)
#        QObject.connect(self.actExecToolFile,
#                        SIGNAL("triggered()"),
#                        self.execToolFile)

        self.actExecToolConfig = QAction(self.executeIcon,
                                           "Execute Tool",
                                           self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecToolConfig,
                        SIGNAL("triggered()"),
                        self.execToolConfig)

        self.actAddToolFile = QAction(self.addIcon,
                                        "Add Tool to Library",
                                        self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddToolFile,
                        SIGNAL("triggered()"),
                        self.addToolFile)

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
                                     "Remove Node",
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

        self.actMakeEditable = QAction(self.applicationIcon,
                                       "Make Editable",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actCloneNode = QAction(self.calendarIcon,
                                    "Copy Node",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)


    def addToolFile(self):
        #print "Add Tool Pressed"
        newNode = self.currentIndex.model().domDocument.createElement(QString("<add valid tool name here, e.g. processing_tool>"))
        newNode.setAttribute(QString("type"),QString("tool_file"))
        newText = self.currentIndex.model().domDocument.createTextNode(QString("<add python module name here, without .py>"))
        newNode.appendChild(newText)
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def newConfig(self):
        #print "newConfig Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = ConfigureToolGui(self,flags)
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
        # First find the tool path...
        toolPath = ""
        if self.currentIndex.internalPointer().parent().node().hasChildNodes():
            children = self.currentIndex.internalPointer().parent().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isElement():
                    domElement = children.item(x).toElement()
                    if not domElement.isNull():
                        if domElement.tagName() == QString("tool_path"):
                            if domElement.hasChildNodes():
                                children2 = domElement.childNodes()
                                for x2 in xrange(0,children2.count(),1):
                                    if children2.item(x2).isText():
                                        toolPath = children2.item(x2).nodeValue()
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        importPath = QString(toolPath).append(QString(".")).append(QString(filePath))
        print "New import ", importPath
        x = OpusTool(self.xmlTreeObject.mainwindow,importPath,{'param1':'val1','param2':'val2'})
        y = RunToolThread(self.xmlTreeObject.mainwindow,x)
        y.run()

    def execToolConfigGen(self,configNode,library):
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

        x = OpusTool(self.xmlTreeObject.mainwindow,importPath,params)
        y = RunToolThread(self.xmlTreeObject.mainwindow,x)
        y.run()

    def execToolConfig(self):
        # First find the tool that this config refers to...
        configNode = self.currentIndex.internalPointer().node().toElement()
        library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        self.execToolConfigGen(configNode,library)
        
    def execBatch(self):
        #print "Execute batch pressed..."
        batchNode = self.currentIndex.internalPointer().node().toElement()
        library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("Tool_Library")).item(0)
        childNodes = batchNode.childNodes()
        for x in xrange(0,childNodes.count(),1):
            thisNode = childNodes.item(x)
            if thisNode.isElement():
                thisElement = thisNode.toElement()
                if thisElement.hasAttribute(QString("type")) and \
                       (thisElement.attribute(QString("type")) == QString("tool_config")):
                    self.execToolConfigGen(thisElement,library)

    def cloneNode(self):
        #print "cloneNode Pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parentIndex = self.currentIndex.model().parent(self.currentIndex)
        model = self.currentIndex.model()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneNodeGui(self,flags,clone,parentIndex,model)
        window.show()

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def makeEditableAction(self):
        thisNode = self.currentIndex.internalPointer().node()
        # Strip the inherited attribute down the tree
        self.currentIndex.model().stripAttributeDown('inherited',thisNode)
        # Now up the tree, only hitting parent nodes and not sibblings
        self.currentIndex.model().stripAttributeUp('inherited',thisNode)
        # Finally we refresh the tree to indicate that there has been a change
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    #################### Old methods not currently used ###################
    def cloneNodeAction(self):
        print "Clone Node pressed..."
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneInheritedGui(self,flags,self.xmlTreeObject.model,clone)
        window.show()

    ##################################################3####################


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
#                    self.menu.addAction(self.actExecToolFile)
                    self.menu.addSeparator()
                    #self.menu.addAction(self.actNewConfig)
                    self.menu.addAction(self.actCloneTool)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
                elif domElement.attribute(QString("type")) == QString("tool_library"):
                    self.menu.addAction(self.actAddToolFile)
                elif domElement.attribute(QString("type")) == QString("tool_config"):
                    self.menu.addAction(self.actExecToolConfig)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
                elif domElement.attribute(QString("type")) == QString("tool_set"):
                    self.menu.addAction(self.actExecBatch)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actNewConfig)
                    self.menu.addAction(self.actCloneBatch)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
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
                        if parentElement and (not parentElement.isNull()) and \
                               parentElement.hasAttribute(QString("type")) and \
                               ((parentElement.attribute(QString("type")) == QString("dictionary")) or \
                                (parentElement.attribute(QString("type")) == QString("selectable_list")) or \
                                (parentElement.attribute(QString("type")) == QString("list"))):
                            self.menu.addSeparator()
                            self.menu.addAction(self.actRemoveNode)
                # Check if the menu has any elements before exec is called
                if not self.menu.isEmpty():
                    self.menu.exec_(QCursor.pos())
        return

