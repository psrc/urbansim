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
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName

class DevelopmentProjectProposalDataset(UrbansimDataset):
    """ contains the proposed development projects, which is created from interaction of parcels with development template;
    it is defined as a child class of building dataset because the proposed development projects are supposed to update building dataset,
    which also allow this dataset to directly use model specification defined for parcels and buildings dataset
    """
    in_table_name_default = "development_project_proposals"
    out_table_name_default = "development_project_proposals"
    dataset_name = "development_project_proposal"
    id_name_default = "proposal_id"

    def __init__(self, resources=None, dataset1=None, dataset2=None, index1=None, **kwargs):
        """ This dataset is an interaction of two datasets (originally, parcel and development template).
            It's similar to InteractionSet, but flattend to 1d, thus regression model can use this dataset without changes
        """ 
        UrbansimDataset.__init__(self, resources=resources, **kwargs)
        if 'dataset1' is not None:
            self.dataset1 = dataset1
        if 'dataset2' is not None:
            self.dataset2 = dataset2
        if 'index1' is not None:
            self.index1 = index1

    def _compute_if_needed(self, name, dataset_pool, resources=None, quiet=False, version=None):
        """ Compute variable given by the argument 'name' only if this variable 
        has not been computed before. 
        Check first if this variable belongs to dataset1 or dataset2.
        dataset_pool holds available datasets.
        """
        if not isinstance(name, VariableName):
            variable_name = VariableName(name)
        else:
            variable_name = name
        short_name = variable_name.get_alias()

        dataset_name = variable_name.get_owner_dataset_name()
        if dataset_name == self.get_dataset_name():
            new_version = UrbansimDataset._compute_if_needed(self, variable_name, dataset_pool, resources, quiet=quiet, version=version)
        else:
            if dataset_name == self.dataset1.get_dataset_name():
                owner_dataset = self.dataset1
#                index = self.get_2d_index_of_dataset1()
            elif dataset_name == self.dataset2.get_dataset_name():
                owner_dataset = self.dataset2
#                index = self.get_2d_index()
            else:
                self._raise_error(StandardError, "Cannot find variable '%s'\nin either dataset or in the interaction set." % 
                                variable_name.get_full_name())
            new_version =  self.compute_variables_return_versions_and_final_value("%s = %s.disaggregate(%s)" % \
                                   (short_name, self.get_dataset_name(), 
                                    variable_name.get_full_name()
                                    ) )[0]
        return new_version
    
def create_from_parcel_and_development_template(parcel_dataset,
                                                development_template_dataset, 
                                                index=None, filter = None,                                                
                                                resources=None):
    """create development project proposals from parcel and development_template_dataset,
    index1 - 1D array, indices of parcel_dataset
    """

    interactionset = InteractionSet(dataset1=parcel_dataset, 
                                    dataset2=development_template_dataset, 
                                    index1=index)
        
    parcel_ids = interactionset.get_2d_dataset_attribute("parcel_id").flat
    template_ids = interactionset.get_2d_dataset_attribute("template_id").flat
        
    storage = StorageFactory().get_storage('dict_storage')        
    storage._write_dataset(out_table_name='development_project_proposals',
                           values = {
                               "proposal_id": arange(1, parcel_ids.size()+1, 1),
                               "parcel_id" : parcel_ids,
                               "template_id": template_ids,
                           }
                       )            
    development_project_proposals = DevelopmentProjectProposalDataset(resources=Resources(resources),
                                                                      dataset1 = parcel_dataset,
                                                                      dataset2 = development_template_dataset,
                                                                      in_storage=storage, 
                                                                      in_table_name='development_project_proposals',
                                                                      )
    if filter is not None:
            development_project_proposals.compute_variables(filter, resources=Resources(resources))
            filter_index = where(development_project_proposals.get_attribute(filter) > 0)[0]
            development_project_proposals.subset_by_index(filter_index, flush_attributes_if_not_loaded=False)

    return development_project_proposals