# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtCore import QString
from xml.etree.cElementTree import SubElement

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.results_manager.controllers.dialogs.abstract_configure_batch_indicator_visualization import AbstractConfigureBatchIndicatorVisualization
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.table import Table
from opus_gui.results_manager.results_manager_functions import update_batch_indicator_visualization
from opus_gui.general_manager.general_manager import get_available_spatial_dataset_names

class ConfigureExistingBatchIndicatorVisualization(AbstractConfigureBatchIndicatorVisualization):
    def __init__(self, project, batch_indicator_visualization_node, parent_widget = None):
        AbstractConfigureBatchIndicatorVisualization.__init__(self, project, parent_widget)


        self.base_node = base_node = batch_indicator_visualization_node
        self.spatial_datasets = get_available_spatial_dataset_names(project = project)
        self.leVizName.setText(base_node.tag)

        prev_dataset = str(base_node.find('dataset_name').text or '')
        prev_indicators = self._process_xml_stored_list_of_strings\
            (value = base_node.find('indicators').text or '')
        prev_output_type = str(base_node.find('output_type').text or '')

        # Use the specified visualization type if provided, otherwise fall back
        # on using Table.
        viz_type_node = base_node.find('visualization_type')
        if viz_type_node is not None:
            viz_type = str(viz_type_node.text or '')

            if viz_type in ['table_per_year', 'table_per_attribute']:
                viz_type = 'Table'
            elif viz_type not in ['Map']:
                viz_type = self._get_inverse_type_mapper()[viz_type]
            prev_viz_type = QString(viz_type)
        else:
            prev_viz_type = QString('Table')

        self._setup_co_dataset_name(value = prev_dataset)
        self._setup_indicators(existing_indicators = prev_indicators)
        self._setup_co_viz_type(value = prev_viz_type)

        inv_map = dict([(v,k) for k,v in self._get_output_types(prev_viz_type).items()])
        self._setup_co_output_type(value = inv_map[str(prev_output_type)])

        fixed_field_specification = None
        if prev_output_type == 'fixed_field':
            fixed_field_specification = base_node.find('fixed_field_specification').text or ''
            id_format = base_node.find('id_format').text or ''
            specs = self._process_xml_stored_list_of_strings(value = fixed_field_specification)
            self._set_column(column = 1, values = specs)
            self.leOption1.setText(QString(id_format))
        elif prev_output_type == 'esri':
            storage_location = base_node.find('storage_location').text or ''
            self.leOption1.setText(QString(storage_location))
        elif prev_output_type == 'sql':
            database_name = base_node.find('database_name').text or ''
            self.leOption1.setText(QString(database_name))
        elif prev_output_type == 'tab':
            try:
                prev_output_style = int(str(base_node.find('output_style').text or ''))
            except: pass
            else:
                if prev_output_style == Table.ALL:
                    self.rbSingleTable.setChecked(True)
                elif prev_output_style == Table.PER_ATTRIBUTE:
                    self.rbTablePerIndicator.setChecked(True)
                else:
                    self.rbTablePerYear.setChecked(True)
        elif prev_output_type == 'mapnik_map':
            self.mapnik_options['bucket_ranges'] = base_node.find('bucket_ranges').text
            self.mapnik_options['bucket_colors'] = base_node.find('bucket_colors').text
            self.mapnik_options['bucket_labels'] = base_node.find('bucket_labels').text

    def _process_xml_stored_list_of_strings(self, value):
        '''
        Strip the Python semantics from the stored list and return the list
        as an actual Python list object
        '''
        list_str = str(value)[1:-1] # Strip brackets
        return [i.strip()[1:-1] for i in list_str.split(',')] # Strip quotes

    def on_buttonBox_accepted(self):
        viz_params = self._get_viz_spec(convert_to_node_dictionary = False)

        if viz_params is None:
            self.close()
            return

        dataset_name = viz_params['dataset_name']
        viz_type = viz_params['visualization_type']

        close = True
        if viz_type == 'mapnik_map' and dataset_name not in self.spatial_datasets:
            MessageBox.warning(mainwindow = self.mainwindow,
                      text = "That indicator cannot be visualized as a map.",
                      detailed_text = ('The dataset %s is either not spatial or cannot be '
                                       'rendered as a grid. If the latter, please try '
                                       'exporting to an external GIS tool.'%dataset_name))
            close = False

        else:
            # Update the XML node with new data
            viz_name = str(self.leVizName.text()).replace('DATASET',dataset_name).replace(' ','_')

            # Renaming must be passed through the models to enable check for
            # inheritance and to keep the integrity of internal representations
            self.base_node.tag = viz_name
            # Update children values, creating new nodes if necessary
            for key, value in viz_params.items():
                child_node = self.base_node.find(key)
                if child_node is None:
                    # TODO Check that type actually should be 'String' for all nodes.
                    child_node = SubElement(self.base_node, key,
                                            {'type':'string', 'hidden': 'True'})
                child_node.text = str(value)
            update_batch_indicator_visualization(self.base_node)

        if close:
            self.close()

    def on_buttonBox_rejected(self):
        self.close()
