# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from opus_core.logger import logger
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_gui.results_manager.run.indicator_framework.visualizer.visualizers.mapnik_map import MapnikMap

class MapnikAnimation(MapnikMap):

    def get_file_extension(self):
        return 'gif'

    def visualize(self, 
                  indicators_to_visualize,
                  computed_indicators):
        """Create a map for the given indicator, save it to the cache
        directory's 'indicators' sub-directory."""
        
        #TODO: eliminate this example indicator stuff
        example_indicator = computed_indicators[indicators_to_visualize[0]]
        source_data = example_indicator.source_data        
        dataset_to_attribute_map = {}
        
        package_order = source_data.get_package_order()
            
            
        self._create_input_stores(years = source_data.years)

        for name, computed_indicator in computed_indicators.items():
            if name not in indicators_to_visualize: continue
            
            if computed_indicator.source_data != source_data:
                raise Exception('result templates in indicator batch must all be the same.')
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
                    in_storage = AttributeCache()) 
                SimulationState().set_cache_directory(source_data.cache_directory)
                SimulationState().set_current_time(year)
                dataset = SessionConfiguration().get_dataset_from_pool(dataset_name)
                dataset.load_dataset()

                if dataset.get_coordinate_system() is not None:
                    dataset.compute_variables(names = dataset.get_coordinate_system())
                
                for indicator_name, computed_name in attributes:
                        
                    indicator = computed_indicators[indicator_name]
                    
                    table_data = self.input_stores[year].load_table(
                        table_name = dataset_name,
                        column_names = [computed_name])

                    if computed_name in table_data:

                        table_name = self.get_name(
                            dataset_name = dataset_name,
                            years = [year],
                            attribute_names = [indicator_name])
                        
                        if self.scale: 
                            min_value, max_value = self.scale
                        else:
                            min_value, max_value = (None, None)
                        
                        file_path = os.path.join(self.storage_location,
                                             'anim_' + table_name + '.' + MapnikMap.get_file_extension(self))
                        
                        dataset.add_attribute(name = str(computed_name), 
                                              data = table_data[computed_name])
                        
                        dataset.plot_map(
                             name = str(computed_name),
                             min_value = min_value, 
                             max_value = max_value, 
                             file = str(file_path), 
                             my_title = str(indicator_name), 
                             color_list = self.color_list,
                             range_list = self.range_list,
                             label_list = self.label_list,
                             is_animation = True,
                             year = year,
                             resolution = self.resolution,
                             page_dims = self.page_dims,
                             map_lower_left = self.map_lower_left,
                             map_upper_right = self.map_upper_right,
                             legend_lower_left = self.legend_lower_left,
                             legend_upper_right = self.legend_upper_right
                             #filter = where(table_data[computed_name] != -1)
                             #filter = 'urbansim.gridcell.is_fully_in_water'                                 
                        )
        
                        #metadata = ([indicator_name], table_name, [year])
                        #viz_metadata.append(metadata)
                    else:
                        logger.log_warning('There is no computed indicator %s'%computed_name)
        
            for indicator_name, computed_name in attributes:                
                self.create_animation(
                    dataset_name = dataset_name,
                    year_list = source_data.years,
                    indicator_name = str(indicator_name),
                    viz_metadata = viz_metadata
                )
                
        visualization_representations = []
        for indicator_names, table_name, years in viz_metadata:            
            visualization_representations.append(
                self._get_visualization_metadata(
                    computed_indicators = computed_indicators,
                    indicators_to_visualize = indicator_names,
                    table_name = table_name,
                    years = years)
            )
        
        return visualization_representations
    
    # precondition: year_list must always have at least one element
    # this function is called by the visualize function
    def create_animation(self, dataset_name, year_list, indicator_name, viz_metadata):
        map_file_list = []
        for year in year_list:
            map_file_list.append(os.path.join(self.storage_location,'anim_'+dataset_name+'_map_'+str(year)+'_'+indicator_name+'.'+MapnikMap.get_file_extension(self)))
        
        table_name = dataset_name+'_animated_map_'+str(min(year_list))+'_'+indicator_name
        animation_file_name = str(os.path.join(self.storage_location,table_name+'.'+self.get_file_extension()))
        os.system('convert -delay 100 %s -loop 0 %s' % (' '.join(map_file_list), animation_file_name))

        # delete intermediate png files
        for i in range(map_file_list.__len__()):
            os.remove(map_file_list[i])

        metadata = ([indicator_name], table_name, [min(year_list)])
        viz_metadata.append(metadata)

                              
if __name__ == '__main__':
    try:
        import mapnik
    except:
        logger.log_warning('could not import mapnik')

