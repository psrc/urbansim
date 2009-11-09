# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class a_test_variable(Variable):
    """A fake variable used for testing.
    Used by tests in variable.py.
    Has to be in a separate file, since Opus looks for a file with the same name as the variable."""
    
    _return_type = 'int8'
    def dependencies(self):
        return ["tests.a_dependent_variable"]

    def compute(self, dataset_pool):
        logger.log_status(self._return_type)
        return self.get_dataset().get_attribute("a_dependent_variable") * 10


from opus_core.tests import opus_unittest
class Tests(opus_unittest.OpusTestCase):
    def test_name(self):
        variable = a_test_variable()
        self.assertEqual(variable.name(), self.__module__)


if __name__ == '__main__':
    opus_unittest.main()