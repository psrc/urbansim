#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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

import os

from opus_core.logger import logger
from opus_gui.results.indicator_framework.visualizer.visualizers.abstract_visualization\
    import Visualization
from opus_core.store.attribute_cache import AttributeCache
from numpy import where, ma, ndarray
from opus_core.storage_factory import StorageFactory

from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration

class MatplotlibMap(Visualization):

    def __init__(self, 
                 indicator_directory,
                 name = None,
                 scale = None,
                 storage_location = None):
        self.name = name
        if storage_location is None:
            storage_location = indicator_directory
        self.storage_location = storage_location
        self.indicator_directory = indicator_directory
        self.scale = scale     #TODO: scale doesn't make sense if mixing multiple datasets
        
    def get_file_extension(self):
        return 'png'

    def get_visualization_type(self):
        return 'map'
    
    def get_additional_metadata(self):
        return  [('scale',self.scale)]
    
    def plot_map(self, dataset, attribute_data, min_value=None, max_value=None, file=None,
                 my_title="", filter=None, background=None):
        """    Plots a 2D image of attribute given by 'name'. matplotlib required.
               The dataset must have a method 'get_2d_attribute' defined that returns
               a 2D array that is to be plotted. If min_value/max_value are given, all values
               that are smaller/larger than these values are set to min_value/max_value.
               Argument background is a value to be used for background. If it is not given,
               it is considered as a 1/100 under the minimum value of the array.
               Filter is a 2D array. Points where filter is > 0 are masked out (put into background).
        """
        import matplotlib
        matplotlib.use('Qt4Agg') 
        
        from matplotlib.pylab import jet,imshow,colorbar,show,axis,savefig,close,figure,title,normalize
        from matplotlib.pylab import rot90
        
        
        
        attribute_data = attribute_data[filter]
        coord_2d_data = dataset.get_2d_attribute(attribute_data = attribute_data)
        data_mask = coord_2d_data.mask
#        if filter is not None:
#            if isinstance(filter, ndarray):
#                if not ma.allclose(filter.shape, coord_2d_data.shape):
#                    raise StandardError, "Argument filter must have the same shape as the 2d attribute."
#                filter_data = filter
#            else:
#                raise TypeError, "The filter type is invalid. A character string or a 2D numpy array allowed."
#            filter_data = where(ma.filled(filter_data,1) > 0, 1,0)
#            data_mask = ma.mask_or(data_mask, filter_data)
        nonmaskedmin = ma.minimum(coord_2d_data) - .2 * (ma.maximum(coord_2d_data) - ma.minimum(coord_2d_data))
        if max_value == None:
            max_value = ma.maximum(coord_2d_data)
        if min_value == None:
            min_value = nonmaskedmin

        coord_2d_data = ma.filled(coord_2d_data,min_value)
        if background is None:
            value_range = max_value-min_value
            background = min_value-value_range/100
        coord_2d_data = ma.filled(ma.masked_array(coord_2d_data, mask=data_mask), background)

        # Our data uses NW as 0,0, while matplotlib uses SW for 0,0.
        # Rotate the data so the map is oriented correctly.
        coord_2d_data = rot90(coord_2d_data, 1)

        jet()
        figure()
        norm = normalize(min_value, max_value)
        im = imshow(coord_2d_data,
            origin='lower',
            aspect='equal',
            interpolation=None,
            norm=norm,
            )
        
        tickfmt = '%4d'
        if isinstance(min_value, float) or isinstance(max_value, float):
            tickfmt='%1.4f'
        colorbar(format=tickfmt)

        title(my_title)
        axis('off')
        if file:
            savefig(file)
            close()
        else:
            show()
            
    def visualize(self, 
                  indicators_to_visualize,
                  computed_indicators):
        """Create a map for the given indicator, save it to the cache
        directory's 'indicators' sub-directory."""
        
        #TODO: eliminate this example indicator stuff
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        source_data = example_indicator.source_data        
        dataset_to_attribute_map = {}
        
        (package_order, package_order_exceptions) = \
            source_data.get_package_order_and_exceptions()
            
            
        self._create_input_stores(years = source_data.years)

        for name, computed_indicator in computed_indicators.items():
            if name not in indicators_to_visualize: continue
            
            if computed_indicator.source_data != source_data:
                raise 'result templates in indicator batch must all be the same.'
            dataset_name = computed_indicator.indicator.dataset_name
            if dataset_name not in dataset_to_attribute_map:
                dataset_to_attribute_map[dataset_name] = []
            dataset_to_attribute_map[dataset_name].append(name)
        
        viz_metadata = []
        for dataset_name, indicator_names in dataset_to_attribute_map.items():  
            attributes = [(name,computed_indicators[name].get_computed_dataset_column_name())
                          for name in indicator_names]                  
            for year in source_data.years:
                SessionConfiguration(
                    new_instance = True,
                    package_order = package_order,
                    package_order_exceptions = package_order_exceptions,
                    in_storage = AttributeCache()) 
                SimulationState().set_cache_directory(source_data.cache_directory)
                SimulationState().set_current_time(year)
                dataset = SessionConfiguration().get_dataset_from_pool(dataset_name)
                
                dataset.compute_variables(names = dataset.get_coordinate_system())
                
                for indicator_name, computed_name in attributes:
                    indicator = computed_indicators[indicator_name]
                    
                    table_data = self.input_stores[year].load_table(
                        table_name = dataset_name,
                        column_names = [computed_name])

                    table_name = self.get_name(
                        dataset_name = dataset_name,
                        years = [year],
                        attribute_names = [indicator_name])
                    
                    if self.scale: 
                        min_value, max_value = self.scale
                    else:
                        min_value, max_value = (None, None)
                    
                    file_path = os.path.join(self.storage_location,
                                         table_name+ '.' + self.get_file_extension())

                    self.plot_map(dataset = dataset, 
                                  attribute_data = table_data[computed_name], 
                                  min_value = min_value, 
                                  max_value = max_value, 
                                  file = file_path, 
                                  my_title = indicator_name, 
                                  filter = where(table_data[computed_name] != -1))

                    metadata = ([indicator_name], table_name, [year])
                    viz_metadata.append(metadata)
                    
        visualization_representations = []
        for indicator_names, table_name, years in viz_metadata:
            visualization_representations.append(
                self._get_visualization_metadata(
                    computed_indicators = computed_indicators,
                    indicators_to_visualize = indicator_names,
                    table_name = table_name,
                    years = years
            ))                  
        
        return visualization_representations


from opus_core.tests import opus_unittest
from opus_gui.results.indicator_framework.test_classes.abstract_indicator_test import AbstractIndicatorTest
from opus_gui.results.indicator_framework.representations.indicator import Indicator
from opus_gui.results.indicator_framework.maker.maker import Maker

class Tests(AbstractIndicatorTest):
        
    #TODO: get 2d attribute in test code
    def skip_test_create_indicator(self):
        indicator = Indicator(
                  dataset_name = 'opus_core', 
                  attribute = 'urbansim.gridcell.population'
        )
                
        maker = Maker()
        computed_indicators = maker.create_batch(
            indicators = {'population':indicator}, 
            source_data = self.source_data)
        
        indicator_path = os.path.join(self.temp_cache_path, 'indicators')
        self.assert_(not os.path.exists(indicator_path))
        
        map = MatplotlibMap(
                  indicator_directory = self.source_data.get_indicator_directory(),
                  name = 'map_of_opus_core.population(gridcell)')
                
        map.create(False)

        viz_result = map.visualize(
                        indicators_to_visualize = ['population'], 
                        computed_indicators = computed_indicators)[0]
        self.assertTrue(os.path.exists(
           os.path.join(viz_result.storage_location,
           viz_result.table_name + '.' + viz_result.file_extension)))
                              
if __name__ == '__main__':
    try: 
        import matplotlib
    except:
        print 'could not import matplotlib'
    else:
        opus_unittest.main()
