# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusMain.ui'
#
# Created: Sun Dec 16 21:18:22 2007
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
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,317,532))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout1 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")
        self.toolBox.addItem(self.datamanager_page,"")

        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0,0,317,532))
        self.modelmanager_page.setObjectName("modelmanager_page")

        self.gridlayout2 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.modelmanager_tree = QtGui.QTreeWidget(self.modelmanager_page)
        self.modelmanager_tree.setObjectName("modelmanager_tree")
        self.gridlayout2.addWidget(self.modelmanager_tree,0,0,1,1)
        self.toolBox.addItem(self.modelmanager_page,"")

        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0,0,317,532))
        self.runmanager_page.setObjectName("runmanager_page")

        self.gridlayout3 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")
        self.toolBox.addItem(self.runmanager_page,"")

        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0,0,112,112))
        self.resultsmanager_page.setObjectName("resultsmanager_page")

        self.gridlayout4 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.resultsmanager_tree = QtGui.QTreeWidget(self.resultsmanager_page)
        self.resultsmanager_tree.setObjectName("resultsmanager_tree")
        self.gridlayout4.addWidget(self.resultsmanager_tree,0,0,1,1)
        self.toolBox.addItem(self.resultsmanager_page,"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_editorView = QtGui.QWidget()
        self.tab_editorView.setObjectName("tab_editorView")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_editorView)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")
        self.tabWidget.addTab(self.tab_editorView,"")

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
        self.tabWidget.addTab(self.tab_mapView,"")

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
        self.tabWidget.addTab(self.tab_pythonView,"")

        self.tab_logView = QtGui.QWidget()
        self.tab_logView.setObjectName("tab_logView")
        self.tabWidget.addTab(self.tab_logView,"")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,974,26))
        self.menubar.setObjectName("menubar")

        self.menuMap = QtGui.QMenu(self.menubar)
        self.menuMap.setObjectName("menuMap")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")

        self.menuUtilities = QtGui.QMenu(self.menubar)
        self.menuUtilities.setObjectName("menuUtilities")
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

        self.actionOpen_Config = QtGui.QAction(MainWindow)
        self.actionOpen_Config.setObjectName("actionOpen_Config")

        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionSave_Config = QtGui.QAction(MainWindow)
        self.actionSave_Config.setObjectName("actionSave_Config")

        self.actionSave_Config_As = QtGui.QAction(MainWindow)
        self.actionSave_Config_As.setObjectName("actionSave_Config_As")

        self.actionRun_Manager = QtGui.QAction(MainWindow)
        self.actionRun_Manager.setObjectName("actionRun_Manager")
        self.menuMap.addAction(self.mpActionZoomIn)
        self.menuMap.addAction(self.mpActionZoomOut)
        self.menuMap.addAction(self.mpActionPan)
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionOpen_Config)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionSave_Config)
        self.menuProject.addAction(self.actionSave_Config_As)
        self.menuProject.addSeparator()
        self.menuProject.addAction(self.actionExit)
        self.menuUtilities.addAction(self.actionRun_Manager)
        self.menubar.addAction(self.menuProject.menuAction())
        self.menubar.addAction(self.menuMap.menuAction())
        self.menubar.addAction(self.menuUtilities.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpusGui", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.modelmanager_tree.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.modelmanager_tree.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.modelmanager_tree.clear()

        item = QtGui.QTreeWidgetItem(self.modelmanager_tree)
        item.setText(0,QtGui.QApplication.translate("MainWindow", "Model System Configurations", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item.setText(1,"")

        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("MainWindow", "base_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item1.setText(1,"")

        item2 = QtGui.QTreeWidgetItem(item1)
        item2.setText(0,QtGui.QApplication.translate("MainWindow", "urbansim_base_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item2.setText(1,"")

        item3 = QtGui.QTreeWidgetItem(item2)
        item3.setText(0,QtGui.QApplication.translate("MainWindow", "base_year", None, QtGui.QApplication.UnicodeUTF8))
        item3.setText(1,QtGui.QApplication.translate("MainWindow", "2005", None, QtGui.QApplication.UnicodeUTF8))

        item4 = QtGui.QTreeWidgetItem(item2)
        item4.setText(0,QtGui.QApplication.translate("MainWindow", "models", None, QtGui.QApplication.UnicodeUTF8))
        item4.setText(1,"")

        item5 = QtGui.QTreeWidgetItem(item4)
        item5.setText(0,QtGui.QApplication.translate("MainWindow", "prescheduled_events", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item5.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item6 = QtGui.QTreeWidgetItem(item4)
        item6.setText(0,QtGui.QApplication.translate("MainWindow", "events_coordinator", None, QtGui.QApplication.UnicodeUTF8))
        item6.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item6.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item7 = QtGui.QTreeWidgetItem(item4)
        item7.setText(0,QtGui.QApplication.translate("MainWindow", "residential_land_share_model", None, QtGui.QApplication.UnicodeUTF8))
        item7.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item7.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item8 = QtGui.QTreeWidgetItem(item4)
        item8.setText(0,QtGui.QApplication.translate("MainWindow", "land_price_model", None, QtGui.QApplication.UnicodeUTF8))
        item8.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item8.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item9 = QtGui.QTreeWidgetItem(item4)
        item9.setText(0,QtGui.QApplication.translate("MainWindow", "development_project_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item9.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item9.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item10 = QtGui.QTreeWidgetItem(item4)
        item10.setText(0,QtGui.QApplication.translate("MainWindow", "residential_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item10.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item10.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item11 = QtGui.QTreeWidgetItem(item4)
        item11.setText(0,QtGui.QApplication.translate("MainWindow", "commercial_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item11.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item11.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item12 = QtGui.QTreeWidgetItem(item4)
        item12.setText(0,QtGui.QApplication.translate("MainWindow", "industriall_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item12.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item12.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item13 = QtGui.QTreeWidgetItem(item4)
        item13.setText(0,QtGui.QApplication.translate("MainWindow", "development_event_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item13.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item13.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item14 = QtGui.QTreeWidgetItem(item4)
        item14.setText(0,QtGui.QApplication.translate("MainWindow", "events_coordinator", None, QtGui.QApplication.UnicodeUTF8))
        item14.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item14.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item15 = QtGui.QTreeWidgetItem(item4)
        item15.setText(0,QtGui.QApplication.translate("MainWindow", "residential_land_share_model", None, QtGui.QApplication.UnicodeUTF8))
        item15.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item15.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item16 = QtGui.QTreeWidgetItem(item4)
        item16.setText(0,QtGui.QApplication.translate("MainWindow", "household_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item16.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item16.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item17 = QtGui.QTreeWidgetItem(item4)
        item17.setText(0,QtGui.QApplication.translate("MainWindow", "employment_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item17.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item17.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item18 = QtGui.QTreeWidgetItem(item4)
        item18.setText(0,QtGui.QApplication.translate("MainWindow", "household_relocation_model", None, QtGui.QApplication.UnicodeUTF8))
        item18.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item18.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item19 = QtGui.QTreeWidgetItem(item4)
        item19.setText(0,QtGui.QApplication.translate("MainWindow", "household_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item19.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item19.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item20 = QtGui.QTreeWidgetItem(item4)
        item20.setText(0,QtGui.QApplication.translate("MainWindow", "employment_relocation_model", None, QtGui.QApplication.UnicodeUTF8))
        item20.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item20.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item21 = QtGui.QTreeWidgetItem(item4)
        item21.setText(0,QtGui.QApplication.translate("MainWindow", "employment_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item21.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item21.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item22 = QtGui.QTreeWidgetItem(item4)
        item22.setText(0,QtGui.QApplication.translate("MainWindow", "distribute_unplaced_jobs_model", None, QtGui.QApplication.UnicodeUTF8))
        item22.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item22.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item23 = QtGui.QTreeWidgetItem(self.modelmanager_tree)
        item23.setText(0,QtGui.QApplication.translate("MainWindow", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        item23.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item23.setText(1,"")

        item24 = QtGui.QTreeWidgetItem(item23)
        item24.setText(0,QtGui.QApplication.translate("MainWindow", "Parcel based", None, QtGui.QApplication.UnicodeUTF8))
        item24.setText(1,"")

        item25 = QtGui.QTreeWidgetItem(item24)
        item25.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_households", None, QtGui.QApplication.UnicodeUTF8))
        item25.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item25.setText(1,"")

        item26 = QtGui.QTreeWidgetItem(item24)
        item26.setText(0,QtGui.QApplication.translate("MainWindow", "housing_value", None, QtGui.QApplication.UnicodeUTF8))
        item26.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item26.setText(1,"")

        item27 = QtGui.QTreeWidgetItem(item24)
        item27.setText(0,QtGui.QApplication.translate("MainWindow", "travel_time_to_cbd", None, QtGui.QApplication.UnicodeUTF8))
        item27.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item27.setText(1,"")

        item28 = QtGui.QTreeWidgetItem(item23)
        item28.setText(0,QtGui.QApplication.translate("MainWindow", "TAZ based", None, QtGui.QApplication.UnicodeUTF8))
        item28.setText(1,"")

        item29 = QtGui.QTreeWidgetItem(item28)
        item29.setText(0,QtGui.QApplication.translate("MainWindow", "average_land_value", None, QtGui.QApplication.UnicodeUTF8))
        item29.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item29.setText(1,"")

        item30 = QtGui.QTreeWidgetItem(item28)
        item30.setText(0,QtGui.QApplication.translate("MainWindow", "average_income", None, QtGui.QApplication.UnicodeUTF8))
        item30.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item30.setText(1,"")

        item31 = QtGui.QTreeWidgetItem(item28)
        item31.setText(0,QtGui.QApplication.translate("MainWindow", "average_household_size", None, QtGui.QApplication.UnicodeUTF8))
        item31.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item31.setText(1,"")

        item32 = QtGui.QTreeWidgetItem(item28)
        item32.setText(0,QtGui.QApplication.translate("MainWindow", "commercial_sqft", None, QtGui.QApplication.UnicodeUTF8))
        item32.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item32.setText(1,"")

        item33 = QtGui.QTreeWidgetItem(item28)
        item33.setText(0,QtGui.QApplication.translate("MainWindow", "jobs_per_acre", None, QtGui.QApplication.UnicodeUTF8))
        item33.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item33.setText(1,"")

        item34 = QtGui.QTreeWidgetItem(item28)
        item34.setText(0,QtGui.QApplication.translate("MainWindow", "population", None, QtGui.QApplication.UnicodeUTF8))
        item34.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item34.setText(1,"")

        item35 = QtGui.QTreeWidgetItem(item28)
        item35.setText(0,QtGui.QApplication.translate("MainWindow", "population_per_acre", None, QtGui.QApplication.UnicodeUTF8))
        item35.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item35.setText(1,"")

        item36 = QtGui.QTreeWidgetItem(item23)
        item36.setText(0,QtGui.QApplication.translate("MainWindow", "RAZ based", None, QtGui.QApplication.UnicodeUTF8))
        item36.setText(1,"")

        item37 = QtGui.QTreeWidgetItem(item23)
        item37.setText(0,QtGui.QApplication.translate("MainWindow", "Census based", None, QtGui.QApplication.UnicodeUTF8))
        item37.setText(1,"")

        item38 = QtGui.QTreeWidgetItem(self.modelmanager_tree)
        item38.setText(0,QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        item38.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item38.setText(1,"")

        item39 = QtGui.QTreeWidgetItem(item38)
        item39.setText(0,QtGui.QApplication.translate("MainWindow", "Choice models", None, QtGui.QApplication.UnicodeUTF8))
        item39.setText(1,"")

        item40 = QtGui.QTreeWidgetItem(item39)
        item40.setText(0,QtGui.QApplication.translate("MainWindow", "household_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item40.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item40.setText(1,"")

        item41 = QtGui.QTreeWidgetItem(item39)
        item41.setText(0,QtGui.QApplication.translate("MainWindow", "employment_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item41.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item41.setText(1,"")

        item42 = QtGui.QTreeWidgetItem(item38)
        item42.setText(0,QtGui.QApplication.translate("MainWindow", "Regression models", None, QtGui.QApplication.UnicodeUTF8))
        item42.setText(1,"")

        item43 = QtGui.QTreeWidgetItem(item42)
        item43.setText(0,QtGui.QApplication.translate("MainWindow", "land_price_model", None, QtGui.QApplication.UnicodeUTF8))
        item43.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item43.setText(1,"")

        item44 = QtGui.QTreeWidgetItem(item43)
        item44.setText(0,QtGui.QApplication.translate("MainWindow", "Specification", None, QtGui.QApplication.UnicodeUTF8))
        item44.setText(1,"")

        item45 = QtGui.QTreeWidgetItem(item38)
        item45.setText(0,QtGui.QApplication.translate("MainWindow", "Travel model connections", None, QtGui.QApplication.UnicodeUTF8))
        item45.setText(1,"")

        item46 = QtGui.QTreeWidgetItem(item45)
        item46.setText(0,QtGui.QApplication.translate("MainWindow", "EMME/2", None, QtGui.QApplication.UnicodeUTF8))
        item46.setIcon(0,QtGui.QIcon(":/Images/Images/car.png"))
        item46.setText(1,"")

        item47 = QtGui.QTreeWidgetItem(item45)
        item47.setText(0,QtGui.QApplication.translate("MainWindow", "TransCAD", None, QtGui.QApplication.UnicodeUTF8))
        item47.setIcon(0,QtGui.QIcon(":/Images/Images/car.png"))
        item47.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsmanager_tree.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsmanager_tree.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.resultsmanager_tree.clear()

        item48 = QtGui.QTreeWidgetItem(self.resultsmanager_tree)
        item48.setText(0,QtGui.QApplication.translate("MainWindow", "Indicator sets", None, QtGui.QApplication.UnicodeUTF8))
        item48.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item48.setText(1,"")

        item49 = QtGui.QTreeWidgetItem(item48)
        item49.setText(0,QtGui.QApplication.translate("MainWindow", "standard_indicator_set", None, QtGui.QApplication.UnicodeUTF8))
        item49.setIcon(0,QtGui.QIcon(":/Images/Images/table_multiple.png"))
        item49.setText(1,"")

        item50 = QtGui.QTreeWidgetItem(item49)
        item50.setText(0,QtGui.QApplication.translate("MainWindow", "Tables", None, QtGui.QApplication.UnicodeUTF8))
        item50.setText(1,"")

        item51 = QtGui.QTreeWidgetItem(item50)
        item51.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_new_units_by_parcel", None, QtGui.QApplication.UnicodeUTF8))
        item51.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item51.setText(1,QtGui.QApplication.translate("MainWindow", "2015", None, QtGui.QApplication.UnicodeUTF8))

        item52 = QtGui.QTreeWidgetItem(item50)
        item52.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_service_jobs_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item52.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item52.setText(1,QtGui.QApplication.translate("MainWindow", "2020", None, QtGui.QApplication.UnicodeUTF8))

        item53 = QtGui.QTreeWidgetItem(item49)
        item53.setText(0,QtGui.QApplication.translate("MainWindow", "Charts", None, QtGui.QApplication.UnicodeUTF8))
        item53.setText(1,"")

        item54 = QtGui.QTreeWidgetItem(item53)
        item54.setText(0,QtGui.QApplication.translate("MainWindow", "total_population", None, QtGui.QApplication.UnicodeUTF8))
        item54.setIcon(0,QtGui.QIcon(":/Images/Images/chart_bar.png"))
        item54.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item55 = QtGui.QTreeWidgetItem(item49)
        item55.setText(0,QtGui.QApplication.translate("MainWindow", "Maps", None, QtGui.QApplication.UnicodeUTF8))
        item55.setText(1,"")

        item56 = QtGui.QTreeWidgetItem(item55)
        item56.setText(0,QtGui.QApplication.translate("MainWindow", "population_density_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item56.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item56.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item57 = QtGui.QTreeWidgetItem(item55)
        item57.setText(0,QtGui.QApplication.translate("MainWindow", "jobs_per_acre_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item57.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item57.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item58 = QtGui.QTreeWidgetItem(item55)
        item58.setText(0,QtGui.QApplication.translate("MainWindow", "population_change_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item58.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item58.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2015", None, QtGui.QApplication.UnicodeUTF8))

        item59 = QtGui.QTreeWidgetItem(item48)
        item59.setText(0,QtGui.QApplication.translate("MainWindow", "indicator_set_working", None, QtGui.QApplication.UnicodeUTF8))
        item59.setIcon(0,QtGui.QIcon(":/Images/Images/table_multiple.png"))
        item59.setText(1,"")

        item60 = QtGui.QTreeWidgetItem(item59)
        item60.setText(0,QtGui.QApplication.translate("MainWindow", "Tables", None, QtGui.QApplication.UnicodeUTF8))
        item60.setText(1,"")

        item61 = QtGui.QTreeWidgetItem(item59)
        item61.setText(0,QtGui.QApplication.translate("MainWindow", "Charts", None, QtGui.QApplication.UnicodeUTF8))
        item61.setText(1,"")

        item62 = QtGui.QTreeWidgetItem(item59)
        item62.setText(0,QtGui.QApplication.translate("MainWindow", "Maps", None, QtGui.QApplication.UnicodeUTF8))
        item62.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_editorView), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapView), QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.pythonLabel.setText(QtGui.QApplication.translate("MainWindow", ">>>", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_pythonView), QtGui.QApplication.translate("MainWindow", "Python Console", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_logView), QtGui.QApplication.translate("MainWindow", "Log View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuMap.setTitle(QtGui.QApplication.translate("MainWindow", "Map", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.menuUtilities.setTitle(QtGui.QApplication.translate("MainWindow", "Utilities", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Project.setText(QtGui.QApplication.translate("MainWindow", "Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project.setText(QtGui.QApplication.translate("MainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Project_As.setText(QtGui.QApplication.translate("MainWindow", "Save Project As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Config.setText(QtGui.QApplication.translate("MainWindow", "Open Config", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Config.setText(QtGui.QApplication.translate("MainWindow", "Save Config", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_Config_As.setText(QtGui.QApplication.translate("MainWindow", "Save Config As...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun_Manager.setText(QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc
