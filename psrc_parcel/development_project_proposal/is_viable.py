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

from opus_core.variables.variable import Variable
from variable_functions import my_attribute_label
from numarray.ma import masked_where

class is_viable(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints
    """

    def dependencies(self):
        return ["parcel_far = parcel:diaggregate(psrc_parcel.parcel.lot_size)",
                "lot_size = diaggregate(psrc_parcel.parcel.lot_size)",
                "far = diaggregate(psrc_parcel.development_template.far)",
                "min_units = diaggregate(psrc_parcel.development_template.far * psrc_parcel.development_template.land_area_min)",
                "max_units = diaggregate(psrc_parcel.development_template.far * psrc_parcel.development_template.land_area_max)",
                "proposed_units = lot_size * far",
                 ]

    def compute(self, dataset_pool):
        dp = self.get_dataset()
        proposed_units = dp.get_attribute("proposed_units")
        results = proposed_units
        results[where(proposed_unit>max_units)] = max_units[where(proposed_unit>max_units)]
        results[where(proposed_unit<min_units)] = min_units[where(proposed_unit<min_units)]
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

#
#from opus_core.tests import opus_unittest
#from opus_core.dataset_pool import DatasetPool
#from opus_core.storage_factory import StorageFactory
#from numarray import array
#from numarray.ma import allequal
#
#class Tests(opus_unittest.OpusTestCase):
#    variable_name = "urbansim.building.building_age"
#
#    def test_my_inputs(self):
#        storage = StorageFactory().get_storage('dict_storage')        
#        
#        storage._write_dataset(
#            'buildings',
#            {
#                'building_id': array([1,2,3,4]),
#                'year_built': array([1995, 2000, 2005, 0])
#            }
#        )
#        storage._write_dataset(
#            'urbansim_constants',
#            {
#                "absolute_min_year": array([1800]),
#            }
#        )
#        
#        SimulationState().set_current_time(2005)
#        dataset_pool = DatasetPool(package_order=['urbansim'],
#                                   storage=storage)
#
#        buildings = dataset_pool.get_dataset('building')
#        buildings.compute_variables(self.variable_name, 
#                                   dataset_pool=dataset_pool)
#        values = buildings.get_attribute(self.variable_name)
#        
#        should_be = array([10, 5, 0, 5])
#        
#        self.assert_(allequal( values, should_be), 
#                     msg = "Error in " + self.variable_name)
#
#
#if __name__=='__main__':
#    opus_unittest.main()