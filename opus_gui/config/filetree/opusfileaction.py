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


class OpusFileAction(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlFileObject = parent
        
        self.currentColumn = None
        self.currentIndex = None
        
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        
        self.actPlaceHolder = QAction(self.applicationIcon, "Placeholder",
                                      self.xmlFileObject.mainwindow)
        QObject.connect(self.actPlaceHolder, SIGNAL("triggered()"),
                        self.placeHolderAction)

        self.actOpenTextFile = QAction(self.applicationIcon, "Open Text File",
                                       self.xmlFileObject.mainwindow)
        QObject.connect(self.actOpenTextFile, SIGNAL("triggered()"),
                        self.openTextFile)
        
        QObject.connect(self.xmlFileObject.treeview,
                        SIGNAL("customContextMenuRequested(const QPoint &)"),
                        self.processCustomMenu)
        
    def placeHolderAction(self):
        print "placeHolderAction pressed with column = %s" % \
              (self.currentColumn)
        
    def openTextFile(self):
        print "openTextFile pressed with column = %s and item = %s" % \
              (self.currentColumn, self.xmlFileObject.model.filePath(self.currentIndex))
        if self.xmlFileObject.mainwindow.editorStuff:
            print "Loading into qscintilla..."
            filename = self.xmlFileObject.model.filePath(self.currentIndex)
            self.xmlFileObject.mainwindow.editorStuff.clear()
            try:
                f = open(filename,'r')
            except:
                return
            for l in f.readlines():
                self.xmlFileObject.mainwindow.editorStuff.append(l)
            f.close()
            self.xmlFileObject.mainwindow.editorStatusLabel.setText(QString(filename))

    def fillInAvailableScripts(self):
        #print "Checking for scripts"
        choices = []
        classification = ""
        if self.xmlFileObject.model.isDir(self.currentIndex):
            regex = QRegExp("\\d{4}")
            name = self.xmlFileObject.model.fileName(self.currentIndex)
            parentname = self.xmlFileObject.model.fileName(self.xmlFileObject.model.parent(self.currentIndex))
            isdir = self.xmlFileObject.model.isDir(self.currentIndex)
            parentisdir = self.xmlFileObject.model.isDir(self.xmlFileObject.model.parent(self.currentIndex))
            # print "%s %s %s %s" % (name, parentname,isdir,parentisdir)
            if isdir and regex.exactMatch(name):
                # We have a database dir
                # print "Database Dir"
                classification = "database"
            elif parentisdir and regex.exactMatch(parentname):
                # We have a dataset
                # print "Dataset Dir"
                classification = "dataset"
        else:
            regex = QRegExp("\\d{4}")
            model = self.xmlFileObject.model
            parentIndex = model.parent(self.currentIndex)
            parentparentIndex = model.parent(parentIndex)
            parentparentname = model.fileName(parentparentIndex)
            parentparentisdir = model.isDir(parentparentIndex)
            if parentparentisdir and regex.exactMatch(parentparentname):
                # We have a file with a parentparent which is a database classification
                classification = "array"
        tree = self.xmlFileObject.mainwindow.toolboxStuff.dataManagerTree
        dbxml = tree.model.index(0,0,QModelIndex()).parent()
        dbindexlist = tree.model.findElementIndexByType("script_batch",dbxml,True)
        for dbindex in dbindexlist:
            if dbindex.isValid():
                indexElement = dbindex.internalPointer()
                tagName = indexElement.domNode.toElement().tagName()
                xmlclassification = ""
                if indexElement.domNode.toElement().hasAttribute(QString("classification")):
                    xmlclassification = str(indexElement.domNode.toElement().attribute(QString("classification")))
                # print "%s - %s" % (xmlclassification,tagName)
                if xmlclassification != "" and xmlclassification == classification:
                    choices.append(tagName)
        return choices
    
    def dataActionMenuFunction(self,action):
        filename = self.xmlFileObject.model.filePath(self.currentIndex)
        actiontext = action.text()
        print "%s - %s" % (filename,actiontext)
        QObject.disconnect(self.menu, SIGNAL("triggered(QAction*)"),self.dataActionMenuFunction)
        
        # Add in the code to take action... like run a script...
        return
    
    def processCustomMenu(self, position):
        self.currentColumn = self.xmlFileObject.treeview.indexAt(position).column()
        self.currentIndex = self.xmlFileObject.treeview.indexAt(position)
        if self.xmlFileObject.model.fileInfo(self.currentIndex).suffix() == "txt":
            self.menu = QMenu(self.xmlFileObject.mainwindow)
            self.menu.addAction(self.actOpenTextFile)
            self.menu.exec_(QCursor.pos())
        else:
            # Do stuff for directories
            choices = self.fillInAvailableScripts()
            if len(choices) > 0:
                self.menu = QMenu(self.xmlFileObject.mainwindow)
                self.dynactions = []
                for i,choice in enumerate(choices):
                    # Add choices with custom text...
                    dynaction = QAction(self.applicationIcon, choice, self.xmlFileObject.mainwindow)
                    self.dynactions.append(dynaction)
                    self.menu.addAction(dynaction)
                QObject.connect(self.menu, SIGNAL("triggered(QAction*)"),
                                self.dataActionMenuFunction)
                self.menu.exec_(QCursor.pos())
