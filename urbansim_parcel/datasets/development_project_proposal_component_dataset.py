# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.storage_factory import StorageFactory
from opus_core.misc import unique
from opus_core.variables.attribute_type import AttributeType
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
    utemplate_ids_in_components = unique(template_ids_in_components)
    component_ids = template_component_dataset.get_id_attribute()
    proposal_ids_in_comp = array([], dtype="int32")
    component_ids_in_comp = array([], dtype="int32")
    for template_id in utemplate_ids_in_components:
        prop_idx = where(template_ids == template_id)[0]
        comp_idx = where(template_ids_in_components == template_id)[0]
        if proposal_ids_in_comp.size == 0:
            proposal_ids_in_comp = resize(proposal_ids[prop_idx], comp_idx.size*proposal_ids[prop_idx].size)
            component_ids_in_comp = resize(component_ids[comp_idx[0]], proposal_ids[prop_idx].size)
            for icomp in range(1, comp_idx.size):
                component_ids_in_comp = concatenate((component_ids_in_comp, 
                    resize(component_ids[comp_idx[icomp]], proposal_ids[prop_idx].size)))
        else:
            proposal_ids_in_comp = concatenate((proposal_ids_in_comp, 
                resize(proposal_ids[prop_idx], comp_idx.size*proposal_ids[prop_idx].size)))
            for icomp in range(comp_idx.size):
                component_ids_in_comp = concatenate((component_ids_in_comp, 
                    resize(component_ids[comp_idx[icomp]], proposal_ids[prop_idx].size)))
        
    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(
        table_name='development_project_proposal_components',
        table_data={
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
                                                 join_attribute="proposal_id", metadata=AttributeType.PRIMARY)
    attributes = ["template_id"]
    if "building_type_id" in template_component_dataset.get_known_attribute_names():
        attributes.append("building_type_id")
    development_project_proposal_components.join(template_component_dataset, attributes,
                                                 join_attribute="component_id", metadata=AttributeType.PRIMARY)
    return development_project_proposal_components

from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from .development_project_proposal_dataset import create_from_parcel_and_development_template
from numpy import array, int32
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    ACRE = 43560
    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='development_templates',
            table_data={
                'template_id': array([1,2,3]),
                'building_type_id': array([1, 1, 2]),
                "density_type":  array(['units_per_acre', 'units_per_acre', 'far']),                
                'density':array([0.6, 2.0, 10]),
                'percent_land_overhead':array([0, 10, 20]),
                'land_sqft_min': array([0, 10, 4],dtype=int32) * self.ACRE,
                'land_sqft_max': array([2, 20, 8],dtype=int32) * self.ACRE
            }
        )
        storage.write_table(
            table_name='development_template_components',
            table_data={
                'template_id': array([1,1,2,3,3,3]),
                'component_id': arange(6)+1
            }
        )
        storage.write_table(
            table_name='parcels',
            table_data={
                "parcel_id": array([1,   2,    3]),
                "vacant_land_area": array([1, 50,  200],dtype=int32)* self.ACRE,
            }
        )
        storage.write_table(
            table_name='development_project_proposal_components',
            table_data={
                "proposal_component_id": arange(14)+1,
                "proposal_id":array([1,  1, 2, 3, 3,3, 5,  6, 6,6,   8, 9, 9,9]),
                "template_id":array([1,  1, 2, 3, 3,3, 2,  3, 3,3,   2, 3,3,3]),
                "component_id": array([1,2,3,4,5,6, 3,4,5,6,3,4,5,6])
            }
        )

        self.dataset_pool = DatasetPool(package_order=['urbansim_parcel'],
                                   storage=storage)
        parcels = self.dataset_pool.get_dataset('parcel')
        templates = self.dataset_pool.get_dataset('development_template')
        template_components = self.dataset_pool.get_dataset('development_template_component')
        proposals = create_from_parcel_and_development_template(parcels, templates, 
                                                                dataset_pool=self.dataset_pool, resources=None)
        self.proposal_components = create_from_proposals_and_template_components(proposals, template_components)

    def test_create(self):
        proposals_components = self.dataset_pool.get_dataset("development_project_proposal_component")
        template_ids = self.proposal_components.get_attribute("template_id")
        
        self.assertTrue(ma.allequal(self.proposal_components.size(), proposals_components.size()))
        self.assertTrue(self.proposal_components.get_attribute("proposal_id").sum(), proposals_components.get_attribute("proposal_id").sum())
        self.assertTrue((template_ids==1).sum(), (proposals_components.get_attribute("template_id")==1).sum())
        self.assertTrue((template_ids==2).sum(), (proposals_components.get_attribute("template_id")==2).sum())
        self.assertTrue((template_ids==3).sum(), (proposals_components.get_attribute("template_id")==3).sum())
        self.assertTrue(self.proposal_components.get_attribute("component_id").sum(), proposals_components.get_attribute("component_id").sum())

if __name__=='__main__':
    opus_unittest.main()