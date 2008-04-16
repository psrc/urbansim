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
from opus_gui.config.datamanager.newdbconnection import NewDbConnectionGui
from opus_gui.config.managerbase.cloneinherited import CloneInheritedGui

class OpusXMLAction_DataDB(object):
    def __init__(self, parent):
        self.parent = parent
        self.mainwindow = parent.mainwindow
        self.xmlTreeObject = parent.xmlTreeObject

        self.currentColumn = None
        self.currentIndex = None

        self.acceptIcon = QIcon(":/Images/Images/accept.png")
        self.removeIcon = QIcon(":/Images/Images/delete.png")
        self.calendarIcon = QIcon(":/Images/Images/calendar_view_day.png")
        self.applicationIcon = QIcon(":/Images/Images/application_side_tree.png")

        self.actCloneDBConnection = QAction(self.calendarIcon,
                                        "Clone DB Connection",
                                        self.xmlTreeObject.parent)
        QObject.connect(self.actCloneDBConnection,
                        SIGNAL("triggered()"),
                        self.cloneDBConnection)

        self.actNewDBConnection = QAction(self.calendarIcon,
                                          "New DB Connection",
                                          self.xmlTreeObject.parent)
        QObject.connect(self.actNewDBConnection,
                        SIGNAL("triggered()"),
                        self.newDBConnection)

        self.actTestDBConnection = QAction(self.calendarIcon,
                                           "Test DB Connection",
                                           self.xmlTreeObject.parent)
        QObject.connect(self.actTestDBConnection,
                        SIGNAL("triggered()"),
                        self.testDBConnection)

        self.actPlaceHolder = QAction(self.applicationIcon,
                                      "Placeholder",
                                      self.xmlTreeObject.parent)
        QObject.connect(self.actPlaceHolder,
                        SIGNAL("triggered()"),
                        self.placeHolderAction)

        self.actRemoveNode = QAction(self.removeIcon,
                                     "Remove Node",
                                     self.xmlTreeObject.parent)
        QObject.connect(self.actRemoveNode,
                        SIGNAL("triggered()"),
                        self.removeNode)

        self.actCloneNode = QAction(self.applicationIcon,
                                    "Clone Down To Child",
                                    self.xmlTreeObject.parent)
        QObject.connect(self.actCloneNode,
                        SIGNAL("triggered()"),
                        self.cloneNodeAction)

    def newDBConnection(self):
        print "newDBConnection pressed"
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = NewDbConnectionGui(self,flags)
        window.show()
        #
        #newNode1 = self.currentIndex.model().domDocument.createElement(QString("new_connection"))
        #newNode1.setAttribute(QString("type"),QString("db_connection"))
        #
        #newNode2 = self.currentIndex.model().domDocument.createElement(QString("host_name"))
        #newNode2.setAttribute(QString("type"),QString("string"))
        #newText = self.currentIndex.model().domDocument.createTextNode(QString(""))
        #newNode2.appendChild(newText)
        #
        #newNode3 = self.currentIndex.model().domDocument.createElement(QString("protocol"))
        #newNode3.setAttribute(QString("type"),QString("string"))
        #newText = self.currentIndex.model().domDocument.createTextNode(QString(""))
        #newNode3.appendChild(newText)
        #
        #newNode4 = self.currentIndex.model().domDocument.createElement(QString("user_name"))
        #newNode4.setAttribute(QString("type"),QString("string"))
        #newText = self.currentIndex.model().domDocument.createTextNode(QString(""))
        #newNode4.appendChild(newText)
        #
        #newNode5 = self.currentIndex.model().domDocument.createElement(QString("password"))
        #newNode5.setAttribute(QString("type"),QString("password"))
        #newText = self.currentIndex.model().domDocument.createTextNode(QString(""))
        #newNode5.appendChild(newText)
        #
        #newNode1.appendChild(newNode2)
        #newNode1.appendChild(newNode3)
        #newNode1.appendChild(newNode4)
        #newNode1.appendChild(newNode5)
        #self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(self.currentIndex),
        #                                    self.currentIndex,
        #                                    newNode1)
        #self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneDBConnection(self):
        print "cloneDBConnection pressed"
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        parent = self.currentIndex.model().parent(self.currentIndex)
        self.currentIndex.model().insertRow(self.currentIndex.model().rowCount(parent),
                                            parent,
                                            clone)
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def testDBConnection(self):
        print "testDBConnection pressed - Not yet implemented"

    def placeHolderAction(self):
        print "Placeholder pressed"

    def removeNode(self):
        #print "Remove Node Pressed"
        self.currentIndex.model().removeRow(self.currentIndex.internalPointer().row(),
                                            self.currentIndex.model().parent(self.currentIndex))
        self.currentIndex.model().emit(SIGNAL("layoutChanged()"))

    def cloneNodeAction(self):
        print "Clone Node pressed..."
        clone = self.currentIndex.internalPointer().domNode.cloneNode()
        flags = Qt.WindowTitleHint | Qt.WindowSystemMenuHint | Qt.WindowMaximizeButtonHint
        window = CloneInheritedGui(self,flags,self.xmlTreeObject.model,clone)
        window.show()

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
                if domElement.hasAttribute(QString("inherited")) and \
                       domElement.hasAttribute(QString("cloneable")) and \
                       domElement.attribute(QString("cloneable")) == QString("True"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actCloneNode)
                    self.menu.exec_(QCursor.pos())
                elif domElement.attribute(QString("type")) == QString("database_library"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actNewDBConnection)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
                    self.menu.exec_(QCursor.pos())
                elif domElement.attribute(QString("type")) == QString("db_connection"):
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actCloneDBConnection)
                    self.menu.addAction(self.actTestDBConnection)
                    self.menu.addSeparator()
                    self.menu.addAction(self.actRemoveNode)
                    self.menu.exec_(QCursor.pos())
                else:
                    self.menu = QMenu(self.xmlTreeObject.parent)
                    self.menu.addAction(self.actRemoveNode)
                    self.menu.exec_(QCursor.pos())
        return

