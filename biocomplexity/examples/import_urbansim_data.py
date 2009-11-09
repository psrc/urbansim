# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

import os

from biocomplexity.datasets.land_cover_dataset import LandCoverDataset

from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory

from urbansim.datasets.gridcell_dataset import GridcellDataset


class ImportUrbansimData(object):
    """ Import data from urbansim cache directory, and compute the following
    computed variables: devt, de, commden, house_den, comm_add and house_add.
    """
    
    land_cover_urbansim_output_variables = ["biocomplexity.land_cover.devt",
                                            #"biocomplexity.land_cover.de",
                                            #"biocomplexity.land_cover.house_add",
                                            #"biocomplexity.land_cover.comm_add",
                                            "biocomplexity.land_cover.house_den",
                                            "biocomplexity.land_cover.comm_den"]
    
    def compute_computed_variables(self, base_directory, urbansim_cache_directory, years):
        
        for year in [years[0]]:
            land_cover_path = os.path.join(base_directory, str(year))
            #print land_cover_path
            land_covers = LandCoverDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path),
                                       out_storage=StorageFactory().get_storage('flt_storage', storage_location=land_cover_path))
            land_covers.load_dataset()
            #print land_covers.get_attribute("devgrid_id")
        
            gridcell_path = os.path.join(urbansim_cache_directory)
            gridcells = GridcellDataset(in_storage=StorageFactory().get_storage('flt_storage', storage_location=gridcell_path))
            gridcells.load_dataset()
            #print gridcells.summary()
        
            ## BUG: dataset_pool is not defined
            land_covers.compute_variables(self.land_cover_urbansim_output_variables, 
                                          dataset_pool=dataset_pool)
            land_covers.write_dataset(attributes='*')
            #land_covers.flush_dataset()
            del gridcells
            del land_covers