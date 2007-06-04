#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
#
# You can redistribute this program and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation
# (http://www.gnu.org/copyleft/gpl.html).
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the file LICENSE.html for copyright
# and licensing information, and the file ACKNOWLEDGMENTS.html for funding and
# other acknowledgments.
#


from urbansim.abstract_variables.abstract_percent_SSS_difference_from_DDD \
    import abstract_percent_SSS_difference_from_DDD
    

class percent_SSS_difference_from_DDD(abstract_percent_SSS_difference_from_DDD):
    """difference of variable SSS (current year - baseyear)"""
    def __init__(self, *args, **kwargs):
        abstract_percent_SSS_difference_from_DDD.__init__(self, 'faz', *args, **kwargs)


from opus_core.tests import opus_unittest
from urbansim.abstract_variables.abstract_percent_SSS_difference_from_DDD import TestFactory

# Need to assign to the same name as the class defined in TestFactory.
__MyTests = TestFactory().get_test_case_for_dataset('faz', 'fazes', 'faz_id')


if __name__ == '__main__':
    opus_unittest.main()
