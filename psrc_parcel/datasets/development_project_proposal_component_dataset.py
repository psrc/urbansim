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

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.storage_factory import StorageFactory
from opus_core.misc import unique_values
from numpy import arange, where, concatenate, resize

class DevelopmentProjectProposalComponentDataset(UrbansimDataset):
    """ contains components of all proposed development projects.
    """
    in_table_name_default = "development_project_proposal_components"
    out_table_name_default = "development_project_proposal_components"
    dataset_name = "development_project_proposal_component"
    id_name_default = "proposal_component_id"


def create_from_proposals_and_template_components(proposal_dataset,
                                                template_component_dataset,
                                                dataset_pool=None,
                                                resources=None):
    """create development project proposal components from proposals and development_template_component_dataset.
    """
    proposal_ids = proposal_dataset.get_id_attribute()
    template_ids = proposal_dataset.get_attribute("template_id")
    template_ids_in_components = template_component_dataset.get_attribute("template_id")
    utemplate_ids_in_components = unique_values(template_ids_in_components)
    component_ids = template_component_dataset.get_id_attribute()
    proposal_ids_in_comp = array([], dtype="int32")
    component_ids_in_comp = array([], dtype="int32")
    for template_id in utemplate_ids_in_components:
        prop_idx = where(template_ids == template_id)[0]
        comp_idx = where(template_ids_in_components == template_id)[0]
        if proposal_ids_in_comp.size == 0:
            proposal_ids_in_comp = resize(proposal_ids[prop_idx], comp_idx.size*proposal_ids[prop_idx].size)
            component_ids_in_comp = resize(component_ids[comp_idx], proposal_ids[prop_idx].size*component_ids[comp_idx].size)
        else:
            proposal_ids_in_comp = concatenate((proposal_ids_in_comp, 
                resize(proposal_ids[prop_idx], comp_idx.size*proposal_ids[prop_idx].size)))
            component_ids_in_comp = concatenate((component_ids_in_comp, 
                resize(component_ids[comp_idx], proposal_ids[prop_idx].size*component_ids[comp_idx].size)))
        
    storage = StorageFactory().get_storage('dict_storage')
    storage._write_dataset(out_table_name='development_project_proposal_components',
                           values = {
                               "proposal_component_id": arange(1, proposal_ids_in_comp.size+1, 1),
                               "proposal_id": proposal_ids_in_comp,
                               "component_id": component_ids_in_comp,
                           }
                       )
    development_project_proposal_components = DevelopmentProjectProposalComponentDataset(resources=resources,
                                                                  in_storage=storage,
                                                                  in_table_name='development_project_proposal_components',
                                                                  )
    development_project_proposal_components.join(proposal_dataset, "parcel_id", 
                                                 join_attribute="proposal_id")
    templates_attributes = template_component_dataset.get_known_attribute_names()
    templates_attributes.remove("component_id")
    development_project_proposal_components.join(template_component_dataset, templates_attributes,
                                                 join_attribute="component_id")
    return development_project_proposal_components

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from opus_core.storage_factory import StorageFactory
from development_project_proposal_dataset import create_from_parcel_and_development_template
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage._write_dataset(
            'development_templates',
            {
                'template_id': array([1,2,3]),
            }
        )
        storage._write_dataset(
            'development_template_components',
            {
                'template_id': array([1,1,2,3,3,3]),
                'component_id': arange(6)+1
            }
        )
        storage._write_dataset(
            'parcels',
            {
                "parcel_id": array([1,   2,    3]),
            }
        )
        storage._write_dataset(
            'development_project_proposal_components',
            {
                "proposal_component_id": arange(18)+1,
                "proposal_id":array([1,  1, 2, 3, 3,3, 4,4, 5,  6, 6,6,7, 7,8, 9, 9,9]),
                "template_id":array([1,  1, 2, 3, 3,3, 1,1, 2,  3,3,3,  1, 1, 2, 3,3,3]),
                "component_id": array([1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6])
            }
        )

        self.dataset_pool = DatasetPool(package_order=['psrc_parcel'],
                                   storage=storage)
        parcels = self.dataset_pool.get_dataset('parcel')
        templates = self.dataset_pool.get_dataset('development_template')
        template_components = self.dataset_pool.get_dataset('development_template_component')
        proposals = create_from_parcel_and_development_template(parcels, templates, resources=None)
        self.proposal_components = create_from_proposals_and_template_components(proposals, template_components)

    def test_create(self):
        proposals_components = self.dataset_pool.get_dataset("development_project_proposal_component")
        template_ids = self.proposal_components.get_attribute("template_id")
        
        self.assert_(ma.allequal(self.proposal_components.size(), proposals_components.size()))
        self.assert_(self.proposal_components.get_attribute("proposal_id").sum(), proposals_components.get_attribute("proposal_id").sum())
        self.assert_((template_ids==1).sum(), (proposals_components.get_attribute("template_id")==1).sum())
        self.assert_((template_ids==2).sum(), (proposals_components.get_attribute("template_id")==2).sum())
        self.assert_((template_ids==3).sum(), (proposals_components.get_attribute("template_id")==3).sum())
        self.assert_(self.proposal_components.get_attribute("component_id").sum(), proposals_components.get_attribute("component_id").sum())

if __name__=='__main__':
    opus_unittest.main()