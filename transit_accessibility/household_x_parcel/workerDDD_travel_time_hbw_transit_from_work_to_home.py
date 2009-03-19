# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from numpy import array, int32, arange
from urbansim.functions import attribute_label
from opus_core.logger import logger

try:
    import networkx
except:
    logger.log_warning('Could not load networkx. Skipping %s.' % __file__)
else:
    class workerDDD_travel_time_hbw_transit_from_work_to_home(Variable):
        """travel_time_hbw_transit_from_work_to_home"""    
    
        default_value = 18000
        def __init__(self, number):
            worker = "worker" + str(number)
            self.work_parcel_id = worker + "_work_place_parcel_id"
            Variable.__init__(self)
        
        def dependencies(self):
            return [attribute_label("parcel","parcel_id"),
                    "psrc.household." + self.work_parcel_id,
                    "transit_accessibility.edge.target"]
    
        def compute(self, dataset_pool):
            edges = dataset_pool.get_dataset('edge')
            edges.get_graph(create_using=networkx.XDiGraph(),edgetype=int)
    
            household_x_parcels = self.get_dataset()
            home_parcel = household_x_parcels.get_2d_dataset_attribute("parcel_id").astype(int32)
            n, m = home_parcel.shape
            n_index = household_x_parcels.get_index(1)
            if n_index is None:
                n_index = arange(n)
            
            work_parcel = household_x_parcels.get_dataset(1).get_attribute_by_index(self.work_parcel_id, 
                                                                                 n_index).astype(int32)
            
            pairs = map(lambda x, y: (x, y.tolist()), work_parcel, home_parcel)
            results = array(edges.compute_dijkstra_path_length(pairs, 
                                                               default_value=self.default_value,
    #                                                           show_progress=True
                                                               ))
            
            return array(results)
                    
    
    from opus_core.tests import opus_unittest
    from numpy import ma
    from psrc.datasets.parcel_dataset import ParcelDataset
    from urbansim.datasets.household_dataset import HouseholdDataset
    from psrc.datasets.household_x_parcel_dataset import HouseholdXParcelDataset
    from opus_core.storage_factory import StorageFactory
    from opus_core.datasets.dataset_pool import DatasetPool
    
    class TestsHouseholdParcelWorkerDddTravelTimeHbwTransitFromWorkToHome(opus_unittest.OpusTestCase):
        variable_name = "transit_accessibility.household_x_parcel.worker2_travel_time_hbw_transit_from_work_to_home"
        
        def setUp(self):
            logger.enable_hidden_error_and_warning_words()
    
        def tearDown(self):
            logger.disable_hidden_error_and_warning_words()
        
        def test_my_inputs(self):
            storage = StorageFactory().get_storage('dict_storage')
            
            edges_table_name = 'edges'
            storage.write_table(
                    table_name=edges_table_name,
                    table_data={
                        'source':array([10,  20,   10,   30]),
                        'target':array([2,  3,   3,   1]),
                        'cost':array([12, 1, 15, 17])                        
                        },
                )
                
            parcels_table_name = 'parcels'
            storage.write_table(
                    table_name=parcels_table_name,
                    table_data={
                        'parcel_id':array([1,2,3])
                        },
                )
                
            households_table_name = 'households'
            storage.write_table(
                    table_name=households_table_name,
                    table_data={
                        'household_id':array([1,2,3,4]),
                        'worker2_work_place_parcel_id':array([10, 30, 30, 20])
                        },
                )
        
            parcels = ParcelDataset(in_storage=storage, in_table_name=parcels_table_name)
            households = HouseholdDataset(in_storage=storage, in_table_name=households_table_name)
            
            household_x_parcels = HouseholdXParcelDataset(dataset1=households, dataset2=parcels)
    
            dataset_pool = DatasetPool(package_order=['transit_accessibility', 'psrc', 'urbansim'],
                                   storage=storage)
            values = household_x_parcels.compute_variables(self.variable_name, dataset_pool=dataset_pool)

            default_value = workerDDD_travel_time_hbw_transit_from_work_to_home.default_value
            should_be = array([[default_value, 12, 15], [17, default_value, default_value], 
                               [17, default_value, default_value], [default_value, default_value, 1]])
            
            self.assert_(ma.allclose(values, should_be, rtol=1e-10),
                'Error in ' + self.variable_name)
    
    
    if __name__=='__main__':
        opus_unittest.main()