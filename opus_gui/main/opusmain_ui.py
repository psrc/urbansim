# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusmain.ui'
#
# Created: Tue Aug 12 00:14:56 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(974, 707)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/cog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setGeometry(QtCore.QRect(0, 22, 974, 665))
        self.centralwidget.setObjectName("centralwidget")
        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName("gridlayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.toolBox = QtGui.QTabWidget(self.splitter)
        self.toolBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(100, 0))
        self.toolBox.setBaseSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toolBox.setFont(font)
        self.toolBox.setObjectName("toolBox")
        self.generalmanager_page = QtGui.QWidget()
        self.generalmanager_page.setGeometry(QtCore.QRect(0, 0, 337, 612))
        self.generalmanager_page.setObjectName("generalmanager_page")
        self.gridlayout1 = QtGui.QGridLayout(self.generalmanager_page)
        self.gridlayout1.setObjectName("gridlayout1")
        self.toolBox.addTab(self.generalmanager_page, "")
        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setGeometry(QtCore.QRect(0, 0, 500, 612))
        self.datamanager_page.setObjectName("datamanager_page")
        self.gridlayout2 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout2.setObjectName("gridlayout2")
        self.dataManager_toolBox = QtGui.QTabWidget(self.datamanager_page)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dataManager_toolBox.setFont(font)
        self.dataManager_toolBox.setObjectName("dataManager_toolBox")
        self.datamanager_dbsconnections = QtGui.QWidget()
        self.datamanager_dbsconnections.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.datamanager_dbsconnections.setObjectName("datamanager_dbsconnections")
        self.gridlayout3 = QtGui.QGridLayout(self.datamanager_dbsconnections)
        self.gridlayout3.setObjectName("gridlayout3")
        self.dataManager_toolBox.addTab(self.datamanager_dbsconnections, "")
        self.datamanager_xmlconfig = QtGui.QWidget()
        self.datamanager_xmlconfig.setGeometry(QtCore.QRect(0, 0, 470, 565))
        self.datamanager_xmlconfig.setObjectName("datamanager_xmlconfig")
        self.gridlayout4 = QtGui.QGridLayout(self.datamanager_xmlconfig)
        self.gridlayout4.setObjectName("gridlayout4")
        self.dataManager_toolBox.addTab(self.datamanager_xmlconfig, "")
        self.datamanager_dirview = QtGui.QWidget()
        self.datamanager_dirview.setGeometry(QtCore.QRect(0, 0, 100, 30))
        self.datamanager_dirview.setObjectName("datamanager_dirview")
        self.gridlayout5 = QtGui.QGridLayout(self.datamanager_dirview)
        self.gridlayout5.setObjectName("gridlayout5")
        self.dataManager_toolBox.addTab(self.datamanager_dirview, "")
        self.gridlayout2.addWidget(self.dataManager_toolBox, 0, 0, 1, 1)
        self.toolBox.addTab(self.datamanager_page, "")
        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0, 0, 500, 612))
        self.modelmanager_page.setObjectName("modelmanager_page")
        self.gridlayout6 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout6.setObjectName("gridlayout6")
        self.toolBox.addTab(self.modelmanager_page, "")
        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0, 0, 500, 612))
        self.runmanager_page.setObjectName("runmanager_page")
        self.gridlayout7 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout7.setObjectName("gridlayout7")
        self.toolBox.addTab(self.runmanager_page, "")
        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0, 0, 500, 612))
        self.resultsmanager_page.setObjectName("resultsmanager_page")
        self.gridlayout8 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout8.setObjectName("gridlayout8")
        self.toolBox.addTab(self.resultsmanager_page, "")
        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setMinimumSize(QtCore.QSize(600, 0))
        self.tabWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.tabWidget.setBaseSize(QtCore.QSize(1000, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_editorView = QtGui.QWidget()
        self.tab_editorView.setGeometry(QtCore.QRect(0, 0, 594, 612))
        self.tab_editorView.setObjectName("tab_editorView")
        self.gridlayout9 = QtGui.QGridLayout(self.tab_editorView)
        self.gridlayout9.setObjectName("gridlayout9")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/Images/table_lightning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_editorView, icon1, "")
        self.tab_pythonView = QtGui.QWidget()
        self.tab_pythonView.setGeometry(QtCore.QRect(0, 0, 431, 612))
        self.tab_pythonView.setObjectName("tab_pythonView")
        self.gridlayout10 = QtGui.QGridLayout(self.tab_pythonView)
        self.gridlayout10.setObjectName("gridlayout10")
        self.pythonLineWidget = QtGui.QWidget(self.tab_pythonView)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pythonLineWidget.sizePolicy().hasHeightForWidth())
        self.pythonLineWidget.setSizePolicy(sizePolicy)
        self.pythonLineWidget.setObjectName("pythonLineWidget")
        self.hboxlayout = QtGui.QHBoxLayout(self.pythonLineWidget)
        self.hboxlayout.setObjectName("hboxlayout")
        self.pythonLabel = QtGui.QLabel(self.pythonLineWidget)
        self.pythonLabel.setObjectName("pythonLabel")
        self.hboxlayout.addWidget(self.pythonLabel)
        self.pythonLineEdit = QtGui.QLineEdit(self.pythonLineWidget)
        self.pythonLineEdit.setObjectName("pythonLineEdit")
        self.hboxlayout.addWidget(self.pythonLineEdit)
        self.gridlayout10.addWidget(self.pythonLineWidget, 1, 0, 1, 1)
        self.pythonWidget = QtGui.QWidget(self.tab_pythonView)
        self.pythonWidget.setObjectName("pythonWidget")
        self.gridlayout10.addWidget(self.pythonWidget, 0, 0, 1, 1)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/Images/python_type.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_pythonView, icon2, "")
        self.tab_logView = QtGui.QWidget()
        self.tab_logView.setGeometry(QtCore.QRect(0, 0, 431, 612))
        self.tab_logView.setObjectName("tab_logView")
        self.gridlayout11 = QtGui.QGridLayout(self.tab_logView)
        self.gridlayout11.setObjectName("gridlayout11")
        self.logViewTextBrowser = QtGui.QTextBrowser(self.tab_logView)
        self.logViewTextBrowser.setObjectName("logViewTextBrowser")
        self.gridlayout11.addWidget(self.logViewTextBrowser, 0, 0, 1, 1)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/Images/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.tab_logView, icon3, "")
        self.gridlayout.addWidget(self.splitter, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 974, 22))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName("menuUtilities")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setGeometry(QtCore.QRect(0, 687, 974, 20))
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/Images/mActionZoomOut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionZoomOut.setIcon(icon4)
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")
        self.mpActionPan = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/Images/mActionPan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionPan.setIcon(icon5)
        self.mpActionPan.setObjectName("mpActionPan")
        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/Images/mActionAddRasterLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionAddRasterLayer.setIcon(icon6)
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")
        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/Images/Images/mActionZoomIn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionZoomIn.setIcon(icon7)
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")
        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Images/Images/mActionAddLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionAddVectorLayer.setIcon(icon8)
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")
        self.actionOpen_Project = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Images/Images/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionOpen_Project.setIcon(icon9)
        self.actionOpen_Project.setObjectName("actionOpen_Project")
        self.actionSave_Project = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Images/Images/script_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Project.setIcon(icon10)
        self.actionSave_Project.setObjectName("actionSave_Project")
        self.actionSave_Project_As = QtGui.QAction(MainWindow)
        self.actionSave_Project_As.setIcon(icon10)
        self.actionSave_Project_As.setObjectName("actionSave_Project_As")
        self.actionOpen_Project_2 = QtGui.QAction(MainWindow)
        self.actionOpen_Project_2.setIcon(icon9)
        self.actionOpen_Project_2.setObjectName("actionOpen_Project_2")
        self.actionExit = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/Images/Images/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon11)
        self.actionExit.setObjectName("actionExit")
        self.actionSave_Project_2 = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/Images/Images/disk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_Project_2.setIcon(icon12)
        self.actionSave_Project_2.setObjectName("actionSave_Project_2")
        self.actionSave_Project_As_2 = QtGui.QAction(MainWindow)
        self.actionSave_Project_As_2.setIcon(icon10)
        self.actionSave_Project_As_2.setObjectName("actionSave_Project_As_2")
        self.actionRun_Manager = QtGui.QAction(MainWindow)
        self.actionRun_Manager.setIcon(icon)
        self.actionRun_Manager.setObjectName("actionRun_Manager")
        self.actionAbout = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/Images/Images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon13)
        self.actionAbout.setObjectName("actionAbout")
        self.tabActionEditor = QtGui.QAction(MainWindow)
        self.tabActionEditor.setIcon(icon3)
        self.tabActionEditor.setObjectName("tabActionEditor")
        self.tabActionMapView = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/Images/Images/map.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabActionMapView.setIcon(icon14)
        self.tabActionMapView.setObjectName("tabActionMapView")
        self.tabActionPythonConsole = QtGui.QAction(MainWindow)
        self.tabActionPythonConsole.setIcon(icon2)
        self.tabActionPythonConsole.setObjectName("tabActionPythonConsole")
        self.tabActionLogView = QtGui.QAction(MainWindow)
        self.tabActionLogView.setIcon(icon9)
        self.tabActionLogView.setObjectName("tabActionLogView")
        self.actionPython_View = QtGui.QAction(MainWindow)
        self.actionPython_View.setIcon(icon2)
        self.actionPython_View.setObjectName("actionPython_View")
        self.actionLog_View = QtGui.QAction(MainWindow)
        self.actionLog_View.setIcon(icon3)
        self.actionLog_View.setObjectName("actionLog_View")
        self.actionEditor_View = QtGui.QAction(MainWindow)
        self.actionEditor_View.setIcon(icon1)
        self.actionEditor_View.setObjectName("actionEditor_View")
        self.actionMap_View = QtGui.QAction(MainWindow)
        self.actionMap_View.setIcon(icon14)
        self.actionMap_View.setObjectName("actionMap_View")
        self.actionIncreaseFontSize = QtGui.QAction(MainWindow)
        self.actionIncreaseFontSize.setObjectName("actionIncreaseFontSize")
        self.actionDecreaseFontSize = QtGui.QAction(MainWindow)
        self.actionDecreaseFontSize.setObjectName("actionDecreaseFontSize")
        self.actionClose_Project = QtGui.QAction(MainWindow)
        self.actionClose_Project.setIcon(icon9)
        self.actionClose_Project.setObjectName("actionClose_Project")
        self.actionEdit_all_variables = QtGui.QAction(MainWindow)
        self.actionEdit_all_variables.setObjectName("actionEdit_all_variables")
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName("actionPreferences")
        self.actLaunchResultBrowser = QtGui.QAction(MainWindow)
        self.actLaunchResultBrowser.setObjectName("actLaunchResultBrowser")
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
        self.menuUtilities.addSeparator()
        self.menuUtilities.addAction(self.actionEdit_all_variables)
        self.menuUtilities.addAction(self.actLaunchResultBrowser)
        self.menuUtilities.addSeparator()
        self.menuUtilities.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuUtilities.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.dataManager_toolBox.setCurrentIndex(1)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.toolBox.setTabText(self.toolBox.indexOf(self.generalmanager_page), QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setTabText(self.dataManager_toolBox.indexOf(self.datamanager_dbsconnections), QtGui.QApplication.translate("MainWindow", "Database Server Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setTabText(self.dataManager_toolBox.indexOf(self.datamanager_xmlconfig), QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setTabText(self.dataManager_toolBox.indexOf(self.datamanager_dirview), QtGui.QApplication.translate("MainWindow", "Opus Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Scenarios", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_editorView), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.pythonLabel.setText(QtGui.QApplication.translate("MainWindow", ">>>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pythonView), QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logView), QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUtilities.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
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
        self.actionIncreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "Increase Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDecreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "Decrease Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClose_Project.setText(QtGui.QApplication.translate("MainWindow", "Close Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionEdit_all_variables.setText(QtGui.QApplication.translate("MainWindow", "View/Edit Expression Library", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actLaunchResultBrowser.setText(QtGui.QApplication.translate("MainWindow", "Launch Result Browser", None, QtGui.QApplication.UnicodeUTF8))

import opusmain_rc
