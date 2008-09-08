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

from opus_gui.run.model.opusrunmodel import OpusModel
from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui
from opus_gui.config.managerbase.clonenode import CloneNodeGui

class OpusXMLAction_Scenario(object):
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
        self.cloneIcon = QIcon(":/Images/Images/application_double.png")
        self.makeEditableIcon = QIcon(":/Images/Images/application_edit.png")

        self.actRunModel = QAction(self.acceptIcon,
                                   "Run This Scenario",
                                   self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRunModel,
                        SIGNAL("triggered()"),
                        self.runModel)

        self.actOpenXMLFile = QAction(self.calendarIcon,
                                      "Open XML File",
                                      self.xmlTreeObject.mainwindow)
        QObject.connect(self.actOpenXMLFile,
                        SIGNAL("triggered()"),
                        self.openXMLFile)

        self.actEditXMLFileGlobal = QAction(self.calendarIcon,
                                            "Edit XML File Global",
                                            self.xmlTreeObject.mainwindow)
        QObject.connect(self.actEditXMLFileGlobal,
                        SIGNAL("triggered()"),
                        self.editXMLFileGlobal)

        self.actEditXMLFileLocal = QAction(self.calendarIcon,
                                           "Edit XML File Local",
                                           self.xmlTreeObject.mainwindow)
        QObject.connect(self.actEditXMLFileLocal,
                        SIGNAL("triggered()"),
                        self.editXMLFileLocal)

        self.actMakeEditable = QAction(self.makeEditableIcon,
                                    "Add to current project",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actMakeEditable,
                        SIGNAL("triggered()"),
                        self.makeEditableAction)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove node from current project",
                                     self.xmlTreeObject.mainwindow)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actCloneNode = QAction(self.cloneIcon,
                                    "Copy Node",
                                    self.xmlTreeObject.mainwindow)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNode)


    def checkIsDirty(self):
        if (self.xmlTreeObject.toolboxbase.resultsManagerTree and self.xmlTreeObject.toolboxbase.resultsManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.modelManagerTree and self.xmlTreeObject.toolboxbase.modelManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.runManagerTree and self.xmlTreeObject.toolboxbase.runManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.dataManagerTree and self.xmlTreeObject.toolboxbase.dataManagerTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.dataManagerDBSTree and self.xmlTreeObject.toolboxbase.dataManagerDBSTree.model.isDirty()) or \
               (self.xmlTreeObject.toolboxbase.generalManagerTree and self.xmlTreeObject.toolboxbase.generalManagerTree.model.isDirty()):
            return True
        else:
            return False

    def runModel(self):
        # Update the XMLConfiguration copy of the XML tree before running the model
        self.xmlTreeObject.toolboxbase.updateOpusXMLTree()
        modelToRun = self.currentIndex.internalPointer().node().nodeName()
        # Add the model to the run Q
        newModel = OpusModel(self.xmlTreeObject,
                             self.xmlTreeObject.toolboxbase.xml_file,
                             modelToRun)
        self.xmlTreeObject.mainwindow.runManagerStuff.addNewModelRun(newModel)

    def openXMLFile(self):
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
        #print "Test - ", newFile.absoluteFilePath()
        self.xmlTreeObject.toolboxbase.openXMLTree(newFile.absoluteFilePath())


    def editXMLFileLocal(self):
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

        # To test QScintilla
        if self.xmlTreeObject.mainwindow.editorStuff:
            #print "Loading into qscintilla..."
            # Now an individual tab
            import opus_gui.util.editorbase
            fileName = newFile.absoluteFilePath()
            x = util.editorbase.EditorTab(self.xmlTreeObject.mainwindow, QString(fileName))

    def editXMLFileGlobal(self):
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

        # To test QScintilla
        if self.xmlTreeObject.mainwindow.editorStuff:
            #print "Loading into qscintilla..."
            # Start with the base tab
            fileName = newFile.absoluteFilePath()
            self.xmlTreeObject.mainwindow.editorStuff.clear()
            try:
                f = open(fileName,'r')
            except:
                return
            for l in f.readlines():
                self.xmlTreeObject.mainwindow.editorStuff.append(l)
            f.close()
            self.xmlTreeObject.mainwindow.editorStatusLabel.setText(QString(fileName))

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
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
                if domElement.attribute(QString("executable")) == QString("True"):
                    self.menu.addAction(self.actRunModel)
                elif domElement.attribute(QString("type")) == QString("file"):
                    self.menu.addAction(self.actOpenXMLFile)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actEditXMLFileGlobal)
                    self.menu.addAction(self.actEditXMLFileLocal)

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


