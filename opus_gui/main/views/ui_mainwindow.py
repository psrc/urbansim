# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Feb 27 18:12:26 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1093, 515)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Images/Images/new-logo-medium-no-mirror.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtGui.QSplitter(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.toolBox = QtGui.QTabWidget(self.splitter)
        self.toolBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolBox.sizePolicy().hasHeightForWidth())
        self.toolBox.setSizePolicy(sizePolicy)
        self.toolBox.setMinimumSize(QtCore.QSize(0, 0))
        self.toolBox.setBaseSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.toolBox.setFont(font)
        self.toolBox.setObjectName("toolBox")
        self.generalmanager_page = QtGui.QWidget()
        self.generalmanager_page.setObjectName("generalmanager_page")
        self.gridlayout = QtGui.QGridLayout(self.generalmanager_page)
        self.gridlayout.setObjectName("gridlayout")
        self.toolBox.addTab(self.generalmanager_page, "")
        self.datamanager_page = QtGui.QWidget()
        self.datamanager_page.setObjectName("datamanager_page")
        self.gridlayout1 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout1.setObjectName("gridlayout1")
        self.dataManager_toolBox = QtGui.QTabWidget(self.datamanager_page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataManager_toolBox.sizePolicy().hasHeightForWidth())
        self.dataManager_toolBox.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(11)
        self.dataManager_toolBox.setFont(font)
        self.dataManager_toolBox.setObjectName("dataManager_toolBox")
        self.datamanager_xmlconfig = QtGui.QWidget()
        self.datamanager_xmlconfig.setObjectName("datamanager_xmlconfig")
        self.gridlayout2 = QtGui.QGridLayout(self.datamanager_xmlconfig)
        self.gridlayout2.setObjectName("gridlayout2")
        self.dataManager_toolBox.addTab(self.datamanager_xmlconfig, "")
        self.datamanager_dirview = QtGui.QWidget()
        self.datamanager_dirview.setObjectName("datamanager_dirview")
        self.gridlayout3 = QtGui.QGridLayout(self.datamanager_dirview)
        self.gridlayout3.setObjectName("gridlayout3")
        self.dataManager_toolBox.addTab(self.datamanager_dirview, "")
        self.gridlayout1.addWidget(self.dataManager_toolBox, 0, 0, 1, 1)
        self.toolBox.addTab(self.datamanager_page, "")
        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setObjectName("modelmanager_page")
        self.gridlayout4 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout4.setObjectName("gridlayout4")
        self.toolBox.addTab(self.modelmanager_page, "")
        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setObjectName("runmanager_page")
        self.gridlayout5 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout5.setObjectName("gridlayout5")
        self.toolBox.addTab(self.runmanager_page, "")
        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setObjectName("resultsmanager_page")
        self.gridlayout6 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout6.setObjectName("gridlayout6")
        self.toolBox.addTab(self.resultsmanager_page, "")
        self.verticalLayout.addWidget(self.splitter)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1093, 27))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName("menuUtilities")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(20, 20))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/Images/Images/mActionZoomOut.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionZoomOut.setIcon(icon1)
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")
        self.mpActionPan = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/Images/Images/mActionPan.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionPan.setIcon(icon2)
        self.mpActionPan.setObjectName("mpActionPan")
        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/Images/Images/mActionAddRasterLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionAddRasterLayer.setIcon(icon3)
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")
        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/Images/Images/mActionZoomIn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionZoomIn.setIcon(icon4)
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")
        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/Images/Images/mActionAddLayer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.mpActionAddVectorLayer.setIcon(icon5)
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")
        self.actOpenProject = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/Images/Images/open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actOpenProject.setIcon(icon8)
        self.actOpenProject.setIconVisibleInMenu(True)
        self.actOpenProject.setObjectName("actOpenProject")
        self.actExit = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/Images/Images/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actExit.setIcon(icon9)
        self.actExit.setObjectName("actExit")
        self.actSaveProject = QtGui.QAction(MainWindow)
        self.actSaveProject.setEnabled(False)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/Images/Images/save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actSaveProject.setIcon(icon10)
        self.actSaveProject.setObjectName("actSaveProject")
        self.actSaveProjectAs = QtGui.QAction(MainWindow)
        self.actSaveProjectAs.setEnabled(False)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/Images/Images/save_as.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actSaveProjectAs.setIcon(icon11)
        self.actSaveProjectAs.setObjectName("actSaveProjectAs")
        self.actShowHidden = QtGui.QAction(MainWindow)
        self.actShowHidden.setEnabled(True)
        self.actShowHidden.setObjectName("actShowHidden")
        self.actShowHidden.setCheckable(True)
        self.actReloadProject = QtGui.QAction(MainWindow)
        self.actReloadProject.setEnabled(False)
        self.actReloadProject.setObjectName("actReloadProject")
        self.actionRun_Manager = QtGui.QAction(MainWindow)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/Images/Images/cog.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun_Manager.setIcon(icon12)
        self.actionRun_Manager.setObjectName("actionRun_Manager")
        self.actAbout = QtGui.QAction(MainWindow)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/Images/Images/help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actAbout.setIcon(icon13)
        self.actAbout.setObjectName("actAbout")
        self.tabActionEditor = QtGui.QAction(MainWindow)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap(":/Images/Images/table.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabActionEditor.setIcon(icon14)
        self.tabActionEditor.setObjectName("tabActionEditor")
        self.tabActionMapView = QtGui.QAction(MainWindow)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap(":/Images/Images/map.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabActionMapView.setIcon(icon15)
        self.tabActionMapView.setObjectName("tabActionMapView")
        self.tabActionPythonConsole = QtGui.QAction(MainWindow)
        icon16 = QtGui.QIcon()
        icon16.addPixmap(QtGui.QPixmap(":/Images/Images/python_type.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabActionPythonConsole.setIcon(icon16)
        self.tabActionPythonConsole.setObjectName("tabActionPythonConsole")
        self.tabActionLogView = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/Images/Images/folder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabActionLogView.setIcon(icon6)
        self.tabActionLogView.setObjectName("tabActionLogView")
        self.actPythonView = QtGui.QAction(MainWindow)
        self.actPythonView.setEnabled(False)
        self.actPythonView.setIcon(icon16)
        self.actPythonView.setVisible(False)
        self.actPythonView.setIconVisibleInMenu(True)
        self.actPythonView.setObjectName("actPythonView")
        self.actLogView = QtGui.QAction(MainWindow)
        self.actLogView.setIcon(icon14)
        self.actLogView.setObjectName("actLogView")
        self.actEditorView = QtGui.QAction(MainWindow)
        icon17 = QtGui.QIcon()
        icon17.addPixmap(QtGui.QPixmap(":/Images/Images/table_lightning.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actEditorView.setIcon(icon17)
        self.actEditorView.setVisible(False)
        self.actEditorView.setObjectName("actEditorView")
        self.actionMap_View = QtGui.QAction(MainWindow)
        self.actionMap_View.setIcon(icon15)
        self.actionMap_View.setObjectName("actionMap_View")
        self.actionIncreaseFontSize = QtGui.QAction(MainWindow)
        self.actionIncreaseFontSize.setObjectName("actionIncreaseFontSize")
        self.actionDecreaseFontSize = QtGui.QAction(MainWindow)
        self.actionDecreaseFontSize.setObjectName("actionDecreaseFontSize")
        self.actCloseProject = QtGui.QAction(MainWindow)
        self.actCloseProject.setEnabled(False)
        icon18 = QtGui.QIcon()
        icon18.addPixmap(QtGui.QPixmap(":/Images/Images/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actCloseProject.setIcon(icon18)
        self.actCloseProject.setObjectName("actCloseProject")
        self.actVariableLibrary = QtGui.QAction(MainWindow)
        icon19 = QtGui.QIcon()
        icon19.addPixmap(QtGui.QPixmap(":/Images/Images/variable_library.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actVariableLibrary.setIcon(icon19)
        self.actVariableLibrary.setObjectName("actVariableLibrary")
        self.actPreferences = QtGui.QAction(MainWindow)
        icon20 = QtGui.QIcon()
        icon20.addPixmap(QtGui.QPixmap(":/Images/Images/configure.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actPreferences.setIcon(icon20)
        self.actPreferences.setObjectName("actPreferences")
        self.actLaunchResultBrowser = QtGui.QAction(MainWindow)
        icon21 = QtGui.QIcon()
        icon21.addPixmap(QtGui.QPixmap(":/Images/Images/result_browser.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actLaunchResultBrowser.setIcon(icon21)
        self.actLaunchResultBrowser.setObjectName("actLaunchResultBrowser")
        self.actDatabaseSettings = QtGui.QAction(MainWindow)
        icon22 = QtGui.QIcon()
        icon22.addPixmap(QtGui.QPixmap(":/Images/Images/database_link.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actDatabaseSettings.setIcon(icon22)
        self.actDatabaseSettings.setObjectName("actDatabaseSettings")
        self.actNewProject = QtGui.QAction(MainWindow)
        icon23 = QtGui.QIcon()
        icon23.addPixmap(QtGui.QPixmap(":/Images/Images/xml_document.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actNewProject.setIcon(icon23)
        self.actNewProject.setObjectName("actNewProject")
        self.menuProject.addAction(self.actNewProject)
        self.menuProject.addAction(self.actOpenProject)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actSaveProject)
        self.menuProject.addAction(self.actSaveProjectAs)
        self.menuProject.addAction(self.actReloadProject)
        self.menuProject.addAction(self.actCloseProject)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actShowHidden)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actExit)
        self.menuHelp.addAction(self.actAbout)
        self.menuUtilities.addAction(self.actPythonView)
        self.menuUtilities.addAction(self.actLogView)
        self.menuUtilities.addAction(self.actEditorView)
        self.menuUtilities.addSeparator()
        self.menuUtilities.addAction(self.actVariableLibrary)
        self.menuUtilities.addAction(self.actLaunchResultBrowser)
        self.menuUtilities.addSeparator()
        self.menuUtilities.addAction(self.actPreferences)
        self.menuUtilities.addAction(self.actDatabaseSettings)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuUtilities.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.toolBar.addAction(self.actOpenProject)
        self.toolBar.addAction(self.actSaveProject)
        self.toolBar.addAction(self.actCloseProject)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actVariableLibrary)
        self.toolBar.addAction(self.actLaunchResultBrowser)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actLogView)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actDatabaseSettings)
        self.toolBar.addAction(self.actPreferences)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.dataManager_toolBox.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        self.toolBox.setTabText(self.toolBox.indexOf(self.generalmanager_page), QtGui.QApplication.translate("MainWindow", "General", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setTabText(self.dataManager_toolBox.indexOf(self.datamanager_xmlconfig), QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.dataManager_toolBox.setTabText(self.dataManager_toolBox.indexOf(self.datamanager_dirview), QtGui.QApplication.translate("MainWindow", "Opus Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Scenarios", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setTabText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUtilities.setTitle(QtGui.QApplication.translate("MainWindow", "Tools", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.actOpenProject.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actSaveProject.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actSaveProjectAs.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actShowHidden.setText(QtGui.QApplication.translate("MainWindow", "Show hidden", None, QtGui.QApplication.UnicodeUTF8))
        self.actReloadProject.setText(QtGui.QApplication.translate("MainWindow", "Reload Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun_Manager.setText(QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.actAbout.setText(QtGui.QApplication.translate("MainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionEditor.setText(QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionMapView.setText(QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionPythonConsole.setText(QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabActionLogView.setText(QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.actPythonView.setText(QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.actPythonView.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.actLogView.setText(QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.actLogView.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.actEditorView.setText(QtGui.QApplication.translate("MainWindow", "Editor View", None, QtGui.QApplication.UnicodeUTF8))
        self.actEditorView.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Editor View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMap_View.setText(QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionIncreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "Increase Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDecreaseFontSize.setText(QtGui.QApplication.translate("MainWindow", "Decrease Font Size", None, QtGui.QApplication.UnicodeUTF8))
        self.actCloseProject.setText(QtGui.QApplication.translate("MainWindow", "Close Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actCloseProject.setToolTip(QtGui.QApplication.translate("MainWindow", "Close Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actVariableLibrary.setText(QtGui.QApplication.translate("MainWindow", "Variable Library", None, QtGui.QApplication.UnicodeUTF8))
        self.actVariableLibrary.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Variable Library", None, QtGui.QApplication.UnicodeUTF8))
        self.actPreferences.setText(QtGui.QApplication.translate("MainWindow", "Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actPreferences.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Preferences", None, QtGui.QApplication.UnicodeUTF8))
        self.actLaunchResultBrowser.setText(QtGui.QApplication.translate("MainWindow", "Result Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.actLaunchResultBrowser.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Result Browser", None, QtGui.QApplication.UnicodeUTF8))
        self.actDatabaseSettings.setText(QtGui.QApplication.translate("MainWindow", "Database Connection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actDatabaseSettings.setToolTip(QtGui.QApplication.translate("MainWindow", "Open Database Connection Settings", None, QtGui.QApplication.UnicodeUTF8))
        self.actNewProject.setText(QtGui.QApplication.translate("MainWindow", "New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actNewProject.setToolTip(QtGui.QApplication.translate("MainWindow", "Create a new project based on a built-in or custom project", None, QtGui.QApplication.UnicodeUTF8))
        self.actNewProject.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))

import opusmain_rc
