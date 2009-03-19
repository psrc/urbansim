# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

# Import all from unittest so that opus_unittest acts just like unittest,
# except for the differences below.
from unittest import *   # Do not delete this line.

from numpy import ndarray

from opus_core.singleton import Singleton


OriginalTestCase = TestCase

class OpusAbstractTestCase(OriginalTestCase):
    """Extends TestCase to remove all singletons before and after each test."""
    
    def __new__(cls, *args, **kwargs):
        """
        Set up to automatically clear out singletons before and after running
        each test.
        """
        an_instance = OriginalTestCase.__new__(cls, *args, **kwargs)

        setup_method = an_instance.setUp
        def wrapped_setup_method(*req_args, **opt_args):
            Singleton().remove_all_singletons()
            return setup_method(*req_args, **opt_args)
        an_instance.setUp = wrapped_setup_method
        
        teardown_method = an_instance.tearDown
        def wrapped_teardown_method(*req_args, **opt_args):
            result = teardown_method(*req_args, **opt_args)
            Singleton().remove_all_singletons()
            return result
        an_instance.tearDown = wrapped_teardown_method
        
        return an_instance
        
    def assertDictsEqual(self, first, second, *args, **kwargs):
        """
        Assert that these two dictionaries have the same structure and contents.
        """
        self.assert_(isinstance(first, dict), *args, **kwargs)
        self.assert_(isinstance(second, dict), *args, **kwargs)
        
        difference_message = self._get_difference(first, second)
        if difference_message is not None:
            self.fail(difference_message)
        
    def assertDictsNotEqual(self, first, second, *args, **kwargs):
        """
        Assert that these two dictionaries do NOT have the same structure and contents.
        """
        self.assert_(isinstance(first, dict), *args, **kwargs)
        self.assert_(isinstance(second, dict), *args, **kwargs)
            
        difference_message = self._get_difference(first, second)
        if difference_message is None:
            self.fail('Dictionaries should not be equal, but are: %s.' % first)
        
    def _get_difference(self, first, second):
        """
        Are the type, structure, and contents of first and second the same?
        """
        if type(first) is not type(second):
            return "Types are different: %s != %s for \n%s\n    and\n%s" % (
                type(first), 
                type(second),
                first,
                second)
        
        if isinstance(first, ndarray):            
            if len(first) != len(second):
                return "Array lengths are different: %s != %s for \n%s\n    and\n%s" % (
                    len(first),
                    len(second),
                    first,
                    second)
                    
            if first.dtype != second.dtype:
                return "Array types are different: %s != %s for \n%s\n    and\n%s" % (
                    first.dtype,
                    second.dtype,
                    first,
                    second)
            
            for i in range(len(first)):
                difference_message = self._get_difference(first[i], second[i])
                if difference_message is not None:
                    return "Index %s, %s" % (i, difference_message)
                
            return None
            
        if isinstance(first, dict):
            if len(first) != len(second):
                return "Number of dictionary entries is different: %s != %s for \n%s\n    and\n%s" % (
                    len(first),
                    len(second),
                    first,
                    second)
            
            for key in first:
                if key not in second:
                    return "'%s' found in first dictionary, but not in second dictionary:\n%s\n    and\n%s" % (
                        key,
                        first,
                        second)
                
                difference_message = self._get_difference(first[key], second[key])
                if difference_message is not None:
                    return "Dictionary key '%s', %s" % (key, difference_message)
                
            return None
            
        if first == second:
            return None
            
        else:
            return "Values are different:\n%s\n    and\n%s" % (
                        first,
                        second)


class OpusTestCase(OpusAbstractTestCase):
    pass
    
TestCase = OpusTestCase


class OpusIntegrationTestCase(OpusAbstractTestCase):
    pass

