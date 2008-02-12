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

from run.model.opusrunmodel import OpusModel

class OpusXMLAction_Scenario(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlTreeObject = parent.xmlTreeObject
        
        self.currentColumn = None
        self.currentIndex = None
        
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        
        self.actRunModel = QAction(self.acceptIcon,
                                   "Run This Model",
                                   self.xmlTreeObject.parent)
        QObject.connect(self.actRunModel,
                        SIGNAL("triggered()"),
                        self.runModel)
        
        self.actRemoveTree = QAction(self.removeIcon,
                                     "Remove this tree from the GUI",
                                     self.xmlTreeObject.parent)
        QObject.connect(self.actRemoveTree,
                        SIGNAL("triggered()"),
                        self.removeTree)
        
        self.actOpenXMLFile = QAction(self.calendarIcon,
                                      "Open XML File",
                                      self.xmlTreeObject.parent)
        QObject.connect(self.actOpenXMLFile,
                        SIGNAL("triggered()"),
                        self.openXMLFile)
        
        self.actEditXMLFileGlobal = QAction(self.calendarIcon,
                                            "Edit XML File Global",
                                            self.xmlTreeObject.parent)
        QObject.connect(self.actEditXMLFileGlobal,
                        SIGNAL("triggered()"),
                        self.editXMLFileGlobal)
        
        self.actEditXMLFileLocal = QAction(self.calendarIcon,
                                           "Edit XML File Local",
                                           self.xmlTreeObject.parent)
        QObject.connect(self.actEditXMLFileLocal,
                        SIGNAL("triggered()"),
                        self.editXMLFileLocal)
        
        self.actPlaceHolder = QAction(self.applicationIcon,
                                      "Placeholder",
                                      self.xmlTreeObject.parent)
        QObject.connect(self.actPlaceHolder,
                        SIGNAL("triggered()"),
                        self.placeHolderAction)
        
        
    def runModel(self):
        # If the XML is not dirty we can go ahead and run... else prompt for saving
        if not self.xmlTreeObject.model.dirty:
            modelToRun = self.currentIndex.internalPointer().node().nodeName()
            # Add the model to the run Q
            newModel = OpusModel(self.xmlTreeObject,
                                 self.xmlTreeObject.parentTool.xml_file,
                                 modelToRun)
            self.xmlTreeObject.parent.runManagerStuff.addNewModelRun(newModel)
        else:
            # Prompt the user to save...
            QMessageBox.warning(self.xmlTreeObject.parent,
                                "Warning",
                                "Please save changes to project before running model")
      
    def removeTree(self):
        if not self.xmlTreeObject.model.dirty:
            self.xmlTreeObject.groupBox.hide()
            self.xmlTreeObject.parentWidget.removeWidget(self.xmlTreeObject.groupBox)
            return True
        else:
            return False
    
    def openXMLFile(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.xmlTreeObject.parentTool.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))
        #print "Test - ", newFile.absoluteFilePath()
        self.xmlTreeObject.parentTool.openXMLTree(newFile.absoluteFilePath())

    
    def editXMLFileLocal(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.xmlTreeObject.parentTool.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))

        # To test QScintilla
        if self.xmlTreeObject.parent.editorStuff:
            #print "Loading into qscintilla..."
            # Now an individual tab
            import util.editorbase
            fileName = newFile.absoluteFilePath()
            x = util.editorbase.EditorTab(self.xmlTreeObject.parent, QString(fileName))
    
    def editXMLFileGlobal(self):
        filePath = ""
        if self.currentIndex.internalPointer().node().hasChildNodes():
            children = self.currentIndex.internalPointer().node().childNodes()
            for x in xrange(0,children.count(),1):
                if children.item(x).isText():
                    filePath = children.item(x).nodeValue()
        fileInfo = QFileInfo(filePath)
        baseInfo = QFileInfo(self.xmlTreeObject.parentTool.xml_file)
        baseDir = baseInfo.absolutePath()
        newFile = QFileInfo(QString(baseDir).append("/").append(QString(fileInfo.filePath())))

        # To test QScintilla
        if self.xmlTreeObject.parent.editorStuff:
            #print "Loading into qscintilla..."
            # Start with the base tab
            fileName = newFile.absoluteFilePath()
            self.xmlTreeObject.parent.editorStuff.clear()
            try:
                f = open(fileName,'r')
            except:
                return
            for l in f.readlines():
                self.xmlTreeObject.parent.editorStuff.append(l)
            f.close()
            self.xmlTreeObject.parent.editorStatusLabel.setText(QString(fileName))

    def placeHolderAction(self):
        pass
    
    def processCustomMenu(self, position):
        if self.xmlTreeObject.view.indexAt(position).isValid() and \
               self.xmlTreeObject.view.indexAt(position).column() == 0:
            self.currentColumn = self.xmlTreeObject.view.indexAt(position).column()
            self.currentIndex = self.xmlTreeObject.view.indexAt(position)
            item = self.currentIndex.internalPointer()
            domNode = item.node()
            if domNode.isNull():
                return
            # Handle ElementNodes
            if domNode.isElement():
                domElement = domNode.toElement()
                if domElement.isNull():
                    return
                if domElement.attribute(QString("executable")) == QString("True"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actRunModel)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveTree)
                    self.menu.exec_(QCursor.pos())
                elif domElement.attribute(QString("type")) == QString("file"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actOpenXMLFile)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actEditXMLFileGlobal)
                    self.menu.addAction(self.actEditXMLFileLocal)
                    self.menu.exec_(QCursor.pos())
                else:
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actPlaceHolder)
                    self.menu.exec_(QCursor.pos())
        return
    
    
