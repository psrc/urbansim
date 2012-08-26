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
            unique_member_ids = ps['member_id'][is_member]
            """
            member_index = arange(members) 

            unique_member_ids = ps['member_id'][is_member]

            unique_ids, unique_index = unique(unique_member_ids, return_index=True)

            ## remove 0
            non_unique_index = where(~ in1d(member_index, unique_index))[0]
            non_unique_index = concatenate((non_unique_index, where(unique_member_ids<=0)[0]))

            if non_unique_index.size > 0:
                new_unique_ids = array(list(set(member_index + 1) - set(unique_ids)), dtype=results.dtype)
                unique_member_ids[non_unique_index] = new_unique_ids[0:non_unique_index.size]
            """
            #print results[is_member], arange(members)+1, type(results[is_member]), type(arange(members,dtype=int)), type(results[is_member][0])
            #print is_member
            results[is_member] = arange(members, dtype=results.dtype) + 1
            #results[is_member] += 1


            """
            if len(set(unique_member_ids)) <> is_member.size:
                print '\nnew hhid', hhid
                print is_member.shape
                #print 'member_index', member_index
                print 'unique_member_ids', unique_member_ids
                #print 'unique ids, unique indexx', unique_ids, unique_index
                #print 'non unique index', non_unique_index
                #print 'unique_member_ids', unique_member_ids
                print 'fina result', results[is_member]
                raise Exception, "Hell caused here ... "
            """
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
                    'household_id': array([2,1,4,5]), #arange(5)+1,
                    },
                'person': {
                    'person_id':    arange(13),
                    'household_id': array([2,  2,   2, 2,  2,  1,  1,  1, 1, 4, 5,  5, 5]),     
                    'member_id':    array([2,  1,   3, 5,  3,  1,  7, -1, 0, 0, 2,  2, 2])
                }
            }
        )

        should_be = array([1, 3, 2, 1, 2, 1, 7, 2, 3, 1, 1, 3, 2])

        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    #import wingdbstub
    opus_unittest.main()
