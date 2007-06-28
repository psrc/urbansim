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
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.logger import logger
from numpy import arange, where, resize

class DevelopmentProjectProposalDataset(UrbansimDataset):
    """ contains the proposed development projects, which is created from interaction of parcels with development template;
    it is defined as a child class of building dataset because the proposed development projects are supposed to update building dataset,
    which also allow this dataset to directly use model specification defined for parcels and buildings dataset
    """
    in_table_name_default = "development_project_proposals"
    out_table_name_default = "development_project_proposals"
    dataset_name = "development_project_proposal"
    id_name_default = "proposal_id"

    id_active = 1
    id_proposed = 2
    id_planned = 3
    id_tentative = 4
    id_not_available = 5
    
    def __init__(self, resources=None, dataset1=None, dataset2=None, index1=None, **kwargs):
        """ This dataset is an interaction of two datasets (originally, parcel and development template).
            It's similar to InteractionSet, but flattend to 1d, thus regression model can use this dataset without changes
        """
        UrbansimDataset.__init__(self, resources=resources, **kwargs)
        if dataset1 is not None:
            self.dataset1 = dataset1
        if dataset2 is not None:
            self.dataset2 = dataset2
        if index1 is not None:
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

        dataset_name = variable_name.get_dataset_name()
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
            owner_dataset.compute_variables([variable_name], dataset_pool, resources=resources, quiet=True)
            new_version =  self.compute_variables_return_versions_and_final_value("%s = %s.disaggregate(%s.%s)" % \
                                   ( short_name, self.get_dataset_name(), owner_dataset.get_dataset_name(), short_name ),
                                   dataset_pool=dataset_pool, resources=resources, quiet=quiet )[0]
        return new_version

    def _check_dataset_name(self, name):
        """check that name is the name of this dataset or one of its components"""
        if name!=self.get_dataset_name() and name!=self.dataset1.get_dataset_name() and name!=self.dataset2.get_dataset_name():
            raise ValueError, 'different dataset names for variable and dataset or a component'

    def create_and_check_qualified_variable_name(self, name):
        """Convert name to a VariableName if it isn't already, and add dataset_name to
        the VariableName if it is missing.  If it already has a dataset_name, make sure
        it is the same as the name of this dataset.
        """
        if isinstance(name, VariableName):
            vname = name
        else:
            vname = VariableName(name)
        if vname.get_dataset_name() is None:
            vname.set_dataset_name(self.get_dataset_name())
        else:
            self._check_dataset_name(vname.get_dataset_name())
            
        return vname
    
def create_from_parcel_and_development_template(parcel_dataset,
                                                development_template_dataset,
                                                index=None,
                                                filter_attribute=None,
                                                dataset_pool=None,
                                                resources=None):
    """create development project proposals from parcel and development_template_dataset,
    index1 - 1D array, indices of parcel_dataset. Status of the proposals is set to 'tentative'.
    """

    if index is not None and index.size <= 0:
        logger.log_warning("parcel index for creating development proposals is of size 0. No proposals will be created.")
        return None
    
    interactionset = InteractionDataset(dataset1=parcel_dataset,
                                    dataset2=development_template_dataset,
                                    index1=index)
    parcel_ids = interactionset.get_attribute("parcel_id").ravel()
    template_ids = interactionset.get_attribute("template_id").ravel()

    storage = StorageFactory().get_storage('dict_storage')
    storage.write_table(table_name='development_project_proposals',
        table_data={
            "proposal_id": arange(1, parcel_ids.size+1, 1),
            "parcel_id" : parcel_ids,
            "template_id": template_ids,
            "start_year": array(parcel_ids.size*[SimulationState().get_current_time(),]),
            "status_id": resize(array([DevelopmentProjectProposalDataset.id_tentative], dtype="int16"), 
                parcel_ids.size)
            }
        )
    development_project_proposals = DevelopmentProjectProposalDataset(resources=Resources(resources),
                                                                      dataset1 = parcel_dataset,
                                                                      dataset2 = development_template_dataset,
                                                                      index1 = index,
                                                                      in_storage=storage,
                                                                      in_table_name='development_project_proposals',
                                                                      )
    if filter_attribute is not None:
            development_project_proposals.compute_variables(filter_attribute, dataset_pool=dataset_pool,
                                                            resources=Resources(resources))
            filter_index = where(development_project_proposals.get_attribute(filter_attribute) > 0)[0]
            development_project_proposals.subset_by_index(filter_index, flush_attributes_if_not_loaded=False)

    return development_project_proposals

from opus_core.tests import opus_unittest
from opus_core.dataset_pool import DatasetPool
from numpy import array
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='development_templates',
            table_data={
                'template_id': array([1,2,3,4]),
                'project_size': array([0, 1999, 2000, 10]),
            }
        )
        storage.write_table(
            table_name='parcels',
            table_data={
                "parcel_id": array([1,   2,    3]),
                "lot_size":  array([0,   2005, 23])
            }
        )
        storage.write_table(
            table_name='development_project_proposals',
            table_data={
                "proposal_id":array([1,  2, 3,  4, 5,  6, 7, 8, 9, 10, 11, 12]),
                "parcel_id":  array([1,  1,  1,  1, 2, 2,  2, 2, 3, 3, 3, 3 ]),
                "template_id":array([1,  2, 3, 4,  1, 2,  3, 4, 1,  2, 3, 4])
            }
        )

        self.dataset_pool = DatasetPool(package_order=['urbansim_parcel'],
                                   storage=storage)
        parcels = self.dataset_pool.get_dataset('parcel')
        templates = self.dataset_pool.get_dataset('development_template')
        self.dataset = create_from_parcel_and_development_template(parcels, templates, resources=None)

    def test_create(self):
        proposals = self.dataset_pool.get_dataset("development_project_proposal")

        self.assert_(ma.allequal(self.dataset.get_id_attribute(), proposals.get_id_attribute()))
        self.assert_(ma.allequal(self.dataset.get_attribute("parcel_id"), proposals.get_attribute("parcel_id")))
        self.assert_(ma.allequal(self.dataset.get_attribute("template_id"), proposals.get_attribute("template_id")))


    def test_compute(self):

        self.dataset.compute_variables("development_template.project_size",
                              dataset_pool=self.dataset_pool)
        values = self.dataset.get_attribute("project_size")
        should_be = array([0, 1999, 2000, 10, 0, 1999, 2000, 10, 0, 1999, 2000, 10])
        self.assert_(ma.allequal( values, should_be),
                     msg = "Error in " + "development_template.project_size")

        self.dataset.compute_variables("parcel.lot_size",
                              dataset_pool=self.dataset_pool)
        values = self.dataset.get_attribute("lot_size")
        should_be = array([0, 0,  0, 0,  2005, 2005,2005,2005, 23, 23, 23, 23])
        self.assert_(ma.allequal( values, should_be),
                     msg = "Error in " + "parcel.lot_size")


if __name__=='__main__':
    opus_unittest.main()