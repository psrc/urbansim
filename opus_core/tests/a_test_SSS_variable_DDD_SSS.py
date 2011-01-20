# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.logger import logger

class a_test_SSS_variable_DDD_SSS(Variable):
    """A fake variable used for testing.
    Used by tests in variable_family_name_translator.py.
    Has to be in a separate file, since Opus looks for a file with the same name as the variable."""
    
    _return_type = 'int8'
    
    def __init__(self,arg1,arg2,arg3):
        # just discard the additional arguments for SSS and DDD
        Variable.__init__(self)

    def dependencies(self):
        return ["tests.a_dependent_variable"]

    def compute(self, dataset_pool):
        logger.log_status(self._return_type)
        return self.get_dataset().get_attribute("a_dependent_variable") * 10