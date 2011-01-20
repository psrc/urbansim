# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array, ma, arange


class Tests(opus_unittest.OpusTestCase):
    
    # like aggregate_disaggregate.py, except that the thing being aggregated is an expression
    # omits tests involving number_of_agents

    def test_aggregate(self):
        # test aggregate with no function specified (so defaults to 'sum')
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'zone_id':array([1,2]),
                }
            )
        storage.write_table(table_name='gridcells',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'grid_id':array([1,2,3,4]),
                'zone_id':array([1,2,1,2]),
                }
            )
        zone_dataset = Dataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name='zone')
        gridcell_dataset = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        dataset_pool._add_dataset('zone', zone_dataset)
        values = zone_dataset.compute_variables(['zone.aggregate(10.0*gridcell.my_variable)'], dataset_pool=dataset_pool)
        should_be = array([45, 90]) 
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate")
        
    def test_aggregate_fully_qualified_variable(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'zone_id':array([1,2]),
                }
            )
        # it would be nicer to call this table 'gridcells' but we want to use the existing test variable
        storage.write_table(table_name='tests',
            table_data={
                'a_dependent_variable':array([4,8,0.5,1]), 
                'id':array([1,2,3,4]),
                'zone_id':array([1,2,1,2]),
                }
            )
        zone_dataset = Dataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name='zone')
        test_dataset = Dataset(in_storage=storage, in_table_name='tests', id_name="id", dataset_name='tests')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('zone', zone_dataset)
        dataset_pool._add_dataset('tests', test_dataset)
        values = zone_dataset.compute_variables(['zone.aggregate(10.0*opus_core.tests.a_test_variable)'], dataset_pool=dataset_pool)
        should_be = array([450, 900]) 
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in test_aggregate_fully_qualified_variable")

    def test_aggregate_sum(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2]),
                }
            )
        storage.write_table(table_name='faz', table_data={"id2":array([1,2])})
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        values = ds2.compute_variables(['myfaz.aggregate(10.0*myzone.my_variable, function=sum)'], dataset_pool=dataset_pool)
        should_be = array([45,90]) 
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_sum")

    def test_aggregate_sum_one_level(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,2,1,40,23,78]), 
                'id0':arange(7)+1,
                'id1':array([1,3,1,2,3,2,1])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3]), 
                'id2':array([1,2,1])
                }
            )
        storage.write_table(table_name='fazdistr',
            table_data={
                'id2':array([1,2])
                }
            )
        ds0 = Dataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistr', id_name="id2", dataset_name="myfazdistr")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds0)
        dataset_pool._add_dataset('myfaz',ds1)
        dataset_pool._add_dataset('myfazdistr',ds2)
        values = ds2.compute_variables(['myfazdistr.aggregate(10.0*myzone.my_variable, intermediates=[myfaz])'], dataset_pool=dataset_pool)
        should_be = array([1320, 240])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_sum_one_level") 

    def test_versioning_with_aggregate(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='households',
            table_data={
                'my_variable':array([4,8,2,1,40,23,78]), 
                'id0':arange(7)+1,
                'id1':array([1,3,1,2,3,2,1])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3]), 
                'id2':array([1,2,1])
                }
            )
        storage.write_table(table_name='fazdistr',
            table_data={
                'id2':array([1,2])
                }
            )
        ds0 = Dataset(in_storage=storage, in_table_name='households', id_name="id0", dataset_name="myhousehold")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistr', id_name="id2", dataset_name="myfazdistr")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myhousehold', ds0)
        dataset_pool._add_dataset('myfaz',ds1)
        dataset_pool._add_dataset('myfazdistr',ds2)
        ds0.modify_attribute("id1", array([1,3,1,2,3,2,1])) # has version 1
        variable = 'my_var = myfazdistr.aggregate(10.0*myhousehold.my_variable, intermediates=[myfaz])'
        ds2.compute_variables([variable], dataset_pool=dataset_pool)
        self.assert_(ds2.get_version("my_var")==0)
        ds2.compute_variables([variable], dataset_pool=dataset_pool)
        self.assert_(ds2.get_version("my_var")==0) # version should stay the same, i.e. it should not recompute
        ds0.touch_attribute("id1") # has version 2
        ds2.compute_variables([variable], dataset_pool=dataset_pool)
        self.assert_(ds2.get_version("my_var")==1) # version should be 1, i.e. it should recompute when id changes
        ds1.touch_attribute("id2") # has version 1
        ds2.compute_variables([variable], dataset_pool=dataset_pool)
        self.assert_(ds2.get_version("my_var")==2) # version should be 2, i.e. it should recompute when id changes
 

    def test_aggregate_sum_two_levels(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,2,1,40,23,78,20, 25]), 
                'id0':arange(9)+1,
                'id1':array([1,3,1,2,3,2,1, 4, 4])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3,4]),
                'id2':array([1,2,1,3])}
            )
        storage.write_table(table_name='fazdistrs',
            table_data={
                'id2':array([1,2,3]), 
                'id3':array([1,2,1])
                }
            )
        storage.write_table(table_name='neighborhoods',
            table_data={
                "id3":array([1,2])
                }
            )
        ds0 = Dataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistrs', id_name="id2", dataset_name="myfazdistr")
        ds3 = Dataset(in_storage=storage, in_table_name='neighborhoods', id_name="id3", dataset_name="myneighborhood")          
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds0)
        dataset_pool._add_dataset('myfaz',ds1)
        dataset_pool._add_dataset('myfazdistr',ds2)
        dataset_pool._add_dataset('myneighborhood',ds3)
        values = ds3.compute_variables(['myneighborhood.aggregate(10.0*myzone.my_variable, intermediates=[myfaz,myfazdistr], function=sum)'], dataset_pool=dataset_pool)
        should_be = array([1770, 240])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_sum_two_levels")    
        
    def test_aggregate_mean(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,10,1]), 
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(table_name='faz',
            table_data={
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        values = ds2.compute_variables(['myfaz.aggregate(10.0*myzone.my_variable, function=mean)'], dataset_pool=dataset_pool)
        should_be = array([70, 45])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_mean")      

    def test_aggregate_all(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={'my_variable': array([4,8,0.5,1]), 'id': array([1,2,3,4])})
        storage.write_table(table_name='regions',
            table_data={'id': array([1])})
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='regions', id_name="id", dataset_name="myregion")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myregion', ds2)
        ds2.compute_variables(["myvar = myregion.aggregate_all(10.0*myzone.my_variable)"], dataset_pool=dataset_pool)         
        values = ds2.get_attribute("myvar")
        should_be = array([135])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_all")

    def test_aggregate_all_sum(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,0.5,1]), 
                'id':array([1,2,3,4]),
                }
            )
        storage.write_table(table_name='regions',
            table_data={
                'id':array([1]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='regions', id_name="id", dataset_name="myregion")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myregion', ds2)
        ds2.compute_variables(["myvar = myregion.aggregate_all(10.0*myzone.my_variable, function=sum)"], dataset_pool=dataset_pool)    
        values = ds2.get_attribute("myvar")
        should_be = array([135])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_all_sum")

    def test_aggregate_all_mean(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'my_variable':array([4,8,10,1]), 
                'id':array([1,2,3,4]),
                }
            )
        storage.write_table(table_name='regions',
            table_data={
                "id":array([1]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='regions', id_name="id", dataset_name="myregion")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myregion', ds2)
        ds2.compute_variables(["myvar = myregion.aggregate_all(10.0*myzone.my_variable, function=mean)"], dataset_pool=dataset_pool)
        values = ds2.get_attribute("myvar")
        should_be = array([57.5])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_all_mean")      

    def test_disaggregate(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        values = ds.compute_variables(["myzone.disaggregate(10.0*myfaz.my_variable)"], dataset_pool=dataset_pool)
        should_be = array([40, 80, 40, 80])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in disaggregate")
        
    def test_versioning_with_disaggregate(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'id':array([1,2,3,4]),
                'id2':array([1,2,1,2])
                }
            )
        storage.write_table(table_name='faz',
            table_data={
                'my_variable':array([4,8]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = Dataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        var = "my_var = myzone.disaggregate(10.0*myfaz.my_variable)"
        ds.modify_attribute("id2", array([2,1,2,1])) # should have version 1
        ds.compute_variables([var], dataset_pool=dataset_pool)
        self.assert_(ds.get_version("my_var")==0)
        ds.compute_variables([var], dataset_pool=dataset_pool)
        self.assert_(ds.get_version("my_var")==0) # version should stay the same, i.e. it should not recompute
        ds.touch_attribute("id2") # has version 2
        ds.compute_variables([var], dataset_pool=dataset_pool)
        self.assert_(ds.get_version("my_var")==1) # version should be 1, i.e. it should recompute when id changes
 
    def test_disaggregate_fully_qualified_variable(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'zone_id':array([1,2,3,4]),
                'id':array([1,2,1,2])
                }
            )
        # it would be nicer to call this table 'fazzes' but we want to use the existing test variable
        storage.write_table(table_name='test_locations',
            table_data={
                'cost':array([4,8]), 
                'id':array([1,2])
                }
            )
        zone_dataset = Dataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name="zone")
        test_dataset = Dataset(in_storage=storage, in_table_name='test_locations', id_name="id", dataset_name='test_location')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('zone', zone_dataset)
        dataset_pool._add_dataset('test_location', test_dataset)
        values = zone_dataset.compute_variables(['zone.disaggregate(10.0*opus_core.test_location.cost_times_3)'], dataset_pool=dataset_pool)
        should_be = array([120, 240, 120, 240]) 
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in test_disaggregate_fully_qualified_variable")

    def test_disaggregate_one_level(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'id0':arange(7)+1,
                'id1':array([1,3,1,2,3,2,1])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3]),
                'id2':array([1,2,1])
                }
            )
        storage.write_table(table_name='fazdistr',
            table_data={
                'my_variable':array([40,50]), 
                'id2':array([1,2])
                }
            )
        ds0 = Dataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistr', id_name="id2", dataset_name="myfazdistr")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds0)
        dataset_pool._add_dataset('myfaz', ds1)
        dataset_pool._add_dataset('myfazdistr', ds2)
        values = ds0.compute_variables(["myzone.disaggregate(10.0*myfazdistr.my_variable, intermediates=[myfaz])"], dataset_pool=dataset_pool)
        should_be = array([400, 400, 400, 500, 400, 500, 400])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in disaggregate_one_level") 
          
    def test_disaggregate_two_levels(self):
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='gridcells',
            table_data={
                'id':arange(9)+1,
                'id0':array([7,6,1,3,4,4,5,2,5])
                }
            )
        storage.write_table(table_name='zones',
            table_data={
                'id0':arange(7)+1,
                'id1':array([1,3,1,2,3,2,1])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3]),
                'id2':array([1,2,1])
                }
            )
        storage.write_table(table_name='fazdistrs',
            table_data={
                'my_variable':array([40,50]), 
                'id2':array([1,2])
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='gridcells', id_name="id0", dataset_name="mygridcell")
        ds0 = Dataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistrs', id_name="id2", dataset_name="myfazdistr")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('mygridcell', ds)
        dataset_pool._add_dataset('myzone', ds0)
        dataset_pool._add_dataset('myfaz', ds1)
        dataset_pool._add_dataset('myfazdistr', ds2)
        values = ds.compute_variables(["mygridcell.disaggregate(10.0*myfazdistr.my_variable, intermediates=[myfaz,myzone])"], dataset_pool=dataset_pool)
        should_be = array([400, 500, 400, 400, 500, 500, 400, 400, 400])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in disaggregate_two_levels")

    def test_disaggregate_and_multiply(self):
        # Perform two different disaggregations and multiply the results.  This tests using a dataset name in both the
        # list of intermediates and as the dataset being disaggregated (myfaz in this case).
        expr = "myzone.disaggregate(2.0*myfaz.fazsqft) * myzone.disaggregate(3.0*myfazdistr.my_variable, intermediates=[myfaz])"
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='zones',
            table_data={
                'id0':arange(7)+1,
                'id1':array([1,3,1,2,3,2,1])
                }
            )
        storage.write_table(table_name='fazes',
            table_data={
                'id1':array([1,2,3]),
                'id2':array([1,2,1]),
                'fazsqft':array([10,50,100])
                }
            )
        storage.write_table(table_name='fazdistrs',
            table_data={
                'my_variable':array([40,50]), 
                'id2':array([1,2])
                }
            )
        ds0 = Dataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = Dataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = Dataset(in_storage=storage, in_table_name='fazdistrs', id_name="id2", dataset_name="myfazdistr")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds0)
        dataset_pool._add_dataset('myfaz', ds1)
        dataset_pool._add_dataset('myfazdistr', ds2)
        values = ds0.compute_variables([expr], dataset_pool=dataset_pool)
        should_be = array([2400, 24000, 2400, 15000, 24000, 15000, 2400])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in disaggregate_and_multiply")
        
if __name__=='__main__':
    opus_unittest.main()
