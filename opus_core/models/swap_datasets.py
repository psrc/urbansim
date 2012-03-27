# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.models.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger
import re, glob, os, shutil
from numpy import where, ones, zeros, logical_and, clip, round_

class SwapDatasets(Model):
    """ swap dataset of specified prefix and suffix
    """
    model_name = "Swap Datasets"

    def __init__(self, model_name=None, model_short_name=None):
        """ A simple model that renames datasets of certain pattern; it is mostly useful 
        for setting up scenarios.  For example, keep development_constraints_scenario1 
        and development_constraints_scenario2 in base_year_data, and set up SwapDataset
        to use which dataset according to which scenario is running
        """
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name

    def run(self, prefix='', suffix='', dataset_pool=None, alt_location=None, target_location=None): 
        """
        prefix, suffix - 'YEAR' is a magic word in prefix/suffix which will be replaced with 
        the current run year number, for example,
           - suffix='_YEAR' will swap 'zoning_2020' to 'zoning' in simulation year 2020, 
                                 and, if existing, 'zoning' to 'zoning_ORIGINAL' 
        by default, only search for datasets in the cache directory for current year
           - alt_location: alternative location to search for datasets of specified patterns,
                           for example, base_year_cache

           - target_location: where to put the datasets to be renamed
        """
        current_year = SimulationState().get_current_time()
        self.prefix = re.sub('YEAR', str(current_year), prefix) 
        self.suffix = re.sub('YEAR', str(current_year), suffix)
        
        if target_location is not None:
            target_location = target_location.get_storage_location()

        locations = []
        if dataset_pool is not None:
            storage = dataset_pool.get_storage().get_flt_storage_for_year(current_year)
            location = storage.get_storage_location()
            locations.append(location)
            if target_location is None:
                target_location = location

        if alt_location is not None:
            location = alt_location.get_storage_location()
            locations.append(location)
            if target_location is None:
                target_location = location

        for pattern in [os.path.join(location, '%s*%s' % (prefix, suffix)) 
                        for location in locations]:
            self._rename_datasets(pattern, target_location)

    def _rename_datasets(self, pattern, location, dataset_pool=None):
        for current_name in glob.iglob(pattern):
            _, new_name = os.path.split(current_name)
            new_name = re.sub("^%s" % self.prefix, '', new_name) 
            new_name = re.sub("%s$" % self.suffix, '', new_name) 
            new_name = os.path.join(location, new_name)

            if os.path.exists(new_name):
                swapped_name = new_name + "_ORIGINAL"
                shutil.move(new_name, swapped_name)
                logger.log_status("Backed up %s to %s" % (new_name, swapped_name))

            shutil.move(current_name, new_name)
            logger.log_status("Renamed %s to %s" % (current_name, new_name))
            ## hack to reload dataset already loaded
            if dataset_pool is not None:
                dataset_name = os.path.split(new_name)[1]
                dataset_pool._remove_dataset(dataset_name)
                dataset_pool.get_dataset(dataset_name)

