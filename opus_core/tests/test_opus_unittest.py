# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.tests import opus_unittest

from opus_core.singleton import Singleton

from numpy import array


class TestSingleton(opus_unittest.OpusTestCase):
    """This test needs to be in a separate class, since TestOpusTestCase
    defines an additional singleton class.
    """
    def test_no_singletons_before_unit_test(self):
        """Also tests Singleton.has_singleton_for_class()."""
        # The only singleton should be Singleton itself.
        self.assertEqual(len(Singleton()._singletons), 1)
        self.assert_(Singleton().has_singleton_for_class(Singleton))
    
class TestOpusTestCase(opus_unittest.OpusTestCase):
    class TestSingleton(Singleton):
        value = 11
        
    def setUp(self):
        self.assertEqual(self.TestSingleton().value, 11,
                         msg='TestSingleton should have just been created.')
        self.TestSingleton().value = 22
    
    def tearDown(self):
        self.assertEqual(self.TestSingleton().value, 22,
                         msg='Singletons should not be removed until after '
                             'the test case tearDown is run.')
    
    def test_get_difference(self):
        values = {
            'dictionary':{1:1},
            'integer':1,
            'numpy_array':array([1,2,3]),
            'array':array(['alpha', 'beta']),
            'long':10L,
            'float':3.1415926,
            'boolean':False,
            }
            
        different_values = {
            'dictionary':{1:2},
            'integer':111,
            'numpy_array':array([111,222,333]),
            'array':array(['ALPHA', 'BETA']),
            'long':101010L,
            'float':2.18,
            'boolean':True,
            }
        
        for type1, value1 in values.iteritems():
            self.assert_(self._get_difference(
                first = {'arg':value1},
                second = {'arg':value1},
                ) is None)
                        
            for type2, value2 in different_values.iteritems():
                self.assert_(self._get_difference(
                    first = {'arg':value1},
                    second = {'arg':value2},
                    ) is not None)
        
        self.assert_(self._get_difference(
            first = {
                'dictionary':{1:1},
                'arg2':{
                    'dictionary':{1:1},
                    'integer':1,
                    'numpy_array':array([1,2,3]),
                    'array':array(['alpha', 'beta']),
                    'long':10L,
                    'float':3.1415926,
                    'boolean':False,
                    },
                },
            second = {
                'dictionary':{1:1},
                'arg2':{
                    'dictionary':{1:1},
                    'integer':1,
                    'numpy_array':array([1,2,3]),
                    'array':array(['alpha', 'beta']),
                    'long':10L,
                    'float':3.1415926,
                    'boolean':False,
                    },
                },
            ) is None)
        
        self.assert_(self._get_difference(
            first = {
                'dictionary':{1:1},
                'arg2':{
                    'dictionary':{1:1},
                    },
                },
            second = {
                'dictionary':{1:1},
                'arg2':{
                    'dictionary':{1:10000000},
                    },
                },
            ) is not None)
            
        self.assert_(self._get_difference(
            first = {
                'dictionary':{1:1},
                'arg2':{
                    'dictionary':{1:1},
                    'boolean':False,
                    },
                },
            second = {
                'dictionary':{1:1},
                'arg2':{
                    'boolean':False,
                    },
                },
            ) is not None)
            
    def test_assert_dicts_equal(self):
        try:
            self.assertDictsEqual(1, {})
        except AssertionError:
            pass
        else:
            self.fail('First argument to assertDictsEqual should be a '
                'dictionary, but assertDictsEqual did not fail when this was '
                'not the case.')
                
        try:
            self.assertDictsEqual({}, 1)
        except AssertionError:
            pass
        else:
            self.fail('Second argument to assertDictsEqual should be a '
                'dictionary, but assertDictsEqual did not fail when this was '
                'not the case.')
                
        self.assertDictsEqual({1:1}, {1:1})
        
        try:
            self.assertDictsEqual({1:1}, {2:2})
        except AssertionError:
            pass
        else:
            self.fail('assertDictsEqual should have failed when the two '
                'arguments differ, but did not.')
                
        
        self.assertDictsEqual({1:array([], dtype='int32')}, {1:array([], dtype='int32')})
        
    def test_assert_dicts_not_equal(self):
        try:
            self.assertDictsNotEqual(1, {})
        except AssertionError:
            pass
        else:
            self.fail('First argument to assertDictsNotEqual should be a '
                'dictionary, but assertDictsEqual did not fail when this was '
                'not the case.')
                
        try:
            self.assertDictsNotEqual({}, 1)
        except AssertionError:
            pass
        else:
            self.fail('Second argument to assertDictsNotEqual should be a '
                'dictionary, but assertDictsEqual did not fail when this was '
                'not the case.')
        
        try:
            self.assertDictsNotEqual({1:1}, {1:1})
        except AssertionError:
            pass
        else:
            self.fail('assertDictsEqual should have failed when the two '
                'arguments were the same, but did not.')
             
        self.assertDictsNotEqual({1:1}, {2:2})
        
        self.assertDictsNotEqual({1:array([], dtype='int32')}, {1:array([], dtype='int8')})


if __name__ == '__main__':
    opus_unittest.main()