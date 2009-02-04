#
# UrbanSim software. Copyright (C) 2005-2008 University of Washington
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

from opus_core.class_factory import ClassFactory 
from opus_core.logger import logger

class VisualizationFactory:

    def visualize(self, 
                  indicators_to_visualize,
                  computed_indicators,
                  visualization_type, 
                  *args, **kwargs):
        
        class_names = {
           'matplotlib_map':'MatplotlibMap',
           'matplotlib_chart':'MatplotlibChart',
           'table':'Table'
        }
        
        module = 'opus_gui.results_manager.run.indicator_framework.visualizer.visualizers'
        module_composed_name = module + '.' + visualization_type
        
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        indicator_directory = example_indicator.source_data.get_indicator_directory()
        additional_args = {
            'indicator_directory':indicator_directory
        }
        kwargs.update(additional_args)
        visualization = ClassFactory().get_class(
            module_composed_name = module_composed_name,
            class_name = class_names[visualization_type],
            arguments=kwargs)
        
        try:
            visualization = visualization.visualize(
               indicators_to_visualize = indicators_to_visualize,
               computed_indicators = computed_indicators, *args)
        except Exception, e: 
            msg = 'Could not create the %s visualization for %s'%(visualization_type, module_composed_name)
            logger.log_error(msg)
            raise
        
        return visualization