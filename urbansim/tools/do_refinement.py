# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
from opus_core.logger import logger
from urbansim.models.refinement_model import RefinementModel
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from shutil import copytree
import os

class RefinementOptionGroup:
    def __init__(self, usage="python %prog <-c /cache/directory> <-s start_year | --refinements-directory > [-e end_year] [--package-order='urbansim,opus_core'] [--backup-before-refinement] [--help]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-c", "--cache-directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory containing cache for the simulated years")
        self.parser.add_option("-s", "--start-year", dest="start_year", default = None, type="int",
                               action="store", help="Start year for refinement(inclusive), if unspecified starting with the smallest year in refinement dataset")
        self.parser.add_option("-e", "--end-year", dest="end_year", default = None, type="int",
                               action="store", help="End year for refinement(inclusive), , if unspecified stoping with the largest year in refinement dataset")
        self.parser.add_option("--refinements-directory", dest="refinements_directory", default = None,
                               action="store", help="Immediate directory containing refinements cache, if not in the cache directory specified by -c or --cache-directory")
        self.parser.add_option("--backup-before-refinement", dest="backup", default=False, action="store_true", 
                               help="Whether backup year cache before doing refinement; not backup by default")
        self.parser.add_option("--package-order", dest="package_order", default="urbansim,opus_core", action="store", type="string",
                               help="The package order for SessionConfiguration, needs to be specified if there are datasets in refinements that are defined in packages other than 'urbansim, opus_core'")
        
        
        
if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    option_group = RefinementOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    if options.cache_directory is None:
        parser.print_usage()
        raise StandardError, "cache directory argument is required (-c or --cache-directory)"

    if (options.start_year is None) and (options.refinements_directory is None):
        parser.print_usage()
        raise StandardError, "Either start year (argument -s or --start-year) or refinements directory (argument --refinements-directory) must be given."

    
    start_year = options.start_year
    end_year = options.end_year
    package_order = [ package.strip() for package in options.package_order.split(",") ]
    refinements = None
    refinements_storage = None
    if options.refinements_directory is not None:
        refinements_storage = StorageFactory().get_storage('flt_storage', storage_location=options.refinements_directory)
        refinements = DatasetFactory().search_for_dataset('refinement', package_order, arguments={'in_storage':refinements_storage})
        years = refinements.get_attribute('year')
        if start_year is None: start_year = years.min()
        if end_year is None: end_year = years.max()
        
    simulation_state = SimulationState()
    simulation_state.set_cache_directory(options.cache_directory)
    simulation_state.set_current_time(start_year)
    attribute_cache = AttributeCache()
    dataset_pool = SessionConfiguration(new_instance=True,
                                        package_order=package_order,
                                        in_storage=attribute_cache).get_dataset_pool()
    
    if refinements is None:
        refinements = dataset_pool.get_dataset('refinement')
        years = refinements.get_attribute('year')
        if start_year is None: start_year = years.min()
        if end_year is None: end_year = years.max()

    for year in range(start_year, end_year+1):
        logger.start_block("Doing refinement for %s" % year )
        simulation_state.set_current_time(year)
        
        ## reload refinements, from original refinement_directory or dataset_pool, in case it's been changed by refinement model
        if refinements_storage is not None:
            refinements = DatasetFactory().search_for_dataset('refinement', package_order, arguments={'in_storage':refinements_storage})
        else:
            refinements = dataset_pool.get_dataset('refinement')
            
        if options.backup:
            src_dir = os.path.join(options.cache_directory, str(year))
            dst_dir = os.path.join(options.cache_directory, 'backup', str(year))
            if os.path.exists(src_dir):
                logger.log_status("Backing up %s to %s" % (src_dir, dst_dir))
                copytree(src_dir, dst_dir)
        RefinementModel().run(refinements, current_year=year, dataset_pool=dataset_pool)
        if dataset_pool.has_dataset('refinement'):
            #avoid caching refinements
            dataset_pool._remove_dataset('refinement')  
        dataset_pool.flush_loaded_datasets()
        dataset_pool.remove_all_datasets()
        logger.end_block()
