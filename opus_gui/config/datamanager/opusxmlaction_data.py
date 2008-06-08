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

from opus_gui.run.script.opusrunscript import *
import opus_gui.util.documentationbase
from opus_gui.config.datamanager.configurescript import ConfigureScriptGui
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

        self.actExecScriptFile = QAction(self.calendarIcon,
                                         "Exec Script (TESTING)",
                                         self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecScriptFile,
                        SIGNAL("triggered()"),
                        self.execScriptFile)

        self.actExecScriptConfig = QAction(self.calendarIcon,
                                           "Execute Script",
                                           self.xmlTreeObject.mainwindow)
        QObject.connect(self.actExecScriptConfig,
                        SIGNAL("triggered()"),
                        self.execScriptConfig)

        self.actAddScriptFile = QAction(self.calendarIcon,
                                        "Add Script",
                                        self.xmlTreeObject.mainwindow)
        QObject.connect(self.actAddScriptFile,
                        SIGNAL("triggered()"),
                        self.addScriptFile)

        self.actNewConfig = QAction(self.calendarIcon,
                                     "Create New Config (TESTING)",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actNewConfig,
                        SIGNAL("triggered()"),
                        self.newConfig)

        self.actCloneBatch = QAction(self.calendarIcon,
                                     "Clone Batch",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneBatch,
                        SIGNAL("triggered()"),
                        self.cloneNode)

        self.actCloneScript = QAction(self.calendarIcon,
                                      "Clone Script",
                                      self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneScript,
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

        self.actMoveNodeUp = QAction(self.calendarIcon,
                                     "Move Up",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMoveNodeUp,
                        SIGNAL("triggered()"),
                        self.moveNodeUp)

        self.actMoveNodeDown = QAction(self.calendarIcon,
                                       "Move Down",
                                       self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMoveNodeDown,
                        SIGNAL("triggered()"),
                        self.moveNodeDown)

        #jesse testing
        self.actExecBatch = QAction(self.applicationIcon,
                                      "Execute batch",
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


    def addScriptFile(self):
        #print "Add Script Pressed"
        newNode = self.currentIndex.model().domDocument.createElement(QString("processing_script"))
        newNode.setAttribute(QString("type"),QString("script_file"))
        newText = self.currentIndex.model().domDocument.createTextNode(QString("script name here"))
        newNode.appendChild(newText)
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
                                            self.currentIndex,
                                            newNode)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def newConfig(self):
        #print "newConfig Pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = ConfigureScriptGui(self,flags)
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


    def execScriptFile(self):
        #print "Exec Script Pressed"
        # First find the script path...
        scriptPath = ""
        if self.currentIndex.internalPointer().parent().node().hasChildNodes():
            children = self.currentIndex.internalPointer().parent().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isElement():
                    domElement = children.item(x).toElement()
                    if not domElement.isNull():
                        if domElement.tagName() == QString("script_path"):
                            if domElement.hasChildNodes():
                                children2 = domElement.childNodes()
                                for x2 in xrange(0,children2.count(),1):
                                    if children2.item(x2).isText():
                                        scriptPath = children2.item(x2).nodeValue()
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        importPath = QString(scriptPath).append(QString(".")).append(QString(filePath))
        print "New import ", importPath
        x = OpusScript(self.xmlTreeObject.mainwindow,importPath,{'param1':'val1','param2':'val2'})
        y = RunScriptThread(self.xmlTreeObject.mainwindow,x)
        y.run()

    def execScriptConfigGen(self,configNode,library):
        script_hook = configNode.elementsByTagName(QString("script_hook")).item(0)
        script_name = QString("")
        if script_hook.hasChildNodes():
            children = script_hook.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    script_name = children.item(x).nodeValue()
        # This will be in the script_library
        script_path = library.toElement().elementsByTagName("script_path").item(0)
        script_file = library.toElement().elementsByTagName(script_name).item(0)
        
        # First find the script path text...
        if script_path.hasChildNodes():
            children = script_path.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    scriptPath = children.item(x).nodeValue()
        # Next if the script_file has a script_name we grab it
        if script_file.hasChildNodes():
            children = script_file.childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isElement():
                    thisElement = children.item(x).toElement()
                    if thisElement.hasAttribute(QString("type")) and \
                           (thisElement.attribute(QString("type")) == QString("script_name")):
                        if thisElement.hasChildNodes():
                            children2 = thisElement.childNodes()
                            for x2 in xrange(0,children2.count(),1):
                                if children2.item(x2).isText():
                                    filePath = children2.item(x2).nodeValue()
        importPath = QString(scriptPath).append(QString(".")).append(QString(filePath))
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

        x = OpusScript(self.xmlTreeObject.mainwindow,importPath,params)
        y = RunScriptThread(self.xmlTreeObject.mainwindow,x)
        y.run()

    def execScriptConfig(self):
        # First find the script that this config refers to...
        configNode = self.currentIndex.internalPointer().node().toElement()
        library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("script_library")).item(0)
        self.execScriptConfigGen(configNode,library)
        
    def execBatch(self):
        #print "Execute batch pressed..."
        batchNode = self.currentIndex.internalPointer().node().toElement()
        library = self.currentIndex.model().xmlRoot.toElement().elementsByTagName(QString("script_library")).item(0)
        childNodes = batchNode.childNodes()
        for x in xrange(0,childNodes.count(),1):
            thisNode = childNodes.item(x)
            if thisNode.isElement():
                thisElement = thisNode.toElement()
                if thisElement.hasAttribute(QString("type")) and \
                       (thisElement.attribute(QString("type")) == QString("script_config")):
                    self.execScriptConfigGen(thisElement,library)

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
                if domElement.attribute(QString("type")) == QString("script_file"):
                    self.menu.addAction(self.actExecScriptFile)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actNewConfig)
                    self.menu.addAction(self.actCloneScript)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                elif domElement.attribute(QString("type")) == QString("script_library"):
                    self.menu.addAction(self.actAddScriptFile)
                elif domElement.attribute(QString("type")) == QString("script_config"):
                    self.menu.addAction(self.actExecScriptConfig)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actMoveNodeUp)
                    self.menu.addAction(self.actMoveNodeDown)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
                elif domElement.attribute(QString("type")) == QString("script_batch"):
                    #jesse testing
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

