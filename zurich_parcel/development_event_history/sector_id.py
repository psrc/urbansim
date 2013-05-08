# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.variables.variable import Variable
from opus_core.logger import logger, log_block
from numpy import append, reshape, argmax
import re

class sector_id(Variable):
    """ number of job spaces that is vacant/unoccupied"""
    
    _return_type = "int32"
    
    def dependencies(self):
        return [
                ]

    @log_block(name='sector_id.compute')
    def compute(self, dataset_pool):
        dataset = self.get_dataset()
        with logger.block("Compute sc_residential_sqm", verbose=True):
            residential_sqm = dataset.compute_variables(["sc_residential_sqm"], dataset_pool=dataset_pool)
            logger.log_note("residential_sqm: %s" % residential_sqm)
            #barf
            # residential_sqm = residential_sqm[:,0]
        logger.log_note("residential_sqm: %s" % sum(residential_sqm))
        
        attr_names_matches = [re.match('sqm_sector([0-9]+)', n) for n in dataset.get_known_attribute_names()]
        sector_ids = sorted([int(m.group(1)) for m in attr_names_matches if m])
        
        sqm_sector_array = reshape(residential_sqm, (-1, 1))
        
        for sector_id in sector_ids:
            sqm_sector = dataset.compute_one_variable_with_unknown_package("sqm_sector%s" % sector_id, dataset_pool=dataset_pool)
            logger.log_note("sqm_sector%s: %s" % (sector_id, sum(sqm_sector)))
            sqm_sector_array = append(sqm_sector_array, reshape(sqm_sector, (-1, 1)), 1)
        
        sqm_sector_argmax = argmax(sqm_sector_array, 1)
        #logger.log_note("sqm_sector_argmax: %s" % sqm_sector_argmax)
        
        sector_id_array = array([0] + sector_ids)
        #logger.log_note("sector_id_array: %s" % sector_id_array)
        
        val = sector_id_array[sqm_sector_argmax]
        #logger.log_note("val: %s" % val)
        return val

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
