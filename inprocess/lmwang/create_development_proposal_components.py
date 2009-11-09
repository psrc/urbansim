# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import os, sys
from numpy import newaxis, array, where, reshape, concatenate, arange, zeros, ones
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.coefficients import create_coefficient_from_specification, Coefficients
from opus_core.equation_specification import EquationSpecification
from opus_core.linear_utilities import linear_utilities
from opus_core.store.attribute_cache import AttributeCache
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from urbansim.datasets.development_project_dataset import DevelopmentProjectDataset
from urbansim.datasets.building_dataset import BuildingDataset
from urbansim.datasets.job_dataset import JobDataset
from urbansim.datasets.household_dataset import HouseholdDataset
#from opus_core.dataset_pool import DatasetPool
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from optparse import OptionParser
import re

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-d", "--cache-directory", dest="cache_directory", action="store",
                      type="string",  help="cache directory")
    parser.add_option("-b", "--base-year", dest="base_year", action="store", type="int",
                      default=2000, help="base year")
    parser.add_option("-y", "--end-year", dest="end_year", action="store", type="int",
                      help="end year")
    (options, args) = parser.parse_args()

    cache_directory = options.cache_directory
    base_year = options.base_year
    end_year = options.end_year

    if cache_directory is None or base_year is None or end_year is None:
        parser.print_usage()
        
    package_order=['psrc_parcel', 'urbansim_parcel', 'psrc', 'urbansim', 'opus_core']
    
    SimulationState().set_cache_directory(cache_directory)
#        SimulationState().set_current_time(year)
    
    SessionConfiguration(new_instance=True,
                         package_order=package_order,
                         in_storage=AttributeCache())
    
    for year in range(base_year+1, end_year+1, 1):
        SimulationState().set_current_time(year)
    
#        SessionConfiguration(new_instance=True,
#                             package_order=package_order,
#                             in_storage=AttributeCache())
    
        dataset_pool=SessionConfiguration().get_dataset_pool()
        dataset_pool.remove_all_datasets()
    #    dataset_pool = DatasetPool(
    #        package_order=['psrc','urbansim','opus_core'],
    #        storage=AttributeCache())
    
        proposal_set = dataset_pool.get_dataset("development_project_proposal")
        template_component = dataset_pool.get_dataset("development_template_component")
    
        from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
        proposal_component = create_from_proposals_and_template_components(proposal_set, 
                                                                           template_component, 
                                                                           dataset_pool=dataset_pool)
    
        proposal_component.write_dataset(out_storage=AttributeCache().get_flt_storage_for_year(year),
                                         out_table_name="development_project_proposal_components")