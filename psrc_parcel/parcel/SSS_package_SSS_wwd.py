# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE
from opus_core.variables.variable import Variable

class SSS_package_SSS_wwd(Variable):
    """Sum of a variable (given by the second SSS, defined in a package given by the first SSS) 
        over parcels connected to gridcells located within walking distance. If the variable is a primary attribute,
        the package is not used (but must be given).
        E.g. psrc_parcel.parcel.urbansim_parcel_package_population_wwd
        computes variable population urbansim_parcel.parcel.population and sums it over gridcells within walking distance.
    """
        
    def __init__(self, package, name):
        self.var_package = package
        self.var_name = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ['%s = gridcell.aggregate(%s.parcel.%s)' % (self.var_name, self.var_package, self.var_name),
                "gridcell.grid_id", 'parcel.grid_id',
                "_%s_wwd = parcel.disaggregate(urbansim_parcel.gridcell.%s_within_walking_distance)" % (self.var_name, self.var_name)
                ]

    def compute(self, dataset_pool):
        return self.get_dataset()["_%s_wwd" % self.var_name]
    
    
from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array

class Tests(opus_unittest.OpusTestCase):

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel', 'urbansim_parcel', 'urbansim'],
            test_data={
            'parcel': {
               "parcel_id":  array([1,  2,  3,  4,  5,  6, 7, 8, 9]),
               'grid_id':    array([1,  1,  1,  2,  2,  3, 4, 4, 4]),
                    },
            'school': {
               "school_id":  array([1,2,3,4,5]),
               "parcel_id":  array([3,4,7, 8, 9]),
               "public": array([True, False, True, False, True])
               },
            'gridcell':{ 
                 'grid_id':array([1, 2, 3, 4]),
                 'relative_x': array([1,2,1,2]),
                 'relative_y': array([1,1,2,2]),
                },
             'urbansim_constant':{
                    "walking_distance_circle_radius": array([150]),
                    'cell_size': array([150]),
                }
             }
            )
        # these are expected values if mode='constant' (in urbansim.gridcell.abstract_within_walking_distance)
        #should_be = array( [1, 1, 1, 3, 3, 3, 2, 2, 2])
        
        # these are expected values if mode='reflect' (influences values at boundaries)
        should_be = array( [3, 3, 3, 3, 3, 3, 6, 6, 6])
        instance_name = "psrc_parcel.parcel.psrc_parcel_package_number_of_public_schools_wwd"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()