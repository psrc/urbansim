# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, repeat, ones, float32, resize, array
from numpy import zeros
from urbansim.functions import attribute_label
from opus_core.logger import logger
from opus_core.misc import unique

class time_space_prism_query(Variable):
    """abstract variable for interaction time-space prism variables"""

    default_value = 0
    _return_type="int32"
    
    agent_resource = "worker.time_window_length"
    origin_zone_id = 'worker.htaz'
    destination_zone_id = 'worker.wtaz'
    travel_data_attribute = 'travel_data.travel_time'
    travel_data_attribute_default_value = 9999  # default value if a zone pair index is not found in travel_data
    #zone_attribute_to_access = "to_be_defined_in_fully_qualified_name"
        
    def dependencies(self):
        return [ self.agent_resource,
                 self.origin_zone_id,
                 self.destination_zone_id,
                 self.travel_data_attribute,
                 #self.zone_attribute_to_access
                 ]

    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        #zones = dataset_pool.get_dataset('zone')
        travel_data = dataset_pool.get_dataset('travel_data')
        travel_data_attr_mat = travel_data.get_attribute_as_matrix(self.travel_data_attribute, 
                                                                   fill=self.travel_data_attribute_default_value)
        agent_resource = dataset.get_attribute(self.agent_resource)
        from_zone = dataset.get_attribute(self.origin_zone_id).astype("int32")
        to_zone = dataset.get_attribute(self.destination_zone_id).astype("int32")
        
        #zone_ids = zones.get_id_attribute()
        zone_ids = unique(travel_data["from_zone_id"])
        print(dir(dataset))
        results = zeros((dataset.size(), zone_ids.max()+1), dtype='bool')        
        for zone in zone_ids:
            tmp_zone = zone * ones(from_zone.shape, dtype="int32")
            t1 = travel_data_attr_mat[from_zone, tmp_zone]
            t2 = travel_data_attr_mat[tmp_zone, to_zone]
            results[where( t1 + t2 <= agent_resource)[0], zone] = 1
        
#        missing_pairs_index = travel_data.get_od_pair_index_not_in_dataset(from_zone, to_zone)
#        if missing_pairs_index[0].size > 0:
#            results[missing_pairs_index] = self.default_value
#            logger.log_warning("zone pairs at index %s are not in travel data; value set to %s." % ( str(missing_pairs_index), self.default_value) )
        return results

from opus_core.tests import opus_unittest
from opus_core.misc import opus_path_for_variable_from_module_path
from opus_core.store.file_flt_storage import file_flt_storage
from opus_core.datasets.dataset_pool import DatasetPool

#class Tests(opus_unittest.OpusTestCase):
class Tests(object):
    def setUp(self):
        cache_path = "/workspace/opus/data/asu"
        self.variable_name = opus_path_for_variable_from_module_path(__file__)
        storage = file_flt_storage(cache_path)
        table_names = storage.get_table_names()
        self.dataset_pool = DatasetPool(package_order=['urbansim'],
                                        storage=storage)
        for table_name in table_names:
            dataset = self.dataset_pool.get_dataset(table_name, dataset_arguments={'id_name':[]})
            
    def test_compute(self):
        dataset_name = self.variable_name.split('.')[-2]
        dataset = self.dataset_pool.get_dataset(dataset_name)
        results = dataset.compute_variables(self.variable_name, dataset_pool=self.dataset_pool)

        #print results.sum(0), self.variable_name

if __name__=='__main__':
    #opus_unittest.main()
    
    import time
    t0 = time.time()    
    t = Tests()
    t.setUp()
    t.test_compute()
    print(time.time() - t0)
