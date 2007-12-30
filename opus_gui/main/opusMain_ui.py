# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusMain.ui'
#
# Created: Sun Dec 30 15:05:45 2007
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,974,707).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")

        self.toolBox = QtGui.QToolBox(self.splitter)
        self.toolBox.setEnabled(True)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setBaseSize(QtCore.QSize(0,0))
        self.toolBox.setObjectName("toolBox")

        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,96,38))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout1 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.toolBox.addItem(self.datamanager_page,QtGui.QIcon(":/Images/Images/database_table.png"),"")

        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0,0,96,38))
        self.modelmanager_page.setObjectName("modelmanager_page")

        self.gridlayout2 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")
        self.toolBox.addItem(self.modelmanager_page,QtGui.QIcon(":/Images/Images/chart_organisation.png"),"")

        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0,0,370,524))
        self.runmanager_page.setObjectName("runmanager_page")

        self.gridlayout3 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")
        self.toolBox.addItem(self.runmanager_page,QtGui.QIcon(":/Images/Images/cog.png"),"")

        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0,0,96,38))
        self.resultsmanager_page.setObjectName("resultsmanager_page")

        self.gridlayout4 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")
        self.toolBox.addItem(self.resultsmanager_page,QtGui.QIcon(":/Images/Images/map_go.png"),"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_editorView = QtGui.QWidget()
        self.tab_editorView.setObjectName("tab_editorView")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_editorView)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")
        self.tabWidget.addTab(self.tab_editorView,QtGui.QIcon(":/Images/Images/table.png"),"")

        self.tab_mapView = QtGui.QWidget()
        self.tab_mapView.setObjectName("tab_mapView")

        self.gridlayout6 = QtGui.QGridLayout(self.tab_mapView)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.widgetMap = QtGui.QWidget(self.tab_mapView)
        self.widgetMap.setMinimumSize(QtCore.QSize(100,100))
        self.widgetMap.setAutoFillBackground(True)
        self.widgetMap.setObjectName("widgetMap")
        self.gridlayout6.addWidget(self.widgetMap,0,0,1,1)
        self.tabWidget.addTab(self.tab_mapView,QtGui.QIcon(":/Images/Images/map.png"),"")

        self.tab_pythonView = QtGui.QWidget()
        self.tab_pythonView.setObjectName("tab_pythonView")

        self.gridlayout7 = QtGui.QGridLayout(self.tab_pythonView)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")

        self.pythonLineWidget = QtGui.QWidget(self.tab_pythonView)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pythonLineWidget.sizePolicy().hasHeightForWidth())
        self.pythonLineWidget.setSizePolicy(sizePolicy)
        self.pythonLineWidget.setObjectName("pythonLineWidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.pythonLineWidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setObjectName("hboxlayout")

        self.pythonLabel = QtGui.QLabel(self.pythonLineWidget)
        self.pythonLabel.setObjectName("pythonLabel")
        self.hboxlayout.addWidget(self.pythonLabel)

        self.pythonLineEdit = QtGui.QLineEdit(self.pythonLineWidget)
        self.pythonLineEdit.setObjectName("pythonLineEdit")
        self.hboxlayout.addWidget(self.pythonLineEdit)
        self.gridlayout7.addWidget(self.pythonLineWidget,1,0,1,1)

        self.pythonWidget = QtGui.QWidget(self.tab_pythonView)
        self.pythonWidget.setObjectName("pythonWidget")
        self.gridlayout7.addWidget(self.pythonWidget,0,0,1,1)
        self.tabWidget.addTab(self.tab_pythonView,QtGui.QIcon(":/Images/Images/python_type.png"),"")

        self.tab_logView = QtGui.QWidget()
        self.tab_logView.setObjectName("tab_logView")
        self.tabWidget.addTab(self.tab_logView,QtGui.QIcon(":/Images/Images/folder.png"),"")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,974,26))
        self.menubar.setObjectName("menubar")

        self.menuMap = QtGui.QMenu(self.menubar)
        self.menuMap.setObjectName("menuMap")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        self.mpActionZoomOut.setIcon(QtGui.QIcon(":/Images/Images/mActionZoomOut.png"))
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")

        self.mpActionPan = QtGui.QAction(MainWindow)
        self.mpActionPan.setIcon(QtGui.QIcon(":/Images/Images/mActionPan.png"))
        self.mpActionPan.setObjectName("mpActionPan")

        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        self.mpActionAddRasterLayer.setIcon(QtGui.QIcon(":/Images/Images/mActionAddRasterLayer.png"))
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")

        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        self.mpActionZoomIn.setIcon(QtGui.QIcon(":/Images/Images/mActionZoomIn.png"))
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")

        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        self.mpActionAddVectorLayer.setIcon(QtGui.QIcon(":/Images/Images/mActionAddLayer.png"))
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")

        self.actionOpen_Project = QtGui.QAction(MainWindow)
        self.actionOpen_Project.setObjectName("actionOpen_Project")

        self.actionSave_Project = QtGui.QAction(MainWindow)
        self.actionSave_Project.setObjectName("actionSave_Project")

        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setObjectName("actionSave_Project_As")

        self.actionOpen_Project_2 = QtGui.QAction(MainWindow)
        self.actionOpen_Project_2.setObjectName("actionOpen_Project_2")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionSave_Project_2 = QtGui.QAction(MainWindow)
        self.actionSave_Project_2.setObjectName("actionSave_Project_2")

        self.actionSave_Project_As_2 = QtGui.QAction(MainWindow)
        self.actionSave_Project_As_2.setObjectName("actionSave_Project_As_2")

        self.actionRun_Manager = QtGui.QAction(MainWindow)
        self.actionRun_Manager.setObjectName("actionRun_Manager")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuMap.addAction(self.mpActionZoomIn)
        self.menuMap.addAction(self.mpActionZoomOut)
        self.menuMap.addAction(self.mpActionPan)
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionOpen_Project_2)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionSave_Project_2)
        self.menuProject.addAction(self.actionSave_Project_As_2)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpusGui", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Scenario Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_editorView), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapView), QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.pythonLabel.setText(QtGui.QApplication.translate("MainWindow", ">>>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pythonView), QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logView), QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMap.setTitle(QtGui.QApplication.translate("MainWindow", "Map", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project_2.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_2.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As_2.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun_Manager.setText(QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc
