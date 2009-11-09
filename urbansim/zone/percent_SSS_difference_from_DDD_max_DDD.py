# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE


from urbansim.abstract_variables.abstract_percent_SSS_difference_from_DDD_max_DDD \
    import abstract_percent_SSS_difference_from_DDD_max_DDD


class percent_SSS_difference_from_DDD_max_DDD(abstract_percent_SSS_difference_from_DDD_max_DDD):
    """percent difference of variable SSS (current year - baseyear)"""
    def __init__(self, *args, **kwargs):
        abstract_percent_SSS_difference_from_DDD_max_DDD.__init__(self, 'zone', *args, **kwargs)
        

from opus_core.tests import opus_unittest
from urbansim.abstract_variables.abstract_percent_SSS_difference_from_DDD_max_DDD import TestFactory

# Need to assign to the same name as the class defined in TestFactory.
__MyTests = TestFactory().get_test_case_for_dataset('zone', 'zones', 'zone_id')


if __name__ == '__main__':
    opus_unittest.main()
