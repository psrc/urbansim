# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

import copy

from opus_core.logger import logger
from opus_core.datasets.dataset import Dataset
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.aspect.dataset_aspect import DatasetAspect


class ExogenousAspectForDataset(DatasetAspect):
    def apply(self, dataset):
        native_get_attribute = dataset.get_attribute
        
        def _proxy_for_get_attribute(name):
            try:
                return native_get_attribute(name)
                
            except NameError:
                if not isinstance(name, VariableName):
                    name = VariableName(name)
                short_name = name.get_alias()

                current_year = SimulationState().get_current_time()
                
                if short_name in dataset.exogenous_attribute_names.keys():
                    exogenous_table_name = dataset.exogenous_attribute_names[short_name]
                    
                    temporary_dataset = Dataset(in_storage=dataset.resources['in_storage'], 
                        in_table_name=exogenous_table_name, id_name='id')
                        
                    if ('year' not in dataset.get_attribute_names() or
                            not self.attribute_boxes['year'].is_in_memory()):
                        # Load the data into a temporary dataset because we
                        # don't want dataset to save the values we retrieve,
                        # since then we can't filter them by year.
                        temporary_dataset.load_dataset(
                            nchunks = 1,
                            attributes = [short_name, 'year', 'base_table_id'],
                            in_table_name = exogenous_table_name
                            )
                                    
                else:
                    raise # re-raise NameError
                                
                exogenous_data = temporary_dataset.attribute_boxes[short_name].get_data()
                year_data = temporary_dataset.attribute_boxes['year'].get_data()
                base_table_id_data = temporary_dataset.attribute_boxes['base_table_id'].get_data()

                exogenous_table_data = zip(exogenous_data, year_data, base_table_id_data)

                exogenous_attribute_values = [_attribute
                    for _attribute, _year, _base_table_id in exogenous_table_data
                    if _year == current_year]
                    
                exogenous_base_table_ids = [_base_table_id
                    for _attribute, _year, _base_table_id in exogenous_table_data
                    if _year == current_year]

                base_table_ids = native_get_attribute(dataset.resources['id_name'])

                exogenous_attributes_by_base_table_id = {}
                for base_table_id, value in zip(exogenous_base_table_ids, exogenous_attribute_values):
                    try: 
                        exogenous_attributes_by_base_table_id[base_table_id]
                    except: 
                        exogenous_attributes_by_base_table_id[base_table_id] = value
                    else: 
                        raise AttributeError("Duplicate data for base_table_id "
                            "'%s', year %s."
                                % (base_table_id, current_year))
                        
                
                result = [None]*len(base_table_ids)
                for index in range(len(base_table_ids)):
                    try:
                        result[index] = exogenous_attributes_by_base_table_id[base_table_ids[index]]
                    except KeyError:
                        raise AttributeError("Missing exogenous data for "
                            "base_table_id '%s', year %s." 
                                % (base_table_ids[index], current_year))

                return result
                
        def _determine_exogenous_attribute_names(self, resources):
            exogenous_attribute_names = {}

            try:
                storage = copy.deepcopy(resources['in_storage'])
            except: pass
            else:
                exogenous_relationships_dataset = Dataset(
                    in_storage = storage, 
                    in_table_name = 'exogenous_relationships', 
                    id_name = 'exogenous_id'
                    )
                
                try:
                    base_tables = exogenous_relationships_dataset.get_attribute('base_table')
                except:
                    logger.log_warning("An exogenous_relationships table was found, but did not contain the 'base_table' attribute.")
                    return {}
                
                try:
                    exogenous_tables = exogenous_relationships_dataset.get_attribute('exogenous_table')
                except:
                    logger.log_warning("An exogenous_relationships table was found, but did not contain the 'exogenous_table' attribute.")
                    return {}
                
                relationships = zip(base_tables, exogenous_tables)
                
                for base_table, exogenous_table in relationships:
                    if base_table == resources['in_table_name']:
                        exogenous_attributes = self.determine_stored_attribute_names(
                            in_storage = resources['in_storage'], 
                            in_table_name = exogenous_table
                            )
                        for exogenous_attribute in exogenous_attributes:
                            try: 
                                exogenous_attribute_names[exogenous_attribute]
                            except: 
                                exogenous_attribute_names[exogenous_attribute] = exogenous_table
                            else: 
                                raise AttributeError("Duplicate exogenous "
                                    "attribute '%s' found in '%s' and '%s'."     
                                       % (exogenous_attribute, 
                                          exogenous_attribute_names[exogenous_attribute], 
                                          exogenous_table
                                       )
                                   )
            return exogenous_attribute_names

        dataset.exogenous_attribute_names = _determine_exogenous_attribute_names(dataset, dataset.resources)

        # Python 2.4 allows __name__ to be set, but lower versions do not.
        # It's not a big deal if we can't change the name; it just makes things
        # easier if there's a problem and multiple aspects have been applied to
        # the same method.
        try: 
            _proxy_for_get_attribute.__name__ = ('%s__%s' 
                % (self.__class__.__name__, dataset.get_attribute.__name__))
        except: 
            pass
        
        dataset.get_attribute = _proxy_for_get_attribute
    

from opus_core.tests import opus_unittest

from numpy import array
from numpy import ma

from opus_core.store.dict_storage import dict_storage


class TestExogenousAttributes(opus_unittest.OpusTestCase):
    def setUp(self):
        self.base_table_name = 'base_table'
        self.base_id = 'base_table_id'
        self.exogenous_attribute1 = 'some_attribute'
        self.exogenous_attribute2 = 'some_other_attribute'

        base_table = {
            self.base_id:array([2,1]),
            }

        self.weather_exogenous_table_name = 'weather_exogenous'
        weather_exogenous = {
            'id':array([1,2,3,4,5,6]),
            'year':array([1980,1981,1982,1980,1981,1982]),
            self.base_id:array([1,1,1,2,2,2]),
            self.exogenous_attribute1:array([40,50,600,70,80,900]),
            self.exogenous_attribute2:array([700,800,90,1000,1100,120]),
            }

        SimulationState().set_current_time(1980)
        self.expected_exogenous_attribute_1980_1 = array([70,40])
        self.expected_exogenous_attribute_1980_2 = array([1000,700])
        self.expected_exogenous_attribute_1981_1 = array([80,50])
        self.expected_exogenous_attribute_1981_2 = array([1100,800])
        self.expected_exogenous_attribute_1982_1 = array([900,600])
        self.expected_exogenous_attribute_1982_2 = array([120,90])

            
        self.exogenous_relationships_table_name = 'exogenous_relationships'
        exogenous_relationships = {
            'exogenous_id':array([1]),
            'base_table':array([self.base_table_name]),
            'exogenous_table':array([self.weather_exogenous_table_name]),
            }        
        
        self.storage = dict_storage()
        
        for table_name, table_values in [
                (self.base_table_name, base_table),
                (self.weather_exogenous_table_name, weather_exogenous),
                (self.exogenous_relationships_table_name, exogenous_relationships)
                ]:
            self.storage.write_table(table_name=table_name, table_data=table_values)
            
    def tearDown(self):
        del self.storage
        
    def test_exogenous_attributes(self):
        base_dataset = Dataset(in_storage=self.storage, in_table_name=self.base_table_name, id_name=self.base_id)
        ExogenousAspectForDataset().apply(base_dataset)
        
        SimulationState().set_current_time(1980)
        exogenous_attribute1 = base_dataset.get_attribute(self.exogenous_attribute1)
        exogenous_attribute2 = base_dataset.get_attribute(self.exogenous_attribute2)
        
        self.assert_(ma.allequal(exogenous_attribute1, self.expected_exogenous_attribute_1980_1),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1980_1, exogenous_attribute1))
        self.assert_(ma.allequal(exogenous_attribute2, self.expected_exogenous_attribute_1980_2),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1980_2, exogenous_attribute2))
        
        SimulationState().set_current_time(1981)                
        exogenous_attribute1 = base_dataset.get_attribute(self.exogenous_attribute1)
        exogenous_attribute2 = base_dataset.get_attribute(self.exogenous_attribute2)
        
        self.assert_(ma.allequal(exogenous_attribute1, self.expected_exogenous_attribute_1981_1),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1981_1, exogenous_attribute1))
        self.assert_(ma.allequal(exogenous_attribute2, self.expected_exogenous_attribute_1981_2),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1981_2, exogenous_attribute2))
                
        SimulationState().set_current_time(1982)
        exogenous_attribute1 = base_dataset.get_attribute(self.exogenous_attribute1)
        exogenous_attribute2 = base_dataset.get_attribute(self.exogenous_attribute2)
        
        self.assert_(ma.allequal(exogenous_attribute1, self.expected_exogenous_attribute_1982_1),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1982_1, exogenous_attribute1))
        self.assert_(ma.allequal(exogenous_attribute2, self.expected_exogenous_attribute_1982_2),
            "Exogenous attribute loaded incorrectly. Expected '%s'; received '%s'."
                % (self.expected_exogenous_attribute_1982_2, exogenous_attribute2))
                
    def test_err_duplicate_data(self):
        weather_exogenous_override = {
            'id':array([1,4]),
            'year':array([1980, 1980]),
            self.base_id:array([1,1]), # Both 1980, both base_table_id 1.
            self.exogenous_attribute1:array([40,70]),
            self.exogenous_attribute2:array([700,1000]),
            }
        self.storage.write_table(table_name=self.weather_exogenous_table_name,
            table_data=weather_exogenous_override)
        
        base_dataset = Dataset(in_storage=self.storage, in_table_name=self.base_table_name, id_name=self.base_id)
        ExogenousAspectForDataset().apply(base_dataset)
        
        SimulationState().set_current_time(1980)
        self.assertRaises(AttributeError, base_dataset.get_attribute, self.exogenous_attribute1)

if __name__ == '__main__':
    opus_unittest.main()