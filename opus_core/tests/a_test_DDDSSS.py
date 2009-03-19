# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class a_test_DDDSSS(Variable):
    """A fake variable used for testing.
    Used by tests in variable_family_name_translator.py.
    Has to be in a separate file, since Opus looks for a file with the same name as the variable."""
    
    _return_type = 'int8'
    
    def __init__(self,arg1,arg2):
        # just discard the additional arguments for DDD and SSS
        Variable.__init__(self)

    def dependencies(self):
        return ["tests.a_dependent_variable"]

    def compute(self, dataset_pool):
        logger.log_status(self._return_type)
        return self.get_dataset().get_attribute("a_dependent_variable") * 10