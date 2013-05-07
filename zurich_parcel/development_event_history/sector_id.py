# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from numpy import ma, clip, where
from opus_core.logger import logger, log_block

class sector_id(Variable):
    """ number of job spaces that is vacant/unoccupied"""
    
    _return_type = "int32"
    
    def dependencies(self):
        return [
                ]

    @log_block(name='sector_id.compute')
    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        residential_sqm = dataset.compute_variables(["sc_residential_sqm"], dataset_pool=dataset_pool)[:,0]
        logger.log_note("residential_sqm: %s" % sum(residential_sqm))

    def post_check(self, values, dataset_pool=None):
        self.do_check("x >= 0", values)

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    pass

if __name__=='__main__':
    opus_unittest.main()
