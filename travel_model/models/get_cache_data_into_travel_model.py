# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.simulation_state import SimulationState
from numpy import array, float32, ones
from opus_core.store.attribute_cache import AttributeCache
from travel_model.models.abstract_travel_model import AbstractTravelModel
from opus_core.datasets.dataset import Dataset
from opus_core.session_configuration import SessionConfiguration

class GetCacheDataIntoTravelModel(AbstractTravelModel):
    """Get needed travel model data from UrbanSim cache into inputs for travel model.
    """

    def run(self, config, year, *args, **kwargs):
        """This is the main entry point.  It gets the appropriate configuration info from the 
        travel_model_configuration part of this config, and then copies the specified 
        UrbanSim data into files for travel mdel to read.  
        """
        cache_directory = config['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration(new_instance=True,
                                            package_order=config['dataset_pool_configuration'].package_order,
                                            in_storage=attribute_cache).get_dataset_pool()

        #cache_storage = AttributeCache().get_flt_storage_for_year(year_for_base_year_cache)
        #datasets = DatasetFactory().create_datasets_from_flt(config.get('datasets_to_preload',{}),
                                                            #"urbansim",
                                                            #additional_arguments={'in_storage': attribute_cache})
        zone_set = dataset_pool.get_dataset('zone')
        self.prepare_for_run(config['travel_model_configuration'], year)
        self.create_travel_model_input_file(config, year, zone_set, dataset_pool,
                                            *args, **kwargs)

    def prepare_for_run(self, *args, **kwargs):
        ##not implemented
        return        

    def create_travel_model_input_file(self, *args, **kwargs):
        """"""
        raise NotImplementedError, "subclass responsibility"
