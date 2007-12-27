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

from run.opusRunScript import *


class OpusXMLAction_Data(object):
    def __init__(self, parent):
        self.parent = parent
        self.xmlTreeObject = parent.xmlTreeObject
        
        self.currentColumn = None
        self.currentIndex = None
        
        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")
        
        self.actExecScriptFile = QAction(self.calendarIcon, "Exec Script", self.xmlTreeObject.parent)
        QObject.connect(self.actExecScriptFile, SIGNAL("triggered()"), self.execScriptFile)

        self.actPlaceHolder = QAction(self.applicationIcon, "Placeholder", self.xmlTreeObject.parent)
        QObject.connect(self.actPlaceHolder, SIGNAL("triggered()"), self.placeHolderAction)
        

    def execScriptFile(self):
        print "Exec Script Pressed"
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
        x = OpusScript(self.xmlTreeObject.parent,importPath)
        y = RunScriptThread(self.xmlTreeObject.parent,x)
        y.run()

    def placeHolderAction(self):
        print "placeHolderAction pressed with column = %s and item = %s" % \
              (self.currentColumn, self.currentIndex.internalPointer().node().toElement().tagName())
    
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
                if domElement.attribute(QString("type")) == QString("script_file"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actExecScriptFile)
                    self.menu.exec_(QCursor.pos())
                else:
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actPlaceHolder)
                    self.menu.exec_(QCursor.pos())
        return

