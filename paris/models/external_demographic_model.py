# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

import h5py
from opus_core.models.model import Model
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.logger import logger
from numpy import ones, in1d, array, allclose, sort, unique

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
            year=None,
            keep_attributes=None,
            fill_value=-1,
            demographic_attributes=None,
            dataset_pool=None
            ): 
        """
        demographic_data_file: an hdf5 file that contains households and persons data
                               in pandas DataFrame format.  
                               Run paris/scripts/prepare_demographic_data.py to create
                               the file.
        household_dataset: opus dataset of household
        year: integer, optional
        keep_attributes: list, attributes to keep from household dataset
        fill_value: fill attributes with fill_value for new households
        demographic_attributes: dictionary, attributes to load from external
                                demographic file.  The key of the dictionary is 
                                attribute name for household data, its value is
                                the expression to compute the attribute value.
                                See unittest for example.
        dataset_pool: opus DatasetPool object, optional
        """
        if dataset_pool is None:
            dataset_pool = SessionConfiguration().get_dataset_pool()

        hh_ds = household_dataset
        if year is None:
            year = SimulationState().get_current_time()
        ## this relies on the order of household_id in
        ## households data and persons attributes summarized 
        ## by household_id is the same
        fh = h5py.File(demographic_data_file, 'r')
        year_str = str(year)
        dmgh_current = fh[year_str]
        #hh_dmgh = fh['household']
        #ps_dmgh = fh['person']
        #hh_dmgh_current = hh_dmgh[hh_dmgh[:,'year'] == year]
        #ps_dmgh_current = ps_dmgh[ps_dmgh[:,'year'] == year]

        hhs_new = compound_array_to_dataset(dmgh_current['household'],
                                        table_name='households',
                                        id_name=hh_ds.get_id_name(),
                                        dataset_name=hh_ds.dataset_name)
        ps = compound_array_to_dataset(dmgh_current['person'],
                                       table_name='persons',
                                       id_name='person_id',
                                       dataset_name='person')

        dataset_pool.replace_dataset(hh_ds.dataset_name, hhs_new)
        dataset_pool.replace_dataset('person', ps)
       
        hh_ids = hhs_new['household_id']
        n_hhs = hh_ids.size
        results = {}
        results['household_id'] = hh_ids
        for k, v in demographic_attributes.iteritems():
            results[k] = hhs_new.compute_variables(v)

        logger.log_status( ('Loaded demographic characteristics {} for {} ' +\
                            'households from external file {}.').format(
                            demographic_attributes.keys(), n_hhs, 
                            demographic_data_file) )

        is_existing = in1d(hh_ids, hh_ds['household_id'])
        for attr in keep_attributes:
            dtype = hh_ds[attr].dtype
            values = fill_value * ones(n_hhs, dtype=dtype)
            values[is_existing] = hh_ds.get_attribute_by_id(attr,
                                                            hh_ids[is_existing])
            results[attr] = values

        storage = StorageFactory().get_storage('dict_storage')

        table_name = 'households'
        storage.write_table(table_name=table_name,
                            table_data=results)

        new_hh_ds = Dataset(in_storage=storage, 
                            in_table_name=table_name,
                            id_name=household_dataset.get_id_name(),
                            dataset_name=household_dataset.dataset_name)
        household_dataset = new_hh_ds
        if dataset_pool is not None:
            dataset_pool.replace_dataset(household_dataset.dataset_name,
                                         household_dataset)
        return household_dataset

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
            self.hh_ds = self.dataset_pool.get_dataset('household')
        else:
            storage = StorageFactory().get_storage('dict_storage')
            table_name = 'households'
            storage.write_table(table_name=table_name,
                                table_data=hh_data)

            self.hh_ds = Dataset(in_storage=storage, 
                                     in_table_name=table_name,
                                     dataset_name='household')

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
                   'age_of_head': "household.aggregate(person.age * (person.disaggregate(household.head_person_id)==person.person_id))"
                     }
        new_hh_ds = model.run(self.dmgh_data_file, self.hh_ds,
                  year=2000, 
                  keep_attributes=['building_id', 'keep'],
                  demographic_attributes=attrs_mapping,
                  dataset_pool=self.dataset_pool)

        assert allclose(new_hh_ds['household_id'], array([ 5, 1,  2,  3]))
        assert allclose(new_hh_ds['building_id'],  array([-1, 11, 22, 33]))
        assert allclose(new_hh_ds['keep'],         array([-1,4.1, 4.2, 4.3]))
        assert allclose(new_hh_ds['income'],       array([65, 61, 62, 63])*1000.0)
        assert allclose(new_hh_ds['size'],         array([ 2, 3,  3,  3]))
        assert allclose(new_hh_ds['age_of_head'],  array([67, 30, -1, 23]))

        new_hh_ds = model.run(self.dmgh_data_file, self.hh_ds,
                  year=2001, 
                  keep_attributes=['building_id', 'keep'],
                  demographic_attributes=attrs_mapping,
                 )

        assert allclose(new_hh_ds['household_id'], array([ 1]))
        assert allclose(new_hh_ds['building_id'],  array([11]))
        assert allclose(new_hh_ds['keep'],         array([4.1]))
        assert allclose(new_hh_ds['income'],       array([71])*1000.0)
        assert allclose(new_hh_ds['size'],         array([ 5]))
        assert allclose(new_hh_ds['age_of_head'],  array([31]))

        
if __name__ == '__main__':
    opus_unittest.main()
