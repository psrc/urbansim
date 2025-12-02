from opus_core.variables.variable import Variable

class SSS_package_SSS_wwd(Variable):
    """Sum of a variable (given by the second SSS, defined in a package given by the first SSS) 
        over gridcells located within walking distance. If the variable is a primary attribute,
        the package is not used (but must be given).
        E.g. psrc_parcel.gridcell.urbansim_parcel_package_population_wwd
        computes variable population urbansim_parcel.gridcell.population and sums it over gridcells within walking distance.
    """
        
    def __init__(self, package, name):
        self.var_package = package
        self.var_name = name
        Variable.__init__(self)
        
    def dependencies(self):
        return ['%s = %s.gridcell.%s' % (self.var_name, self.var_package, self.var_name),
                "gridcell.grid_id", 
                "_%s_wwd = urbansim_parcel.gridcell.%s_within_walking_distance" % (self.var_name, self.var_name)
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
            'job': {
               "job_id":  array([1,2,3,4,5]),
               "grid_id":  array([3,4,1, 1, 3])
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
        
        # these are expected values if mode='reflect' (influences values at boundaries)
        should_be = array( [8, 3, 9, 5])
        instance_name = "psrc_parcel.gridcell.urbansim_package_number_of_jobs_wwd"
        tester.test_is_equal_for_family_variable(self, should_be, instance_name)


if __name__=='__main__':
    opus_unittest.main()