# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from PyQt4.QtCore import QString

from opus_gui.results_manager.controllers.dialogs.abstract_configure_batch_indicator_visualization import AbstractConfigureBatchIndicatorVisualization
from xml.etree.cElementTree import Element, SubElement
from opus_gui.results_manager.results_manager_functions import add_batch_indicator_visualization

class ConfigureNewBatchIndicatorVisualization(AbstractConfigureBatchIndicatorVisualization):
    def __init__(self, project, batch_node, parent_widget = None):
        AbstractConfigureBatchIndicatorVisualization.__init__(self, project, parent_widget)

        self._setup_co_dataset_name()
        self._setup_indicators()
        self._setup_co_viz_type()
        self._setup_co_output_type()

        self.batch_node = batch_node
        self.set_default_mapnik_options()

    def set_default_mapnik_options(self):
        # these default values are also hard-coded in opus_gui.results_manager.run.batch_processor.py
        self.mapnik_options['bucket_colors'] = '#e0eee0, #c7e9c0, #a1d99b, #7ccd7c, #74c476, #41ab5d, #238b45, #006400, #00441b, #00340b' # green
        self.mapnik_options['bucket_ranges'] = 'linear_scale'
        self.mapnik_options['bucket_labels'] = 'range_labels'

    def on_buttonBox_accepted(self):
        # Quickie for defining attrib dicts
        _t = lambda x: {'type': x, 'hidden':'True'}

        viz_params = self._get_viz_spec()
        if viz_params is None:
            self.close()
            return

        viz_name = str(self.leVizName.text()).replace(' ','_')

#        viz_type_text = str(self.cboVizType.currentText())
#        viz_type = self._get_type_mapper()[viz_type_text]

        # Assemble the visualization node
        viz_node = Element(viz_name, {'type':'batch_visualization'})
#        SubElement(viz_node, 'visualization_type',
#                   _t('string')).text = viz_type
        for viz_param in viz_params:
            tag = viz_param['name']
            value = viz_param['value']
            type_ = ''
            if isinstance(value, (str, QString)):
                type_ = 'string'
            elif isinstance(value, int):
                type_ = 'integer'
            elif isinstance(value, list):
                type_ = 'list'
            SubElement(viz_node, tag, _t(type_)).text = str(value)
        add_batch_indicator_visualization(self.batch_node, viz_node)

        self.close()
