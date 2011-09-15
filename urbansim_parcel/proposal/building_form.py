# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
import numpy as np
from numpy import ma, zeros, arange, array, asarray
from numpy import float32, column_stack, asscalar, concatenate
from scipy.optimize import fmin_slsqp

minimum_lobby = 1000
size_of_parking_stall = 350
maximum_floors_of_ground_parking = 15
ground_floor_retail_floor_to_floor_height = 15
open_space_required_for_home_builder = .10

class building_form(Variable):
    """
    determine the optimal building form
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return [
                            "buildable_area = parcel.parcel_area * .8", ##TODO replace this with result from geometry query
                            "buildable_area = proposal.disaggregate(parcel.buildable_area)",
            #                "maximum_number_of_floors = parcel.ground_floor_retail * numpy.floor((parcel.building_height - %s)/parcel.floor_to_floor_height) + 1 + numpy.logical_not(parcel.ground_floor_retail) * (parcel.multi_story * parcel.building_height / parcel.floor_to_floor_height + numpy.logical_not(parcel.multi_story))" % ground_floor_retail_floor_to_floor_height, 
            #            ## if ground_floor_retail:
            #              ## = ((parcel.building_height - %s)/parcel.floor_to_floor_height) + 1
            #            ## else:
            #              ## if multi_story:
            #                    ## = building_height / floor_to_floor_height
            #              ## else:
            #                    ## = 1
            #                "maximum_floor_area = numpy.minimum(parcel.parcel_sqft * parcel.floor_area_ratio, parcel.buildable_area * parcel.maximum_number_of_floors)",
            #                "maximum_footprint = numpy.minimum(parcel.parcel_sqft * parcel.floor_area_ratio, parcel.buildable_area)",
            #                "minimum_footprint = proposal.aggregate(proposal_component.minimum_units) + proposal.aggregate(proposal_component.ground_floor_retail) * %s" % minimum_lobby,
            #                "maximum_footprint = proposal.disaggregate(parcel.maximum_footprint)",
            #            #"footprint = (proposal.maximum_footprint - proposal.minimum_footprint) * numpy.random.random()",
                            "openspace_requirement = parcel.disaggregate(zoning.openspace_requirement)",
                            "parcel_area = proposal.disaggregate(parcel.parcel_area)",
                            "openspace_required = proposal.disaggregate(parcel.parcel_area) * proposal.disaggregate(parcel.openspace_requirement)",
            #                "surface_parking_ratio = proposal.disaggregate(parcel.surface_parking_ratio)",
            #                "surface_parking = (proposal.disaggregate(parcel.parcel_area) - proposal.footprint) * proposal.surface_parking_ratio",
            #                "ground_floor_parking = (proposal.footprint - proposal.ground_floor_retail_sqft - %s) * proposal.ground_floor_retail" % minimum_lobby,
            #                "deck_parking = proposal.maximum_floor_area - proposal.footprint * proposal.ground_floor_retail - proposal.aggregate(proposal_component.sqft * proposal_component.is_non_residential) - proposal.aggregate(proposal_component.unit_size * proposal_component.units * proposal_component.is_mf_residential)",
            #                "underground_parking = proposal.parcel_sqft * %s" % maximum_floors_of_ground_parking,
            #                "parking_required = proposal.aggregate(proposal_component.parking_requirement * proposal_component.units_proposed)",

                ]

    def compute(self, dataset_pool):
        pp = self.get_dataset()
        #c = dataset_pool.get_dataset('proposal_component')
        max_footprint = pp['parcel_area'] - pp['openspace_required']
        max_buildable_area = pp['buildable_area']

        ##constraints
        #1. 'footprint' <= 
        def ieqcons(x, *args):
            cons = concatenate(([max_footprint, max_buildable_area]))
            res = cons - x
            return res

        def fprime_ieqcons(x, *args):
            return array([[-1.0, 0], 
                          [0, -1.0]])

        ##Sequential Least-square fitting with constraints (fmin_slsqp)
        x0 = array([pp['parcel_area'], pp['parcel_area']])
        X = fmin_slsqp(self._objfunc,
                       x0,
                       args=(-1.0,),
                       f_ieqcons=ieqcons, 
                       #fprime_ieqcons=fprime_ieqcons,
                       #ieqcons=[lambda x, args: max_footprint-x[0] ], 
                       #ieqcons=[lambda x, args: max_footprint-x[0],
                       #         lambda x, args: max_buildable_area-x[1]
                       #        ],
                       iprint=2, full_output=1)
        return asarray(X[0])

    def _objfunc(self, params, *args):
        #minimize or maximize?
        try:
            sign = args[0]
        except:
            sign = 1.0
    
        #proposal['footprint'] = params[0]
        #proposal[''] = params[]
    
        #npv = proposal.compute_variable("urbansim_parcel.proposal.proforma")
        #return npv
        #x, y = params[0], params[1]
        x = params[0]
        #print params 
        v = sign * x
        return v

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            'parcel':
            {
                "parcel_id":        array([1]),
                "parcel_area":      array([45000]),
                "zoning_id"  :      array([6]),
                "property_tax":     array([0.01]),
                "land_cost":        array([ 5]) * 1000000, #Land + other equity                
            },

            'zoning':
            {
                'zoning_id':       array([6]),
                'zoning_code':     array(['MX-R']),
                'front_setback':   array([10]),
                'side_setback':    array([0]),
                'rear_setback':    array([10]),
                'building_height': array([55]),
                'floor_area_ratio':array([4]),
                'ground_floor_retail_parking_ratio':array([3]),  #per 1000sqft
                'parking_per_unit':array([1.25]),
                'surface_parking_ratio':array([0]), #Non-footprint available for surface parking (%)
                'multi_story':     array([1]),
                'ground_floor_retail': array([1]),
                'single_family_builder':array([0]),
                'floor_to_floor_height':array([10]),
                'openspace_requirement':array([.1]),
            },

                #            'proposal_component':
                #            {
                #                "proposal_component_id": array([1,  2,  3,  4,  5]),
                #                "proposal_id":           array([1,  1,  1,  1,  1]),
                #           "building_type_id":           array([3,  3,  3,  3,  4, 4, 4, 4, 5, 6]),  
                #                                         #3-multi-Family, 4-Condo, 5-commercial, 6-office
                #                   "bedrooms":           array([1,  2,  3,  4,  0]),
                #                   
                #                   "lot_size":           array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
                #                   "unit_size":          array([750, 1000, 1250, 1500, 950, 1100, 1300, 1600, 0, 0]),
                #
                #                   "efficiency":          array([750, 1000, 1250, 1500, 950, 1100, 1300, 1600, 0, 0]),
                #                   "open_space":          array([750, 1000, 1250, 1500, 950, 1100, 1300, 1600, 0, 0]),
                #                   "min_units":          array([0, 0, 0, 0, 0, 0, 0, 0, 1000, 0]),
                #          "parking_requirement":          array([1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 1.25, 3000, 5000]),
                #                   
                #                   "sales_revenue":      array([2,  3,  4,  5,  0]) * 1000000, #total
                #                "sales_absorption":    array([.25,0.3,0.35,0.4,  0]) * 1000000, #per period
                #                    "rent_revenue":    array([ .1,0.2,0.3,0.4,  0]) * 1000000, #per period
                #                  "rent_absorption":   array([  8,  4,  4,  8,  8]),
                #                 "leases_revenue":      array([  0,  0,  0,  0,  4]) * 1000000, #per period
                #                  "leases_absorption":  array([  0,  0,  0,  0,  8]),                   
                #              "vacancy_rates":         array([ 1.0, 0.5, 0.25, 1.0,  0.6]) / 12,
                #             "operating_cost":         array([0.2,0.2,0.2,0.2, 0.1]),
                #             },
            'proposal':
            {
             
                "proposal_id":array([1]),
                  "parcel_id":array([1]),
  "construction_start_period":array([ 1]),           #construction start date                  
     "sales_start_period":    array([ 5]),           #Sales/Rent start date
     "rent_sqft":             array([ 75]) * 1000,
     "total_sqft":            array([ 75]) * 1000,  #TODO:fake it so that it pays taxes on all portions
     "construction_cost":     array([ 30]) * 1000000,
     "public_contribution":   array([ 0.0]),
            },
            
            }
        )
        
        should_be = array([ 40500,  36000])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)

if __name__=='__main__':
    opus_unittest.main()
    
