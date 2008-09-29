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
from PyQt4.QtCore import QString, QModelIndex
from PyQt4.QtGui import QTreeView

class XmlView(QTreeView):
    def __init__(self, mainwindow):
        QTreeView.__init__(self, mainwindow)
        self.mainwindow = mainwindow

    def openDefaultItems(self):
        # Loop through all the data model items displayed and expand
        # if they are marked to be expanded by default
        model = self.model()
        self.loopItems(model,model.index(0,0,QModelIndex()).parent())

    def loopItems(self,model,parentIndex):
        rows = model.rowCount(parentIndex)
        for x in xrange(0,rows,1):
            child = model.index(x,0,parentIndex)
            childElement = child.internalPointer().domNode.toElement()
            if not childElement.isNull():
                # If this child needs to be expanded we do it
                if childElement.hasAttribute(QString("setexpanded")) and \
                       childElement.attribute(QString("setexpanded")) == QString("True"):
                    self.expand(child)
                # If this child has other children then we recurse
                if model.rowCount(child)>0:
                    self.loopItems(model,child)

