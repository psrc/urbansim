# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import QObject, SIGNAL, Qt
from PyQt4.QtGui import QTabWidget, QWidget, QTableWidgetItem, QSizePolicy

from opus_gui.main.controllers.dialogs.message_box import MessageBox

from opus_gui.results_manager.run.opus_gui_thread import OpusGuiThread
from opus_gui.results_manager.run.batch_processor import BatchProcessor

from opus_gui.results_manager.views.ui_results_browser import Ui_ResultsBrowser
from opus_gui.results_manager.controllers.tabs.view_image_form import ViewImageForm
from opus_gui.results_manager.controllers.tabs.view_animation_form import ViewAnimationForm
from opus_gui.results_manager.controllers.tabs.view_table_form import ViewTableForm
from opus_core.logger import logger

from opus_gui.general_manager.general_manager_functions import get_available_indicator_nodes
from opus_core.configurations.xml_configuration import get_variable_dataset_and_name, get_variable_dataset
from opus_gui.results_manager.results_manager_functions import get_simulation_runs
from opus_gui.results_manager.results_manager_functions import get_years_for_simulation_run
from opus_gui.main.controllers.instance_handlers import get_manager_instance
from opus_gui.main.controllers.instance_handlers import get_mainwindow_instance
from opus_gui.util.icon_library import IconLibrary

class ResultBrowser(QWidget, Ui_ResultsBrowser):
    def __init__(self, project, parent_widget):
        QWidget.__init__(self, parent_widget)
        self.setupUi(self)

        self.project = project

        #TODO handle this as the variables are handled
        try:
            obj = get_manager_instance('results').xml_controller.model
            self.connect(obj, SIGNAL("layoutChanged()"), self._setup_simulation_data)
        except AttributeError:
            pass

        def test():
            print 'Variables updated'
        self.connect(get_mainwindow_instance(), SIGNAL('variables_updated'), test)

        tool_tip = ('If checked, indicator results will automatically be\n'
                    'created for the currently selected simulation run,\n'
                    'indicator, and years. If unchecked, click\n'
                    'Generate results in order to make results available.')
        self.cb_auto_gen.setToolTip(tool_tip)

        self.inGui = False
        self.logFileKey = 0
        self.available_years_for_simulation_runs = {}

        self.current_indicator = ''
        self.current_indicator_dataset = ''
        self.current_run = ''
        self.current_year = ''
        self._update_current_label()

        self.running_key = None
        self.queued_results = None

        self.setup = True

        self._setup_available_indicators()
        self._setup_simulation_data()

        self.setup = False

        self.already_browsed = {}

        self.generating_results = False
        if self.cb_auto_gen.isChecked():
            self.on_pb_generate_results_released()
        # self.pb_export_results.setEnabled(False)
        self.tabwidget_visualizations.removeTab(0)
        self.tabIcon = IconLibrary.icon('table')
        self.tabLabel = "Result Browser"

    def _update_current_label(self):
        msg = '%s > %s > %s' %(self.current_run, self.current_year, self.current_indicator)
        self.lbl_current_selection.setText(msg)

    def _setup_available_indicators(self):
        indicator_nodes = get_available_indicator_nodes(self.project)

        current_row = self.indicator_table.currentRow()

        self.indicator_table.clear()
        self.indicator_table.setColumnCount(3)
        self.indicator_table.setRowCount(len(indicator_nodes))

        col = QTableWidgetItem()
        col.setText('Name')
        self.indicator_table.setHorizontalHeaderItem(0,col)

        col = QTableWidgetItem()
        col.setText('Dataset')
        self.indicator_table.setHorizontalHeaderItem(1,col)

        col = QTableWidgetItem()
        col.setText('Definition')
        self.indicator_table.setHorizontalHeaderItem(2,col)

        for i, indicator in enumerate(indicator_nodes):
            row = QTableWidgetItem()
            self.indicator_table.setVerticalHeaderItem(i, row)

            dataset, name = get_variable_dataset_and_name(indicator)

            item = QTableWidgetItem()
            item.setText(name)
            self.indicator_table.setItem(i,0,item)

            item = QTableWidgetItem()
            item.setText(dataset)
            self.indicator_table.setItem(i,1,item)

            item = QTableWidgetItem()
            item.setText(indicator.text or '')
            self.indicator_table.setItem(i,2,item)

        if current_row is None or current_row == -1:
            current_row = 0
        self.indicator_table.resizeRowsToContents()
        self.indicator_table.resizeColumnsToContents()

        self.indicator_table.setCurrentCell(current_row,0)
        self.on_indicator_table_itemSelectionChanged()

    def on_cb_auto_gen_released(self):
        self.pb_generate_results.setEnabled(self.cb_auto_gen.checkState() != Qt.Checked)

    def _setup_simulation_data(self):
        current_row = self.lst_available_runs.currentRow()

        runs = get_simulation_runs(self.project)

        self.lst_available_runs.clear()
        idx = -1
        for i, run in enumerate(runs):
            run_name = run.get('name')
            if run_name == 'base_year_data':
                idx = i

            years = get_years_for_simulation_run(project = self.project,
                                                 simulation_run_node = run)
            self.available_years_for_simulation_runs[run_name] = years

            self.lst_available_runs.addItem(run_name)

        if current_row is None or current_row == -1:
            current_row = idx
        if current_row != -1:
            self.lst_available_runs.setCurrentRow(current_row)
            self.on_lst_available_runs_currentRowChanged(current_row)

    def on_lst_available_runs_currentRowChanged(self, _):
        currentItem = self.lst_available_runs.currentItem()
        if currentItem is None: return

        current_run = str(currentItem.text())
        if current_run == self.current_run and not self.setup:
            return

        self.current_run = current_run
        self._update_current_label()

        setup = self.setup
        if current_run in self.available_years_for_simulation_runs:
            self.setup = True
            self.lst_years.clear()

            years = self.available_years_for_simulation_runs[current_run]
            for yr in sorted(years):
                self.lst_years.addItem(str(yr))

            self.lst_years.setCurrentRow(0)
            self.on_lst_years_currentRowChanged(0)
            self.setup = False

        if not setup and self.cb_auto_gen.isChecked():
            self.on_pb_generate_results_released()
        else:
            self.pb_generate_results.setEnabled(True)
            self.pb_generate_results.setText('Generate Results')

    def on_lst_years_currentRowChanged(self, _):
        current_item = self.lst_years.currentItem()
        if current_item is None: return

        current_year = int(current_item.text())

        if self.current_year == current_year and not self.setup:
            return
        self.current_year = current_year
        self._update_current_label()

        if not self.setup and self.cb_auto_gen.isChecked():
            self.on_pb_generate_results_released()
        else:
            self.pb_generate_results.setEnabled(True)
            self.pb_generate_results.setText('Generate Results')

    def on_indicator_table_itemSelectionChanged(self):
        currentRow = self.indicator_table.currentRow()
        if currentRow is None: return

        indicator_name = str(self.indicator_table.item(currentRow,0).text())
        indicator_dataset = str(self.indicator_table.item(currentRow,1).text())
        if self.current_indicator == indicator_name and \
                self.current_indicator_dataset == indicator_dataset and \
                not self.setup: return

        self.current_indicator = indicator_name
        self.current_indicator_dataset = indicator_dataset
        
        self._update_current_label()

        if not self.setup and self.cb_auto_gen.isChecked():
            self.on_pb_generate_results_released()
        else:
            self.pb_generate_results.setEnabled(True)
            self.pb_generate_results.setText('Generate Results')

    def on_pb_generate_results_released(self):
        run_name = self.current_run
        indicator_name = self.current_indicator
        indicator_dataset = self.current_indicator_dataset
        start_year = int(self.current_year)
        end_year = start_year

        if run_name is None or indicator_name is None or start_year is None:
            return

        key = (run_name, indicator_name, start_year)

        if key in self.already_browsed:
            if not self.generating_results:
                (tab_widget,map_widget) = self.already_browsed[key]
#                self.swap_visualizations(map_widget, tab_widget)
                self.pb_generate_results.setText('Results Generated')
            else:
                self.queued_results = ('swap', (map_widget, tab_widget))
            return

        self.pb_generate_results.setEnabled(False)
        self.pb_generate_results.setText('Generating Results...')

        indicator_nodes = get_available_indicator_nodes(self.project)

        dataset = None
        for indicator_node in indicator_nodes:
            ind_dataset, name = get_variable_dataset_and_name(indicator_node)
            if name == indicator_name and ind_dataset == indicator_dataset:
                dataset = ind_dataset
                break

        if dataset is None:
            raise Exception('Could not find dataset for indicator %s' % indicator_name)

        table_params = {
            'name': None,
            'output_type' : 'tab',
            'indicators' : [indicator_name],
        }

        map_params = {'name':None,
                      'indicators':[indicator_name]}

        visualizations = [
            ('table_per_year', dataset, table_params),
            ('mapnik_map', dataset, map_params)
        ]

        batch_processor = BatchProcessor(self.project)
        batch_processor.guiElement = self

        batch_processor.set_data(
            visualizations = visualizations,
            source_data_name = run_name,
            years = range(start_year, end_year + 1))

        if not self.generating_results:
            self.generating_results = True
            logger.log_note('Generating results for %s on run %s for year %indicator_node'%(run_name, indicator_name, start_year))
            self.running_key = key
            self.batch_processor = batch_processor
            batch_processor_thread = OpusGuiThread(
                                  parentThread = get_mainwindow_instance(),
                                  parentGuiElement = self,
                                  thread_object = self.batch_processor)

            # Use this signal from the thread if it is capable of producing its own status signal
            self.connect(batch_processor_thread, SIGNAL("runFinished(PyQt_PyObject)"), self._run_finished)
            self.connect(batch_processor_thread, SIGNAL("runError(PyQt_PyObject)"), self._run_error)

            batch_processor_thread.start()
        else:
            self.queued_results = (key, batch_processor)

    # Called when the model is finished...
    def _run_finished(self, success):
        key = self.running_key
        self.running_key = None

        size = QSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        self.tabwidget_visualizations.setSizePolicy(size)

        name = '%s/%s/%s'%key
        new_tab = QTabWidget(self.tabwidget_visualizations)
        self.tabwidget_visualizations.addTab(new_tab, name)

        map_widget = None
        tab_widget = None
        for (visualization_type, visualizations) in self.batch_processor.get_visualizations():
            if len(visualizations) > 0:
                if visualization_type == 'mapnik_map':
                    viz = visualizations[0]
                    map_widget = ViewImageForm(viz, new_tab)
                    map_widget.setSizePolicy(size)
                elif visualization_type == 'mapnik_animated_map':
                    viz = visualizations[0]
                    map_widget = ViewAnimationForm(viz, new_tab)
                    map_widget.setSizePolicy(size)
                elif visualization_type == 'table_per_year':
                    viz = visualizations[0]
                    tab_widget = ViewTableForm(viz, new_tab)
                    tab_widget.setSizePolicy(size)
#            else:
#                map_widget = self.tabMap
#                tab_widget = self.tabTable

#        if not map_widget or not tab_widget: return

#        self.tabMap = map_widget
#        self.tabTable = tab_widget

        if tab_widget:
            new_tab.addTab(tab_widget, "Table")

        if map_widget:
            new_tab.addTab(map_widget, "Map")

        self.already_browsed[key] = (tab_widget, map_widget)

#        self.lblViewIndicator.setText(QString(key[1]))
#        self.lblViewRun.setText(QString(key[0]))
#        self.lblViewYear.setText(QString(repr(key[2])))

        swap = self.queued_results is not None and self.queued_results[0] == 'swap'

        if self.queued_results is not None and not swap:
            self.running_key = self.queued_results[0]

            logger.log_note('Generating queued results for %s on run %s for year %i'%self.running_key)
            self.batch_processor = self.queued_results[1]
            self.queued_results = None

            runThread = OpusGuiThread(
                                  parentThread = get_mainwindow_instance(),
                                  parentGuiElement = self,
                                  thread_object = self.batch_processor)

            # Use this signal from the thread if it is capable of producing its own status signal
            QObject.connect(runThread, SIGNAL("runFinished(PyQt_PyObject)"), self._run_finished)
            QObject.connect(runThread, SIGNAL("runError(PyQt_PyObject)"), self._run_error)
            runThread.start()
        else:
#            if swap:
#                (map_widget, tab_widget) = self.queued_results[1]
#
##                self.swap_visualizations(map_widget, tab_widget)
#                name = '%s/%s/%s'%key
#        #        self.swap_visualizations(map_widget, tab_widget)
#                self.add_visualization(map_widget = map_widget, tab_widget = tab_widget, name = name)

            self.queued_results = None

            self.generating_results = False
            self.pb_generate_results.setText('Results Generated')

#    def swap_visualizations(self, map_widget, tab_widget):
#        cur_index = self.tabwidget_visualizations.currentIndex()
#
#        self.tabwidget_visualizations.removeTab(self.tabwidget_visualizations.indexOf(self.tabTable))
#        self.tabwidget_visualizations.removeTab(self.tabwidget_visualizations.indexOf(self.tabMap))
#        self.tabMap = None
#        self.tabTable = None
#
#        self.tabMap = map_widget
#        self.tabTable = tab_widget
#
#        self.tabwidget_visualizations.addTab(self.tabTable, "")
#        self.tabwidget_visualizations.addTab(self.tabMap, "")
#
#        self.tabwidget_visualizations.setTabText(self.tabwidget_visualizations.indexOf(self.tabTable), QString('Table'))
#        self.tabwidget_visualizations.setTabText(self.tabwidget_visualizations.indexOf(self.tabMap), QString('Map'))
#        #self.tabMap.show()
#        #self.tabTable.show()
#
#        self.tabwidget_visualizations.setCurrentIndex(cur_index)

    def removeElement(self):
        return True

    def _run_error(self,errorMessage):
        text = 'Error in computing or displaying indicator'
        MessageBox.error(mainwindow = self, text = text, detailed_text = errorMessage)

#        box = QMessageBox(QMessageBox.Warning, '', 'Error in computing or displaying indicator', QMessageBox.Ok, self.mainwindow, Qt.Dialog|Qt.WindowMaximizeButtonHint)
#        box.setDetailedText(errorMessage)
#        #box.setSizeGripEnabled(True)
#        #box.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Expanding )
#        box.setFixedWidth(500)
#        box.setMinimumWidth(500)
#        box.show()
