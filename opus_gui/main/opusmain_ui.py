# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusmain.ui'
#
# Created: Mon Jun 09 13:34:41 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,974,707).size()).expandedTo(MainWindow.minimumSizeHint()))

        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        MainWindow.setWindowIcon(QtGui.QIcon(":/Images/Images/cog.png"))

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

        self.generalmanager_page = QtGui.QWidget()
        self.generalmanager_page.setGeometry(QtCore.QRect(0,0,98,38))
        self.generalmanager_page.setObjectName("generalmanager_page")

        self.gridlayout1 = QtGui.QGridLayout(self.generalmanager_page)
        self.gridlayout1.setObjectName("gridlayout1")
        self.toolBox.addItem(self.generalmanager_page,QtGui.QIcon(":/Images/Images/application_side_tree.png"),"")

        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,426,491))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout2 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.dataManager_toolBox = QtGui.QToolBox(self.datamanager_page)

        font = QtGui.QFont()
        font.setPointSize(8)
        self.dataManager_toolBox.setFont(font)
        self.dataManager_toolBox.setObjectName("dataManager_toolBox")

        self.datamanager_dbsconnections = QtGui.QWidget()
        self.datamanager_dbsconnections.setGeometry(QtCore.QRect(0,0,98,38))
        self.datamanager_dbsconnections.setObjectName("datamanager_dbsconnections")

        self.gridlayout3 = QtGui.QGridLayout(self.datamanager_dbsconnections)
        self.gridlayout3.setObjectName("gridlayout3")
        self.dataManager_toolBox.addItem(self.datamanager_dbsconnections,"")

        self.datamanager_xmlconfig = QtGui.QWidget()
        self.datamanager_xmlconfig.setGeometry(QtCore.QRect(0,0,408,389))
        self.datamanager_xmlconfig.setObjectName("datamanager_xmlconfig")

        self.gridlayout4 = QtGui.QGridLayout(self.datamanager_xmlconfig)
        self.gridlayout4.setObjectName("gridlayout4")
        self.dataManager_toolBox.addItem(self.datamanager_xmlconfig,"")

        self.datamanager_dirview = QtGui.QWidget()
        self.datamanager_dirview.setGeometry(QtCore.QRect(0,0,98,38))
        self.datamanager_dirview.setObjectName("datamanager_dirview")

        self.gridlayout5 = QtGui.QGridLayout(self.datamanager_dirview)
        self.gridlayout5.setObjectName("gridlayout5")
        self.dataManager_toolBox.addItem(self.datamanager_dirview,"")
        self.gridlayout2.addWidget(self.dataManager_toolBox,0,0,1,1)
        self.toolBox.addItem(self.datamanager_page,QtGui.QIcon(":/Images/Images/database_table.png"),"")

        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0,0,98,38))
        self.modelmanager_page.setObjectName("modelmanager_page")

        self.gridlayout6 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")
        self.toolBox.addItem(self.modelmanager_page,QtGui.QIcon(":/Images/Images/chart_organisation.png"),"")

        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0,0,98,38))
        self.runmanager_page.setObjectName("runmanager_page")

        self.gridlayout7 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout7.setMargin(9)
        self.gridlayout7.setSpacing(6)
        self.gridlayout7.setObjectName("gridlayout7")
        self.toolBox.addItem(self.runmanager_page,QtGui.QIcon(":/Images/Images/cog.png"),"")

        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0,0,98,38))
        self.resultsmanager_page.setObjectName("resultsmanager_page")

        self.gridlayout8 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout8.setMargin(9)
        self.gridlayout8.setSpacing(6)
        self.gridlayout8.setObjectName("gridlayout8")
        self.toolBox.addItem(self.resultsmanager_page,QtGui.QIcon(":/Images/Images/map_go.png"),"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_editorView = QtGui.QWidget()
        self.tab_editorView.setObjectName("tab_editorView")

        self.gridlayout9 = QtGui.QGridLayout(self.tab_editorView)
        self.gridlayout9.setMargin(9)
        self.gridlayout9.setSpacing(6)
        self.gridlayout9.setObjectName("gridlayout9")
        self.tabWidget.addTab(self.tab_editorView,QtGui.QIcon(":/Images/Images/table_lightning.png"),"")

        self.tab_pythonView = QtGui.QWidget()
        self.tab_pythonView.setObjectName("tab_pythonView")

        self.gridlayout10 = QtGui.QGridLayout(self.tab_pythonView)
        self.gridlayout10.setMargin(9)
        self.gridlayout10.setSpacing(6)
        self.gridlayout10.setObjectName("gridlayout10")

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
        self.gridlayout10.addWidget(self.pythonLineWidget,1,0,1,1)

        self.pythonWidget = QtGui.QWidget(self.tab_pythonView)
        self.pythonWidget.setObjectName("pythonWidget")
        self.gridlayout10.addWidget(self.pythonWidget,0,0,1,1)
        self.tabWidget.addTab(self.tab_pythonView,QtGui.QIcon(":/Images/Images/python_type.png"),"")

        self.tab_logView = QtGui.QWidget()
        self.tab_logView.setObjectName("tab_logView")
        self.tabWidget.addTab(self.tab_logView,QtGui.QIcon(":/Images/Images/table.png"),"")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,974,21))
        self.menubar.setObjectName("menubar")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName("menuUtilities")

        self.menuModel_System = QtGui.QMenu(self.menubar)
        self.menuModel_System.setObjectName("menuModel_System")
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
        self.actionOpen_Project.setIcon(QtGui.QIcon(":/Images/Images/folder.png"))
        self.actionOpen_Project.setObjectName("actionOpen_Project")

        self.actionSave_Project = QtGui.QAction(MainWindow)
        self.actionSave_Project.setIcon(QtGui.QIcon(":/Images/Images/script_save.png"))
        self.actionSave_Project.setObjectName("actionSave_Project")

        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setIcon(QtGui.QIcon(":/Images/Images/script_save.png"))
        self.actionSave_Project_As.setObjectName("actionSave_Project_As")

        self.actionOpen_Project_2 = QtGui.QAction(MainWindow)
        self.actionOpen_Project_2.setIcon(QtGui.QIcon(":/Images/Images/folder.png"))
        self.actionOpen_Project_2.setObjectName("actionOpen_Project_2")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setIcon(QtGui.QIcon(":/Images/Images/cross.png"))
        self.actionExit.setObjectName("actionExit")

        self.actionSave_Project_2 = QtGui.QAction(MainWindow)
        self.actionSave_Project_2.setIcon(QtGui.QIcon(":/Images/Images/script_save.png"))
        self.actionSave_Project_2.setObjectName("actionSave_Project_2")

        self.actionSave_Project_As_2 = QtGui.QAction(MainWindow)
        self.actionSave_Project_As_2.setIcon(QtGui.QIcon(":/Images/Images/script_save.png"))
        self.actionSave_Project_As_2.setObjectName("actionSave_Project_As_2")

        self.actionRun_Manager = QtGui.QAction(MainWindow)
        self.actionRun_Manager.setIcon(QtGui.QIcon(":/Images/Images/cog.png"))
        self.actionRun_Manager.setObjectName("actionRun_Manager")

        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setIcon(QtGui.QIcon(":/Images/Images/help.png"))
        self.actionAbout.setObjectName("actionAbout")

        self.tabActionEditor = QtGui.QAction(MainWindow)
        self.tabActionEditor.setIcon(QtGui.QIcon(":/Images/Images/table.png"))
        self.tabActionEditor.setObjectName("tabActionEditor")

        self.tabActionMapView = QtGui.QAction(MainWindow)
        self.tabActionMapView.setIcon(QtGui.QIcon(":/Images/Images/map.png"))
        self.tabActionMapView.setObjectName("tabActionMapView")

        self.tabActionPythonConsole = QtGui.QAction(MainWindow)
        self.tabActionPythonConsole.setIcon(QtGui.QIcon(":/Images/Images/python_type.png"))
        self.tabActionPythonConsole.setObjectName("tabActionPythonConsole")

        self.tabActionLogView = QtGui.QAction(MainWindow)
        self.tabActionLogView.setIcon(QtGui.QIcon(":/Images/Images/folder.png"))
        self.tabActionLogView.setObjectName("tabActionLogView")

        self.actionPython_View = QtGui.QAction(MainWindow)
        self.actionPython_View.setIcon(QtGui.QIcon(":/Images/Images/python_type.png"))
        self.actionPython_View.setObjectName("actionPython_View")

        self.actionLog_View = QtGui.QAction(MainWindow)
        self.actionLog_View.setIcon(QtGui.QIcon(":/Images/Images/table.png"))
        self.actionLog_View.setObjectName("actionLog_View")

        self.actionEditor_View = QtGui.QAction(MainWindow)
        self.actionEditor_View.setIcon(QtGui.QIcon(":/Images/Images/table_lightning.png"))
        self.actionEditor_View.setObjectName("actionEditor_View")

        self.actionMap_View = QtGui.QAction(MainWindow)
        self.actionMap_View.setIcon(QtGui.QIcon(":/Images/Images/map.png"))
        self.actionMap_View.setObjectName("actionMap_View")

        self.actionClose_Project = QtGui.QAction(MainWindow)
        self.actionClose_Project.setIcon(QtGui.QIcon(":/Images/Images/folder.png"))
        self.actionClose_Project.setObjectName("actionClose_Project")

        self.actionEdit_all_variables = QtGui.QAction(MainWindow)
        self.actionEdit_all_variables.setObjectName("actionEdit_all_variables")
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionOpen_Project_2)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionSave_Project_2)
        self.menuProject.addAction(self.actionSave_Project_As_2)
        self.menuProject.addAction(self.actionClose_Project)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuUtilities.addAction(self.actionPython_View)
        self.menuUtilities.addAction(self.actionLog_View)
        self.menuUtilities.addAction(self.actionEditor_View)
        self.menuModel_System.addAction(self.actionEdit_all_variables)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuModel_System.menuAction())
        self.menubar.addAction(self.menuUtilities.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(1)
        self.dataManager_toolBox.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.toolBox.setItemText(self.toolBox.indexOf(self.generalmanager_page), QtGui.QApplication.translate("MainWindow", "General Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setItemText(self.dataManager_toolBox.indexOf(self.datamanager_dbsconnections), QtGui.QApplication.translate("MainWindow", "Database Server Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setItemText(self.dataManager_toolBox.indexOf(self.datamanager_xmlconfig), QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setItemText(self.dataManager_toolBox.indexOf(self.datamanager_dirview), QtGui.QApplication.translate("MainWindow", "Opus Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Scenario Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_editorView), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.pythonLabel.setText(QtGui.QApplication.translate("MainWindow", ">>>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pythonView), QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logView), QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUtilities.setTitle(QtGui.QApplication.translate("MainWindow", "Utilities", None, QtGui.QApplication.UnicodeUTF8))
        self.menuModel_System.setTitle(QtGui.QApplication.translate("MainWindow", "Model System", None, QtGui.QApplication.UnicodeUTF8))
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
        self.tabActionEditor.setText(QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionMapView.setText(QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionPythonConsole.setText(QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionLogView.setText(QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPython_View.setText(QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLog_View.setText(QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEditor_View.setText(QtGui.QApplication.translate("MainWindow", "Editor View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMap_View.setText(QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Project.setText(QtGui.QApplication.translate("MainWindow", "Close Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_all_variables.setText(QtGui.QApplication.translate("MainWindow", "View/Edit all_variables", None, QtGui.QApplication.UnicodeUTF8))

import opusmain_rc
