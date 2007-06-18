#
# Opus software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#

from sets import Set

from numpy import array, int32
from numpy import arange
from numpy import ma

from opus_core.datasets.abstract_dataset import AbstractDataset

from opus_core.misc import all_in_list
from opus_core.misc import get_distinct_list
from opus_core.variables.attribute_box import AttributeBox
from opus_core.resources import Resources
from opus_core.storage_factory import StorageFactory
from opus_core.dataset_pool import DatasetPool
from opus_core.variables.attribute_type import AttributeType
from opus_core.variables.variable_name import VariableName

class Dataset(AbstractDataset):
    """
    Dataset is defined as a set of individuals of the same dataset that are characterized by a set of attributes.
    One can imagine it as an n x m table where n is the number of individuals and m is the number of attributes.
    Different attributes can be of different type (of scalars). Each attribute has a name.
    A Dataset is characterized by:
        - list of attribute names that serve as a unique identifier of the individuals. Values of unique identifiers
            should be integers > 0.
        - n - number of individuals
        - list of attribute names
        - a storage object that points to media where the dataset is stored.
        - dataset name which determines the directory in which variables for this dataset are implemented.

    The class provides a method for accessing the data, called 'get_attribute(attribute_name)' which returns
    an array of values of the given attribute.
    The class offers a method 'load_dataset' which reads the data from storage. If this method is not used,
    the data are loaded as they are needed, i.e. when using 'get_attribute'. Note that a method 'load_dataset'
    implemented for the given storage object is required.

    Computed variables for the dataset are treated as attributes. They can be thought as additional columns in
    the n x m table. In order to differentiate them from fixed attributes, each attribute/variable (represented
    by the class AttributeBox) holds one of the metadata
    PRIMARY (fixed attribute), COMPUTED (computed variable).
    """

    def __init__(self, resources=None, in_storage=None, id_name=None, dataset_name=None,
            out_storage=None, in_table_name=None, out_table_name=None, debug=None):
        """The argument 'resources' is of type Resources and can contain all other arguments
        (as a pair of argument_name:value). If not None, argument values given directly to the constructor overwrite
        the corresponding values in resources (in a local copy, thus not seen outside).
        'in_storage' is a Storage object and the constructor uses it to determine what attributes
            are on storage (without loading them). These names are stored in '_primary_attribute_names'.
        'id_name' is a list of strings that determine a unique identifiers of the dataset.
            If 'id_name' is an empty list, there will be a hidden unique identifier created (its name is given
            in the class constant 'hidden_id_name'). In that case, in_storage is not allowed to be None,
            in order to determine the size of the dataset.
        'dataset_name' specifies the directory in which variables for this dataset are implemented.
            It also used as a directory for caching.
        'out_storage' is a Storage object that is used for dataset output.
        'in_table_name' is name of the table/file that contains the data for this dataset.
        'out_table_name' is name of the table/file for the dataset output.
        'debug' is either of type DebugPrinter or an integer value determining the level of debugging messages.

        id_name has to be given (but can be an empty list), all other arguments are optional.
        """

        if resources is None:
            resources = Resources()
        resources.merge_if_not_None({"in_storage":in_storage})

        AbstractDataset.__init__(self,
            resources = resources,
            id_name = id_name,
            dataset_name = dataset_name,
            out_storage = out_storage,
            in_table_name = in_table_name,
            out_table_name = out_table_name,
            debug = debug)

        storage = self.resources.get("in_storage", None)

        if storage == None:
            self._raise_error(StandardError,
                              "'in_storage' must be given to the constructor of this dataset.")

    def get_attribute(self, name):
        """ Return an array of the (by the argument name) given attribute.
        If it is not found, it is loaded from opus_core.store.storage (lazy loading principle)
        or from cache if the attribute was previously cached."""
        if not isinstance(name, VariableName):
            attr_name = VariableName(name)
        else:
            attr_name = name
        short_name = attr_name.get_alias()
        if short_name not in self.get_attribute_names():
            # Hack!  Check if the real short name is a primary attribute; if so, use that, so that we
            # can access that primary attribute.
            real_short_name = attr_name.get_short_name()
            if short_name!=real_short_name and real_short_name in self._primary_attribute_names:
                short_name = real_short_name
            if short_name in self._primary_attribute_names:
                if self._id_names == None:
                    self._raise_error(NameError,
                                      "Key 'id_name' is missing from resources of this dataset!")
                self.load_dataset(nchunks=1, attributes=[short_name])
            else:
                self._raise_error(NameError,
                                  "Cannot find attribute '%s'." % name)
        elif not self.attribute_boxes[short_name].is_in_memory():
            if self.attribute_boxes[short_name].is_cached():
                self.load_dataset(nchunks=1, attributes=[short_name], in_storage=self.attribute_cache,
                                  load_id_with_each_chunk=False)
            else:
                if short_name in self._primary_attribute_names:
                    self.load_dataset(nchunks=1, attributes=[short_name])
                else:
                    self._raise_error(NameError,
                                      "Cannot find attribute '%s'." % name)

        return self.attribute_boxes[short_name].get_data()

    def load_dataset(self, resources=None, nchunks=None, attributes=None, in_storage=None,
                     in_table_name=None, lowercase=None, load_id_with_each_chunk=None,
                     flush_after_each_chunk=None):
        """
        The argument 'resources' is of type Resources and can contain all other arguments
        (as a pair of argument_name:value).
        The argument values have higher priority than entries in resources.
        Thus, resources are overwritten by the given arguments (if not None).
        It is merged with self.resources and thus, entries that were given
        to the constructor do not need to be given here. It can also contain any other entries needed by
        the corresponding storage module, since it is passed to the load_dataset method of the storage module.
        The method loads data from a medium given by the entry 'in_storage'.
        The data are loaded in several chunks given by 'nchunks' (default is 1).
        Argument 'in_table_name' determines the storage place (e.g. subdirectory, MySQL table, file name).
        Argument 'attributes' can be a list of attributes to be loaded or an integer code of the attributes type
        (PRIMARY, COMPUTED), or '*'. If the entry is missing or is '*', all attributes found on the medium are loaded.
        'lowercase' specifies if attribute names are supposed to be converted to lower case (default is True).
        'load_id_with_each_chunk' specifies if the id-attributes should be loaded with each chunk (e.g. for sorting purposes),
        (default is True).

        Each loaded attribute array is stored as a dictionary entry of type AttributeBox in 'set'.
        If any of the attributes has been already contained in 'set', its values
        are overwritten. The class attribute 'n' is set to the number of values in one array (they
        should be all the same length). For a fast search, the class attribute 'id_mapping' is created which is
        a dictionary with entries whose keys are the unique identifiers of the data set and values are the indices
        of the corresponding array elements.

        Each chunk reads also values of the id_name attribute. These are sorted and all other attributes are
        stored in this order.

        Note that the corresponding storage module must have a method 'load_dataset'.
        """
        #set defaults
        nchunks_default = 1
        attributes_default = '*'
        lower_default = 1 # if 1, use lowercase for attribute names
        load_id_with_each_chunk_default = True
        flush_after_each_chunk_default = False

        # merge arguments with dictionaries and add missing entries
        local_resources = Resources(self.resources)
        if resources is not None:
            local_resources.merge_if_not_None(resources)
        local_resources.merge_if_not_None({"nchunks":nchunks,
                                           "attributes":attributes,
                                           "in_storage":in_storage,
                                           "in_table_name":in_table_name,
                                           "lowercase":lowercase,
                                           "load_id_with_each_chunk":load_id_with_each_chunk,
                                           "flush_after_each_chunk":flush_after_each_chunk})
        local_resources.merge_with_defaults({"nchunks":nchunks_default,
                                             "attributes":attributes_default,
                                             "lowercase":lower_default,
                                             "load_id_with_each_chunk":load_id_with_each_chunk_default,
                                             "flush_after_each_chunk":flush_after_each_chunk_default})

        # check obligatory entries
        local_resources.check_obligatory_keys(["in_storage", "in_table_name"])

        # prepare for loading
        in_storage = local_resources["in_storage"]

        if not self._is_hidden_id():
            local_resources.merge({"id_name":self._id_names})
            
        table_name = local_resources['in_table_name']
        column_names = local_resources['attributes']
        nchunks = local_resources['nchunks']
        # determine set of attributes for each chunk (a list of nchunks lists)
        chunked_attributes = in_storage.chunk_columns(table_name=table_name, 
                                                      column_names=column_names,
                                                      nchunks=nchunks)
        nchunks = len(chunked_attributes)

        if chunked_attributes:
            id_name_stored = 0
            if self._is_id_loaded():
                id_name_stored = 1
            for ichunk in range(nchunks): # iterate over chunks
                if local_resources["load_id_with_each_chunk"]:
                    if not all_in_list(self._id_names, chunked_attributes[ichunk]) and (not self._is_hidden_id()):
                        chunked_attributes[ichunk] = \
                              get_distinct_list(chunked_attributes[ichunk] + self._id_names)
                        
                data = in_storage.load_table(table_name = table_name, 
                                             column_names = chunked_attributes[ichunk], 
                                             id_name = self.get_non_hidden_id_name())
                
                for attr in data:
                    if self.attribute_boxes.has_key(attr):
                        if not (attr in self._id_names) or not self.attribute_boxes[attr].is_in_memory():
                            self.attribute_boxes[attr].set_data(data[attr])
                            self.attribute_boxes[attr].set_is_in_memory(True)
                    elif not ((attr in self._id_names) and self.attribute_boxes.has_key(attr)): #do not store id_name every time
                        self.attribute_boxes[attr] = AttributeBox(self,
                                                      data[attr],
                                                      variable_name=self.create_and_check_qualified_variable_name(attr),
                                                      type=AttributeType.PRIMARY,
                                                      header=None,
                                                      version=0)
                if local_resources["flush_after_each_chunk"]:
                    self.flush_dataset()
            if not id_name_stored:
                try:
                    self.n = len(self.get_attribute(self.get_attribute_names()[0]))
                except ValueError: #happens with a Rank-0 array
                    self.n = 1
                
                if not self._id_names:
                    self._create_hidden_id()
                    
                else:
                    for id in self._id_names:
                        # Convert all values to int32
                        self.attribute_boxes[id].set_data(values=self.attribute_boxes[id].get_data().astype(int32))
                        
                    self._create_id_mapping()

    def load_dataset_if_not_loaded(self, resources=None, nchunks=None, attributes=None,
                            in_storage=None, in_table_name=None, lowercase=None):
        """ Like load_dataset, but loads only attributes that are not already loaded.
        'attributes' is a list of attribute names. If it is not given, primary attributes
        are considered.
        """
        if attributes == None:
            attributes = self.get_primary_attribute_names()
        new_attributes = []
        new_attributes_from_cache = []
        for attr in attributes:
            if attr in self.get_attribute_names() and self.attribute_boxes[attr].is_cached() and not self.attribute_boxes[attr].is_in_memory():
                new_attributes_from_cache.append(attr)
            elif attr not in self.get_attribute_names() or (not self.attribute_boxes[attr].is_in_memory() and not self.attribute_boxes[attr].is_cached()):
                new_attributes.append(attr)
        if new_attributes:
            self.load_dataset(resources=resources, nchunks=nchunks, attributes=new_attributes,
                                in_storage=in_storage, in_table_name=in_table_name,
                                lowercase=lowercase)
        if new_attributes_from_cache:
            self.load_dataset(nchunks=nchunks, attributes=new_attributes_from_cache,
                               in_storage=self.attribute_cache,
                               load_id_with_each_chunk=False)

    def determine_stored_attribute_names(self, resources=None, in_storage=None,
                                              in_table_name=None, attribute_type=AttributeType.PRIMARY):
        """Return name of attributes that are found on storage. The storage module must have a method
        'determine_field_names'.
        """
        place_default = ""
        lower_default = 1
        # merge arguments with dictionaries and add missing entries
        local_resources = Resources(self.resources)
        if resources is not None:
            local_resources.merge_if_not_None(resources)
        local_resources.merge_if_not_None({"in_storage":in_storage, "in_table_name":in_table_name})
        local_resources.merge_with_defaults({"in_table_name":place_default, "lowercase":lower_default})
        local_resources['attributes'] = attribute_type

        # check obligatory entries
        local_resources.check_obligatory_keys(["in_storage"])
        return local_resources["in_storage"].determine_field_names(local_resources, attribute_type)

    def _do_flush_attribute(self, name):
        if not isinstance(name, VariableName):
            name = VariableName(name)

        short_name = name.get_alias()
        if short_name <> self.hidden_id_name:
            type = self._get_attribute_type(short_name)
            if type not in (AttributeType.LAG, AttributeType.EXOGENOUS):
                self.debug.print_debug("Flushing %s.%s" % (self.get_dataset_name(), short_name), 4)
                #logger.log_status("Flushing %s.%s" % (self.get_dataset_name(), short_name))
                self.write_dataset(attributes=[short_name], out_storage=self.attribute_cache)
                self.attribute_boxes[short_name].set_is_cached(True)
                self.unload_one_attribute(short_name)

    def write_dataset(self, resources = None, attributes=None, out_storage=None,
                       out_table_name=None, valuetypes=None):
        """Write dataset into the media given in out_storage (see also load_dataset).
        If 'attributes' is '*' all attributes that are known to the dataset (i.e. primary  + computed) are written.
        'attributes' can be also a list of attributes or AttributeType.PRIMARY or AttributeType.COMPUTED.
        """

        #set defaults
        place_default = ""
        attributes_default = '*'

        # merge arguments with dictionaries and add missing entries
        local_resources = Resources(self.resources)
        if resources is not None:
            local_resources.merge_if_not_None(resources)
        local_resources.merge_if_not_None({"attributes":attributes, "out_storage":out_storage,
                                        "out_table_name":out_table_name,
                                        "valuetypes":valuetypes})
        local_resources.merge_with_defaults({"out_table_name":place_default,
                                             "attributes":attributes_default})

        # check obligatory entries
        local_resources.check_obligatory_keys(["out_storage"])

        attributes = local_resources["attributes"]
        values = {}
        attrtypes = {}
        if attributes == '*':
            attr_names = self.get_known_attribute_names()
        if isinstance(attributes, list) or isinstance(attributes, tuple):
            attr_names = attributes
        elif attributes == AttributeType.COMPUTED:
            attr_names = self.get_computed_attribute_names()
        elif attributes == AttributeType.PRIMARY:
            attr_names = self.get_primary_attribute_names()

        for attr in attr_names:
            values[attr] = ma.filled(self.get_attribute(attr),0.0)
            attrtypes[attr] = self._get_attribute_type(attr)
        local_resources.merge({"values":values,
                        "attrtype":attrtypes,
                        "id_name":self._id_names,
                        "in_table_name": self._get_in_table_name_for_cache()
                        })
        
        table_name = local_resources["in_table_name"]
        table_data = local_resources["values"]
        local_resources["out_storage"].write_table(
            table_name=table_name,
            table_data=table_data,
            )

class DatasetSubset(Dataset):
    """Class for viewing a subset of a Dataset object, identified by a list of indices."""
    def __init__(self, parent, index):
        self.parent = parent
        if index == None:
            index = arange(self.parent.size())
        self.n = len(index)
        self.index = index
        self.resources = parent.resources
        self._primary_attribute_names = self.parent._primary_attribute_names
        self.debug = self.parent.debug
        self.id_mapping = self.parent.id_mapping
        self.id_mapping_type = self.parent.id_mapping_type
        self.id_mapping_shift = self.parent.id_mapping_shift
        self._id_names = self.parent._id_names
        self.dataset_name = self.parent.dataset_name
        self.attribute_boxes = self.parent.attribute_boxes

    def get_attribute(self, name):
        """ Return an array of the (by the argument name) given attribute."""
        return self.parent.get_attribute(name)[self.index]

    def get_index(self):
        """Return the indices of the parent's rows that are in this subset."""
        return self.index

from opus_core.tests import opus_unittest

class DatasetTests(opus_unittest.OpusTestCase):
    def test_dataset_table_does_not_exist(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            'tests',
            {
                'id':array([1,2,3]),
            }
        )

        self.assertRaises(Exception,
                          Dataset,
                          in_storage = storage,
                          in_table_name = 'idonotexist',
                          id_name = 'bogo',
                          dataset_name = 'bogo',
                          )

    def test_get_primary_attribute_names(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            'tests',
            {
                'id':array([1,2,3]),
                'attr':array([100,200,300]),
                'attr2':array([11,22,33]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='tests', id_name='id')

        # Should only have attributes that exist in the storage.
        self.assertEqual(Set(ds.get_primary_attribute_names()),
                         Set(['id','attr','attr2']))

        # Should only have attributes that exist in the storage.
        dataset_pool = DatasetPool(package_order=['opus_core'],
                                   storage=storage)
        ds = dataset_pool.get_dataset('test')
        ds.compute_variables(['opus_core.test.attr2_times_2'],
                             dataset_pool = dataset_pool)
        self.assertEqual(Set(ds.get_known_attribute_names()),
                         Set(['id','attr','attr2','attr2_times_2']))

    def test_get_attribute_names(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset',
            table_data = {
                'id':array([1,2,3]),
                'attr':array([100,200,300]),
                'attr2':array([11,22,33]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')

        # Should be empty at first.
        self.assertEqual(ds.get_attribute_names(),
                         [])

        # Should have the attributes requested after load_dataset.
        ds.load_dataset(attributes=['id'])
        self.assertEqual(Set(ds.get_attribute_names()),
                         Set(['id']))

        # Always loads the id attributes.
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')
        ds.load_dataset(attributes=['attr'])
        self.assertEqual(Set(ds.get_attribute_names()),
                         Set(['id','attr']))

        # '*' should load all attributes.
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')
        ds.load_dataset(attributes='*')
        self.assertEqual(Set(ds.get_attribute_names()),
                         Set(['id','attr','attr2']))

        # Default is to load all attributes.
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')
        ds.load_dataset()
        self.assertEqual(Set(ds.get_attribute_names()),
                         Set(['id','attr','attr2']))

    def test_subset(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset',
            table_data = {
                'id':array([1,2,3]),
                'attr':array([100,200,300]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')

        # Check subset that contains entire parent dataset.
        subset = DatasetSubset(ds, index=None)
        self.assert_(ma.allequal(subset.get_attribute('attr'),
                              ds.get_attribute('attr')))

        # Check subset that is an actual subset.
        subset = DatasetSubset(ds, index=array([0,2]))
        self.assert_(ma.allequal(subset.get_attribute('attr'),
                              array([100,300])))
        self.assert_(ma.allequal(subset.get_index(),
                              array([0,2])))


    def test_exceptions(self):
        raised_exception = False
        try:
            Dataset()
        except StandardError, e:
            raised_exception = True
            self.assert_("Must specify 'id_name'" in e.args[0])
        self.assert_(raised_exception)

    def test_empty_dataset_like_me(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset',
            table_data = {
                'id':array([1]),
                'attr':array([100]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')

        ds2 = ds.empty_dataset_like_me(resources=Resources({'my_key':'my_value'}))
        self.assert_(ma.allequal(ds2.get_id_attribute(), ds.get_id_attribute()))
        self.assert_(ma.allequal(ds2.get_attribute('attr'), ds.get_attribute('attr')))
        self.assert_('my_key' not in ds.resources.keys())
        self.assertEqual(ds2.resources['my_key'], 'my_value')
        ds.set_values_of_one_attribute('id', array([11]))
        self.assert_(not ma.allequal(ds2.get_id_attribute(), ds.get_id_attribute()))
        self.assert_(ma.allequal(ds2.get_attribute('attr'), ds.get_attribute('attr')))

    def test_join(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset1',
            table_data = {
                'id1':array([1,2,3,4,5]),
                'attr1':array([100, 36, 76, 21, 10]),
                'attr2':array([1, 2, 6, 7, 100]),
                'attr3':array(["ab", "cd", "XXX", "efg", "ZZZ"]),
                }
            )

        storage.write_table(table_name='dataset2',
            table_data = {
                'id2':array([1,2,3,4,5,6,7,8,10]),
                'id1':array([2,3,2,5,1,1,5,5,6]),
                'myattr':array([60, 45, 100, 21, 100, 30, 70,42, 0]),
                }
            )

        ds1 = Dataset(in_storage=storage, in_table_name='dataset1', id_name='id1')
        ds2 = Dataset(in_storage=storage, in_table_name='dataset2', id_name='id2')

        ds2.join(ds1,['attr1', 'attr2', 'attr3'])

        self.assertEqual(len(ds2.get_known_attribute_names()), 6, msg="Error in join")
        self.assertEqual(ma.allclose(ds2.get_attribute('attr2'), array([2,6,2,100,1,1,100,100, -1])), True, msg="Error in join")
        self.assertEqual("cd", ds2.get_attribute('attr3')[0], msg="Error in join")
        self.assertEqual('', ds2.get_attribute('attr3')[8], msg="Error in join")

    def test_join_by_rows(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset1',
            table_data = {
                'id1':array([1,2,3,4,5]),
                'attr1':array([100, 36, 76, 21, 10]),
                'attr2':array([1, 2, 6, 7, 100]),
                'attr3':array(["ab", "cd", "XXX", "efg", "ZZZ"]),
                }
            )

        storage.write_table(table_name='dataset2',
            table_data = {
                'id1':array([6,8,2,20]),
                'attr1':array([40,200,407,100]),
                'attr3':array(["rrr", "t","YYYY", ""]),
                }
            )


        ds1 = Dataset(in_storage=storage, in_table_name='dataset1', id_name='id1')
        ds2 = Dataset(in_storage=storage, in_table_name='dataset2', id_name='id1')

        ds1.join_by_rows(ds2, require_all_attributes=False, change_ids_if_not_unique=True)

        self.assertEqual(ds1.size(), 9, msg="Error in join_by_rows")
        self.assertEqual(ds1.get_attribute("attr1").sum(), 990, msg="Error in join_by_rows")
        self.assertEqual(ds1.get_id_attribute().max(), 9, msg="Error in join_by_rows")
        self.assertEqual(ds1.get_attribute("attr3")[7], "YYYY", msg="Error in join_by_rows")


    def test_has_attribute(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset',
            table_data = {
                'id1':array([6,8,2,20]),
                'attr1':array([40,200,407,100]),
                'attr3':array(["rrr", "t","YYYY", ""]),
                }
            )
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id1')

        self.assertEqual(True, ds.has_attribute('attr1'))
        self.assertEqual(False, ds.has_attribute('does_not_have_this_one'))

    def test_correlation(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='dataset',
            table_data = {
                'id':array([1,2,3,4,5]),
                'attr1':array([100, 36, 76, 21, 10]),
                'attr2':array([1, 2, 6, 7, 100]),
                'attr3':array([25, 54, 105, 120, 1000]),
                      })
        ds = Dataset(in_storage=storage, in_table_name='dataset', id_name='id')
        corrmat = ds.correlation_matrix(["attr1", "attr2", "attr3"])
        self.assertEqual(ma.allclose(corrmat.diagonal(), 1), True, msg="Error in correlation matrix")
        self.assertEqual(ma.allclose(corrmat[0,1], ds.correlation_coefficient("attr1", "attr2")), True,
                         msg="Error in correlation matrix or/and correlation coefficient")
        self.assertEqual(corrmat[0,1] < 0, True,  msg="Error in correlation matrix")
        self.assertEqual(corrmat[0,1] > -1, True,  msg="Error in correlation matrix")
        self.assertEqual(ma.allclose(corrmat[2,1], ds.correlation_coefficient("attr2", "attr3")), True,
                         msg="Error in correlation matrix or/and correlation coefficient")
        self.assertEqual(corrmat[2,1] > 0, True,  msg="Error in correlation matrix")
        self.assertEqual(corrmat[2,1] < 1, True,  msg="Error in correlation matrix")
        

if __name__ == '__main__':
    opus_unittest.main()