# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE
 
from opus_core.class_factory import ClassFactory 

class ModelComponentCreator(object):
    """
    Contains methods used by model creator classes.
    """
    def get_model_component(self, name, arguments={}, debuglevel=0):
        return ClassFactory().get_class(name, arguments=arguments, debug=debuglevel)
                                             
    def get_package_name(self, operation_name):
        if (operation_name == None):
            return None
        return operation_name.split(".")[0].lower()
        
    def get_operation_name(self, operation_name):
        if (operation_name == None):
            return None
        words = operation_name.split(".")
        return words[len(words)-1].lower()

    def add_suffix_to_operation_name(self, user_defined_name, name_of_operation_type=None):
        """Create the lower-case compound name that uniquely identifies the specific instance of this 
        type of operation.  For example return 'linear_utilities' for user_defined_name='linear' and 
        name_of_operation_type='utilities'.
        """
        if user_defined_name == None:
            return None
        if name_of_operation_type == None:
            return self.get_operation_prefix(user_defined_name)
        return self.get_operation_name(user_defined_name) + '_' + name_of_operation_type.lower()
        
    def get_subdirectory(self, operation_name):
        """Extract subdirectory from an operation name. E.g. if operation_name is 'opus_core.operations.uilities', it 
        returns 'operations'.
        """
        if (operation_name == None):
            return None
        words = operation_name.split(".")
        dir = ""
        for iw in range(1,len(words)-1):
            dir=dir + words[iw]
            if iw < len(words)-2:
                dir=dir+"."
        return  dir

#============================================================================
# Tests
#============================================================================
from opus_core.tests import opus_unittest
class ModelComponentCreatorTests(opus_unittest.OpusTestCase):
    def test(self):
        mc = ModelComponentCreator()
        self.assertEqual("a", mc.get_package_name("a.bc"))
        self.assertEqual("bc", mc.get_operation_name("a.Bc"))
        self.assertEqual("a_bc", mc.add_suffix_to_operation_name("p.a", "bc"))
        self.assertEqual("module_name_prefix", mc.add_suffix_to_operation_name("package_name.module_name", "prefix"))
        self.assertEqual("subdir", mc.get_subdirectory("abc.subdir.operation"))
        self.assertEqual("", mc.get_subdirectory("abc.operation"))
        self.assertEqual("subdir1.subdir2", mc.get_subdirectory("abc.subdir1.subdir2.operation"))

if __name__=='__main__':
    opus_unittest.main()
