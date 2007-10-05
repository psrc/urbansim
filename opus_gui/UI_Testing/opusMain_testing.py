# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'opusMain_testing.ui'
#
# Created: Mon Oct 01 15:37:18 2007
#      by: PyQt4 UI code generator 4-snapshot-20070727
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import os, sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,950,991).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setFrameShape(QtGui.QFrame.NoFrame)
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
        self.datamanager_page.setGeometry(QtCore.QRect(0,0,529,821))
        self.datamanager_page.setObjectName("datamanager_page")

        self.gridlayout1 = QtGui.QGridLayout(self.datamanager_page)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.treeWidget_2 = QtGui.QTreeWidget(self.datamanager_page)
        self.treeWidget_2.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.gridlayout1.addWidget(self.treeWidget_2,0,0,1,1)
        self.toolBox.addItem(self.datamanager_page,"")

        self.modelmanager_page = QtGui.QWidget()
        self.modelmanager_page.setGeometry(QtCore.QRect(0,0,529,821))
        self.modelmanager_page.setObjectName("modelmanager_page")

        self.gridlayout2 = QtGui.QGridLayout(self.modelmanager_page)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.treeWidget_3 = QtGui.QTreeWidget(self.modelmanager_page)
        self.treeWidget_3.setObjectName("treeWidget_3")
        self.gridlayout2.addWidget(self.treeWidget_3,0,0,1,1)
        self.toolBox.addItem(self.modelmanager_page,"")

        self.runmanager_page = QtGui.QWidget()
        self.runmanager_page.setGeometry(QtCore.QRect(0,0,98,80))
        self.runmanager_page.setObjectName("runmanager_page")

        self.gridlayout3 = QtGui.QGridLayout(self.runmanager_page)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.treeWidget_4 = QtGui.QTreeWidget(self.runmanager_page)
        self.treeWidget_4.setObjectName("treeWidget_4")
        self.gridlayout3.addWidget(self.treeWidget_4,0,0,1,1)
        self.toolBox.addItem(self.runmanager_page,"")

        self.resultsmanager_page = QtGui.QWidget()
        self.resultsmanager_page.setGeometry(QtCore.QRect(0,0,98,80))
        self.resultsmanager_page.setObjectName("resultsmanager_page")

        self.gridlayout4 = QtGui.QGridLayout(self.resultsmanager_page)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.treeWidget_5 = QtGui.QTreeWidget(self.resultsmanager_page)
        self.treeWidget_5.setObjectName("treeWidget_5")
        self.gridlayout4.addWidget(self.treeWidget_5,0,0,1,1)
        self.toolBox.addItem(self.resultsmanager_page,"")

        self.tabWidget = QtGui.QTabWidget(self.splitter)
        self.tabWidget.setObjectName("tabWidget")

        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab,"")

        self.tab_mapView = QtGui.QWidget()
        self.tab_mapView.setObjectName("tab_mapView")

        self.gridlayout5 = QtGui.QGridLayout(self.tab_mapView)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.widgetMap = QtGui.QWidget(self.tab_mapView)
        self.widgetMap.setMinimumSize(QtCore.QSize(100,100))
        self.widgetMap.setAutoFillBackground(True)
        self.widgetMap.setObjectName("widgetMap")
        self.gridlayout5.addWidget(self.widgetMap,0,0,1,1)
        self.tabWidget.addTab(self.tab_mapView,"")

        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3,"")
        self.gridlayout.addWidget(self.splitter,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,950,21))
        self.menubar.setObjectName("menubar")

        self.menuProject = QtGui.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.mpActionZoomOut = QtGui.QAction(MainWindow)
        self.mpActionZoomOut.setObjectName("mpActionZoomOut")

        self.mpActionPan = QtGui.QAction(MainWindow)
        self.mpActionPan.setObjectName("mpActionPan")

        self.mpActionAddRasterLayer = QtGui.QAction(MainWindow)
        self.mpActionAddRasterLayer.setObjectName("mpActionAddRasterLayer")

        self.mpActionZoomIn = QtGui.QAction(MainWindow)
        self.mpActionZoomIn.setObjectName("mpActionZoomIn")

        self.mpActionAddVectorLayer = QtGui.QAction(MainWindow)
        self.mpActionAddVectorLayer.setObjectName("mpActionAddVectorLayer")
        self.menuProject.addSeparator()
        self.menuProject.addSeparator()
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.treeWidget_2,QtCore.SIGNAL("customContextMenuRequested(QPoint)"),self.someContextMenu)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def someContextMenu(self,pos):
        # Get mouse position:
        cursor_position = QtGui.QCursor.pos()
        # Get item at position
        itm = self.treeWidget_2.itemAt(QtGui.QCursor.pos())
        # Build menu:
        menu = QtGui.QMenu()
        action = menu.addAction("Open Calculator")
        action.setObjectName("open_calc")
        action = menu.addAction("Open Notepad")
        action.setObjectName("open_notepad")
        action = menu.addAction("Message box")
        action.setObjectName("message_box")
        # Set up signal
        menu.connect(menu, QtCore.SIGNAL("triggered ( QAction * )"), self.someContextMenuTriggered)
        # Open menu at cursor position:
        menu.exec_(cursor_position)

    def someContextMenuTriggered(self, action):
        cmd = action.objectName()
        if cmd == 'open_calc':
            self.openCalculator()
        elif cmd == 'open_notepad':
            self.openNotepad()
        elif cmd == 'message_box':
            self.messageBox()

    def messageBox(self):
        QtGui.QMessageBox.information(None, 'b', 'e')
        
    def openCalculator(self):
        os.system('calc')

    def openNotepad(self):
        os.system('notepad')

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpusGui", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_2.clear()

        item = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item.setText(0,QtGui.QApplication.translate("MainWindow", "Database Server Connections", None, QtGui.QApplication.UnicodeUTF8))
        item.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item.setText(1,"")

        item1 = QtGui.QTreeWidgetItem(item)
        item1.setText(0,QtGui.QApplication.translate("MainWindow", "trondhem", None, QtGui.QApplication.UnicodeUTF8))
        item1.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item1.setText(1,QtGui.QApplication.translate("MainWindow", "MySQL", None, QtGui.QApplication.UnicodeUTF8))
        
        item2 = QtGui.QTreeWidgetItem(item)
        item2.setText(0,QtGui.QApplication.translate("MainWindow", "aarhus01", None, QtGui.QApplication.UnicodeUTF8))
        item2.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item2.setText(1,QtGui.QApplication.translate("MainWindow", "PostGRES", None, QtGui.QApplication.UnicodeUTF8))

        item3 = QtGui.QTreeWidgetItem(item)
        item3.setText(0,QtGui.QApplication.translate("MainWindow", "aarhus02", None, QtGui.QApplication.UnicodeUTF8))
        item3.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item3.setText(1,QtGui.QApplication.translate("MainWindow", "MSSQL", None, QtGui.QApplication.UnicodeUTF8))

        item4 = QtGui.QTreeWidgetItem(item)
        item4.setText(0,QtGui.QApplication.translate("MainWindow", "aarhus03", None, QtGui.QApplication.UnicodeUTF8))
        item4.setIcon(0,QtGui.QIcon(":/Images/Images/database_link.png"))
        item4.setText(1,QtGui.QApplication.translate("MainWindow", "ArcSDE", None, QtGui.QApplication.UnicodeUTF8))

        item5 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item5.setText(0,QtGui.QApplication.translate("MainWindow", "Databases", None, QtGui.QApplication.UnicodeUTF8))
        item5.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item5.setText(1,"")

        item6 = QtGui.QTreeWidgetItem(item5)
        item6.setText(0,QtGui.QApplication.translate("MainWindow", "base_year_db", None, QtGui.QApplication.UnicodeUTF8))
        item6.setIcon(0,QtGui.QIcon(":/Images/Images/database.png"))
        item6.setText(1,QtGui.QApplication.translate("MainWindow", "database", None, QtGui.QApplication.UnicodeUTF8))

        item7 = QtGui.QTreeWidgetItem(item6)
        item7.setText(0,QtGui.QApplication.translate("MainWindow", "parcels", None, QtGui.QApplication.UnicodeUTF8))
        item7.setIcon(0,QtGui.QIcon(":/Images/Images/database_table.png"))
        item7.setText(1,QtGui.QApplication.translate("MainWindow", "table", None, QtGui.QApplication.UnicodeUTF8))

        item8 = QtGui.QTreeWidgetItem(item7)
        item8.setText(0,QtGui.QApplication.translate("MainWindow", "assessor_parcel_id", None, QtGui.QApplication.UnicodeUTF8))
        item8.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item8.setText(1,QtGui.QApplication.translate("MainWindow", "string", None, QtGui.QApplication.UnicodeUTF8))

        item9 = QtGui.QTreeWidgetItem(item7)
        item9.setText(0,QtGui.QApplication.translate("MainWindow", "improvement_value", None, QtGui.QApplication.UnicodeUTF8))
        item9.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item9.setText(1,QtGui.QApplication.translate("MainWindow", "integer", None, QtGui.QApplication.UnicodeUTF8))

        item10 = QtGui.QTreeWidgetItem(item7)
        item10.setText(0,QtGui.QApplication.translate("MainWindow", "parcel_id", None, QtGui.QApplication.UnicodeUTF8))
        item10.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item10.setText(1,QtGui.QApplication.translate("MainWindow", "integer", None, QtGui.QApplication.UnicodeUTF8))

        item11 = QtGui.QTreeWidgetItem(item6)
        item11.setText(0,QtGui.QApplication.translate("MainWindow", "jobs", None, QtGui.QApplication.UnicodeUTF8))
        item11.setIcon(0,QtGui.QIcon(":/Images/Images/database_table.png"))
        item11.setText(1,QtGui.QApplication.translate("MainWindow", "table", None, QtGui.QApplication.UnicodeUTF8))

        item12 = QtGui.QTreeWidgetItem(item6)
        item12.setText(0,QtGui.QApplication.translate("MainWindow", "buildings", None, QtGui.QApplication.UnicodeUTF8))
        item12.setIcon(0,QtGui.QIcon(":/Images/Images/database_table.png"))
        item12.setText(1,QtGui.QApplication.translate("MainWindow", "table", None, QtGui.QApplication.UnicodeUTF8))

        item13 = QtGui.QTreeWidgetItem(item5)
        item13.setText(0,QtGui.QApplication.translate("MainWindow", "scenario01_db", None, QtGui.QApplication.UnicodeUTF8))
        item13.setIcon(0,QtGui.QIcon(":/Images/Images/database.png"))
        item13.setText(1,QtGui.QApplication.translate("MainWindow", "database", None, QtGui.QApplication.UnicodeUTF8))

        item14 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item14.setText(0,QtGui.QApplication.translate("MainWindow", "OPUS Data", None, QtGui.QApplication.UnicodeUTF8))
        item14.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item14.setText(1,"")

        item15 = QtGui.QTreeWidgetItem(item14)
        item15.setText(0,QtGui.QApplication.translate("MainWindow", "D:\\opus_data", None, QtGui.QApplication.UnicodeUTF8))
        item15.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item15.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item16 = QtGui.QTreeWidgetItem(item15)
        item16.setText(0,QtGui.QApplication.translate("MainWindow", "Scenario01", None, QtGui.QApplication.UnicodeUTF8))
        item16.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item16.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item17 = QtGui.QTreeWidgetItem(item16)
        item17.setText(0,QtGui.QApplication.translate("MainWindow", "2000", None, QtGui.QApplication.UnicodeUTF8))
        item17.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item17.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item18 = QtGui.QTreeWidgetItem(item17)
        item18.setText(0,QtGui.QApplication.translate("MainWindow", "parcels", None, QtGui.QApplication.UnicodeUTF8))
        item18.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item18.setText(1,QtGui.QApplication.translate("MainWindow", "dataset", None, QtGui.QApplication.UnicodeUTF8))

        item19 = QtGui.QTreeWidgetItem(item18)
        item19.setText(0,QtGui.QApplication.translate("MainWindow", "improvement_value", None, QtGui.QApplication.UnicodeUTF8))
        item19.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item19.setText(1,QtGui.QApplication.translate("MainWindow", "array:integer", None, QtGui.QApplication.UnicodeUTF8))

        item20 = QtGui.QTreeWidgetItem(item18)
        item20.setText(0,QtGui.QApplication.translate("MainWindow", "parcel_id", None, QtGui.QApplication.UnicodeUTF8))
        item20.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item20.setText(1,QtGui.QApplication.translate("MainWindow", "array:integer", None, QtGui.QApplication.UnicodeUTF8))

        item21 = QtGui.QTreeWidgetItem(item18)
        item21.setText(0,QtGui.QApplication.translate("MainWindow", "assessor_parcel_id", None, QtGui.QApplication.UnicodeUTF8))
        item21.setIcon(0,QtGui.QIcon(":/Images/Images/table_lightning.png"))
        item21.setText(1,QtGui.QApplication.translate("MainWindow", "array:string", None, QtGui.QApplication.UnicodeUTF8))

        item22 = QtGui.QTreeWidgetItem(item17)
        item22.setText(0,QtGui.QApplication.translate("MainWindow", "buildings", None, QtGui.QApplication.UnicodeUTF8))
        item22.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item22.setText(1,QtGui.QApplication.translate("MainWindow", "dataset", None, QtGui.QApplication.UnicodeUTF8))

        item23 = QtGui.QTreeWidgetItem(item17)
        item23.setText(0,QtGui.QApplication.translate("MainWindow", "households", None, QtGui.QApplication.UnicodeUTF8))
        item23.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item23.setText(1,QtGui.QApplication.translate("MainWindow", "dataset", None, QtGui.QApplication.UnicodeUTF8))

        item24 = QtGui.QTreeWidgetItem(item17)
        item24.setText(0,QtGui.QApplication.translate("MainWindow", "jobs", None, QtGui.QApplication.UnicodeUTF8))
        item24.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item24.setText(1,QtGui.QApplication.translate("MainWindow", "dataset", None, QtGui.QApplication.UnicodeUTF8))

        item25 = QtGui.QTreeWidgetItem(item16)
        item25.setText(0,QtGui.QApplication.translate("MainWindow", "2001", None, QtGui.QApplication.UnicodeUTF8))
        item25.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item25.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item26 = QtGui.QTreeWidgetItem(item16)
        item26.setText(0,QtGui.QApplication.translate("MainWindow", "2002", None, QtGui.QApplication.UnicodeUTF8))
        item26.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item26.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item27 = QtGui.QTreeWidgetItem(item15)
        item27.setText(0,QtGui.QApplication.translate("MainWindow", "Scenario02", None, QtGui.QApplication.UnicodeUTF8))
        item27.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item27.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item28 = QtGui.QTreeWidgetItem(item14)
        item28.setText(0,QtGui.QApplication.translate("MainWindow", "X:\\opus_data_archive", None, QtGui.QApplication.UnicodeUTF8))
        item28.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item28.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item29 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item29.setText(0,QtGui.QApplication.translate("MainWindow", "Other Data", None, QtGui.QApplication.UnicodeUTF8))
        item29.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item29.setText(1,"")

        item30 = QtGui.QTreeWidgetItem(item29)
        item30.setText(0,QtGui.QApplication.translate("MainWindow", "C:\\shapefiles", None, QtGui.QApplication.UnicodeUTF8))
        item30.setIcon(0,QtGui.QIcon(":/Images/Images/folder.png"))
        item30.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item31 = QtGui.QTreeWidgetItem(item30)
        item31.setText(0,QtGui.QApplication.translate("MainWindow", "zones.shp", None, QtGui.QApplication.UnicodeUTF8))
        item31.setIcon(0,QtGui.QIcon(":/Images/Images/layers.png"))
        item31.setText(1,QtGui.QApplication.translate("MainWindow", "shapefile", None, QtGui.QApplication.UnicodeUTF8))

        item32 = QtGui.QTreeWidgetItem(item30)
        item32.setText(0,QtGui.QApplication.translate("MainWindow", "arterials.shp", None, QtGui.QApplication.UnicodeUTF8))
        item32.setIcon(0,QtGui.QIcon(":/Images/Images/layers.png"))
        item32.setText(1,QtGui.QApplication.translate("MainWindow", "shapefile", None, QtGui.QApplication.UnicodeUTF8))

        item33 = QtGui.QTreeWidgetItem(item29)
        item33.setText(0,QtGui.QApplication.translate("MainWindow", "D:\\working", None, QtGui.QApplication.UnicodeUTF8))
        item33.setText(1,QtGui.QApplication.translate("MainWindow", "directory", None, QtGui.QApplication.UnicodeUTF8))

        item34 = QtGui.QTreeWidgetItem(item33)
        item34.setText(0,QtGui.QApplication.translate("MainWindow", "census_sf3_data.csv", None, QtGui.QApplication.UnicodeUTF8))
        item34.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item34.setText(1,QtGui.QApplication.translate("MainWindow", "delimited table", None, QtGui.QApplication.UnicodeUTF8))

        item35 = QtGui.QTreeWidgetItem(item33)
        item35.setText(0,QtGui.QApplication.translate("MainWindow", "data_table.txt", None, QtGui.QApplication.UnicodeUTF8))
        item35.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item35.setText(1,QtGui.QApplication.translate("MainWindow", "delimited table", None, QtGui.QApplication.UnicodeUTF8))

        item36 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item36.setText(0,QtGui.QApplication.translate("MainWindow", "Data Processing", None, QtGui.QApplication.UnicodeUTF8))
        item36.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item36.setText(1,"")

        item37 = QtGui.QTreeWidgetItem(item36)
        item37.setText(0,QtGui.QApplication.translate("MainWindow", "ProcessingSequence01", None, QtGui.QApplication.UnicodeUTF8))
        item37.setText(1,"")

        item38 = QtGui.QTreeWidgetItem(item37)
        item38.setText(0,QtGui.QApplication.translate("MainWindow", "Query01", None, QtGui.QApplication.UnicodeUTF8))
        item38.setIcon(0,QtGui.QIcon(":/Images/Images/table_go.png"))
        item38.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item39 = QtGui.QTreeWidgetItem(item37)
        item39.setText(0,QtGui.QApplication.translate("MainWindow", "Query02", None, QtGui.QApplication.UnicodeUTF8))
        item39.setIcon(0,QtGui.QIcon(":/Images/Images/table_go.png"))
        item39.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item40 = QtGui.QTreeWidgetItem(item37)
        item40.setText(0,QtGui.QApplication.translate("MainWindow", "PythonScript01", None, QtGui.QApplication.UnicodeUTF8))
        item40.setIcon(0,QtGui.QIcon(":/Images/Images/python_script.png"))
        item40.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item41 = QtGui.QTreeWidgetItem(item37)
        item41.setText(0,QtGui.QApplication.translate("MainWindow", "Test01", None, QtGui.QApplication.UnicodeUTF8))
        item41.setIcon(0,QtGui.QIcon(":/Images/Images/python_script.png"))
        item41.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item42 = QtGui.QTreeWidgetItem(item37)
        item42.setText(0,QtGui.QApplication.translate("MainWindow", "Geoprocessing01", None, QtGui.QApplication.UnicodeUTF8))
        item42.setIcon(0,QtGui.QIcon(":/Images/Images/map_go.png"))
        item42.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item43 = QtGui.QTreeWidgetItem(item37)
        item43.setText(0,QtGui.QApplication.translate("MainWindow", "Test02", None, QtGui.QApplication.UnicodeUTF8))
        item43.setIcon(0,QtGui.QIcon(":/Images/Images/python_script.png"))
        item43.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item44 = QtGui.QTreeWidgetItem(item36)
        item44.setText(0,QtGui.QApplication.translate("MainWindow", "ProcessingSequence02", None, QtGui.QApplication.UnicodeUTF8))
        item44.setText(1,"")

        item45 = QtGui.QTreeWidgetItem(self.treeWidget_2)
        item45.setText(0,QtGui.QApplication.translate("MainWindow", "Schemas", None, QtGui.QApplication.UnicodeUTF8))
        item45.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item45.setText(1,"")

        item46 = QtGui.QTreeWidgetItem(item45)
        item46.setText(0,QtGui.QApplication.translate("MainWindow", "Schema01", None, QtGui.QApplication.UnicodeUTF8))
        item46.setIcon(0,QtGui.QIcon(":/Images/Images/chart_organisation.png"))
        item46.setText(1,"")

        item47 = QtGui.QTreeWidgetItem(item45)
        item47.setText(0,QtGui.QApplication.translate("MainWindow", "Schema02", None, QtGui.QApplication.UnicodeUTF8))
        item47.setIcon(0,QtGui.QIcon(":/Images/Images/chart_organisation.png"))
        item47.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.datamanager_page), QtGui.QApplication.translate("MainWindow", "Data Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_3.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_3.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_3.clear()

        item48 = QtGui.QTreeWidgetItem(self.treeWidget_3)
        item48.setText(0,QtGui.QApplication.translate("MainWindow", "Model System Configurations", None, QtGui.QApplication.UnicodeUTF8))
        item48.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item48.setText(1,"")

        item49 = QtGui.QTreeWidgetItem(item48)
        item49.setText(0,QtGui.QApplication.translate("MainWindow", "base_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item49.setText(1,"")

        item50 = QtGui.QTreeWidgetItem(item49)
        item50.setText(0,QtGui.QApplication.translate("MainWindow", "urbansim_base_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item50.setText(1,"")

        item51 = QtGui.QTreeWidgetItem(item50)
        item51.setText(0,QtGui.QApplication.translate("MainWindow", "base_year", None, QtGui.QApplication.UnicodeUTF8))
        item51.setText(1,QtGui.QApplication.translate("MainWindow", "2005", None, QtGui.QApplication.UnicodeUTF8))

        item52 = QtGui.QTreeWidgetItem(item50)
        item52.setText(0,QtGui.QApplication.translate("MainWindow", "models", None, QtGui.QApplication.UnicodeUTF8))
        item52.setText(1,"")

        item53 = QtGui.QTreeWidgetItem(item52)
        item53.setText(0,QtGui.QApplication.translate("MainWindow", "prescheduled_events", None, QtGui.QApplication.UnicodeUTF8))
        item53.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item53.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item54 = QtGui.QTreeWidgetItem(item52)
        item54.setText(0,QtGui.QApplication.translate("MainWindow", "events_coordinator", None, QtGui.QApplication.UnicodeUTF8))
        item54.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item54.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item55 = QtGui.QTreeWidgetItem(item52)
        item55.setText(0,QtGui.QApplication.translate("MainWindow", "residential_land_share_model", None, QtGui.QApplication.UnicodeUTF8))
        item55.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item55.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item56 = QtGui.QTreeWidgetItem(item52)
        item56.setText(0,QtGui.QApplication.translate("MainWindow", "land_price_model", None, QtGui.QApplication.UnicodeUTF8))
        item56.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item56.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item57 = QtGui.QTreeWidgetItem(item52)
        item57.setText(0,QtGui.QApplication.translate("MainWindow", "development_project_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item57.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item57.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item58 = QtGui.QTreeWidgetItem(item52)
        item58.setText(0,QtGui.QApplication.translate("MainWindow", "residential_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item58.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item58.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item59 = QtGui.QTreeWidgetItem(item52)
        item59.setText(0,QtGui.QApplication.translate("MainWindow", "commercial_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item59.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item59.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item60 = QtGui.QTreeWidgetItem(item52)
        item60.setText(0,QtGui.QApplication.translate("MainWindow", "industriall_development_project_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item60.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item60.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item61 = QtGui.QTreeWidgetItem(item52)
        item61.setText(0,QtGui.QApplication.translate("MainWindow", "development_event_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item61.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item61.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item62 = QtGui.QTreeWidgetItem(item52)
        item62.setText(0,QtGui.QApplication.translate("MainWindow", "events_coordinator", None, QtGui.QApplication.UnicodeUTF8))
        item62.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item62.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item63 = QtGui.QTreeWidgetItem(item52)
        item63.setText(0,QtGui.QApplication.translate("MainWindow", "residential_land_share_model", None, QtGui.QApplication.UnicodeUTF8))
        item63.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item63.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item64 = QtGui.QTreeWidgetItem(item52)
        item64.setText(0,QtGui.QApplication.translate("MainWindow", "household_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item64.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item64.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item65 = QtGui.QTreeWidgetItem(item52)
        item65.setText(0,QtGui.QApplication.translate("MainWindow", "employment_transition_model", None, QtGui.QApplication.UnicodeUTF8))
        item65.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item65.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item66 = QtGui.QTreeWidgetItem(item52)
        item66.setText(0,QtGui.QApplication.translate("MainWindow", "household_relocation_model", None, QtGui.QApplication.UnicodeUTF8))
        item66.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item66.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item67 = QtGui.QTreeWidgetItem(item52)
        item67.setText(0,QtGui.QApplication.translate("MainWindow", "household_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item67.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item67.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item68 = QtGui.QTreeWidgetItem(item52)
        item68.setText(0,QtGui.QApplication.translate("MainWindow", "employment_relocation_model", None, QtGui.QApplication.UnicodeUTF8))
        item68.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item68.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item69 = QtGui.QTreeWidgetItem(item52)
        item69.setText(0,QtGui.QApplication.translate("MainWindow", "employment_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item69.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item69.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item70 = QtGui.QTreeWidgetItem(item52)
        item70.setText(0,QtGui.QApplication.translate("MainWindow", "distribute_unplaced_jobs_model", None, QtGui.QApplication.UnicodeUTF8))
        item70.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item70.setText(1,QtGui.QApplication.translate("MainWindow", "run", None, QtGui.QApplication.UnicodeUTF8))

        item71 = QtGui.QTreeWidgetItem(self.treeWidget_3)
        item71.setText(0,QtGui.QApplication.translate("MainWindow", "Variables", None, QtGui.QApplication.UnicodeUTF8))
        item71.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item71.setText(1,"")

        item72 = QtGui.QTreeWidgetItem(item71)
        item72.setText(0,QtGui.QApplication.translate("MainWindow", "Parcel based", None, QtGui.QApplication.UnicodeUTF8))
        item72.setText(1,"")

        item73 = QtGui.QTreeWidgetItem(item72)
        item73.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_households", None, QtGui.QApplication.UnicodeUTF8))
        item73.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item73.setText(1,"")

        item74 = QtGui.QTreeWidgetItem(item72)
        item74.setText(0,QtGui.QApplication.translate("MainWindow", "housing_value", None, QtGui.QApplication.UnicodeUTF8))
        item74.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item74.setText(1,"")

        item75 = QtGui.QTreeWidgetItem(item72)
        item75.setText(0,QtGui.QApplication.translate("MainWindow", "travel_time_to_cbd", None, QtGui.QApplication.UnicodeUTF8))
        item75.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item75.setText(1,"")

        item76 = QtGui.QTreeWidgetItem(item71)
        item76.setText(0,QtGui.QApplication.translate("MainWindow", "TAZ based", None, QtGui.QApplication.UnicodeUTF8))
        item76.setText(1,"")

        item77 = QtGui.QTreeWidgetItem(item76)
        item77.setText(0,QtGui.QApplication.translate("MainWindow", "average_land_value", None, QtGui.QApplication.UnicodeUTF8))
        item77.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item77.setText(1,"")

        item78 = QtGui.QTreeWidgetItem(item76)
        item78.setText(0,QtGui.QApplication.translate("MainWindow", "average_income", None, QtGui.QApplication.UnicodeUTF8))
        item78.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item78.setText(1,"")

        item79 = QtGui.QTreeWidgetItem(item76)
        item79.setText(0,QtGui.QApplication.translate("MainWindow", "average_household_size", None, QtGui.QApplication.UnicodeUTF8))
        item79.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item79.setText(1,"")

        item80 = QtGui.QTreeWidgetItem(item76)
        item80.setText(0,QtGui.QApplication.translate("MainWindow", "commercial_sqft", None, QtGui.QApplication.UnicodeUTF8))
        item80.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item80.setText(1,"")

        item81 = QtGui.QTreeWidgetItem(item76)
        item81.setText(0,QtGui.QApplication.translate("MainWindow", "jobs_per_acre", None, QtGui.QApplication.UnicodeUTF8))
        item81.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item81.setText(1,"")

        item82 = QtGui.QTreeWidgetItem(item76)
        item82.setText(0,QtGui.QApplication.translate("MainWindow", "population", None, QtGui.QApplication.UnicodeUTF8))
        item82.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item82.setText(1,"")

        item83 = QtGui.QTreeWidgetItem(item76)
        item83.setText(0,QtGui.QApplication.translate("MainWindow", "population_per_acre", None, QtGui.QApplication.UnicodeUTF8))
        item83.setIcon(0,QtGui.QIcon(":/Images/Images/chart_line.png"))
        item83.setText(1,"")

        item84 = QtGui.QTreeWidgetItem(item71)
        item84.setText(0,QtGui.QApplication.translate("MainWindow", "RAZ based", None, QtGui.QApplication.UnicodeUTF8))
        item84.setText(1,"")

        item85 = QtGui.QTreeWidgetItem(item71)
        item85.setText(0,QtGui.QApplication.translate("MainWindow", "Census based", None, QtGui.QApplication.UnicodeUTF8))
        item85.setText(1,"")

        item86 = QtGui.QTreeWidgetItem(self.treeWidget_3)
        item86.setText(0,QtGui.QApplication.translate("MainWindow", "Models", None, QtGui.QApplication.UnicodeUTF8))
        item86.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item86.setText(1,"")

        item87 = QtGui.QTreeWidgetItem(item86)
        item87.setText(0,QtGui.QApplication.translate("MainWindow", "Choice models", None, QtGui.QApplication.UnicodeUTF8))
        item87.setText(1,"")

        item88 = QtGui.QTreeWidgetItem(item87)
        item88.setText(0,QtGui.QApplication.translate("MainWindow", "household_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item88.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item88.setText(1,"")

        item89 = QtGui.QTreeWidgetItem(item87)
        item89.setText(0,QtGui.QApplication.translate("MainWindow", "employment_location_choice_model", None, QtGui.QApplication.UnicodeUTF8))
        item89.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item89.setText(1,"")

        item90 = QtGui.QTreeWidgetItem(item86)
        item90.setText(0,QtGui.QApplication.translate("MainWindow", "Regression models", None, QtGui.QApplication.UnicodeUTF8))
        item90.setText(1,"")

        item91 = QtGui.QTreeWidgetItem(item90)
        item91.setText(0,QtGui.QApplication.translate("MainWindow", "land_price_model", None, QtGui.QApplication.UnicodeUTF8))
        item91.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item91.setText(1,"")

        item92 = QtGui.QTreeWidgetItem(item91)
        item92.setText(0,QtGui.QApplication.translate("MainWindow", "Specification", None, QtGui.QApplication.UnicodeUTF8))
        item92.setText(1,"")

        item93 = QtGui.QTreeWidgetItem(item86)
        item93.setText(0,QtGui.QApplication.translate("MainWindow", "Travel model connections", None, QtGui.QApplication.UnicodeUTF8))
        item93.setText(1,"")

        item94 = QtGui.QTreeWidgetItem(item93)
        item94.setText(0,QtGui.QApplication.translate("MainWindow", "EMME/2", None, QtGui.QApplication.UnicodeUTF8))
        item94.setIcon(0,QtGui.QIcon(":/Images/Images/car.png"))
        item94.setText(1,"")

        item95 = QtGui.QTreeWidgetItem(item93)
        item95.setText(0,QtGui.QApplication.translate("MainWindow", "TransCAD", None, QtGui.QApplication.UnicodeUTF8))
        item95.setIcon(0,QtGui.QIcon(":/Images/Images/car.png"))
        item95.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.modelmanager_page), QtGui.QApplication.translate("MainWindow", "Model Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_4.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_4.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_4.clear()

        item96 = QtGui.QTreeWidgetItem(self.treeWidget_4)
        item96.setText(0,QtGui.QApplication.translate("MainWindow", "scenario_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item96.setText(1,"")

        item97 = QtGui.QTreeWidgetItem(self.treeWidget_4)
        item97.setText(0,QtGui.QApplication.translate("MainWindow", "base_scenario", None, QtGui.QApplication.UnicodeUTF8))
        item97.setIcon(0,QtGui.QIcon(":/Images/Images/accept.png"))
        item97.setText(1,"")

        item98 = QtGui.QTreeWidgetItem(item97)
        item98.setText(0,QtGui.QApplication.translate("MainWindow", "base_year_cache", None, QtGui.QApplication.UnicodeUTF8))
        item98.setIcon(0,QtGui.QIcon(":/Images/Images/folder_database.png"))
        item98.setText(1,QtGui.QApplication.translate("MainWindow", "c:/urbansim_cache/run_962.2006_11_07_08_50", None, QtGui.QApplication.UnicodeUTF8))

        item99 = QtGui.QTreeWidgetItem(item97)
        item99.setText(0,QtGui.QApplication.translate("MainWindow", "years_to_run", None, QtGui.QApplication.UnicodeUTF8))
        item99.setIcon(0,QtGui.QIcon(":/Images/Images/calendar_view_day.png"))
        item99.setText(1,"")

        item100 = QtGui.QTreeWidgetItem(item99)
        item100.setText(0,QtGui.QApplication.translate("MainWindow", "start_year", None, QtGui.QApplication.UnicodeUTF8))
        item100.setText(1,QtGui.QApplication.translate("MainWindow", "2000", None, QtGui.QApplication.UnicodeUTF8))

        item101 = QtGui.QTreeWidgetItem(item99)
        item101.setText(0,QtGui.QApplication.translate("MainWindow", "end_year", None, QtGui.QApplication.UnicodeUTF8))
        item101.setText(1,QtGui.QApplication.translate("MainWindow", "2030", None, QtGui.QApplication.UnicodeUTF8))

        item102 = QtGui.QTreeWidgetItem(item97)
        item102.setText(0,QtGui.QApplication.translate("MainWindow", "model_system_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item102.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item102.setText(1,QtGui.QApplication.translate("MainWindow", "urbansim_base_configuration", None, QtGui.QApplication.UnicodeUTF8))

        item103 = QtGui.QTreeWidgetItem(item97)
        item103.setText(0,QtGui.QApplication.translate("MainWindow", "indicator_sets", None, QtGui.QApplication.UnicodeUTF8))
        item103.setText(1,"")

        item104 = QtGui.QTreeWidgetItem(item103)
        item104.setText(0,QtGui.QApplication.translate("MainWindow", "standard_indicator_set", None, QtGui.QApplication.UnicodeUTF8))
        item104.setIcon(0,QtGui.QIcon(":/Images/Images/table_multiple.png"))
        item104.setText(1,"")

        item105 = QtGui.QTreeWidgetItem(self.treeWidget_4)
        item105.setText(0,QtGui.QApplication.translate("MainWindow", "no_ugb_scenario", None, QtGui.QApplication.UnicodeUTF8))
        item105.setIcon(0,QtGui.QIcon(":/Images/Images/exclamation.png"))
        item105.setText(1,"")

        item106 = QtGui.QTreeWidgetItem(item105)
        item106.setText(0,QtGui.QApplication.translate("MainWindow", "base_year_cache", None, QtGui.QApplication.UnicodeUTF8))
        item106.setIcon(0,QtGui.QIcon(":/Images/Images/exclamation.png"))
        item106.setText(1,QtGui.QApplication.translate("MainWindow", "?", None, QtGui.QApplication.UnicodeUTF8))

        item107 = QtGui.QTreeWidgetItem(item105)
        item107.setText(0,QtGui.QApplication.translate("MainWindow", "years_to_run", None, QtGui.QApplication.UnicodeUTF8))
        item107.setIcon(0,QtGui.QIcon(":/Images/Images/calendar_view_day.png"))
        item107.setText(1,"")

        item108 = QtGui.QTreeWidgetItem(item107)
        item108.setText(0,QtGui.QApplication.translate("MainWindow", "start_year", None, QtGui.QApplication.UnicodeUTF8))
        item108.setText(1,QtGui.QApplication.translate("MainWindow", "2000", None, QtGui.QApplication.UnicodeUTF8))

        item109 = QtGui.QTreeWidgetItem(item107)
        item109.setText(0,QtGui.QApplication.translate("MainWindow", "end_year", None, QtGui.QApplication.UnicodeUTF8))
        item109.setText(1,QtGui.QApplication.translate("MainWindow", "2030", None, QtGui.QApplication.UnicodeUTF8))

        item110 = QtGui.QTreeWidgetItem(item105)
        item110.setText(0,QtGui.QApplication.translate("MainWindow", "model_system_configuration", None, QtGui.QApplication.UnicodeUTF8))
        item110.setIcon(0,QtGui.QIcon(":/Images/Images/cog.png"))
        item110.setText(1,QtGui.QApplication.translate("MainWindow", "urbansim_base_configuration", None, QtGui.QApplication.UnicodeUTF8))

        item111 = QtGui.QTreeWidgetItem(item105)
        item111.setText(0,QtGui.QApplication.translate("MainWindow", "indicator_sets", None, QtGui.QApplication.UnicodeUTF8))
        item111.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.runmanager_page), QtGui.QApplication.translate("MainWindow", "Run Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_5.headerItem().setText(0,QtGui.QApplication.translate("MainWindow", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_5.headerItem().setText(1,QtGui.QApplication.translate("MainWindow", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_5.clear()

        item112 = QtGui.QTreeWidgetItem(self.treeWidget_5)
        item112.setText(0,QtGui.QApplication.translate("MainWindow", "Indicator sets", None, QtGui.QApplication.UnicodeUTF8))
        item112.setIcon(0,QtGui.QIcon(":/Images/Images/bullet_black.png"))
        item112.setText(1,"")

        item113 = QtGui.QTreeWidgetItem(item112)
        item113.setText(0,QtGui.QApplication.translate("MainWindow", "standard_indicator_set", None, QtGui.QApplication.UnicodeUTF8))
        item113.setIcon(0,QtGui.QIcon(":/Images/Images/table_multiple.png"))
        item113.setText(1,"")

        item114 = QtGui.QTreeWidgetItem(item113)
        item114.setText(0,QtGui.QApplication.translate("MainWindow", "Tables", None, QtGui.QApplication.UnicodeUTF8))
        item114.setText(1,"")

        item115 = QtGui.QTreeWidgetItem(item114)
        item115.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_new_units_by_parcel", None, QtGui.QApplication.UnicodeUTF8))
        item115.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item115.setText(1,QtGui.QApplication.translate("MainWindow", "2015", None, QtGui.QApplication.UnicodeUTF8))

        item116 = QtGui.QTreeWidgetItem(item114)
        item116.setText(0,QtGui.QApplication.translate("MainWindow", "number_of_service_jobs_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item116.setIcon(0,QtGui.QIcon(":/Images/Images/table.png"))
        item116.setText(1,QtGui.QApplication.translate("MainWindow", "2020", None, QtGui.QApplication.UnicodeUTF8))

        item117 = QtGui.QTreeWidgetItem(item113)
        item117.setText(0,QtGui.QApplication.translate("MainWindow", "Charts", None, QtGui.QApplication.UnicodeUTF8))
        item117.setText(1,"")

        item118 = QtGui.QTreeWidgetItem(item117)
        item118.setText(0,QtGui.QApplication.translate("MainWindow", "total_population", None, QtGui.QApplication.UnicodeUTF8))
        item118.setIcon(0,QtGui.QIcon(":/Images/Images/chart_bar.png"))
        item118.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item119 = QtGui.QTreeWidgetItem(item113)
        item119.setText(0,QtGui.QApplication.translate("MainWindow", "Maps", None, QtGui.QApplication.UnicodeUTF8))
        item119.setText(1,"")

        item120 = QtGui.QTreeWidgetItem(item119)
        item120.setText(0,QtGui.QApplication.translate("MainWindow", "population_density_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item120.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item120.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item121 = QtGui.QTreeWidgetItem(item119)
        item121.setText(0,QtGui.QApplication.translate("MainWindow", "jobs_per_acre_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item121.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item121.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2030", None, QtGui.QApplication.UnicodeUTF8))

        item122 = QtGui.QTreeWidgetItem(item119)
        item122.setText(0,QtGui.QApplication.translate("MainWindow", "population_change_by_taz", None, QtGui.QApplication.UnicodeUTF8))
        item122.setIcon(0,QtGui.QIcon(":/Images/Images/map.png"))
        item122.setText(1,QtGui.QApplication.translate("MainWindow", "2000-2015", None, QtGui.QApplication.UnicodeUTF8))

        item123 = QtGui.QTreeWidgetItem(item112)
        item123.setText(0,QtGui.QApplication.translate("MainWindow", "indicator_set_working", None, QtGui.QApplication.UnicodeUTF8))
        item123.setIcon(0,QtGui.QIcon(":/Images/Images/table_multiple.png"))
        item123.setText(1,"")

        item124 = QtGui.QTreeWidgetItem(item123)
        item124.setText(0,QtGui.QApplication.translate("MainWindow", "Tables", None, QtGui.QApplication.UnicodeUTF8))
        item124.setText(1,"")

        item125 = QtGui.QTreeWidgetItem(item123)
        item125.setText(0,QtGui.QApplication.translate("MainWindow", "Charts", None, QtGui.QApplication.UnicodeUTF8))
        item125.setText(1,"")

        item126 = QtGui.QTreeWidgetItem(item123)
        item126.setText(0,QtGui.QApplication.translate("MainWindow", "Maps", None, QtGui.QApplication.UnicodeUTF8))
        item126.setText(1,"")
        self.toolBox.setItemText(self.toolBox.indexOf(self.resultsmanager_page), QtGui.QApplication.translate("MainWindow", "Results Manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QtGui.QApplication.translate("MainWindow", "Editor", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Python Shell", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_mapView), QtGui.QApplication.translate("MainWindow", "Map View", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProject.setTitle(QtGui.QApplication.translate("MainWindow", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomOut.setText(QtGui.QApplication.translate("MainWindow", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionPan.setText(QtGui.QApplication.translate("MainWindow", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddRasterLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Raster Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionZoomIn.setText(QtGui.QApplication.translate("MainWindow", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.mpActionAddVectorLayer.setText(QtGui.QApplication.translate("MainWindow", "Add Vector Layer", None, QtGui.QApplication.UnicodeUTF8))

import opusMain_rc


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
