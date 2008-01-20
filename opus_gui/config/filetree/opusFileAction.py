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
        
        self.actPlaceHolder = QAction(self.applicationIcon, "Placeholder", self.xmlFileObject.mainwindow)
        QObject.connect(self.actPlaceHolder, SIGNAL("triggered()"), self.placeHolderAction)

        self.actOpenTextFile = QAction(self.applicationIcon, "Open Text File", self.xmlFileObject.mainwindow)
        QObject.connect(self.actOpenTextFile, SIGNAL("triggered()"), self.openTextFile)
        
        QObject.connect(self.xmlFileObject.treeview, SIGNAL("customContextMenuRequested(const QPoint &)"),
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

    def processCustomMenu(self, position):
        self.currentColumn = self.xmlFileObject.treeview.indexAt(position).column()
        self.currentIndex = self.xmlFileObject.treeview.indexAt(position)
        if self.xmlFileObject.model.isDir(self.currentIndex):
            # Do stuff for directories
            pass
        elif self.xmlFileObject.model.fileInfo(self.currentIndex).suffix() == "txt":
            self.menu = QMenu(self.xmlFileObject.mainwindow)
            self.menu.addAction(self.actOpenTextFile)
            self.menu.exec_(QCursor.pos())
        else:
            # got something we werent expecting... just return with no menu
            self.menu = QMenu(self.xmlFileObject.mainwindow)
            self.menu.addAction(self.actPlaceHolder)
            self.menu.exec_(QCursor.pos())
