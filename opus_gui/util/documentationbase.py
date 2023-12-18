# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 


# PyQt4 includes for python bindings to QT
from PyQt4.QtCore import QUrl, Qt, QString, QObject, SIGNAL
from PyQt4.QtGui import QTextBrowser, QWidget, QIcon, QVBoxLayout, QLabel, QPushButton


# Main 
class DocumentationBase(QTextBrowser):
    def __init__(self, mainwindow, src):
        QTextBrowser.__init__(self, mainwindow)
        self.mainwindow = mainwindow
        self.src = src
        self.setOpenExternalLinks(True)
        self.setSource(QUrl(self.src))


class DocumentationTab(QWidget):
    def __init__(self, mainwindow, filePath):
        QWidget.__init__(self, mainwindow)
        self.mainwindow = mainwindow

        self.tabIcon = QIcon(":/Images/Images/chart_organisation.png")
        self.tabLabel = "Documentation Tab"

        self.tab = QWidget(self.mainwindow)

        self.widgetLayout = QVBoxLayout(self.tab)
        self.widgetLayout.setAlignment(Qt.AlignTop)
        self.docStatusLabel = QLabel(self.tab)
        self.docStatusLabel.setAlignment(Qt.AlignCenter)
        self.docStatusLabel.setObjectName("docStatusLabel")
        self.docStatusLabel.setText(QString("No documentation currently loaded..."))
        self.widgetLayout.addWidget(self.docStatusLabel)

        self.pbnRemoveDoc = QPushButton(self.tab)
        self.pbnRemoveDoc.setObjectName("pbnRemoveDoc")
        self.pbnRemoveDoc.setText(QString("Remove Documentation"))
        QObject.connect(self.pbnRemoveDoc, SIGNAL("clicked()"),
                        self.clicked)
        self.widgetLayout.addWidget(self.pbnRemoveDoc)

        self.docStuff = DocumentationBase(self.mainwindow,filePath)
        self.widgetLayout.addWidget(self.docStuff)
        self.docStatusLabel.setText(QString(filePath))

        self.mainwindow.tabWidget.insertTab(0,self.tab,self.tabIcon,self.tabLabel)
        self.mainwindow.tabWidget.setCurrentIndex(0)

    def clicked(self):
        print("Remove Documentation Pressed...")
        self.mainwindow.tabWidget.removeTab(self.mainwindow.tabWidget.indexOf(self.tab))
        self.tab.hide()

