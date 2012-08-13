# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import zeros_like, where, arange, unique, in1d, concatenate, array

class unique_member_id(Variable):
    def dependencies(self):
        return ['person.member_id',
                'person.household_id',
                'household.household_id']

    def compute(self, dataset_pool):
        hs = dataset_pool['household']
        ps = self.get_dataset()
        results = zeros_like(ps['member_id'])
        for hhid in hs['household_id']:
            is_member = where(ps['household_id'] == hhid)[0]
            members = is_member.size
            member_index = arange(members)
            unique_member_ids = ps['member_id'][is_member]
            unique_ids, unique_index = unique(unique_member_ids, return_index=True)
            ## remove 0
            non_unique_index = where(~ in1d(member_index, unique_index))[0]
            non_unique_index = concatenate((non_unique_index, where(unique_member_ids<=0)[0]))
            if non_unique_index.size > 0:
                new_unique_ids = array(list(set(member_index + 1) - set(unique_ids)), dtype=results.dtype)
                unique_member_ids[non_unique_index] = new_unique_ids[0:non_unique_index.size]
            results[is_member] = unique_member_ids

        return results

from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['mag_zone'],
            test_data={            
                'household':
                {
                    'household_id': arange(5)+1,
                    },
                'person': {
                    'person_id':    arange(13),
                    'household_id': array([2,  2,   2, 3,  3,  1,  1,  1, 1, 4, 5,  5, 5]),     
                    'member_id':    array([1, -1,   2, 1,  2,  1,  7, -1, 0, 0, 1,  3, 2])
                }
            }
        )

        should_be = array([1, 3, 2, 1, 2, 1, 7, 2, 3, 1, 1, 3, 2])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    import wingdbstub
    opus_unittest.main()
