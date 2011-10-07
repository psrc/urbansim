# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

# Import all from unittest so that opus_unittest acts just like unittest,
# except for the differences below.
from unittest import *   # Do not delete this line. @UnusedWildImport

# If FunctionTestCase remains defined here, unit tests fail to complete if running from within Eclipse.
# Reason: The base class FunctionTestCase does not constitute a valid test. Perhaps this is a bug in unittest?
# The given workaround removes the faulty behavior.
_FunctionTestCase = FunctionTestCase
del FunctionTestCase
class FunctionTestCase(_FunctionTestCase):
    _parent = _FunctionTestCase
    def __init__(self, testFunc, setUp=None, tearDown=None, description=None):
        if isinstance(testFunc, str):
            testFunc = lambda: None
        self._parent.__init__(self, testFunc, setUp, tearDown, description)
        
del _FunctionTestCase

        
        

from numpy import ndarray

from opus_core.singleton import Singleton


OriginalTestCase = TestCase

class OpusAbstractTestCase(OriginalTestCase):
    """Extends TestCase to remove all singletons before and after each test."""
    
    def __init__(self, *args, **kwargs):
        """
        Set up to automatically clear out singletons before and after running
        each test.
        """
        OriginalTestCase.__init__(self, *args, **kwargs)
        setup_method = self.setUp
        def wrapped_setup_method(*req_args, **opt_args):
            Singleton().remove_all_singletons()
            return setup_method(*req_args, **opt_args)
        self.setUp = wrapped_setup_method
        teardown_method = self.tearDown
        def wrapped_teardown_method(*req_args, **opt_args):
            result = teardown_method(*req_args, **opt_args)
            Singleton().remove_all_singletons()
            return result
        self.tearDown = wrapped_teardown_method
        
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
            
    def assertArraysEqual(self, first, second, *args, **kwargs):
        """
        Assert that these two numpy arrays are equal.
        """
        self.assert_(isinstance(first, ndarray), *args, **kwargs)
        self.assert_(isinstance(second, ndarray), *args, **kwargs)
        
        if not all(first == second):
            self.fail('Arrays are different: %s vs %s.' % (first, second))

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

