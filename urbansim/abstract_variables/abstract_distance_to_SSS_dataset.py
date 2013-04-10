# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.abstract_variables.abstract_nearest_element_of_SSS_dataset import abstract_nearest_element_of_SSS_dataset

class abstract_distance_to_SSS_dataset(abstract_nearest_element_of_SSS_dataset):
    """distance of a dataset centroid to nearest SSS dataset point.
    """
    _return_type = "float32"
    
    def compute(self, dataset_pool):
        distances, indices =  abstract_nearest_element_of_SSS_dataset._compute(self, dataset_pool)
        return distances



