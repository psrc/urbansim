# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class units_proposed_for_building_type_DDD(Variable):
    
    def __init__(self, building_type_id):
        Variable.__init__(self)
        self.building_type = building_type_id
        
    def dependencies(self):
        return ["_units_proposed_for_%s = parcel.aggregate(psrc_parcel.development_project_proposal.units_proposed_for_building_type_%s, function=maximum)"  % (self.building_type, self.building_type)]

    def compute(self,  dataset_pool):
        return self.get_dataset()["_units_proposed_for_%s" % self.building_type]

    
from opus_core.tests import opus_unittest
from numpy import array, arange
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'development_project_proposal':
            {
                "proposal_id":    array([1,  2,    3,  4, 5]),
                "units_proposed": array([34, 250, 130, 0, 52]),
                "parcel_id":      array([1,   1,   2,  3, 3])
            },
            'development_project_proposal_component':
            {
                "proposal_component_id": arange(8)+1,
                 "proposal_id":           array([3,   3, 5,  2,   5,   1, 3, 1]),
                 "building_type_id":     array([19, 2, 4, 19, 1, 2, 3, 19]),
                 "template_id":           array([4,   2, 1,  3,   2,   2,  4, 1]),
                 "percent_building_sqft": array([30, 25, 1, 100, 99, 90, 45, 10]),
                 "is_residential":        array([True,False, True, True,False,True,False, True]),
                 "building_sqft_per_unit": array([3.5, 1, 20, 1, 1, 0.1, 10, 50])
             },
             'development_template':
            {
                'template_id': array([1,2,3,4]),
                'density_type': array(['units_per_acre', 'far', 'units_per_acre', 'far']),
            },
            'parcel':
            {
                'parcel_id': array([1,2,3,4]),
            },
        })
        instance_name = 'psrc_parcel.parcel.units_proposed_for_building_type_19'
        should_be = array([array([34/100. * 10/50., 250]).max(), 130/100. * 30/3.5, 0, 0])

        tester.test_is_close_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()