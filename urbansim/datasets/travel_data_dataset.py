# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 
from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.logger import logger
from opus_core.misc import unique
from numpy import logical_and, logical_or, isscalar, where, ones
from numpy import setdiff1d, zeros_like 
        
class TravelDataDataset(UrbansimDataset):
    """Dataset containing O-D matrices"""

    id_name_default = []      # use _hidden_id
    origin_id_name = "from_zone_id"
    destination_id_name = "to_zone_id"
    in_table_name_default = "travel_data"
    out_table_name_default = "travel_data"
    dataset_name = "travel_data"
    
    def number_of_logsums(self):
        """Return the number of logsums in this travel data set"""
        n = 0
        # use self.get_primary_attribute_names() so that we count the logsums whether or not they have been loaded already
        for name in self.get_primary_attribute_names():
            if name.startswith("logsum"): 
                n=n+1
        return n

    def get_attribute_as_matrix(self, name, fill=0):
        """return attribute "name" of travel_data as a 2d array, index by (from_zone_id, to_zone_id)
        """
        
        name_attribute = self.get_attribute(name)
        rows = self.get_attribute(self.origin_id_name)
        cols = self.get_attribute(self.destination_id_name)
        
        results = fill * ones((rows.max()+1, cols.max()+1), dtype=name_attribute.dtype)
        results.put(indices=rows * results.shape[1] + cols, values = name_attribute)
        
        return results

    def set_values_of_one_attribute_with_od_pairs(self, attribute, values, O, D, fill=0):
        """set travel_data attribute with a 2d array (matrix) index by [O, D].
        o-d pairs appearing in travel_data ids, but not specified in O and D arguments, are filled with 'fill' (0)
        o-p pairs not appearing in travel_data ids, but specified in O and D arguments, are ignored
                
        This provides similar function as: 
        
        index = travel_data.get_index_by_origin_and_destination_ids(O, D)
        travel_data.set_values_of_one_attribute(attribute=attribute, values=values)
        
        but is more efficient when the O, D and values arrays are large in size.
        """
        assert O.shape == D.shape == values.shape
        
        oids = self.get_attribute(self.origin_id_name)
        dids = self.get_attribute(self.destination_id_name)
        nrows = max(O.max(), oids.max()) + 1
        ncols = max(D.max(), dids.max()) + 1
        matrix = fill * ones((nrows, ncols), dtype=values.dtype)
        matrix.put(indices=O * ncols + D, values = values)              
        
        if attribute not in self.get_attribute_names():
            self.add_primary_attribute(fill * ones(self.size(), dtype=values.dtype), attribute)
        
        results = matrix[oids, dids]
        self.set_values_of_one_attribute(attribute, results)
    
    def get_od_pair_index_not_in_dataset(self, O, D):
        """Return indices to O (D) from whose elements an od pair is not included in the travel data
        see unittest for an example
        """
        
        assert O.shape == D.shape
        
        origin_ids = self.get_attribute(self.origin_id_name)
        destination_ids = self.get_attribute(self.destination_id_name)
        
        max_id = max(O.max(), D.max(), origin_ids.max(), destination_ids.max())
        digits = len(str(max_id)) + 1
        multiplier = 10 ** digits

        ODpair = O * multiplier + D
        idpair = origin_ids * multiplier + destination_ids
        missing_pairs = setdiff1d( unique(ODpair), unique(idpair) )

        results = zeros_like(D)
        for pair in missing_pairs:
            results += logical_and( O == pair // multiplier, D == pair % multiplier)
        
        results += logical_or(O < origin_ids.min(), O > origin_ids.max())
        results += logical_or(D < destination_ids.min(), D > destination_ids.max())
        
        return where(results)
    
    def get_index_by_origin_and_destination_ids(self, origin_id, destination_id, return_value_if_not_found=-1, verbose=False):
        """return dataset index for given origin and destination pair(s)
        origin_id and destination_id can be either integers, lists, or arrays; of the same type and size
        """
        origin_ids = self.get_attribute(self.origin_id_name)
        destination_ids = self.get_attribute(self.destination_id_name)
        def match((o, d), rv=return_value_if_not_found, verbose=verbose):
            w = where(logical_and(origin_ids==o, destination_ids==d))[0]
            if w.size == 0:
                if verbose: logger.log_warning("O-D pair (%s, %s) has no entry in travel_data; returns %s." % (o, d, rv))
                w = rv
            elif w.size == 1:
                w = w[0]
            else:
                logger.log_error("O-D pair (%s, %s) has more than 1 entries in travel_data." % (o, d))
                raise ValueError, "O-D pair (%s, %s) has more than 1 entries in travel_data." % (o, d)
            return w

        if isscalar(origin_id) and isscalar(destination_id):
            return array([match((origin_id, destination_id))])
        else:
            if len(origin_id) != len(destination_id):
                logger.log_error("origin_id and destination_id can be either scalar integer, list, or array; of the same type and size.")
                raise TypeError, "origin_id and destination_id can be either scalar integer, list, or array; of the same type and size."

            return array(map(match, zip(origin_id, destination_id)))

from opus_core.tests import opus_unittest
from numpy import array, ma, allclose
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
    def setUp(self):
        # create a simple travel data set and check one attribute
        storage = StorageFactory().get_storage('dict_storage')

        travel_data_table_name = 'travel_data'        
        storage.write_table(
                table_name=travel_data_table_name,
                table_data={
                    "from_zone_id": array([1,       1,    1,     2,     2,     2,     5,     5]),
                    "to_zone_id":   array([1,       2,    5,     1,     2,     5,     1,     5]),
                    "logsum0":      array([-3.0, -6.0, -9.0, -12.0, -15.0, -18.0, -21.0, -24.0]),
                    "logsum1":      array([-4.0, -7.0, -10.0,-13.0, -16.0, -19.0, -22.0, -25.0]),
                    "logsum2":      array([-5.0, -8.0, -11.0,-14.0, -17.0, -20.0, -23.0, -26.0])          
                    }
            )

        self.travel_data = TravelDataDataset(in_storage=storage, in_table_name=travel_data_table_name)
        self.travel_data.load_dataset(attributes='*')
        
        
    def test_travel_data(self):
        
        self.assertNotEqual(self.travel_data.size(), 0, msg = "No data loaded - expected data to be loaded at this point.")
        
        k = len(self.travel_data.get_attribute_names())
        self.assertEqual(k, 6, msg = "Number of attributes should be 5 but is " + str(k) + ".")
        
        k = len(self.travel_data.get_primary_attribute_names())
        self.assertEqual(k, 5, msg = "Number of stored attributes should be 5 but is " + str(k) + ".")
        
        n = self.travel_data.number_of_logsums()
        self.assertEqual(n, 3, msg = "Number of logsums should be 3 but is " + str(k) + ".")
        
        results = self.travel_data.get_attribute('logsum0')
        
        should_be = array([-3.0, -6.0, -9.0, -12.0, -15.0, -18.0, -21.0, -24.0])
        
        self.assertEqual(ma.allclose(results, should_be, rtol=1e-7), True, 
                          msg = "query results should be %s but is %s." % (should_be, results))
 
    def test_get_attribute_as_matrix(self):
        result = self.travel_data.get_attribute_as_matrix('logsum0')
        should_be = array([[0,    0,    0,  0,  0,    0], 
                           [0, -3.0, -6.0,  0,  0, -9.0], 
                           [0,-12.0,-15.0,  0,  0,-18.0], 
                           [0,    0,    0,  0,  0,    0], 
                           [0,    0,    0,  0,  0,    0], 
                           [0,-21.0,    0,  0,  0,-24.0]])
        self.assertEqual(result.shape, should_be.shape, msg = "Shape of returned matrix should be %s but is %s" % ( str(should_be.shape), str(result.shape) ) )
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))

    def test_set_values_of_one_attribute_with_od_pairs(self):
        O = array([1,       1,    1,     2,     2,     2,     5,     5])
        D = array([1,       2,    5,     1,     2,     5,     1,     5])
        values=array([-5.0, -8.0, -11.0,-14.0, -17.0, -20.0, -23.0, -26.0])
        should_be = array([-5.0, -8.0, -11.0,-14.0, -17.0, -20.0, -23.0, -26.0])
        self.travel_data.set_values_of_one_attribute_with_od_pairs('attr_x', values, O, D)
        result = self.travel_data.get_attribute('attr_x')
        self.assertEqual(result.shape, should_be.shape, msg = "Shape of returned matrix should be %s but is %s" % ( str(should_be.shape), str(result.shape) ) )
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))
        
        ## o-d pairs appearing in id, but not specified in O and D arguments are filled with 'fill' (0)
        ## o-p pairs not appearing in id, but specified in O and D arguments are ignored
        O = array([1,       1,    1,            2,     2,     5,  5,     5,  6])
        D = array([1,       2,    5,            2,     5,     1,  2,     5,  0])
        values=array([-5.0, -8.0, -11.0,     -17.0, -20.0, -23.0,-99.0,-26.0,-999])
        should_be = array([-5.0, -8.0, -11.0,  0.0, -17.0, -20.0, -23.0, -26.0])
        self.travel_data.set_values_of_one_attribute_with_od_pairs('attr_x', values, O, D)
        result = self.travel_data.get_attribute('attr_x')
        self.assertEqual(result.shape, should_be.shape, msg = "Shape of returned matrix should be %s but is %s" % ( str(should_be.shape), str(result.shape) ) )
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))        
        
    def test_get_od_pair_index_not_in_dataset_1d(self):
        O = array([-1, 1, 1, 7, 5, 5, 5, 3,  2])
        D = array([ 5, 2, 3, 2, 5, 2, 1, 1, -1])
        #index    [ 0, 1, 2, 3, 4, 5, 6, 7,  8]
        result = self.travel_data.get_od_pair_index_not_in_dataset(O, D)
        should_be = array([0, 2, 3, 5, 7, 8])
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))                    

    def test_get_od_pair_index_not_in_dataset_2d(self):
        O = array([[-1, 1, 1,], [7, 5, 5,], [5, 3,  2]])
        D = array([[ 5, 2, 3,], [2, 5, 2,], [1, 1, -1]])
        #index    [  0, 0, 0,    1, 1, 1,    2, 2,  2]
        #index    [  0, 1, 2,    0, 1, 2,    0, 1,  2]
        result = self.travel_data.get_od_pair_index_not_in_dataset(O, D)
        should_be = (array([0, 0, 1, 1, 2, 2]), array([0, 2, 0, 2, 1, 2]))
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))                    

    def test_get_index_by_origin_and_destination_ids(self):
        result = self.travel_data.get_index_by_origin_and_destination_ids(2, 5)
        should_be = array([5])
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))                    
        
        O = array([-1, 1, 1, 7, 5, 5, 5, 3,  2])
        D = array([ 5, 2, 3, 2, 5, 2, 1, 1, -1])
        #index    [ 0, 1, 2, 3, 4, 5, 6, 7,  8]
        #          -1, 1,-1,-1, 7,-1, 6,-1, -1 
        result = self.travel_data.get_index_by_origin_and_destination_ids(O, D)
        should_be = array([-1, 1,-1,-1, 7,-1, 6, -1, -1])
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))                    

        O = [-1, 1, 1, 7, 5, 5, 5, 3,  2]
        D = [ 5, 2, 3, 2, 5, 2, 1, 1, -1]
        #index    [ 0, 1, 2, 3, 4, 5, 6, 7,  8]
        #          -1, 1,-1,-1, 7,-1, 6,-1, -1 
        result = self.travel_data.get_index_by_origin_and_destination_ids(O, D)
        self.assert_(allclose( result, should_be),  msg="returned results should be %s but is %s" % (should_be, result))

if __name__=="__main__":
    opus_unittest.main()
    

        