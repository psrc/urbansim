# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from opus_core.misc import safe_array_divide
import numpy as np
from numpy import ma, zeros, arange, array
from numpy import float32, column_stack, asscalar

periods_per_year = 4
area_per_stall = 400

class cost(Variable):
    """
    cost calculation for the new real estate model
    """ 
    _return_type = "float32"
    
    def dependencies(self):
        return ["total_non_residential_sqft = proposal.retail_sqft + proposal.cultural_sqft",
                "total_parking = proposal.total_units * proposal.residential_parking_ratio + proposal.total_non_residential_sqft*non_residential_parking_ratio",
                "deck_stalls = proposal.deck_parking / %s" % area_per_stall,
                "surface_stalls = proposal.surface_parking / %s" % area_per_stall,
                "underground_stalls = numpy.ceil(proposal.total_parking - proposal.deck_stalls - proposal.surface_stalls)",

                "open_space = proposal.aggregate(proposal_component.footprint_sqft) * 0.33",
                "podium_total = proposal.aggregate(proposal_component.footprint_sqft * proposal_component.commercial_floors)",
                "podium_parking = proposal.podium_total - proposal.retail_sqft", 
                "podium_stalls = numpy.minimum(proposal.underground_stalls, podium_parking / %s)" % area_per_stall, 
                "podium_housing = proposal.podium_total - proposal.retail_sqft - proposal.podium_stalls * %s" % area_per_stall,

                "residential_potential = proposal_component.footprint_sqft * proposal_component.residential_floors",
                "special_residential_sqft = proposal.aggregate(proposal_component.residential_potential * proposal_component.special)",
                "non_special_residential_sqft = proposal.aggregate(proposal_component.residential_potential * numpy.logical_not(proposal_component.special))",
                "remaining_residential = proposal.residential_sqft_permitted - proposal.podium_housing - proposal.special_residential_sqft",
                "non_special_residential_sqft = safe_array_divide(proposal_component.disaggregate(proposal.remaining_residential) * proposal_component.residential_potential," + \
                                                                  "proposal_component.disaggregate(proposal.non_special_residential_sqft)) * numpy.logical_not(proposal_component.special)",
                "special_residential_sqft = proposal_component.residential_potential * proposal_component.special",
                "residential_sqft = proposal_component.special_residential_sqft + proposal_component.non_special_residential_sqft",
                "construction_cost = proposal_component.residential_sqft * proposal_component.cost_per_unit",

                "construction_cost = proposal.aggregate(proposal_component.construction_cost)",
                "parking_cost_surface = proposal.surface_stalls * 3000",
                "parking_cost_deck = proposal.deck_stalls * (61*1.25) * 400",
                "parking_cost_underground = proposal.underground_stalls * 35000",
                "parking_cost = proposal.parking_cost_surface + proposal.parking_cost_deck + proposal.parking_cost_underground",
                "open_space_cost = proposal.open_space * 20",
                "podium_cost = proposal.podium_total * 50 * 1.26",
                
                ]

    def compute(self, dataset_pool):
        p = self.get_dataset()
        results = (p['construction_cost'] + p['open_space_cost'] + p['parking_cost'] + p['road_cost'] + p['podium_cost']) * (1 + p['infrastructure_cost'])
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numpy import array
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_visitacion(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel','urbansim'],
            test_data={
            
            'proposal_component':
            {
                "proposal_component_id": array([1,  2,  3,  4, 5, 6, 7, 8]),
                "proposal_id":           array([1,  1,  1,  1, 1, 1, 1, 1]),
           "building_type_id":           array([2,  3,  5,  9, 0, 0, 0, 0]), 
                                           #MXD Townhome
                                               #Townhome
                                               #MXD Midrise 55
                                               #Midrise 55
                                               #MXD Midrise 65
                                               #Midrise 65
                                               #MXD Highrise 85
                                               #Highrise 85
                    "special":           array([0,  1,  0,  0, 0, 0, 0, 1]),   #why these are special?
              "cost_per_unit":           array([140, 140, 140, 140, 140, 168, 0, 168]) * 1.26,
             "footprint_sqft":           array([0,6000,308750,6000,85000,42875,0,102500]),
             "commercial_floors":         array([0,   0,     1,   0,    1,    0,1,     0]),
            "residential_floors":         array([0,   1,     3,   4,    4,    5,6,     7]),
            
               #"sqft":               array([0,  0,  105, 15]) * 1000,
              #"price_per_unit":      array([400,0,  0,  0]) * 1000,
          #"rent_per_unit":       array([0,  15, 0,  0]) * 1000,
          #"lease_per_sqft":      array([0,  0,  21, 0]),
                  #"parking_ratio":       array([4/3.0,4/3.0,500,500]),
                  #"common_area":         array([.2, .2, .15, .15]),
             },

            'proposal':{
                'proposal_id': array([1]),
 'residential_sqft_permitted': array([1875000]),
                'total_units': array([1250]),
                'retail_sqft': array([105000]),
                'cultural_sqft': array([15000]),                
 
  'residential_parking_ratio': array([.75]), 
 'non_residential_parking_ratio': array([2.0/1000]),
                'surface_parking': array([0]),
                'deck_parking': array([60000 * 3]),
                'road_cost': array([2500 * 2000]),
                'infrastructure_cost':array([0.075]),
            },
            
            }
        )
        
        should_be = array([  467087722 ])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be, rtol=1e-2)
        
if __name__=='__main__':
    opus_unittest.main()
    
