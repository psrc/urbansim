# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class SSS_within_DDD_radius(Variable):
    """Sum SSS over cells within DDD radius. """

    def __init__(self, name, radius):
        self.varname = name
        self.radius = radius
        self.gc_name = "_gc_%s" % name
        Variable.__init__(self)
        
    def dependencies(self):
        return ['grid_id=household.disaggregate(parcel.grid_id, intermediates=[building])',
                'grid_id=job.disaggregate(parcel.grid_id, intermediates=[building])',
                "gridcell.grid_id", 'parcel.grid_id', 
                '%s = psrc_parcel.gridcell.%s_within_%s_radius' % (self.gc_name, self.varname, self.radius)]

    def compute(self, dataset_pool):
        gcs = dataset_pool.get_dataset('gridcell')
        parcels = self.get_dataset()
        return parcels.get_join_data(gcs, self.gc_name)



from opus_core.tests import opus_unittest
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'gridcell':
            {
                "grid_id":    array([1,   2,    3, 4,5,6,7,8]),
                "relative_x": array([1,   2,    3, 4,1,2,3,4]),
                "relative_y": array([1,   1,    1, 1, 2,2,2,2 ]),
            },
            'parcel':
            {
                "parcel_id":  array([1,   2,    3, 4,5]),
                "grid_id":    array([5,   3,    7, 7,8]),
            },
            'building':
            {
                "building_id":      array([1,2,3,4,5,6]),
                "parcel_id":        array([1,1,2,1,4,5]),
                "residential_units":array([1,2,1,5,7,3])
             },
             'urbansim_constant':
             {
              "cell_size": array([1])
              },
             # the following datasets do not influence the test results 
             'household':
             {
              "household_id":array([1,2,3,4,5,6]),
              "building_id":array([1,2,3,4,5,6]),
             },
            'job':
             {
              "job_id":array([1,2,3,4,5,6]),
              "building_id":array([1,2,3,4,5,6]),
             }
        })
        # these are expected values if mode='constant' (in gridcell.SSS_within_DDD_radius)
        #should_be = array([15, 11, 19, 19, 11])
        
        # these are expected values if mode='reflect' (default in gridcell.SSS_within_DDD_radius)
        should_be = array([39, 26, 34, 34, 34])

        instance_name = 'psrc_parcel.parcel.residential_units_within_2_radius'
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)

if __name__=='__main__':
    opus_unittest.main()