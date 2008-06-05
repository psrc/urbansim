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
from PyQt4.Qsci import *

# General system includes
import sys,string


# Main 
class EditorBase(QsciScintilla):
    def __init__(self, mainwindow):
        QsciScintilla.__init__(self, mainwindow)
        self.mainwindow = mainwindow

class EditorTab(object):
    def __init__(self, mainwindow, filePath):
        self.mainwindow = mainwindow

        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "Editor Dyn Tab"

        self.tab = QWidget(self.mainwindow)

        self.widgetLayout = QVBoxLayout(self.tab)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.editorStatusLabel = QLabel(self.tab)
        self.editorStatusLabel.setAlignment(Qt.AlignCenter)
        self.editorStatusLabel.setObjectName("editorStatusLabel")
        self.editorStatusLabel.setText(QString("No files currently loaded..."))
        self.widgetLayout.addWidget(self.editorStatusLabel)
        self.editorStuff = EditorBase(self.mainwindow)
        self.widgetLayout.addWidget(self.editorStuff)
        try:
            f = open(filePath,'r')
        except:
            return
        for l in f.readlines():
            self.editorStuff.append(l)
        f.close()
        self.editorStatusLabel.setText(QString(filePath))

        self.mainwindow.tabWidget.insertTab(0,self.tab,self.tabIcon,self.tabLabel)
        self.mainwindow.tabWidget.setCurrentIndex(0)

