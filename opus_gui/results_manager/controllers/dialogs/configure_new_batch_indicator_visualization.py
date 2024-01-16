# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_gui.results_manager.controllers.dialogs.abstract_configure_batch_indicator_visualization import AbstractConfigureBatchIndicatorVisualization
from lxml.etree import Element, SubElement
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

    def on_buttonBox_accepted(self):
        viz_params = self._get_viz_spec()
        if viz_params is None:
            self.reject()

        viz_name = str(self.leVizName.text()).strip()
        viz_node = Element('batch_visualization', {'name': viz_name,
                                                   'type':'batch_visualization',
                                                   'hidden': 'Children'})
        self._update_xml_from_dict(viz_node, viz_params)
        add_batch_indicator_visualization(self.batch_node, viz_node)
        self.accept()
