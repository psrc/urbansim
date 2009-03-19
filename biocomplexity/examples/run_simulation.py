
# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from urbansim.datasets.gridcell_dataset import GridcellDataset
from biocomplexity.datasets.land_cover_dataset import LandCoverDataset
from biocomplexity.models.land_cover_change_model import LandCoverChangeModel
from biocomplexity.equation_specification import EquationSpecification
from opus_core.coefficients import Coefficients
from opus_core.storage_factory import StorageFactory
from opus_core.opus_package import OpusPackage
from opus_core.store.attribute_cache import AttributeCache
from opus_core.simulation_state import SimulationState
from biocomplexity.constants import Constants
from numpy import arange

import os


class Simulation(object):
    """ Import data from urbansim cache directory, and compute the following
    computed variables: devt, de, commden, house_den, comm_add and house_add.
    """
    
    package_path = OpusPackage().get_path_for_package("biocomplexity") 
    lct_attribute = "biocomplexity.land_cover.lct_recoded"
    #lct_attribute = "lct"
    possible_lcts = range(1,15)
    
    def run(self, base_directory, urbansim_cache_directory, years):
        """ run the simulation
                base_directory: directory contains all years folder of lccm.
                urbansim_cache_directory: directory contains all years folder of urbansim cache.
                years: lists of year to run."""
        model = LandCoverChangeModel(self.possible_lcts, submodel_string=self.lct_attribute, 
                                     choice_attribute_name= self.lct_attribute, debuglevel=4)
        coefficients = Coefficients()
        storage = StorageFactory().get_storage('tab_storage', 
            storage_location=os.path.join(self.package_path, 'data'))
        coefficients.load(in_storage=storage, in_table_name="land_cover_change_model_coefficients")
        specification = EquationSpecification(in_storage=storage)
        specification.load(in_table_name="land_cover_change_model_specification")
        specification.set_variable_prefix("biocomplexity.land_cover.")
        constants = Constants()
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(urbansim_cache_directory)
        attribute_cache = AttributeCache()
        index = arange(100000)
        for year in years:
            simulation_state.set_current_time(year)
            #land_cover_path = os.path.join(base_directory, str(year))
            land_cover_path = base_directory
            land_covers = LandCoverDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path),
                                       out_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path),
                                       debuglevel=4)
            land_covers.subset_by_index(index)
            #land_covers.load_dataset()
            gridcells = GridcellDataset(in_storage=attribute_cache, debuglevel=4)

            agents_index = None
            model.run(specification, coefficients, land_covers, data_objects={"gridcell":gridcells,
                          "constants":constants, "flush_variables":True},
                          chunk_specification = {'nchunks':1}
                          )
            land_covers.flush_dataset()
            del gridcells
            del land_covers
    
if __name__ == "__main__":
    #base_dir = "/home/hana/data/lccm/LCCM_4County"
    #base_dir = r"O:\unix\projects\urbansim9\land_cover_change_model\LCCM_4County_converted/1995"
    base_dir = "/projects/urbansim9/land_cover_change_model/LCCM_4County_converted/1995"
    #base_dir = "/home/hana/data/LCCM_4County/1995"
    #urbansim_cache  = r"D:\urbansim_cache\2006_01_12__11_44"
    urbansim_cache  = "/projects/urbansim/urbbuild/urbansim_cache"
    Simulation().run(base_dir, urbansim_cache, [2007])
    