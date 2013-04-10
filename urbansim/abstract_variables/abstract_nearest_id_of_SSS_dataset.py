# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_nearest_element_of_SSS_dataset import abstract_nearest_element_of_SSS_dataset

class abstract_nearest_id_of_SSS_dataset(abstract_nearest_element_of_SSS_dataset):
    """id of the nearest element of the given dataset to the centroid of the base dataset.
    """
    _return_type = "int32"
    
    def compute(self, dataset_pool):
        distances, indices =  abstract_nearest_element_of_SSS_dataset._compute(self, dataset_pool)
        return dataset_pool.get_dataset(self.to_dataset).get_id_attribute()[indices]



