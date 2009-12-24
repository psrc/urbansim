# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import DatasetSubset
from numpy import array, where, ones, zeros
from numpy import arange, resize
from opus_core.model import Model
from opus_core.logger import logger
from opus_core.sampling_toolbox import sample_noreplace, sample_replace
from opus_core.simulation_state import SimulationState

class ScheduledEventsModel(Model):
    """ The generic model handling scheduled events, such as scheduled employment events, scheduled development events.
    Specifically, this model handles 4 types of scheduled events:
    1. put a given number of "agents"  to certain location, e.g. build a new building of specified attributes on a certain parcel;
    2. put a given number of "agents"  to certain geography (not necessarily the location set)
    3. modify certain attributes of location_set/agent_set, e.g. building renovation and remodel
    4. manipulate records satisfying certain conditions,
        e.g. demolish all buildings on certain parcels;
        close down a factory and relocate all employment.
        
    See unittests for examples.
    """
    
    model_name = "Scheduled Events Model"
    model_short_name = "SEM"
    
    def __init__(self, dataset, scheduled_events_dataset=None, model_name=None, model_short_name=None):
        self.dataset = dataset
        if scheduled_events_dataset:
            self.scheduled_events = scheduled_events_dataset
        if model_name:
            self.model_name = model_name
        if model_short_name:
            self.model_short_name = model_short_name
        
    def run(self, year=None,
            dataset_pool=None,  **kwargs):
        """
        """
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()

        if year is None:
            year = SimulationState().get_current_time()
        
        this_year_index = where(self.scheduled_events.get_attribute('year')==year)[0]
        scheduled_events_for_this_year = DatasetSubset(self.scheduled_events, this_year_index)
        scheduled_events_for_this_year.load_dataset_if_not_loaded()
        column_names = list(set( self.scheduled_events.get_known_attribute_names() ) - set( [ 'year', 'action', 'attribute', 'amount', 'event_id', '_hidden_id_'] ))
        column_names.sort()
#        column_values = dict([ (name, scheduled_events_for_this_year.get_attribute(name)) for name in column_names])
        
        for index in range(scheduled_events_for_this_year.size()):
            indicator = ones( self.dataset.size(), dtype='bool' )
            event_attr = {}
            for attribute in column_names:
                if attribute in self.dataset.get_known_attribute_names():
                    dataset_attribute = self.dataset.get_attribute(attribute)
                else:
                    ## this is done inside the loop because some action may delete computed attributes, such as dataset.add_elements()
                    try:
                        dataset_attribute = self.dataset.compute_one_variable_with_unknown_package(attribute, dataset_pool=dataset_pool)
                    except:
                        raise ValueError, "attribute %s used in scheduled events dataset can not be found in dataset %s" % (attribute, self.dataset.get_dataset_name())
                
#                if attribute in column_names: 
                aval = scheduled_events_for_this_year.get_attribute(attribute)[index]
                if aval == -1:
                    continue    # ignore if column value is -1
                else:
                    indicator *= dataset_attribute == aval
                    event_attr.update({attribute:aval})
            
            #agents in dataset satisfying all conditions are identified by indicator
            legit_index = where(indicator)[0]
            
            this_event = scheduled_events_for_this_year.get_data_element(index)
            if not hasattr(this_event, 'attribute'):
                action_attr_name = ''
            else:
                action_attr_name = this_event.attribute
            action_function = getattr(self, '_' + this_event.action.strip().lower())
            action_function( amount=this_event.amount,
                             attribute=action_attr_name,
                             dataset=self.dataset, 
                             index=legit_index,
                             data_dict=event_attr )
            
            self.post_run(self.dataset, legit_index, **kwargs)

        return self.dataset

    def _add(self, amount=0, attribute='', dataset=None, index=None, data_dict={}, **kwargs):
        new_data = {}
        dataset_known_attributes = dataset.get_known_attribute_names() 
        if index.size > 0:  # sample from agents
            lucky_index = sample_replace(index, amount)
            for attr in dataset_known_attributes:
                new_data[attr] = dataset.get_attribute_by_index(attr, lucky_index)
        else:
            ## if attributes are not fully specified, the missing attributes will be filled with 0's
            for attr in dataset.get_primary_attribute_names():
                if data_dict.has_key(attr):
                    new_data[attr] = resize(array(data_dict[attr]), amount)
                else:
                    if attr == dataset.get_id_name()[0]:
                        new_data[attr] = zeros(amount, dtype=dataset.get_id_attribute().dtype)
                    else:
                        logger.log_warning("Attribute %s is unspecified for 'add' event; its value will be sampled from all %s values of %s." % 
                                           (attr, attr, dataset.get_dataset_name()) )
                        new_data[attr] = sample_replace(dataset.get_attribute(attr), amount)
        
        dataset.add_elements(data=new_data, change_ids_if_not_unique=True)
    
    def _remove(self, amount=0, attribute='', dataset=None, index=None, **kwargs):
        if index is None:
            index = arange(dataset.size())
        if index.size < amount:
            logger.log_warning("Number of observations satisfying event condition (%s) is less than the number to be removed (%s); remove %s instead" % 
                               (index.size, amount, index.size))
            amount = index.size
        
        if index.size == amount:
            to_be_removed = index
        else:
            to_be_removed = sample_noreplace(index, amount)
        
        if to_be_removed.size > 0:
            dataset.remove_elements(to_be_removed)
    
    def _target(self, amount=0, attribute='', dataset=None, index=None, **kwargs):
        if dataset is None:
            dataset = self.dataset
        actual_num = index.size
        target_num = amount
        if actual_num < target_num:
            self._add(amount=target_num - actual_num, attribute=attribute, dataset=dataset, index=index, **kwargs)
        elif actual_num > target_num:
            self._remove(amount=actual_num - target_num, attribute=attribute, dataset=dataset, index=index, **kwargs)
    
    def _set_value(self, amount, attribute, dataset=None, index=None, **kwargs):
        #set_values_of_one_attribute(self, attribute, values, index=None):
        values = resize(array(amount), index.shape)
        dataset.set_values_of_one_attribute(attribute, values, index=index)

    def _add_value(self, amount, attribute, dataset=None, index=None, **kwargs):
        values = dataset.get_attribute_by_index(attribute, index) + amount
        dataset.set_values_of_one_attribute(attribute, values, index=index)

    def _subtract_value(self, amount, attribute, dataset=None, index=None, **kwargs):
        values = dataset.get_attribute_by_index(attribute, index) - amount
        dataset.set_values_of_one_attribute(attribute, values, index=index)

    def _multiply_value(self, amount, attribute, dataset=None, index=None, **kwargs):
        values = dataset.get_attribute_by_index(attribute, index) * amount
        dataset.set_values_of_one_attribute(attribute, values, index=index)
    
    def prepare_for_run(self, scheduled_events_dataset_name=None, scheduled_events_table=None, scheduled_events_storage=None):
        if (scheduled_events_storage is None) or ((scheduled_events_table is None) and (scheduled_events_dataset_name is None)):
            ## this should not happen
            dataset_pool = SessionConfiguration().get_dataset_pool()
            self.scheduled_events = dataset_pool.get_dataset( 'scheduled_%s_events' % self.dataset.get_dataset_name() )
            return self.scheduled_events
        
        if not scheduled_events_dataset_name:
            scheduled_events_dataset_name = DatasetFactory().dataset_name_for_table(scheduled_events_table)
        
        self.scheduled_events = DatasetFactory().search_for_dataset(scheduled_events_dataset_name,
                                                                  package_order=SessionConfiguration().package_order,
                                                                  arguments={'in_storage':scheduled_events_storage, 
                                                                             'in_table_name':scheduled_events_table,
                                                                             'id_name':[]
                                                                             }
                                                                  )
        return self.scheduled_events
    
    def post_run(self, *args, **kwargs):
        """ To be implemented in child class for additional function, like synchronizing persons with households table
        """
        pass
                
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from numpy import allclose, logical_and
import tempfile, shutil
from opus_core.store.attribute_cache import AttributeCache
from urbansim.job.aliases import aliases

aliases +=[ 'raz_id = job.disaggregate(parcel.raz_id, intermediates=[building])' ]
class Tests(opus_unittest.OpusTestCase):
        
    def setUp(self):
        building_data = {
            'building_id': array([1, 2, 3, 4, 5, 6, 7, 8]),
            'parcel_id':   array([1, 2, 2, 3, 4, 4, 5, 5]),
            'non_residential_sqft': \
                           array([6, 2, 3, 6, 1, 2, 5, 0]),
            'residential_units': \
                           array([0, 0, 0, 0, 0, 0, 1, 1]),
            'price_per_unit': \
                           array([50,21,32,15,60,90,100,200])
            }
        parcel_data = {
            'parcel_id':                array([1, 2, 3, 4, 5]),
            'generic_land_use_type_id': array([6, 6, 3, 4, 1]),
            'raz_id':                   array([3, 4, 5, 5, 6])
            }
        job_data = {
            'job_id':      array([ 1, 2, 3, 4, 5, 6, 7, 8]),
            'building_id': array([ 1, 1, 2, 3, 6, 1, 6, 4]),
            #'parcel_id':   array([ 1, 1, 2, 2, 4, 1, 4, 3]),
            #'raz_id':      array([ 3, 3, 4, 4, 5, 3, 5, 5]),
            'sector_id':   array([13,12,13,12,13,13,12,13]),
            'dummy_id':    array([ 1, 2, 3, 4, 5, 6, 7, 8]),
        }
        
        self.tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')

        SimulationState().set_cache_directory(self.tmp_dir)
        self.attribute_cache = AttributeCache()
        self.dataset_pool = SessionConfiguration(new_instance=True,
                                                 package_order=['urbansim', 'opus_core'],
                                                 in_storage=self.attribute_cache).get_dataset_pool()        

        #storage = StorageFactory().get_storage('flt_storage', storage_location=self.tmp_dir)
        self.attribute_cache.write_table(table_name = 'buildings', table_data = building_data)
        self.attribute_cache.write_table(table_name = 'parcels', table_data = parcel_data)
#        self.attribute_cache.write_table(table_name = 'households', table_data = household_data)
        self.attribute_cache.write_table(table_name = 'jobs', table_data = job_data)
#        self.attribute_cache.write_table(table_name = 'persons', table_data = person_data)
#        self.attribute_cache.write_table(table_name = 'refinements', table_data = refinement_data)
        
        #self.dataset_pool = DatasetPool(storage = storage, package_order = ['urbansim_parcel', 'urbansim', 'opus_core'])
#        self.refinement = self.dataset_pool.get_dataset('refinement')
        self.jobs = self.dataset_pool.get_dataset('job')
#        self.persons = self.dataset_pool.get_dataset('person')
#        self.hhs = self.dataset_pool.get_dataset('household')
        self.buildings = self.dataset_pool.get_dataset('building')
        #self.buildings.compute_variables('raz_id=building.disaggregate(parcel.raz_id)', self.dataset_pool)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)        

    def test_add_and_remove_agents(self):
        """
        """
        scheduled_events_data = {
            "year":       array([    2000,      2000,      2000,   2000,    2000]),
            "action":     array(["remove",  "remove",     "add",  "add", "target"]),
            "amount":     array([       1,         1,         4,      3,    7]),
            "sector_id":  array([      13,        12,        -1,     11,    12]),
            "building_id":array([      -1,        -1,        -1,      8,    -1]),
            "raz_id":     array([       3,         5,         5,     -1,    -1]),
            }

#        self.attribute_cache.write_table(table_name = 'scheduled_events', table_data = scheduled_events_data)
#        events_dataset = self.dataset_pool.get_dataset('scheduled_event')

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='events', table_data=scheduled_events_data)
        events_dataset = Dataset(in_storage=storage, in_table_name='events', id_name=[])

        model = ScheduledEventsModel(self.jobs, scheduled_events_dataset=events_dataset)
        model.run(year=2000, dataset_pool=self.dataset_pool)

        #check that there are indeed 50000 total households after running the model
        results = self.jobs.size()
        should_be = 18
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        #examine each action in turn:
        results = logical_and(self.jobs.get_attribute("sector_id")==13, self.jobs.get_attribute("raz_id")==3).sum()
        should_be = 2-1
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = logical_and(self.jobs.get_attribute("sector_id")==12, self.jobs.get_attribute("raz_id")==5).sum()
        should_be = 1-1
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = (self.jobs.get_attribute("raz_id")==5).sum()
        should_be = 3-1+4
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = logical_and(self.jobs.get_attribute("sector_id")==11, self.jobs.get_attribute("building_id")==8).sum()
        should_be = 0+3
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = (self.jobs.get_attribute("sector_id")==12).sum()
        should_be = 7
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
    def DELtest_add_and_remove_agents_from_geography_other_than_location_set(self):
        """this has been included in the above test
        """
        scheduled_events_data = {
            "year":       array([    2000,      2000,      2000,   2000,    2000]),
            "action":     array(["remove",  "remove",     "add",  "add", "target"]),
            "amount":     array([       1,         1,         4,      3,    7]),
            "sector_id":  array([      13,        13,        -1,     11,    12]),
            "building_id":array([      -1,        -1,        -1,      8,    -1]),
            "raz_id":     array([       3,         4,         5,     -1,    -1]),
            }

#        self.attribute_cache.write_table(table_name = 'scheduled_events', table_data = scheduled_events_data)
#        events_dataset = self.dataset_pool.get_dataset('scheduled_event')

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='events', table_data=scheduled_events_data)
        events_dataset = Dataset(in_storage=storage, in_table_name='events', id_name=[])

        model = ScheduledEventsModel(self.jobs, scheduled_events_dataset=events_dataset)
        model.run(year=2000, dataset_pool=self.dataset_pool)

        #check that there are indeed 50000 total households after running the model
        results = self.jobs.size()
        should_be = 17
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        #examine each action in turn:
        results = logical_and(self.jobs.get_attribute("sector_id")==13, self.jobs.get_attribute("raz_id")==3).sum()
        should_be = 2-1
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = logical_and(self.jobs.get_attribute("sector_id")==13, self.jobs.get_attribute("raz_id")==4).sum()
        should_be = 1-1
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = (self.jobs.get_attribute("raz_id")==5).sum()
        should_be = 2+4
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = logical_and(self.jobs.get_attribute("sector_id")==11, self.jobs.get_attribute("building_id")==8).sum()
        should_be = 0+3
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = (self.jobs.get_attribute("sector_id")==12).sum()
        should_be = 7
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))


    def test_modify_dataset_attribute(self):
        """
        """
        scheduled_events_data = {
            "year":       array([    2000,               2000,          2000,             2000,             2001,             2001]),
            "action":     array(["set_value", "subtract_value",  "add_value", "multiply_value", "subtract_value", "multiply_value"]),
            "amount":     array([       4,                   2,            3,               1.1,               1,              0.9]),
            "attribute":  array(["residential_units", "non_residential_sqft", "non_residential_sqft","price_per_unit", "non_residential_sqft", "price_per_unit"]),
            "building_id":array([       3,                   3,            5,                -1,               3,               -1]),
            "parcel_id":  array([      -1,                  -1,           -1,                 5,              -1,                5]),
            }

#        self.attribute_cache.write_table(table_name = 'scheduled_events', table_data = scheduled_events_data)
#        events_dataset = self.dataset_pool.get_dataset('scheduled_event')

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='events', table_data=scheduled_events_data)
        events_dataset = Dataset(in_storage=storage, in_table_name='events', id_name=[])

        model = ScheduledEventsModel(self.buildings, scheduled_events_dataset=events_dataset)
        model.run(year=2000, dataset_pool=self.dataset_pool)

        results = self.buildings.size()
        should_be = 8
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        #examine each action in turn:
        index = self.buildings.get_attribute("building_id")==3
        results = (self.buildings.get_attribute("residential_units")[index], self.buildings.get_attribute("non_residential_sqft")[index])
        should_be = (4, 1) 
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        index = self.buildings.get_attribute("building_id")==5    
        results = self.buildings.get_attribute("non_residential_sqft")[index]
        should_be = 1+3
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        results = self.buildings.get_attribute("price_per_unit")
        should_be = array([50,21,32,15,60,90,100*1.1,200*1.1])
        self.assertTrue(allclose(should_be, results),
                         "Error, should_be: %s, but result: %s" % (should_be, results))

        model.run(year=2001)

        index = self.buildings.get_attribute("building_id")==3
        results = (self.buildings.get_attribute("residential_units")[index], self.buildings.get_attribute("non_residential_sqft")[index])
        should_be = (4, 0) 
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        results = self.buildings.get_attribute("price_per_unit")
        should_be = array([50,21,32,15,60,90,100*1.1*0.9,200*1.1*0.9])
        self.assertTrue(allclose(should_be, results),
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
    def test_demolish_buildings_on_a_parcel(self):
        """test demolish buildings, create new buildings, and convert an existing building
        """
        scheduled_events_data = {
            "year":       array([    2000,    2000,          2000,              2000,             2000]),
            "action":     array(["remove",   "add",   "set_value",             "set_value", "set_value"]),
            "amount":     array([       4,       2,             8,                 7,              150]),
            "attribute":  array(["",             "", "residential_units","non_residential_sqft", "price_per_unit"]),
            "building_id":array([       3,      -1,             5,                 5,               5]),
            "parcel_id":  array([      -1,       1,            -1,                -1,              -1]),
    "residential_units":  array([      -1,       2,            -1,                -1,              -1]),
 "non_residential_sqft":  array([      -1,       1,            -1,                -1,              -1]),
       "price_per_unit":  array([      -1,      99,            -1,                -1,              -1]),                        
            }

#        self.attribute_cache.write_table(table_name = 'scheduled_events', table_data = scheduled_events_data)
#        events_dataset = self.dataset_pool.get_dataset('scheduled_event')

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='events', table_data=scheduled_events_data)
        events_dataset = Dataset(in_storage=storage, in_table_name='events', id_name=[])

        model = ScheduledEventsModel(self.buildings, scheduled_events_dataset=events_dataset)
        model.run(year=2000, dataset_pool=self.dataset_pool)

        results = self.buildings.size()
        should_be = 9
        self.assertEqual(should_be, results,
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        index = self.buildings.get_attribute("building_id")>8
        results = array([ 
                    self.buildings.get_attribute("parcel_id")[index],
                    self.buildings.get_attribute("residential_units")[index],
                    self.buildings.get_attribute("non_residential_sqft")[index],
                    self.buildings.get_attribute("price_per_unit")[index]
                   ]) 
        should_be = array([[1, 1], [2, 2], [1, 1], [99, 99]])
        self.assertTrue(allclose(should_be, results),
                         "Error, should_be: %s, but result: %s" % (should_be, results))
        
        index = where(self.buildings.get_attribute("building_id")==5)
        results = self.buildings.get_multiple_attributes(["parcel_id", "residential_units", "non_residential_sqft", "price_per_unit"])[index]
        
        should_be = array([4, 8, 7, 150])
        self.assertTrue(allclose(should_be, results),
                         "Error, should_be: %s, but result: %s" % (should_be, results))
                
if __name__=='__main__':
    opus_unittest.main()