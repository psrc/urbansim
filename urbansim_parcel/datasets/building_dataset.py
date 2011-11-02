# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from urbansim.datasets.dataset import Dataset as UrbansimDataset

class BuildingDataset(UrbansimDataset):
    
    id_name_default = "building_id"
    in_table_name_default = "buildings"
    out_table_name_default = "buildings"
    dataset_name = "building"
    
    def __init__(self, id_values=None, **kwargs):
        UrbansimDataset.__init__(self, **kwargs)
        
    def compute_coordinate_system(self, dataset_pool):
        parcels = dataset_pool.get_dataset('parcel')
        pcl_coordsys = parcels.get_coordinate_system()
        if pcl_coordsys is not None:
            self.compute_variables(["%s = building.disaggregate(parcel.%s)" % (pcl_coordsys[0], pcl_coordsys[0]), 
                                    "%s = building.disaggregate(parcel.%s)" % (pcl_coordsys[1], pcl_coordsys[1])],
                               dataset_pool=dataset_pool)
        return (pcl_coordsys)
