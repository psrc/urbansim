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
from opus_gui.run.script.opusrunscript import *


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
                classificationindex = tree.model.findElementIndexByType("classification",dbindex)
                classificationindexElement = None
                classificationtext = ""
                if classificationindex[0].isValid():
                    classificationindexElement = classificationindex[0].internalPointer()
                    if classificationindexElement.node().hasChildNodes():
                        children = classificationindexElement.node().childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                classificationtext = children.item(x).nodeValue()
                dbindexElement = dbindex.internalPointer()
                tagName = dbindexElement.domNode.toElement().tagName()
                if classificationtext != "" and classificationtext == classification:
                    choices.append(tagName)
        return choices
    
    def dataActionMenuFunction(self,action):
        filename = self.xmlFileObject.model.filePath(self.currentIndex)
        actiontext = action.text()
        # print "%s - %s" % (filename,actiontext)
        QObject.disconnect(self.menu, SIGNAL("triggered(QAction*)"),self.dataActionMenuFunction)
        
        # Add in the code to take action... like run a script...
        # First find the batch to loop over the configs to execute
        tree = self.xmlFileObject.mainwindow.toolboxStuff.dataManagerTree
        scriptxml = tree.model.index(0,0,QModelIndex()).parent()
        scriptindexlist = tree.model.findElementIndexByName(actiontext,scriptxml,False)
        scriptindex = scriptindexlist[0]
        if scriptindex.isValid():
            # print scriptindex.internalPointer().node().toElement().tagName()
            # We have the script_batch... time to loop over the children and get the configs
            configindexlist = tree.model.findElementIndexByType("script_config",scriptindex,True)
            # print len(configindexlist)
            for configindex in configindexlist:
                if configindex.isValid():
                    # Now for each config index we need to run the scripts
                    # Now find the script that this config refers to...
                    configNode = configindex.internalPointer().node().toElement()
                    script_hook = configNode.elementsByTagName(QString("script_hook")).item(0)
                    script_name = QString("")
                    if script_hook.hasChildNodes():
                        children = script_hook.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                script_name = children.item(x).nodeValue()
                    # This will be in the script_library
                    library = configindex.model().xmlRoot.toElement().elementsByTagName(QString("script_library")).item(0)
                    script_path = library.toElement().elementsByTagName("script_path").item(0)
                    script = library.toElement().elementsByTagName(script_name).item(0)
                    
                    # First find the script path text...
                    if script_path.hasChildNodes():
                        children = script_path.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                scriptPath = children.item(x).nodeValue()
                    if script.hasChildNodes():
                        children = script.childNodes()
                        for x in xrange(0,children.count(),1):
                            if children.item(x).isText():
                                filePath = children.item(x).nodeValue()
                    importPath = QString(scriptPath).append(QString(".")).append(QString(filePath))
                    # print "New import ", importPath
                    
                    # Now loop and build up the parameters...
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
                        if thisElement.toElement().tagName() == QString("path"):
                            thisElementText = filename
                        if thisElement.toElement().tagName() != QString("script_hook"):
                            params[thisElement.toElement().tagName()] = thisElementText
                    x = OpusScript(self.xmlFileObject.mainwindow,importPath,params)
                    y = RunScriptThread(self.xmlFileObject.mainwindow,x)
                    y.run()
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
