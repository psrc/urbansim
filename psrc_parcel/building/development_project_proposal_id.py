#
# UrbanSim software. Copyright (C) 1998-2004 University of Washington
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
from numarray.ma import masked_where, filled
from numarray import Float32, concatenate, array
from opus_core.misc import do_id_mapping_dict_from_array

class development_project_proposal_id(Variable):
    """Identify which template a compounded building was developed from"""
    ##TODO: to be finished when the development template is defined
    ##TODO: what to do where a parcel was developed from multiple template (additive)    
    def dependencies(self):
        return [my_attribute_label("development_template_id"), 
                my_attribute_label("parcel_id"),
                "psrc_parcel.development_project_proposal.proposal_id",]
        
    def compute(self,  dataset_pool):
        dpp = dataset_pool.get_dataset("development_project_proposal")
        parcel_id_template_ids = concatenate((dpp.get_attribute_as_column("parcel_id"), 
                                             dpp.get_attribute_as_column("template_id")),
                                             axis=1)
        id_mapping = do_id_mapping_dict_from_array(parcel_id_template_ids)
        buildings = self.get_dataset()
        building_parcel_id_template_ids = concatenate((buildings.get_attribute_as_column("parcel_id"), 
                                                      buildings.get_attribute_as_column("development_template_id")),
                                                      axis=1)
        index = array(map(lambda x: id_mapping[tuple(x)], building_parcel_id_template_ids))
        return dpp.get_id_attribute()[index]

    def post_check(self,  values, dataset_pool=None):
        self.do_check("x >= 0", values)
            
from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from numarray import array
import numarray.strings as strarray
from opus_core.tests.utils.variable_tester import VariableTester

class Tests(opus_unittest.OpusTestCase):
    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['psrc_parcel','urbansim'],
            test_data={
            'development_project_proposal':
            {
                'proposal_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                'parcel_id':   array([1, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
                'template_id': array([1, 2, 3, 4, 2, 3, 4, 1, 2, 4])
                },           
            "building":{
                'building_id': array([1, 2, 3, 4, 5]),
                'parcel_id':   array([1, 2, 3, 2, 1]),
                'development_template_id': array([1, 3, 4, 4, 3])
            },        
        }
        )
        
        should_be = array([1, 6, 10, 7, 3])
        
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()
    