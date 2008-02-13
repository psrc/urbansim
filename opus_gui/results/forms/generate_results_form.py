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

from PyQt4.QtCore import QString, QObject, SIGNAL, \
                         Qt, QTimer
from PyQt4.QtGui import QMessageBox, QComboBox, QGridLayout, \
                        QTextEdit, QTabWidget, QWidget, QPushButton, \
                        QGroupBox, QVBoxLayout, QIcon, QLabel

from opus_gui.results.xml_helper_methods import elementsByAttributeValue, get_child_values

from opus_gui.results.opus_result_generator import OpusGuiThread, OpusResultGenerator
from opus_gui.config.xmlmodelview.opusdataitem import OpusDataItem

class GenerateResultsForm(QWidget):
    def __init__(self, parent, result_manager):
        QWidget.__init__(self, parent)
        #parent is an OpusGui
        self.parent = parent
        self.result_manager = result_manager
        self.toolboxStuff = self.result_manager.parent.toolboxStuff

        self.inGui = False
        self.logFileKey = 0
        self.domDocument = self.toolboxStuff.doc

        self.result_generator = OpusResultGenerator(
                                    xml_path = self.toolboxStuff.xml_file,
                                    domDocument = self.domDocument)
            
        self.result_generator.guiElement = self
        
        self.tabIcon = QIcon(":/Images/Images/cog.png")
        self.tabLabel = "Generate results"

        self.widgetLayout = QVBoxLayout(self)
        self.widgetLayout.setAlignment(Qt.AlignTop)

        self.groupBox = QGroupBox(self)
        self.widgetLayout.addWidget(self.groupBox)
        
        self._setup_definition_widget()

        self._setup_buttons()
        self._setup_tabs()
        
    def _setup_buttons(self):
        # Add Generate button...
        self.pbn_generate_results = QPushButton(self.groupBox)
        self.pbn_generate_results.setObjectName("pbn_generate_results")
        self.pbn_generate_results.setText(QString("Generate results..."))
        
        QObject.connect(self.pbn_generate_results, SIGNAL("released()"),
                        self.on_pbn_generate_results_released)        
        self.widgetLayout.addWidget(self.pbn_generate_results)
        
    def _setup_tabs(self):
        # Add a tab widget and layer in a tree view and log panel
        self.tabWidget = QTabWidget(self.groupBox)
    
        # Log panel
        self.logText = QTextEdit(self.groupBox)
        self.logText.setReadOnly(True)
        self.logText.setLineWidth(0)
        self.tabWidget.addTab(self.logText,"Log")

        # Finally add the tab to the model page
        self.widgetLayout.addWidget(self.tabWidget)
        
#
    def _setup_definition_widget(self):
        self.gridlayout = QGridLayout(self.groupBox)
        self.gridlayout.setObjectName("gridlayout")

        self.lbl_indicator_name = QLabel(self.groupBox)
        self.lbl_indicator_name.setObjectName("lbl_indicator_name")
        self.lbl_indicator_name.setText(QString("Indicator"))
        self.gridlayout.addWidget(self.lbl_indicator_name,0,0,1,1)

        self._setup_co_indicator_name()
        self.gridlayout.addWidget(self.co_indicator_name,0,1,1,1)

        self.lbl_dataset_name = QLabel(self.groupBox)
        self.lbl_dataset_name.setObjectName("lbl_dataset_name")
        self.lbl_dataset_name.setText(QString("Dataset"))
        self.gridlayout.addWidget(self.lbl_dataset_name,1,0,1,1)

        self._setup_co_dataset_name()
        
        self.gridlayout.addWidget(self.co_dataset_name,1,1,1,1)

        self.lbl_source_data = QLabel(self.groupBox)
        self.lbl_source_data.setObjectName("lbl_source_data")
        self.lbl_source_data.setText(QString("Source data"))
        self.gridlayout.addWidget(self.lbl_source_data,2,0,1,1)

        self._setup_co_source_data()
        self.gridlayout.addWidget(self.co_source_data,2,1,1,1) 

    def _setup_co_indicator_name(self):
        
        self.co_indicator_name = QComboBox(self.groupBox)
        self.co_indicator_name.setObjectName("co_indicator_name")
        self.co_indicator_name.addItem(QString("[select]"))
        
        node_list = elementsByAttributeValue(domDocument = self.domDocument, 
                                              attribute = 'type', 
                                              value = 'indicator')
            
        for node in node_list:
            self.co_indicator_name.addItem(QString(node.nodeName()))
            

        
    def _setup_co_dataset_name(self):
        available_datasets = [
            '[select]',
            #'parcel',
            'zone',
            #'taz',
            #'county',
            #'alldata'
        ]
        self.co_dataset_name = QComboBox(self.groupBox)
        self.co_dataset_name.setObjectName("co_dataset_name")
        
        for dataset in available_datasets:
            self.co_dataset_name.addItem(QString(dataset))
            
    def _setup_co_source_data(self):
        self.co_source_data = QComboBox(self.groupBox)
        self.co_source_data.setObjectName("co_source_data")
        self.co_source_data.addItem(QString("[select]"))
        
        node_list = elementsByAttributeValue(domDocument = self.domDocument, 
                                              attribute = 'type', 
                                              value = 'source_data')
    
        for node in node_list:
            self.co_source_data.addItem(QString(node.nodeName()))
        
    def on_pbnRemoveModel_released(self):
        self.result_manager.removeTab(self)
        self.result_manager.updateGuiElements()
    
    def on_pbn_generate_results_released(self):
        # Fire up a new thread and run the model
        print "Generate results button pressed"

        # References to the GUI elements for status for this run...
        #self.statusLabel = self.runStatusLabel
        #self.statusLabel.setText(QString("Model initializing..."))
        
        self.pbn_generate_results.setEnabled(False)

        source_text = QString(self.co_source_data.currentText())
        if str(source_text) == '[select]':
            raise 'need to select a data source!!'
        
        indicator_text = QString(self.co_indicator_name.currentText())
        if str(indicator_text) == '[select]':
            raise 'need to select an indicator!!'
        
        dataset_name = str(self.co_dataset_name.currentText())
        if dataset_name == '[select]':
            raise 'need to select a dataset!!'

        self.result_generator.set_data(
                                   source_data_name = source_text,
                                   indicator_name = indicator_text,
                                   dataset_name = dataset_name)
        
        self.runThread = OpusGuiThread(
                              parentThread = self.parent,
                              parent = self,
                              thread_object = self.result_generator)
        
        # Use this signal from the thread if it is capable of producing its own status signal
        QObject.connect(self.runThread, SIGNAL("runFinished(PyQt_PyObject)"),
                        self.runFinishedFromThread)
        QObject.connect(self.runThread, SIGNAL("runError(PyQt_PyObject)"),
                        self.runErrorFromThread)
        

        # Use this timer to call a function in the thread to check status if the thread is unable
        # to produce its own signal above
        self.timer = QTimer()
        QObject.connect(self.timer, SIGNAL("timeout()"),
                        self.runUpdateLog)
        self.timer.start(1000)
        
        self.runThread.start()

    def runUpdateLog(self):
        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)

    # Called when the model is finished... 
    def runFinishedFromThread(self,success):
        print "Results generated met with success = ", success

        self.update_results_xml()
        
        # Get the final logfile update after model finishes...
        self.logFileKey = self.result_generator._get_current_log(self.logFileKey)
        self.pbn_generate_results.setEnabled(True)

    def update_results_xml(self):
        print "update results"
        xml_tree = self.toolboxStuff.resultsManagerTree
        model = xml_tree.model
        document = self.domDocument
        xmlAction = xml_tree.xmlAction.actionObject
        
        newNode = document.createElement(QString("new node"))
        newNode.setAttribute(QString("type"),QString("my type"))
        newText = document.createTextNode(QString("my value"))
        newNode.appendChild(newText)

        grandparent_node = document.elementsByTagName(QString('results_manager')).item(0)
        grandparent_item = OpusDataItem(document,grandparent_node, 0, model)
        
        parent_node = document.elementsByTagName(QString('Results')).item(0)
        parent_item = OpusDataItem(document,parent_node, 0, grandparent_item)
        
        index = model.createIndex(2, 0, parent_item)
        model.insertRow(0,
                        index,
                        newNode)
        
        model.emit(SIGNAL("layoutChanged()"))

    def runErrorFromThread(self,errorMessage):
        QMessageBox.warning(self.parent,"Warning",errorMessage)
