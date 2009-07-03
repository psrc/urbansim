# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os
from shutil import rmtree

from opus_core.model import Model
from opus_core.logger import logger
from opus_core.resources import Resources
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.flt_storage import flt_storage
from opus_core.storage_factory import StorageFactory
from opus_core.simulation_state import SimulationState
from opus_core.variables.attribute_type import AttributeType
from opus_core.storage_factory import StorageFactory
from opus_core.session_configuration import SessionConfiguration

from urbansim.rollback_gridcells import RollbackGridcells
from urbansim.rollback_gridcells_from_buildings import RollbackGridcellsFromBuildings

class UnrollGridcells(Model):
    def unroll_gridcells_to_cache(self, gridcells, development_event_history, 
                                  cache_directory, base_year):
        """Populate the cache with the unrolled gridcells info derived
        from the development_event_history table.
        """
        logger.start_block('Unrolling gridcell data')

        try:
            storage = AttributeCache().get_flt_storage_for_year(base_year)
            
            urbansim_constant = SessionConfiguration().get_dataset_from_pool('urbansim_constant')
            print "recent_years = %s" % urbansim_constant['recent_years']
            
            recent_years = urbansim_constant['recent_years']
            
            # Unroll for each year in the development_event_history table.
            years = self._years_in_development_event_history(development_event_history)
            
            earliest_year = min(years)
            
            roller = RollbackGridcells()
            for year in range(base_year, earliest_year-1, -1):
                logger.start_block('Unrolling gridcells into year %d' % year)
                try:
                    roller.unroll_gridcells_for_one_year(gridcells, 
                                                         development_event_history, 
                                                         year)
                    flt_directory = os.path.join(cache_directory, str(year-1))
                    flt_storage = StorageFactory().get_storage(
                        type='flt_storage', subdir='store', 
                        storage_location=flt_directory)
                    gridcells.write_dataset(out_storage=flt_storage)
                finally:
                    logger.end_block()
            
        finally:
            logger.end_block()

    def _years_in_development_event_history(self, dataset):
        """Returns the set of years with data in this dataset, in descending order."""
        years = set()
        for v in dataset.get_attribute('scheduled_year'):
            years.add(v)
        
        years = list(years)
        years.sort()
        years.reverse()
        
        return years
    
    def unroll_gridcells_to_cache_from_buildings(self, gridcells, buildings, 
                                  cache_directory, base_year):
        """Populate the cache with the unrolled gridcells info derived
        from the buildings table.
        """
        logger.start_block('Unrolling gridcell data from buildings')

        try:
            storage = AttributeCache().get_flt_storage_for_year(base_year)
            
            urbansim_constant = SessionConfiguration().get_dataset_from_pool('urbansim_constant')
            print "recent_years = %s" % urbansim_constant['recent_years']
            
            recent_years = urbansim_constant['recent_years']
            roller = RollbackGridcellsFromBuildings()
            for year in range(base_year, base_year-recent_years-1, -1):
                logger.start_block('Unrolling gridcells into year %d' % (year-1))
                try:
                    roller.unroll_gridcells_for_one_year(gridcells, 
                                                         buildings, 
                                                         year,
                                                         dataset_pool=SessionConfiguration().get_dataset_pool())
                    flt_directory = os.path.join(cache_directory, str(year-1))
                    flt_storage = StorageFactory().get_storage(
                        type='flt_storage', subdir='store', 
                        storage_location=flt_directory)
                    gridcells.write_dataset(out_storage=flt_storage)
                finally:
                    logger.end_block()
                
        finally:
            logger.end_block()