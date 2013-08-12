# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

import copy
import inspect
import numpy as np
from numpy import isscalar, NaN, ndarray, resize, any, where, nan
from opus_core.datasets.dataset import Dataset
from opus_core.datasets.abstract_dataset import DataElement
from opus_core.variables.attribute_box import AttributeBox
from opus_core.variables.variable_name import VariableName
from opus_core.resources import Resources
from opus_core.store.attribute_cache import AttributeCache
from opus_core.variables.attribute_type import AttributeType
from opus_core.variables.variable_factory import VariableFactory
from opus_core.misc import is_masked_array
from opus_core.logger import logger

import pandas as pd
 

class PandasClassFactory:
    """Creates PandasDataset from an Opus Dataset on the fly.
        It uses type() to preserve the whole inheritance chain of the Dataset.  
    """
    def get_dataset(self, dataset, index=None):
        new_dataset = type('PandasChildDataset', (PandasDataset,) + inspect.getmro(dataset.__class__), dict(dataset.__dict__))(create_from_data=False)
        #new_dataset = dataset.empty_dataset_like_me()        
        data = {}
        for attr in dataset.get_known_attribute_names():
            data[attr] = dataset[attr]
            if isscalar(dataset[attr]):
                data[attr] = array([data[attr]])
        new_dataset.df = pd.DataFrame(data)
        new_dataset.df.set_index(dataset.get_id_name(), inplace=True)
        if index is not None:
            new_dataset.df = new_dataset.df.iloc[index]
        new_dataset.n = new_dataset.df.shape[0]
        
        for attr in dataset.attribute_boxes.keys():
            new_dataset.attribute_boxes[attr] = AttributeBox(
                 new_dataset, [],
                 variable_name=dataset.attribute_boxes[attr].get_variable_name(),
                 version=dataset.attribute_boxes[attr].get_version(),
                 is_cached=dataset.attribute_boxes[attr].is_cached(),
                 is_in_memory=True,
                 variable_instance=dataset.attribute_boxes[attr].get_variable_instance())      
        return new_dataset
         
class PandasDataset(Dataset):
    """
    This is under construction.
    It is an attempt to have an analogous to an Opus Dataset that would use 
    Pandas DataFrame. The actual data is stored in an attribute called df 
    which is a DataFrame and is indexed by the dataset's unique identifier. 
    The dataset can be created from the same inputs as Opus dataset.
    Alternatively, it can be created from an existing Opus dataset using 
    the constructor PandasClassFactory.
    """
    def __init__(self, create_from_data=True, **kwargs):
        if create_from_data:
            self.create_from_data(**kwargs)

    
    def create_from_data(self, resources=None, id_name=None, in_storage=None, dataset_name=None,
            out_storage=None, in_table_name=None, out_table_name=None):
        self.resources = Resources(resources)
        self.resources.merge_if_not_None({ "id_name":id_name,
                            "dataset_name":dataset_name,
                            "in_storage":in_storage,
                            "out_storage":out_storage,
                            "in_table_name":in_table_name,
                            "out_table_name":out_table_name})
        self.resources.merge_with_defaults({"dataset_name":"dataset"})
        self.dataset_name = self.resources.get("dataset_name", None)
        self.attribute_cache = AttributeCache()
        self._aliases = {}
        self._id_names = self.resources.get("id_name", [])
        if not isinstance(self._id_names, list):
            self._id_names = [self._id_names]
        self.variable_factory = VariableFactory()
        self.debug = self.resources.get("debug",  0)
        self.df = pd.DataFrame(self.resources.get('in_storage').load_table(self.resources.get('in_table_name')))
        self._primary_attribute_names = self.get_attribute_names()
        self.df.set_index(self._id_names, inplace=True)
        self.attribute_boxes = {}
        for attr in self._primary_attribute_names:
            self.attribute_boxes[attr] = AttributeBox(self, [],
                                                variable_name=self.create_and_check_qualified_variable_name(attr),
                                                type=AttributeType.PRIMARY,
                                                is_in_memory=True,
                                                header=None,
                                                version=0)
        self.n = self.df.shape[0]
            
    def __getitem__(self, attr):
        """ dataset[attr]
        """
        return self.get_attribute(attr)

    def __setitem__(self, attr, values):
        """ dataset[attr] = values
        """
        self.df[attr] = values

    def get_attribute(self, name):
        if isinstance(name, VariableName):
            name = name.get_alias()
        else:
            name = VariableName(name).get_alias()
        if name in self.get_id_name():
            return self.get_id_attribute()
        return self.df[name].values
    
    def get_id_attribute(self):
        return self.df.index.values
    
    def get_attribute_by_id(self, name, id):
        return self.df[name][id]
    
    def get_attribute_names(self):
        return self.df.columns
    
    def _do_flush_attribute(self, name):
        """For now don't do anything."""
        pass
        
    def load_dataset(self, resources=None, attributes=None, in_storage=None,
                     in_table_name=None, lowercase=None, **kwargs):

        #set defaults
        attributes_default = '*'
        lower_default = 1 # if 1, use lowercase for attribute names

        # merge arguments with dictionaries and add missing entries
        local_resources = Resources(self.resources)
        if resources is not None:
            local_resources.merge_if_not_None(resources)
        local_resources.merge_if_not_None({"attributes":attributes,
                                           "in_storage":in_storage,
                                           "in_table_name":in_table_name,
                                           "lowercase":lowercase})
        local_resources.merge_with_defaults({"attributes":attributes_default,
                                             "lowercase":lower_default,
                                            })

        # check obligatory entries
        local_resources.check_obligatory_keys(["in_storage", "in_table_name"])

        # prepare for loading
        in_storage = local_resources["in_storage"]

        if not self._is_hidden_id():
            local_resources.merge({"id_name":self._id_names})
            
        table_name = local_resources['in_table_name']
        column_names = local_resources['attributes']
        chunked_attributes = self.chunk_columns(storage=in_storage,
                                                   table_name=table_name, 
                                                   column_names=column_names,
                                                   nchunks=1)
        # flatten list
        column_names = [name for name in chunked_attributes[0]
                                if name in in_storage.get_column_names(table_name)]
        data = in_storage.load_table(table_name = table_name, 
                                             column_names = column_names)
        self.df = pd.DataFrame(data)
        self.df.set_index(self._id_names, inplace=True)
        data_computed = {}
        if table_name+".computed" in in_storage.get_table_names():
            column_names_computed = [name for name in column_names
                                if name in in_storage.get_column_names(table_name+".computed")]
            data_computed = in_storage.load_table(table_name = table_name+".computed", 
                                                 column_names = column_names_computed)
            dfcomp = pd.DataFrame(data_computed)
            dfcomp.set_index(self._id_names, inplace=True)
            self.df = concat(self.df, dfcomp)
                      
        for attr in data:
            if not ((attr in self._id_names) and self.attribute_boxes.has_key(attr)): #do not store id_name every time
                self.attribute_boxes[attr] = AttributeBox(self, [],
                                                variable_name=self.create_and_check_qualified_variable_name(attr),
                                                type=AttributeType.PRIMARY,
                                                is_in_memory=True,
                                                header=None,
                                                version=0)

        for attr in data_computed:
            if not ((attr in self._id_names) and self.attribute_boxes.has_key(attr)): #do not store id_name every time
                self.attribute_boxes[attr] = AttributeBox(self, [],
                                                variable_name=self.create_and_check_qualified_variable_name(attr),
                                                type=AttributeType.COMPUTED,
                                                is_in_memory=True,
                                                header=None,
                                                version=0)
                                                                        
        self.n = self.df.shape[0]

    def add_attribute(self, data, name, metadata=2):
        """Add values given in argument 'data' to dataset as an attribute 'name' as type 'metadata'. If this
        attribute already exists, its values are overwritten. 
        'metadata' should be of type AttributeType (PRIMARY=1, COMPUTED=2).
        The method increments and returns the version number of the attribute.
        """
        if not (isinstance(data, ndarray) or is_masked_array(data)):
            data=array(data)
        name = self.create_and_check_qualified_variable_name(name)
        short_name = name.get_alias()
        if short_name in self.get_attribute_names():
            self.attribute_boxes[short_name].set_is_in_memory(True)
            self.attribute_boxes[short_name].set_type(metadata)
        else:
            self.attribute_boxes[short_name] = AttributeBox(self, data=[], variable_name=name,
                                                type=metadata)
        if metadata == AttributeType.PRIMARY:
            self._add_to_primary_attribute_names(short_name)
        self.df[short_name] = data
        self.__increment_version(short_name)
        return self.get_version(short_name)
    
    def attribute_sum(self, name):
        """Return the sum of values of the attribute 'name'.
        """
        return self.df[name].sum()

    def attribute_average(self, name):
        """Return the value of the given attribute averaged over the dataset.
        """
        return self.df[name].mean()

    def summary(self, index=None):
        if index is not None:
            self.df[index].describe()
        else:
            self.df.describe()

    def size(self):
        """Return size of the dataset."""
        return self.df.shape[0]
    
    def get_data_element_by_id(self, id, all_attributes=False):
        """Return an object of class DataElement of the given identifier id. See get_data_element."""
        return self.get_data_element(id, all_attributes)
    
    def get_data_element(self, id, **kwargs):
        """Return an object of class DataElement of the given index. 
        """
        object = DataElement()
        for col in self.get_attribute_names():
            setattr(object, col, self.df[col][id])
        return object
    
    def subset_by_ids(self, ids, **kwargs):
        """Shrink the dataset to values given by 'index'. The removed data are then lost.
        """
        self.df = self.df.loc[ids]
        self.n = self.df.shape[0]

    def aggregate_dataset_over_ids(self, dataset, function='sum', attribute_name=None, constant=None):
        """Aggregate attribute (given by 'attribute_name') of the given 'dataset' over
        self by applying the given function. The dataset is expected to have an attribute of the same
        name as the unique identifier of self. If attribute_name is not given, the
        argument 'constant' must be given, which is either a scalar or a numpy array. if it
        is a scalar, for each individual to be counted the constant value is taken into the function;
        if it is a numpy array of the same size as dataset, the value in the same index as
        individual is counted into the function.
        """
        workdf = dataset.df
        if attribute_name == None:
            if constant == None:
                self._raise_error(StandardError,
                                  "Either 'attribute_name' or 'constant' must be given.")
            elif isinstance(constant, ndarray):
                if constant.size <> dataset_id_values.size:
                    self._raise_error(StandardError,
                                      "constant's size (%d) must be of the same as dataset's size (%d)"
                                      % (constant.size, dataset_id_values.size))
                values = constant
            else:
                values = resize(array([constant]), dataset.size())
            attribute_name = '__constant__'
            workdf[attribute_name] = values 
        else: 
            if is_masked_array(dataset[attribute_name]):
                w = where(ma.getmask(dataset[attribute_name]))
                if len(w)>0:
                    where_masked = w[0]
                    # do not consider those elements in the computation
                    workdf[attribute_name] = ma.filled(workdf[attribute_name], NaN)
        #logger.start_block('Aggregate Pandas')
        grouped = workdf.groupby(self.get_id_name())[attribute_name]
        f = getattr(np, function)
        res = grouped.aggregate(f)
        #logger.end_block()
        return res

    def get_join_data(self, dataset, name, join_attribute=None, return_value_if_not_found=None, **kwargs):
        """Does a join on a attribute of two datasets (self and 'dataset').
        'join_attribute' specifies the join attribute of self. If this is None it is
        assumed to be identical to dataset._id_names which is the join attribute of 'dataset'.
        The method returns values of the attribute 'name' (which is an attribute of 'dataset')
        for the joined ids, i.e. the resulting array should have the same size as self.
        """
        default_return_values_by_type = default_filled_values_by_type = {'S':'',
                                                                         'U':'',
                                                                         'b':False,
                                                                         'i':-1,
                                                                         'u':0,
                                                                         'f':-1.0}
        id_name = dataset.get_id_name()
        jattr = join_attribute
        if jattr == None:
            jattr = id_name
        if not isinstance(jattr, list):
            jattr = [jattr]
        if not isinstance(name, list):
            name = [name]
        #logger.start_block('Disaggregate Pandas')
        result = self.df[jattr].join(dataset.df[name], on=jattr)[name]
        #result = dataset.df[name].loc[self.df[jattr[0]]]
        #logger.end_block()
        for attr in result.columns:
            if result[attr].dtype == object:
                result[attr] = result[attr].astype(dataset.df[attr].dtype)
            if np.isnan(result[attr].values).any():
                k = dataset.df[attr].values.dtype.kind
                if return_value_if_not_found is None and default_return_values_by_type.has_key(k):
                    val = default_return_values_by_type[k]
                else:
                    val = return_value_if_not_found
                result[attr].iloc[where(np.isnan(result[attr].values))] = val                
        return result
    
    def __set_version(self, name, version):
        self.attribute_boxes[name].set_version(version)

    def __increment_version(self, name):
        if self.get_version(name) == None:
            self.__set_version(name, 0)
        else:
            self.__set_version(name, self.get_version(name)+1)

from opus_core.tests import opus_unittest
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import array, all, ma, arange

class PandaDatasetTests(opus_unittest.OpusTestCase):
    def test_create(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            'tests',
            {
                'id':array([1,2,3]),
                'attr':array([100,200,300]),
                'attr2':array([11,22,33]),
                }
            )
        # create from Opus Dataset
        ds = Dataset(in_storage=storage, in_table_name='tests', id_name='id')
        pds = PandasClassFactory().get_dataset(ds)
        self.assert_(all(pds['attr'] == array([100,200,300])))
        self.assert_(all(pds.get_id_attribute() == array([1,2,3])))
        
        # create from data
        pds = PandasDataset(in_storage=storage, in_table_name='tests', id_name='id')
        pds.load_dataset()
        self.assert_(all(pds['attr2'] == array([11,22,33])))
        self.assert_(all(pds.get_id_attribute() == array([1,2,3])))
        
        # data element
        el = pds.get_data_element(2)
        self.assert_(el.attr == 200)
        self.assert_(el.attr2 == 22)
        
        #subset
        pds.subset_by_ids(array([1,3]))
        self.assert_(all(pds['attr'] == array([100,300])))
        self.assert_(all(pds['attr2'] == array([11,33])))
       
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
        zone_dataset = PandasDataset(in_storage=storage, in_table_name='zones', id_name="zone_id", dataset_name='zone')
        gridcell_dataset = PandasDataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name='gridcell')
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('gridcell', gridcell_dataset)
        dataset_pool._add_dataset('zone', zone_dataset)
        values = zone_dataset.compute_variables(['zone.aggregate(gridcell.my_variable)'], dataset_pool=dataset_pool)
        should_be = array([4.5, 9]) 
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate")
         
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
        ds0 = PandasDataset(in_storage=storage, in_table_name='zones', id_name="id0", dataset_name="myzone")
        ds1 = PandasDataset(in_storage=storage, in_table_name='fazes', id_name="id1", dataset_name="myfaz")             
        ds2 = PandasDataset(in_storage=storage, in_table_name='fazdistrs', id_name="id2", dataset_name="myfazdistr")
        ds3 = PandasDataset(in_storage=storage, in_table_name='neighborhoods', id_name="id3", dataset_name="myneighborhood")          
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
        ds = PandasDataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = PandasDataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        values = ds2.compute_variables(['myfaz.aggregate(10.0*myzone.my_variable, function=mean)'], dataset_pool=dataset_pool)
        should_be = array([70, 45])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in aggregate_mean") 
        
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
        ds = PandasDataset(in_storage=storage, in_table_name='zones', id_name="id", dataset_name="myzone")
        ds2 = PandasDataset(in_storage=storage, in_table_name='faz', id_name="id2", dataset_name="myfaz")
        dataset_pool = DatasetPool()
        dataset_pool._add_dataset('myzone', ds)
        dataset_pool._add_dataset('myfaz', ds2)
        values = ds.compute_variables(["myzone.disaggregate(10.0*myfaz.my_variable)"], dataset_pool=dataset_pool)
        should_be = array([40, 80, 40, 80])
        self.assert_(ma.allclose(values, should_be, rtol=1e-6), "Error in disaggregate")
        
if __name__ == '__main__':
    opus_unittest.main() 