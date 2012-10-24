# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from lxml.etree import SubElement

from PyQt4.QtCore import QString,QFileInfo, pyqtSlot, QModelIndex
from PyQt4.QtGui import QDialog, QTableWidgetItem, QFileDialog

from opus_core.logger import logger
from opus_gui.general_manager.general_manager_functions import get_available_spatial_dataset_names
from opus_core.configurations.xml_configuration import get_variable_dataset_and_name
from opus_gui.general_manager.general_manager_functions import get_available_dataset_names
from opus_gui.general_manager.general_manager_functions import get_available_indicator_nodes
from opus_gui.main.controllers.dialogs.message_box import MessageBox
#from opus_gui.results_manager.xml_helper_methods import ResultsManagerXMLHelper
from opus_gui.results_manager.views.ui_configure_batch_indicator_visualization import Ui_dlgConfigureBatchIndicatorVisualization
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.table import Table
from opus_gui.util.exception_formatter import formatExceptionInfo
from opus_gui.results_manager.run.get_mapnik_options import MapOptions
from opus_core import paths


class AbstractConfigureBatchIndicatorVisualization(QDialog, Ui_dlgConfigureBatchIndicatorVisualization):
    def __init__(self, project, parent_widget = None):
        QDialog.__init__(self, parent_widget)

        self.setModal(True)
        self.setupUi(self)
        # self.resultManagerBase = resultManagerBase

        self.project = project
        self.mapnik_options = {}

#        self.model = resultManagerBase.toolboxBase.resultsManagerTree.model
#        self.xml_helper = ResultsManagerXMLHelper(self.resultManagerBase.toolboxBase)
        self.leVizName.setText(QString('New visualization'))
        self.dataset_name = None
#        self.twAvailableIndicators.verticalHeader().hide()
#        self.twIndicatorsToVisualize.verticalHeader().hide()
#
#        self.twAvailableIndicators.horizontalHeader().setResizeMode(QHeaderView.Stretch)
#        self.twIndicatorsToVisualize.horizontalHeader().setResizeMode(QHeaderView.Stretch)

        self.lblOption1.hide()
        self.leOption1.hide()
        self.pbn_set_storage_location.hide()
        #self.setToolTip(QString('In this visualization, a table of values \nwill be output for every simulation year. \nThe table consists of the ID columns \nof the specified dataset and \nthe values for each of the indicators \nspecified in this form.'))
        self.spatial_datasets = get_available_spatial_dataset_names(project = project)

    def _setup_indicators(self, existing_indicators = []):
        if self.dataset_name is None: return

        indicator_nodes = get_available_indicator_nodes(self.project)
        # self.xml_helper.get_available_indicator_names(attributes = ['dataset'])

        current_row = self.twAvailableIndicators.currentRow()

        self.twAvailableIndicators.clear()
        self.twAvailableIndicators.setColumnCount(2)
        self.twAvailableIndicators.horizontalHeader().setStretchLastSection(True)
        self.twIndicatorsToVisualize.horizontalHeader().setStretchLastSection(True)

        while self.twAvailableIndicators.rowCount() > 0:
            self.twAvailableIndicators.removeRow(0)

        while self.twIndicatorsToVisualize.rowCount() > 0:
            self.twIndicatorsToVisualize.removeRow(0)

#        self.twAvailableIndicators.setRowCount(len(indicators) - len(existing_indicators))

        col = QTableWidgetItem()
        col.setText(QString('Name'))
        self.twAvailableIndicators.setHorizontalHeaderItem(0,col)

        #col = QTableWidgetItem()
        #col.setText(QString('Dataset'))
        #self.twAvailableIndicators.setHorizontalHeaderItem(1,col)

        col = QTableWidgetItem()
        col.setText(QString('Definition'))
        self.twAvailableIndicators.setHorizontalHeaderItem(1,col)

        self.indicator_nodes = {}

        for indicator in indicator_nodes:

            dataset, name = get_variable_dataset_and_name(indicator)

            self.indicator_nodes[name] = indicator

            if name not in existing_indicators:
                if self.dataset_name == dataset:
                    item = QTableWidgetItem()
                    item.setText(name)
                    row = self.twAvailableIndicators.rowCount()
                    self.twAvailableIndicators.insertRow(row)
                    #self.twAvailableIndicators.setVerticalHeaderItem(row,QTableWidgetItem())

                    self.twAvailableIndicators.setItem(row,0,item)

                    #item = QTableWidgetItem()
                    #item.setText(dataset)
                    #self.twAvailableIndicators.setItem(i,1,item)

                    item = QTableWidgetItem()
                    item.setText(indicator.text or '')
                    self.twAvailableIndicators.setItem(row,1,item)
            else:
                if self.dataset_name != dataset:
                    logger.log_warning('Visualization configured incorrectly. Cannot have indicators for different datasets. Skipping indicator %s'%str(name))
                    continue
                item = QTableWidgetItem()
                item.setText(name)
                row = self.twIndicatorsToVisualize.rowCount()
                self.twIndicatorsToVisualize.insertRow(row)
                self.twIndicatorsToVisualize.setItem(row, 0, item)

        if current_row is None or current_row == -1:
            current_row = 0

        self.twAvailableIndicators.setCurrentCell(current_row,0)

#        self.twAvailableIndicators.resizeColumnsToContents()
#        self.twAvailableIndicators.resizeRowsToContents()
#
#        self.twIndicatorsToVisualize.resizeColumnsToContents()
#        self.twIndicatorsToVisualize.resizeRowsToContents()


    def _set_column(self, column, values):
        row = 0
        for value in values:
            item = QTableWidgetItem(value)
            self.twIndicatorsToVisualize.setItem(row, column, item)
            row += 1

    def _get_output_types(self, viz_type):
        if str(viz_type) == 'Table':
            available_output_types = {
                'Tab delimited file (.tab)':'tab',
    #            'Comma separated':'csv',
                'ESRI database':'esri',
                'Export to SQL database':'sql',
                'Fixed field file (.dat)':'fixed_field',
                'Excel (.xls)':'xls'
            }
        elif str(viz_type) == 'Map':
            available_output_types = {
                'Mapnik map (.png)':'mapnik_map'
            }
        elif str(viz_type) == 'Animation':
            available_output_types = {
                'Animated Mapnik map (.gif)':'mapnik_animated_map'
            }
        else:
            available_output_types = {}

        return available_output_types


    def _setup_co_output_type(self, value = None):
        viz_type = self.cboVizType.currentText()
        available_output_types = self._get_output_types(viz_type = viz_type)

        if value is None:
            value = 'Tab delimited file (.tab)'

        loc = -1
        self.cboOutputType.clear()
        for idx,(k,v) in enumerate(available_output_types.items()):
            self.cboOutputType.addItem(QString(k))

            if k == value:
                loc = idx

        if loc != -1:
            self.cboOutputType.setCurrentIndex(loc)
            if loc == 0:
                self.on_cboOutputType_currentIndexChanged(QString(value))

    def _setup_co_dataset_name(self, value = None):
        available_datasets = get_available_dataset_names(self.project)
        # self.xml_helper.get_available_datasets()

        for dataset in available_datasets:
            self.cboDataset.addItem(QString(dataset))

        if value is not None:
            idx = self.cboDataset.findText(value)
            if idx != -1:
                self.dataset_name = value
                self.cboDataset.setCurrentIndex(idx)

        if value is None or idx == -1:
            self.dataset_name = QString(str(self.cboDataset.currentText()))

    def _setup_co_viz_type(self, value = None):

        if value is not None:
            idx = self.cboVizType.findText(value)
            if idx != -1:
                self.cboVizType.setCurrentIndex(idx)

    def _update_xml_from_dict(self, xml_node, viz_params):
        ''' convert the dictionary into XML structure and update/create child nodes of xml_node '''
        # Update the XML node with new data

        viz_name = str(self.leVizName.text()).replace('DATASET', viz_params['dataset_name'])

        # Renaming must be passed through the models to enable check for
        # inheritance and to keep the integrity of internal representations
        xml_node.set('name', viz_name)
        xml_node.set('hidden', 'Children') # hide all the kids
        # Convert the dictionary to XML
        fixed_node_names = ['dataset_name', 'visualization_type', 'indicators', 'output_type']
        for key, value in viz_params.items():
            if key in fixed_node_names:
                node = xml_node.find(key)
                if node is None:
                    node = SubElement(xml_node, key)
            else:
                settings_node = xml_node.find('settings')
                if settings_node is None:
                    settings_node = SubElement(xml_node, 'settings')
                node = settings_node.find("setting[@name='%s']" % key)
                if node is None:
                    node = SubElement(settings_node, 'setting', {'name': key})
            node.text = str(value).strip()

    def set_default_mapnik_options(self):
        # these default values are also hard-coded in opus_gui.results_manager.run.batch_processor.py
        self.mapnik_options['mapnik_bucket_colors'] = '#e0eee0, #c7e9c0, #a1d99b, #7ccd7c, #74c476, #41ab5d, #238b45, #006400, #00441b, #00340b' # green
        self.mapnik_options['mapnik_bucket_ranges'] = 'linear_scale'
        self.mapnik_options['mapnik_bucket_labels'] = 'range_labels'
        self.mapnik_options['mapnik_resolution'] = '96'
        self.mapnik_options['mapnik_page_dims'] = '8.5,5.5'
        self.mapnik_options['mapnik_map_lower_left'] = '0.5,0.5'
        self.mapnik_options['mapnik_map_upper_right'] = '6.0,5.0'
        self.mapnik_options['mapnik_legend_lower_left'] = '6.5,0.5'
        self.mapnik_options['mapnik_legend_upper_right'] = '6.9,5.0'

    def on_cboVizType_currentIndexChanged(self, param):
        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one

        if param == 'Map' or param == 'Animation':
            self.set_default_mapnik_options()

        self._setup_co_output_type()

    def on_cboDataset_currentIndexChanged(self, param):

        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one

        dataset = param
        if self.dataset_name != dataset:
            self.dataset_name = QString(str(dataset))
            self._setup_indicators()

        map_pos = self.cboVizType.findText(QString('Map'))
        if self.dataset_name not in self.spatial_datasets and map_pos > -1:
            self.cboVizType.removeItem(map_pos)
            self._setup_co_viz_type()
        elif self.dataset_name in self.spatial_datasets and map_pos == -1:
            self.cboVizType.addItem(QString('Map'))
            self._setup_co_viz_type()

    def _get_type_mapper(self):
        return {
            'Table': 'tab',
            'Map': 'mapnik_map',
            'Animation': 'mapnik_animated_map'
        }
    def _get_inverse_type_mapper(self):
        mapper = self._get_type_mapper()
        inv = dict([(v,k) for k,v in mapper.items()])

        return inv

    def _get_viz_spec_from_xml_node(self, xml_node):
        spec = {}
        for key in ['indicators', 'output_type', 'dataset_name', 'visualization_type']:
            spec[key] = (xml_node.find(key).text or '').strip()
        for setting_node in xml_node.findall('settings/setting'):
            spec[setting_node.get('name')] = (setting_node.text or '').strip()
        return spec

    def _get_viz_spec(self):
        viz_type = self.cboVizType.currentText()
        translation = self._get_output_types(viz_type)
        dataset_name = self.dataset_name
        output_type = QString(translation[str(self.cboOutputType.currentText())])
        indicators = QString(str(self._get_column_values(column = 0)))

        vals = {
                'indicators': indicators,
                'output_type': output_type,
                'dataset_name': dataset_name,
                'visualization_type': QString(self._get_type_mapper()[str(viz_type)])
        }

        if output_type == 'mapnik_map' or output_type == 'mapnik_animated_map':
            vals['mapnik_bucket_labels'] = self.mapnik_options['mapnik_bucket_labels']
            vals['mapnik_bucket_colors'] = self.mapnik_options['mapnik_bucket_colors']
            vals['mapnik_bucket_ranges'] = self.mapnik_options['mapnik_bucket_ranges']
            vals['mapnik_resolution'] = self.mapnik_options['mapnik_resolution']
            vals['mapnik_page_dims'] = self.mapnik_options['mapnik_page_dims']
            vals['mapnik_map_lower_left'] = self.mapnik_options['mapnik_map_lower_left']
            vals['mapnik_map_upper_right'] = self.mapnik_options['mapnik_map_upper_right']
            vals['mapnik_legend_lower_left'] = self.mapnik_options['mapnik_legend_lower_left']
            vals['mapnik_legend_upper_right'] = self.mapnik_options['mapnik_legend_upper_right']


        elif output_type == 'fixed_field':
            try:
                fixed_field_params = QString(str(self._get_column_values(column = 1)))
            except:
                errorInfo = formatExceptionInfo()
                logger.log_error(errorInfo)
                MessageBox.error(mainwindow = self,
                                text = 'Could not get fixed field parameters for all columns',
                                detailed_text = '')
                return None

            vals['fixed_field_specification'] = fixed_field_params
            vals['id_format'] = self.leOption1.text()
        elif output_type == 'sql':
            vals['database_name'] = self.leOption1.text()
        elif output_type == 'esri':
            vals['storage_location'] = self.leOption1.text()
        elif output_type in ('tab', 'xls'):
            if self.rbSingleTable.isChecked():
                output_style = Table.ALL
            elif self.rbTablePerIndicator.isChecked():
                output_style = Table.PER_ATTRIBUTE
            elif self.rbTablePerYear.isChecked():
                output_style = Table.PER_YEAR
            vals['output_style'] = QString(str(output_style))
            if self.appendTypeCheckBox.isChecked():
                vals['append_col_type'] = True
            else:
                vals['append_col_type'] = False
            if output_type == 'xls':
                vals['storage_location'] = self.leOption1.text()

        return vals


    def _get_column_values(self, column = 0):
        #column 0 will get you the indicators
        col_vals = []
        for row in range(self.twIndicatorsToVisualize.rowCount()):
            item = self.twIndicatorsToVisualize.item(row,column)
            col_vals.append(str(item.text()))
        return col_vals

    @pyqtSlot()
    def on_mapnikOptions_clicked(self):
        options = MapOptions(self, options_dict=self.mapnik_options)
        options.show()

    def on_cboOutputType_currentIndexChanged(self, param):
        if isinstance(param, int):
            return #qt sends two signals for the same event; only process one

        output_type = str(param)

        if output_type in ['Fixed field file (.dat)', 'Export to SQL database',
                           'ESRI database']:
            self.lblOption1.show()
            self.leOption1.show()
            self.leOption1.activateWindow()
            self.rbSingleTable.hide()
            self.rbTablePerIndicator.hide()
            self.rbTablePerYear.hide()
            self.mapnikOptions.hide()
            self.appendTypeCheckBox.hide()
        elif output_type == 'Mapnik map (.png)' or output_type == 'Animated Mapnik map (.gif)':
            self.mapnikOptions.show()
            self.appendTypeCheckBox.hide()
        elif output_type == 'Tab delimited file (.tab)':
            self.lblOption1.hide()
            self.leOption1.hide()
            self.rbSingleTable.show()
            self.rbTablePerIndicator.show()
            self.rbTablePerYear.show()
            self.mapnikOptions.hide()
            self.appendTypeCheckBox.show()
        elif output_type == 'Excel (.xls)':
            self.lblOption1.show()
            self.leOption1.show()
            self.leOption1.activateWindow()
            self.rbSingleTable.show()
            self.rbTablePerIndicator.show()
            self.rbTablePerYear.show()
            self.mapnikOptions.hide()
            self.appendTypeCheckBox.hide()
        else:
            self.lblOption1.hide()
            self.leOption1.hide()
            self.rbSingleTable.hide()
            self.rbTablePerIndicator.hide()
            self.rbTablePerYear.hide()
            self.appendTypeCheckBox.hide()


        if output_type == 'Fixed field file (.dat)':
            self.twIndicatorsToVisualize.horizontalHeader().showSection(1)
            self.twIndicatorsToVisualize.resizeColumnsToContents()
        else:
            self.twIndicatorsToVisualize.horizontalHeader().hideSection(1)

        if output_type == 'ESRI database':
            self.pbn_set_storage_location.show()
        else:
            self.pbn_set_storage_location.hide()

        if output_type == 'Fixed field file (.dat)':
            self.lblOption1.setText(QString('ID format:'))
            self.lblOption1.setToolTip(QString('The fixed format of all id \ncolumns of the indicator result'))
        elif output_type == 'Export to SQL database':
            self.lblOption1.setText(QString('Database name:'))
            self.lblOption1.setToolTip(QString('The name of the SQL database to \noutput the indicator result.\n The database will be created if \nit does not already exist. If a table with the same name \nas this indicator already exists in the database,\nit will be overwritten.'))
        elif output_type == 'ESRI database':
            self.lblOption1.setText(QString('Path:'))
            self.lblOption1.setToolTip(QString('The location on disk of \na geodatabase file which \ncan then be loaded into ArcMap'))
        elif output_type == 'Excel (.xls)':
            self.lblOption1.setText(QString('Filename:'))
            self.lblOption1.setToolTip(QString('The location on disk of the xls file'))

    @pyqtSlot()
    def on_pbn_set_storage_location_released(self):
        start_dir = paths.OPUS_PROJECT_CONFIGS_PATH

        configDialog = QFileDialog()
        filter_str = QString("*.gdb")
        fd = configDialog.getExistingDirectory(self,
                    QString("Please select an ESRI geodatabase (*.gdb)..."), #, *.sde, *.mdb)..."),
                    QString(start_dir), QFileDialog.ShowDirsOnly)
        if len(fd) != 0:
            fileName = QString(fd)
            fileNameInfo = QFileInfo(QString(fd))
            fileNameBaseName = fileNameInfo.completeBaseName()
            self.leOption1.setText(fileName)

    @pyqtSlot()
    def on_pbnAddIndicator_clicked(self):
        row = self.twAvailableIndicators.currentRow()
        from_table_widget = self.twAvailableIndicators
        to_table_widget = self.twIndicatorsToVisualize

        cur_value = from_table_widget.item(row, 0)
        if cur_value is not None:
            indicator_name = QString(cur_value.text())
            last_row = to_table_widget.rowCount()
            to_table_widget.insertRow(last_row)
            to_table_widget.setItem(last_row, 0, QTableWidgetItem(indicator_name))
            if to_table_widget.columnCount() > 1:
                to_table_widget.setItem(last_row, 1, QTableWidgetItem())

        from_table_widget.removeRow(row)

    @pyqtSlot()
    def on_pbnRemoveIndicator_clicked(self):
        row = self.twIndicatorsToVisualize.currentRow()

        cur_item = self.twIndicatorsToVisualize.item(row, 0)
        if cur_item is not None:
            value = str(cur_item.text())

            item = QTableWidgetItem(value) #need to create new item because QT deletes object
            last_row = self.twAvailableIndicators.rowCount()
            indicator = self.indicator_nodes[value]
            new_row = QTableWidgetItem()
            self.twAvailableIndicators.setRowCount(last_row + 1)
            self.twAvailableIndicators.setVerticalHeaderItem(last_row,new_row)

            self.twAvailableIndicators.setItem(last_row,0,item)

            item = QTableWidgetItem()
            item.setText(indicator.text or '')
            self.twAvailableIndicators.setItem(last_row,1,item)

#            item = QTableWidgetItem()
#            item.setText(indicator['value'])
#            self.twAvailableIndicators.setItem(last_row,2,item)

        self.twIndicatorsToVisualize.removeRow(row)
#        if self.twIndicatorsToVisualize.rowCount() == 0:
#            self.dataset_name = None

    @pyqtSlot(QModelIndex)
    def on_twAvailableIndicators_activated(self, index):
        self.on_pbnAddIndicator_clicked()

    @pyqtSlot(QModelIndex)
    def on_twIndicatorsToVisualize_activated(self, index):
        self.on_pbnRemoveIndicator_clicked()


