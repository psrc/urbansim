# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from PyQt4.QtCore import QString

from opus_gui.main.controllers.dialogs.message_box import MessageBox
from opus_gui.results_manager.controllers.dialogs.abstract_configure_batch_indicator_visualization import AbstractConfigureBatchIndicatorVisualization
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.table import Table
from opus_gui.results_manager.results_manager_functions import update_batch_indicator_visualization
from opus_gui.general_manager.general_manager_functions import get_available_spatial_dataset_names

class ConfigureExistingBatchIndicatorVisualization(AbstractConfigureBatchIndicatorVisualization):
    def __init__(self, project, batch_indicator_visualization_node, parent_widget = None):
        AbstractConfigureBatchIndicatorVisualization.__init__(self, project, parent_widget)

        self.base_node = base_node = batch_indicator_visualization_node
        self.spatial_datasets = get_available_spatial_dataset_names(project = project)

        viz_name = base_node.get('name')
        viz_spec = self._get_viz_spec_from_xml_node(base_node)

        self.leVizName.setText(viz_name)

        prev_dataset = str(viz_spec['dataset_name'])
        indicator_list = viz_spec['indicators']
        prev_indicators = self._process_xml_stored_list_of_strings(value = indicator_list)
        prev_output_type = viz_spec['output_type']
        viz_type = viz_spec['visualization_type']

        # don't really know what's going on here...
        if viz_type in ['table_per_year', 'table_per_attribute']:
            viz_type = 'Table'
        elif viz_type not in ['Map']:
            viz_type = self._get_inverse_type_mapper()[viz_type]
        prev_viz_type = QString(viz_type)

        self._setup_co_dataset_name(value = prev_dataset)
        self._setup_indicators(existing_indicators = prev_indicators)
        self._setup_co_viz_type(value = prev_viz_type)

        inv_map = dict([(v,k) for k,v in self._get_output_types(prev_viz_type).items()])
        self._setup_co_output_type(value = inv_map[str(prev_output_type)])

        fixed_field_specification = None
        if prev_output_type == 'fixed_field':
            fixed_field_specification = viz_spec['fixed_field_specification']
            id_format = viz_spec['id_format'] or ''
            specs = self._process_xml_stored_list_of_strings(value = fixed_field_specification)
            self._set_column(column = 1, values = specs)
            self.leOption1.setText(QString(id_format))
        elif prev_output_type == 'esri':
            storage_location = viz_spec['storage_location'] or ''
            self.leOption1.setText(QString(storage_location))
        elif prev_output_type == 'sql':
            database_name = viz_spec['database_name'] or ''
            self.leOption1.setText(QString(database_name))
        elif prev_output_type == 'tab':
            try:
                prev_output_style = int(str(viz_spec['output_style'] or ''))
            except: pass
            else:
                if prev_output_style == Table.ALL:
                    self.rbSingleTable.setChecked(True)
                elif prev_output_style == Table.PER_ATTRIBUTE:
                    self.rbTablePerIndicator.setChecked(True)
                else:
                    self.rbTablePerYear.setChecked(True)
        elif prev_output_type == 'mapnik_map' or prev_output_type == 'mapnik_animated_map':
            self.mapnik_options['mapnik_bucket_ranges'] = viz_spec['mapnik_bucket_ranges']
            self.mapnik_options['mapnik_bucket_colors'] = viz_spec['mapnik_bucket_colors']
            self.mapnik_options['mapnik_bucket_labels'] = viz_spec['mapnik_bucket_labels']
            self.mapnik_options['mapnik_resolution'] = viz_spec['mapnik_resolution']
            self.mapnik_options['mapnik_page_dims'] = viz_spec['mapnik_page_dims']
            self.mapnik_options['mapnik_map_lower_left'] = viz_spec['mapnik_map_lower_left']
            self.mapnik_options['mapnik_map_upper_right'] = viz_spec['mapnik_map_upper_right']
            self.mapnik_options['mapnik_legend_lower_left'] = viz_spec['mapnik_legend_lower_left']
            self.mapnik_options['mapnik_legend_upper_right'] = viz_spec['mapnik_legend_upper_right']
    def _process_xml_stored_list_of_strings(self, value):
        '''
        Strip the Python semantics from the stored list and return the list
        as an actual Python list object
        '''
        list_str = str(value)[1:-1] # Strip brackets
        return [i.strip()[1:-1] for i in list_str.split(',')] # Strip quotes

    def on_buttonBox_accepted(self):
        viz_params = self._get_viz_spec()

        if viz_params is None:
            self.close()
            return

        dataset_name = viz_params['dataset_name']
        viz_type = viz_params['visualization_type']

        close = True
        if (viz_type == 'mapnik_map' or viz_type == 'mapnik_animated_map') and dataset_name not in self.spatial_datasets:
            MessageBox.warning(mainwindow = self.mainwindow,
                      text = "That indicator cannot be visualized as a map.",
                      detailed_text = ('The dataset %s is either not spatial or cannot be '
                                       'rendered as a grid. If the latter, please try '
                                       'exporting to an external GIS tool.'%dataset_name))
            close = False

        else:
            self._update_xml_from_dict(self.base_node, viz_params)
            update_batch_indicator_visualization(self.base_node)

        if close:
            self.close()

    def on_buttonBox_rejected(self):
        self.close()
