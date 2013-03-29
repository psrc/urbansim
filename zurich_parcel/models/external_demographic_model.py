# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import h5py
from opus_core.models.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger
from numpy import ones, in1d, array, allclose, sort, unique, empty, string_
import os.path

class ExternalDemographicModel(Model):
    """ A model that updates households with external demographic data; 
        it replaces household transition model
    """
    model_name = "External Demographic Model"

    def __init__(self, model_name=None, model_short_name=None):
        """
        model_name: optional
        model_short_name: optional
        """
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name

    def run(self, demographic_data_file, 
            household_dataset,
            person_dataset, 
            year=None,
            keep_attributes=None,
            keep_attributes_p=None,
            fill_value=-1,
            demographic_attributes=None,
            demographic_attributes_p=None,
            dataset_pool=None
            ): 
        """
        demographic_data_file: an hdf5 file that contains households and persons data
                               in pandas DataFrame format.  
                               Run paris/scripts/prepare_demographic_data.py to create
                               the file.
        household_dataset: opus dataset of household
        person_dataset: opus dataset of household
        year: integer, optional
        keep_attributes: list, attributes to keep from household dataset
        keep_attributes_p: list, attributes to keep from person dataset
        fill_value: fill attributes with fill_value for new households
        demographic_attributes: dictionary, attributes to load from external
                                demographic file.  The key of the dictionary is 
                                attribute name for household data, its value is
                                the expression to compute the attribute value.
                                See unittest for example.
        demographic_attributes_p: Same as demographic_attributes, for persons 
        dataset_pool: opus DatasetPool object, optional
        """
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()

        if not os.path.isabs(demographic_data_file):
            demographic_data_file = os.path.join(dataset_pool.get_storage().get_storage_location(), demographic_data_file)
        
        if year is None:
            year = SimulationState().get_current_time()
        ## this relies on the order of household_id in
        ## households data and persons attributes summarized 
        ## by household_id is the same
        fh = h5py.File(demographic_data_file, 'r')
        year_str = str(year)
        dmgh_current = fh[year_str]
        
        household_id = household_dataset.get_id_name()[0]
        person_id = person_dataset.get_id_name()[0]

        hhs_new = compound_array_to_dataset(dmgh_current['household'],
                                        table_name='households',
                                        id_name=household_id,
                                        dataset_name=household_dataset.dataset_name)
        ps_new = compound_array_to_dataset(dmgh_current['person'],
                                       table_name='persons',
                                       id_name=person_id,
                                       dataset_name=person_dataset.dataset_name)

        dataset_pool.replace_dataset(household_dataset.dataset_name, hhs_new)
        dataset_pool.replace_dataset(person_dataset.dataset_name, ps_new)
        
        hh_ids = hhs_new[household_id]
        n_hhs = hh_ids.size
        results = {}
        results[household_id] = hh_ids
        for k, v in demographic_attributes.iteritems():
            results[k] = hhs_new.compute_variables(v)

        logger.log_status( ('Loaded demographic characteristics {0} for {1} ' +\
                            'households from external file {2}.').format(
                            demographic_attributes.keys(), n_hhs, 
                            demographic_data_file) )

        p_ids = ps_new[person_id]
        n_ps = p_ids.size
        results_p = {}
        results_p[person_id] = p_ids
        for k, v in demographic_attributes_p.iteritems():
            results_p[k] = ps_new.compute_variables(v)

        logger.log_status( ('Loaded demographic characteristics {0} for {1} ' +\
                            'persons from external file {2}.').format(
                            demographic_attributes_p.keys(), n_ps, 
                            demographic_data_file) )

        is_existing = in1d(hh_ids, household_dataset[household_id])
        for attr in keep_attributes:
            dtype = household_dataset[attr].dtype
            values = fill_value * ones(n_hhs, dtype=dtype)
            values[is_existing] = household_dataset.get_attribute_by_id(attr,
                                                            hh_ids[is_existing])
            results[attr] = values

        is_existing = in1d(p_ids, person_dataset[person_id])
        for attr in keep_attributes_p:
            if attr in person_dataset.get_known_attribute_names():
                dtype = person_dataset[attr].dtype

                if dtype.type is string_:
                    values = empty(n_ps, dtype=dtype)
                else:
                    values = fill_value * ones(n_ps, dtype=dtype)
                values[is_existing] = person_dataset.get_attribute_by_id(attr,
                                                                p_ids[is_existing])
                results_p[attr] = values

        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name='households', table_data=results)
        storage.write_table(table_name='persons', table_data=results_p)

        new_household_ds = Dataset(in_storage=storage, 
                            in_table_name='households',
                            id_name=household_id,
                            dataset_name=household_dataset.dataset_name)
        
        new_person_ds = Dataset(in_storage=storage, 
                            in_table_name='persons',
                            id_name=person_id,
                            dataset_name=person_dataset.dataset_name)
        
        dataset_pool.replace_dataset(household_dataset.dataset_name,
                                     new_household_ds)
        dataset_pool.replace_dataset(person_dataset.dataset_name,
                                     new_person_ds)
        return (new_household_ds, new_person_ds)

def compound_array_to_dataset(nparray, table_name, **dataset_kwargs):
    ds_dict = {}
    for name in nparray.dtype.names:
        ds_dict[name] = nparray[name]

    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(table_name=table_name,
                        table_data=ds_dict)

    ds = Dataset(in_storage=storage, 
                 in_table_name=table_name,
                 **dataset_kwargs)
    return ds

import os        
import tempfile
import shutil
from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.store.attribute_cache import AttributeCache

class Tests(opus_unittest.OpusTestCase):
    """unittest"""        
    def setUp(self, attribute_cache=True):
        hh_data = {
            'household_id':  array([1,   2,  3,  4]),
            'building_id':   array([11, 22, 33, 22]),
            'size':          array([4,   3,  2,  1]),
            'income':        array([51, 52, 53, 54])*1000,
            'keep':          array([4.1, 4.2, 4.3, 4.4]),
            }
        p_data = {
            'person_id':    array([ 1,  2,  3,  5,  6,  7,  8,  9, 10]),
            'household_id': array([ 1,  1,  1,  2,  2,  3,  3,  3,  4]),
            'age':          array([75, 71, 29, 56, 16, 22, 20, 96, 88]),
            }
        if attribute_cache:
            self.tmp_dir = tempfile.mkdtemp(prefix='urbansim_tmp')
            SimulationState().set_cache_directory(self.tmp_dir)
            self.attribute_cache = AttributeCache()
            self.dataset_pool = SessionConfiguration(new_instance=True,
                                     package_order=['urbansim', 'opus_core'],
                                     in_storage=self.attribute_cache
                                    ).get_dataset_pool()        

            self.attribute_cache.write_table(table_name='households',
                                             table_data=hh_data)
            self.attribute_cache.write_table(table_name='persons',
                                             table_data=p_data)
            self.hh_ds = self.dataset_pool.get_dataset('household')
            self.p_ds = self.dataset_pool.get_dataset('person')
        else:
            storage = StorageFactory().get_storage('dict_storage')
            storage.write_table(table_name='households',
                                table_data=hh_data)
            self.hh_ds = Dataset(in_storage=storage, 
                                     in_table_name='households',
                                     dataset_name='household')
            storage.write_table(table_name='persons',
                                table_data=p_data)
            self.p_ds = Dataset(in_storage=storage, 
                                     in_table_name='persons',
                                     dataset_name='person')

        self.dmgh_data_dir = tempfile.mkdtemp(prefix='urbansim_tmp')
        self.dmgh_data_file = os.path.join(self.dmgh_data_dir, 
                                           'demographic_data.h5')
        
        out_fh = h5py.File(self.dmgh_data_file, 'w')

        n_hhs = 5
        hh_dtype = {'names':['year', 'household_id', 'income', 'head_person_id'],
                 'formats':['i4', 'i4', 'f8', 'i4']}
        hhdata = out_fh.create_dataset('household', shape=(n_hhs, ), dtype=hh_dtype, 
                                       compression='gzip', compression_opts=9)
        
        hhs = [(2000, 5, 65000.0, 9),
               (2000, 1, 61000.0, 3),
               (2000, 2, 62000.0, 4),
               (2000, 3, 63000.0, 7),
               (2001, 1, 71000.0, 3)]
        hhdata[:] = array(hhs, dtype=hh_dtype)

        n_ps = 16
        ps_dtype = {'names':['year', 'person_id', 'household_id', 'age'],
                    'formats':['i4', 'i4', 'i4', 'i4']}
        psdata = out_fh.create_dataset('person', shape=(n_ps, ), dtype=ps_dtype, 
                                       compression='gzip', compression_opts=9)
        
        ps =  [(2000, 1, 1, 76),
               (2000, 2, 1, 72),
               (2000, 3, 1, 30),
               (2000, 4, 2, -1),
               (2000, 5, 2, 57),
               (2000, 6, 2, 17),
               (2000, 9, 5, 67),
               (2000,10, 5, 71),
               (2000, 7, 3, 23),
               (2000, 8, 3, 21),
               (2000,81, 3, 2),
               (2001, 1, 1, 77),
               (2001, 2, 1, 73),
               (2001, 3, 1, 31),
               (2001, 4, 1, 35),
               (2001,31, 1, 1)]
        psdata[:] = array(ps, dtype=ps_dtype)

        dataset_names = ['household', 'person']
        for dataset_name in dataset_names:
            for year in unique(out_fh[dataset_name][:, 'year']):
                year_str = str(year)
                group = out_fh.get(year_str, None)
                if group is None:
                    group = out_fh.create_group(year_str)

                is_year = out_fh[dataset_name][:, 'year'] == year
                group.create_dataset(dataset_name, data=out_fh[dataset_name][is_year])

            del out_fh[dataset_name]
        out_fh.close()

    def tearDown(self):
        shutil.rmtree(self.dmgh_data_dir)        
        if hasattr(self, 'tmp_dir'):
            shutil.rmtree(self.tmp_dir)        

    def test_run1(self):
        model = ExternalDemographicModel()
        attrs_mapping = {'income': "household.income",
                          'size': "household.number_of_agents(person)",
                          'age_of_head': "household.aggregate(person.age * (person.disaggregate(household.head_person_id)==person.person_id))",
                     }
        attrs_mapping_p = { 'household_id': 'person.household_id',
                            'age': 'person.age',
                            'age_months' : 'age * 12', }
        model.run(self.dmgh_data_file, self.hh_ds, self.p_ds,
                  year=2000, 
                  keep_attributes=['building_id', 'keep'],
                  keep_attributes_p=[],
                  demographic_attributes=attrs_mapping,
                  demographic_attributes_p=attrs_mapping_p,
                  dataset_pool=self.dataset_pool)
        
        new_hh_ds = self.dataset_pool.get_dataset('household')

        self.assert_(allclose(new_hh_ds['household_id'], array([ 5, 1,  2,  3])))
        self.assert_(allclose(new_hh_ds['building_id'],  array([-1, 11, 22, 33])))
        self.assert_(allclose(new_hh_ds['keep'],         array([-1,4.1, 4.2, 4.3])))
        self.assert_(allclose(new_hh_ds['income'],       array([65, 61, 62, 63])*1000.0))
        self.assert_(allclose(new_hh_ds['size'],         array([ 2, 3,  3,  3])))
        self.assert_(allclose(new_hh_ds['age_of_head'],  array([67, 30, -1, 23])))
        
        new_p_ds = self.dataset_pool.get_dataset('person')
        
        print('array([' + ', '.join([str(i) for i in new_p_ds['person_id']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['household_id']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['age']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['age_months']]) + '])')
        self.assert_(allclose(new_p_ds['person_id'], array([1, 2, 3, 4, 5, 6, 9, 10, 7, 8, 81])))
        self.assert_(allclose(new_p_ds['household_id'], array([1, 1, 1, 2, 2, 2, 5, 5, 3, 3, 3])))
        self.assert_(allclose(new_p_ds['age'], array([76, 72, 30, -1, 57, 17, 67, 71, 23, 21, 2])))
        self.assert_(allclose(new_p_ds['age_months'], array([912, 864, 360, -12, 684, 204, 804, 852, 276, 252, 24])))
        self.assert_((new_p_ds['age'] * 12 == new_p_ds['age_months']).all(), 'age_months computed correctly')

        model.run(self.dmgh_data_file, self.hh_ds, self.p_ds,
                  year=2001, 
                  keep_attributes=['building_id', 'keep'],
                  keep_attributes_p=[],
                  demographic_attributes=attrs_mapping,
                  demographic_attributes_p=attrs_mapping_p,
                  dataset_pool=self.dataset_pool)

        new_hh_ds = self.dataset_pool.get_dataset('household')

        self.assert_(allclose(new_hh_ds['household_id'], array([ 1])))
        self.assert_(allclose(new_hh_ds['building_id'],  array([11])))
        self.assert_(allclose(new_hh_ds['keep'],         array([4.1])))
        self.assert_(allclose(new_hh_ds['income'],       array([71])*1000.0))
        self.assert_(allclose(new_hh_ds['size'],         array([ 5])))
        self.assert_(allclose(new_hh_ds['age_of_head'],  array([31])))

        new_p_ds = self.dataset_pool.get_dataset('person')
        
        print('array([' + ', '.join([str(i) for i in new_p_ds['person_id']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['household_id']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['age']]) + '])')
        print('array([' + ', '.join([str(i) for i in new_p_ds['age_months']]) + '])')
        self.assert_(allclose(new_p_ds['person_id'], array([1, 2, 3, 4, 31])))
        self.assert_(allclose(new_p_ds['household_id'], array([1, 1, 1, 1, 1])))
        self.assert_(allclose(new_p_ds['age'], array([77, 73, 31, 35, 1])))
        self.assert_(allclose(new_p_ds['age_months'], array([924, 876, 372, 420, 12])))
        self.assert_((new_p_ds['age'] * 12 == new_p_ds['age_months']).all(), 'age_months computed correctly')
        
if __name__ == '__main__':
    opus_unittest.main()
