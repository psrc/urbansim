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
#from variable_functions import my_attribute_label
from numarray import Bool, zeros, Bool, logical_and

class is_size_fit(Variable):
    """whether the proposed development template is viable for a given parcel and its constraints
    """

    def dependencies(self):
        return ["vacant_land_area=development_project_proposal.disaggregate(psrc_parcel.parcel.vacant_land_area)",
                "land_area_min=development_project_proposal.disaggregate(psrc_parcel.development_template.land_area_min)",
                "land_area_max=development_project_proposal.disaggregate(psrc_parcel.development_template.land_area_max)",
                 ]

    def compute(self, dataset_pool):
        dp = self.get_dataset()
        results = zeros(dp.size(), type=Bool)
        results[logical_and(dp.get_attribute("vacant_land_area") >= dp.get_attribute("land_area_min"),
                              dp.get_attribute("vacant_land_area") <= dp.get_attribute("land_area_max") )] = 1
        return results

    def post_check(self, values, dataset_pool):
        self.do_check("x in (0, 1)", values)


from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numarray import array
from numarray.ma import allequal

class Tests(opus_unittest.OpusTestCase):
    variable_name = "psrc_parcel.development_project_proposal.is_size_fit"

    def test_my_inputs(self):
        storage = StorageFactory().get_storage('dict_storage')
        
        storage._write_dataset(
            'development_templates',
            {
                'template_id': array([1,2,3,4]),
                'land_area_min': array([0, 10, 1000, 0]),
                'land_area_max': array([0, 1999, 2000, 10]),                
            }
        )
        storage._write_dataset(
            'parcels',
            {
                "parcel_id":        array([1,   2,    3]),
                "vacant_land_area":array([10, 1000,  2000]),
            }
        )
        storage._write_dataset(
            'development_project_proposals',
            {
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11]),
                "parcel_id":  array([1,  1,  1,  1, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  2,  3, 4, 1,  2, 3, 4])
            }
        )
        
        dataset_pool = DatasetPool(package_order=['psrc_parcel'],
                                   storage=storage)

        proposals = dataset_pool.get_dataset('development_project_proposal')
        proposals.compute_variables(self.variable_name, 
                                   dataset_pool=dataset_pool)
        values = proposals.get_attribute(self.variable_name)
        
        should_be = array([0, 1,  0, 1,  1, 1, 0, 0, 0, 1, 0])
        
        self.assert_(allequal( values, should_be), 
                     msg = "Error in " + self.variable_name)


if __name__=='__main__':
    opus_unittest.main()