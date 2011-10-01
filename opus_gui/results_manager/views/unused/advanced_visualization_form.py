# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from PyQt4.QtCore import QString, QObject, SIGNAL, \
                         Qt, QTimer, QModelIndex, QFileInfo, pyqtSlot
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel, \
                        QFileDialog, QLineEdit, QListWidget

from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper

from opus_gui.results_manager.run.opus_result_generator import OpusResultGenerator
import os

class AdvancedVisualizationForm(QWidget):
    def __init__(self, mainwindow, result_manager):
        QWidget.__init__(self, mainwindow)
        #mainwindow is an OpusGui
        self.mainwindow = mainwindow
        self.result_manager = result_manager
        self.toolboxBase = self.result_manager.mainwindow.toolboxBase

        self.inGui = False
        self.logFileKey = 0
        
        self.xml_helper = ResultsManagerXMLHelper(toolboxBase = self.toolboxBase)
        self.result_generator = OpusResultGenerator(
                                    toolboxBase = self.toolboxBase)
            
        self.result_generator.guiElement = self
        
        self.tabIcon = QIcon(':/Images/Images/cog.png')
        self.tabLabel = 'Advanced Visualization'

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.resultsGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.resultsGroupBox)
        
        self.dataGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.dataGroupBox)
        
        self.optionsGroupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.optionsGroupBox)
                
        self._setup_definition_widget()

        self._setup_buttons()
        self._setup_tabs()
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_go = QPushButton(self.resultsGroupBox)
        self.pbn_go.setObjectName('pbn_go')
        self.pbn_go.setText(QString('Go!'))
        
        QObject.connect(self.pbn_go, SIGNAL("clicked()"),
                        self.on_pbn_go_clicked)
        self.widgetLayout.addWidget(self.pbn_go)
        
        self.pbn_set_esri_storage_location = QPushButton(self.optionsGroupBox)
        self.pbn_set_esri_storage_location.setObjectName('pbn_set_esri_storage_location')
        self.pbn_set_esri_storage_location.setText(QString('...'))
        self.pbn_set_esri_storage_location.hide()
        
        QObject.connect(self.pbn_set_esri_storage_location, SIGNAL("clicked()"),
                        self.on_pbn_set_esri_storage_location_clicked)
        
    def _setup_tabs(self):
        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.resultsGroupBox)
    
        # Log panel
        self.logText = QTextEdit(self.resultsGroupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,'Log')

        # Finally add the tab to the model page
        self.widgetLayout.addWidget(self.tabWidget)
        
#
    def _setup_definition_widget(self):
        
        #### setup results group box ####
        
        self.gridlayout = QGridLayout(self.resultsGroupBox)
        self.gridlayout.setObjectName('gridlayout')

        self.lbl_results = QLabel(self.resultsGroupBox)
        self.lbl_results.setObjectName('lbl_results')
        self.lbl_results.setText(QString('Results'))
        self.gridlayout.addWidget(self.lbl_results,0,0,1,3)

        self._setup_co_results()
        self.gridlayout.addWidget(self.co_results,0,3,1,10)

        self.pbn_add = QPushButton(self.resultsGroupBox)
        self.pbn_add.setObjectName('pbn_add')
        self.pbn_add.setText(QString('+'))
        
        QObject.connect(self.pbn_add, SIGNAL("clicked()"),
                        self.on_pbn_add_clicked)
        self.gridlayout.addWidget(self.pbn_add, 0, 14, 1, 1)

        self.lw_indicators = QListWidget(self.resultsGroupBox)
        self.lw_indicators.setObjectName('lw_indicators')
        self.gridlayout.addWidget(self.lw_indicators,1,1,1,13)

        self.pbn_remove = QPushButton(self.resultsGroupBox)
        self.pbn_remove.setObjectName('pbn_remove')
        self.pbn_remove.setText(QString('-'))
        
        QObject.connect(self.pbn_remove, SIGNAL("clicked()"),
                        self.on_pbn_remove_clicked)
        self.gridlayout.addWidget(self.pbn_remove, 1, 14, 1, 1)


        #### setup data group box ####

        self.gridlayout2 = QGridLayout(self.dataGroupBox)
        self.gridlayout2.setObjectName('gridlayout2')

        self._setup_co_result_style()
        self.gridlayout2.addWidget(self.co_result_style,1,0,1,2)
                
        self.lbl_result_style_sep = QLabel(self.resultsGroupBox)
        self.lbl_result_style_sep.setObjectName('lbl_result_style_sep')
        self.lbl_result_style_sep.setText(QString('<center>as</center>'))
        self.gridlayout2.addWidget(self.lbl_result_style_sep,1,2,1,1)

        self._setup_co_result_type()
        self.gridlayout2.addWidget(self.co_result_type,1,3,1,2)

        ##### setup options group box ####
        
        self.gridlayout3 = QGridLayout(self.optionsGroupBox)
        self.gridlayout3.setObjectName('gridlayout3')
        
        self.le_esri_storage_location = QLineEdit(self.optionsGroupBox)
        self.le_esri_storage_location.setObjectName('le_esri_storage_location')
        self.le_esri_storage_location.setText('[set path]')
        self.le_esri_storage_location.hide()
        self.optionsGroupBox.hide()

        
        QObject.connect(self.co_result_style, SIGNAL('currentIndexChanged(int)'),
                self.on_co_result_style_changed)
        QObject.connect(self.co_result_type, SIGNAL('currentIndexChanged(int)'),
                self.on_co_result_type_changed)

    def _setup_co_results(self):
        
        self.co_results = QComboBox(self.resultsGroupBox)
        self.co_results.setObjectName('co_results')
        self.co_results.addItem(QString('[select]'))
        
        results = self.xml_helper.get_available_results()
            
        for result in results:
            name = '%i.%s'%(result['run_id'],result['indicator_name'])
            self.co_results.addItem(QString(name))

    def _setup_co_result_style(self):
        available_styles = [
            'visualize',
            'export',
        ]
        self.co_result_style = QComboBox(self.dataGroupBox)
        self.co_result_style.setObjectName('co_result_style')
        
        for dataset in available_styles:
            self.co_result_style.addItem(QString(dataset))

    def _setup_co_result_type(self):
        available_types = [
            'Table (per year, spans indicators)',
            'Chart (per indicator, spans years)',
            'Map (per indicator per year)',
            'Chart (per indicator, spans years)',
        ]
                
        self.co_result_type = QComboBox(self.dataGroupBox)
        self.co_result_type.setObjectName('co_result_type')
        
        for dataset in available_types:
            self.co_result_type.addItem(QString(dataset))
                    
    @pyqtSlot()
    def on_pbnRemoveModel_clicked(self):
        self.result_manager.removeTab(self)
        self.result_manager.updateGuiElements()
        
    @pyqtSlot()
    def on_pbn_add_clicked(self):
        cur_selected = self.co_results.currentText()        
        for i in range(self.lw_indicators.count()):
            if self.lw_indicators.item(i).text() == cur_selected:
                return
        
        self.lw_indicators.addItem(cur_selected)
        
    @pyqtSlot()
    def on_pbn_remove_clicked(self):
        selected_idxs = self.lw_indicators.selectedIndexes()
        for idx in selected_idxs:
            self.lw_indicators.takeItem(idx.row())
        
    def on_co_result_style_changed(self, ind):
        available_viz_types = [
            'Table (per year, spans indicators)',
            'Chart (per indicator, spans years)',
            'Map (per indicator per year)',
            'Chart (per indicator, spans years)',
        ]
        
        available_export_types = [
            'ESRI table (for loading in ArcGIS)'
        ]
                
        txt = self.co_result_style.currentText()
        if txt == 'visualize':
            available_types = available_viz_types
        else:
            available_types = available_export_types
            
        self.co_result_type.clear()
        for result_type in available_types:
            r_type = QString(result_type)
            self.co_result_type.addItem(r_type)
    
    def on_co_result_type_changed(self, ind):
        self.gridlayout3.removeWidget(self.le_esri_storage_location)
        self.gridlayout3.removeWidget(self.pbn_set_esri_storage_location)
        self.optionsGroupBox.hide()
        
        self.pbn_set_esri_storage_location.hide()
        self.le_esri_storage_location.hide()
        
        txt = self.co_result_type.currentText()

        print txt
        if txt == 'ESRI table (for loading in ArcGIS)':
            self.pbn_set_esri_storage_location.show()   
            self.le_esri_storage_location.show()   
            self.gridlayout3.addWidget(self.le_esri_storage_location,0,1,1,6)
            self.gridlayout3.addWidget(self.pbn_set_esri_storage_location,0,7,1,1)   
            self.optionsGroupBox.show()   
            
    @pyqtSlot()
    def on_pbn_set_esri_storage_location_clicked(self):
        print 'pbn_set_esri_storage_location clicked'
        from opus_core.misc import directory_path_from_opus_path
        start_dir = directory_path_from_opus_path('opus_gui.projects')

        configDialog = QFileDialog()
        filter_str = QString("*.gdb")
        fd = configDialog.getExistingDirectory(self,QString("Please select an ESRI geodatabase (*.gdb)..."), #, *.sde, *.mdb)..."),
                                          QString(start_dir), QFileDialog.ShowDirsOnly)
        if len(fd) != 0:
            fileName = QString(fd)
            fileNameInfo = QFileInfo(QString(fd))
            fileNameBaseName = fileNameInfo.completeBaseName()
            self.le_esri_storage_location.setText(fileName)
            
                
    @pyqtSlot()
    def on_pbn_go_clicked(self):
        # Fire up a new thread and run the model
        print 'Go button pressed'

        # References to the GUI elements for status for this run...
        #self.statusLabel = self.runStatusLabel
        #self.statusLabel.setText(QString('Model initializing...'))
        
        indicator_names = []
        for i in range(self.lw_indicators.count()):
            indicator_names.append(str(self.lw_indicators.item(i).text()))
                
        if indicator_names == []:
            print 'no indicators selected'
            return
                
        indicator_type = str(self.co_result_type.currentText())
        indicator_type = {
            #'Map (per indicator per year)':'matplotlib_map',
            'Map (per indicator per year)':'mapnik_map',
            'Chart (per indicator, spans years)':'matplotlib_chart',
            'Table (per indicator, spans years)':'table_per_attribute',
            'Table (per year, spans indicators)':'table_per_year',
            'ESRI table (for loading in ArcGIS)':'table_esri'
        }[indicator_type]
        
        kwargs = {}
        if indicator_type == 'table_esri':
            storage_location = str(self.le_esri_storage_location.text())
            if not os.path.exists(storage_location):
                print 'Warning: %s does not exist!!'%storage_location
            kwargs['storage_location'] = storage_location
        
        self.result_manager.addIndicatorForm(indicator_type = indicator_type,
                                             indicator_names = indicator_names,
                                             kwargs = kwargs)

    def runUpdateLog(self):
        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)


    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.mainwindow, 'Warning', errorMessage)
