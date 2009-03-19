# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.abstract_variables.abstract_absolute_SSS_difference_from_DDD \
    import abstract_absolute_SSS_difference_from_DDD


class absolute_SSS_difference_from_DDD(abstract_absolute_SSS_difference_from_DDD):
    """difference of variable SSS (current year - baseyear)"""

    def __init__(self, *args, **kwargs):
        abstract_absolute_SSS_difference_from_DDD.__init__(self, 'zone', package_name='psrc', *args, **kwargs)


from opus_core.tests import opus_unittest
from urbansim.abstract_variables.abstract_absolute_SSS_difference_from_DDD import TestFactory

# Need to assign to the same name as the class defined in TestFactory.
__MyTests = TestFactory().get_test_case_for_dataset('zone', 'zones', 'zone_id')


if __name__ == '__main__':
    opus_unittest.main()
