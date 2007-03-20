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
        
if __name__=='__main__':
    import unittest
    from urbansim.variable_test_toolbox import VariableTestToolbox
    from numarray import array
    from numarray.ma import allclose
    from opus_core.resources import Resources    
    from psrc_parcel.datasets.building_dataset import BuildingDataset
    from psrc_parcel.datasets.development_project_proposal_dataset import DevelopmentProjectProposalDataset
    from opus_core.storage_factory import StorageFactory
    
    class Tests(unittest.TestCase):
        variable_name = "psrc_parcel.building.development_project_proposal_id"

        def test_my_inputs(self):
#            storage1 = StorageFactory().get_storage('dict_storage')
#            table_name1 = 'buildings'            
#            storage1.write_dataset(
#                Resources({
#                    'out_table_name':table_name1,
#                    'values':{
#                        'building_id': array([1, 2, 3, 4, 5]),
#                        'parcel_id':   array([1, 2, 3, 2, 1]),
#                        'development_template_id': array([1, 3, 4, 4, 3])
#                        },
#                    })
#                )
#            building = BuildingDataset(in_storage=storage1, in_table_name=table_name1)

            storage2 = StorageFactory().get_storage('dict_storage')
            table_name2 = 'development_project_proposals'            
            storage2.write_dataset(
                Resources({
                    'out_table_name':table_name2,
                    'values':{
                        'proposal_id': array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                        'parcel_id':   array([1, 1, 1, 1, 2, 2, 2, 3, 3, 3]),
                        'template_id': array([1, 2, 3, 4, 2, 3, 4, 1, 2, 4])
                        },
                    })
                )
            proposals = DevelopmentProjectProposalDataset(in_storage=storage2, in_table_name=table_name2)


            values = VariableTestToolbox().compute_variable(self.variable_name, \
                {"building":{
                        'building_id': array([1, 2, 3, 4, 5]),
                        'parcel_id':   array([1, 2, 3, 2, 1]),
                        'development_template_id': array([1, 3, 4, 4, 3])
                        },
                 "development_project_proposal":proposals,
                 }, 
                dataset = "building")
            should_be = array([1, 6, 10, 7, 3])
            
            self.assertEqual(allclose(values, should_be), \
                             True, msg = "Error in " + self.variable_name)
            
    unittest.main()