# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from urbansim.datasets.dataset import Dataset as UrbansimDataset
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.storage_factory import StorageFactory
from opus_core.resources import Resources
from opus_core.variables.variable_name import VariableName
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset_pool import DatasetPool
from opus_core.misc import unique_values, DebugPrinter
from opus_core.logger import logger
from numpy import arange, where, resize, zeros, array, logical_and, logical_or, concatenate, ones

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
    id_refused = 6
    id_with_velocity = 7
    
    def __init__(self, resources=None, dataset1=None, dataset2=None, index1=None, index2=None, **kwargs):
        """ This dataset is an interaction of two datasets (originally, parcel and development template).
            It's similar to InteractionSet, but flattend to 1d, thus regression model can use this dataset without changes
        """
        UrbansimDataset.__init__(self, resources=resources, **kwargs)
        self._set_my_class_attributes(dataset1, dataset2, index1, index2)

    def _set_my_class_attributes(self, dataset1=None, dataset2=None, index1=None, index2=None):
        if dataset1 is not None:
            self.dataset1 = dataset1
        if dataset2 is not None:
            self.dataset2 = dataset2
        if index1 is not None:
            self.index1 = index1
        if index2 is not None:
            self.index2 = index2
        
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
                                variable_name.get_expression())
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
                                                parcel_index=None,
                                                template_index=None,
                                                filter_attribute=None,
                                                consider_constraints_as_rules=True,
                                                template_opus_path="urbansim_parcel.development_template",
                                                dataset_pool=None,
                                                resources=None):
    """create development project proposals from parcel and development_template_dataset,
    parcel_index - 1D array, indices of parcel_dataset. Status of the proposals is set to 'tentative'.
    template_index - index to templates that are available to create proposals;
    filter_attribute - variable that is used to filter proposals;
    
    If a development constraint table exists, create proposal dataset include only proposals that are allowed by constraints,
    otherwise, create a proposal dataset with Cartesian product of parcels x templates 
    """

    resources = Resources(resources)
    debug = resources.get("debug",  0)
    if not isinstance(debug, DebugPrinter):
        debug = DebugPrinter(debug)

    if parcel_index is not None and parcel_index.size <= 0:
        logger.log_warning("parcel index for creating development proposals is of size 0. No proposals will be created.")
        return None
        
    storage = StorageFactory().get_storage('dict_storage')
    current_year = SimulationState().get_current_time()
    
    def _get_data(parcel_ids, template_ids):
        return {
                "proposal_id": arange(1, parcel_ids.size+1, 1),
                "parcel_id" : parcel_ids,
                "template_id": template_ids,
                "start_year": array(parcel_ids.size*[current_year]),
                "status_id": resize(array([DevelopmentProjectProposalDataset.id_tentative], dtype="int16"), 
                    parcel_ids.size)
                }
        
    def _create_project_proposals(parcel_ids, template_ids):
        storage.write_table(table_name='development_project_proposals',
            table_data = _get_data(parcel_ids, template_ids)
            )
        development_project_proposals = DevelopmentProjectProposalDataset(resources=Resources(resources),
                                                                          dataset1 = parcel_dataset,
                                                                          dataset2 = development_template_dataset,
                                                                          index1 = parcel_index,
                                                                          index2 = template_index,
                                                                          in_storage=storage,
                                                                          in_table_name='development_project_proposals',
                                                                          )
        return development_project_proposals
    
    def _compute_filter(proposals):
        if filter_attribute is not None:
            proposals.compute_variables(filter_attribute, dataset_pool=dataset_pool,
                                                          resources=Resources(resources))
            filter_index = where(proposals.get_attribute(filter_attribute) > 0)[0]
            return filter_index
        return None
    
    def _subset_by_filter(proposals):
        filter_index = _compute_filter(proposals)
        if filter_index is not None:
            proposals.subset_by_index(filter_index, flush_attributes_if_not_loaded=False)
        return proposals


    if parcel_index is not None:
        index1 = parcel_index
    else:
        index1 = arange(parcel_dataset.size())

    if template_index is not None:
        index2 = template_index
    else:
        index2 = arange(development_template_dataset.size())

    has_constraint_dataset = True
    try:
        constraints = dataset_pool.get_dataset("development_constraint") 
        constraints.load_dataset_if_not_loaded()
    except:
        has_constraint_dataset = False

    if has_constraint_dataset:
        constraint_types = unique_values(constraints.get_attribute("constraint_type"))  #unit_per_acre, far etc
        development_template_dataset.compute_variables(map(lambda x: "%s.%s" % (template_opus_path, x), constraint_types), dataset_pool)
            
        parcel_dataset.get_development_constraints(constraints, dataset_pool, 
                                                   index=index1, 
                                                   consider_constraints_as_rules=consider_constraints_as_rules)
        generic_land_use_type_ids = development_template_dataset.compute_variables("urbansim_parcel.development_template.generic_land_use_type_id",
                                                       dataset_pool=dataset_pool)
    parcel_ids = parcel_dataset.get_id_attribute()
    template_ids = development_template_dataset.get_id_attribute()
    
    proposal_parcel_ids = array([],dtype="int32")
    proposal_template_ids = array([],dtype="int32")
    logger.start_block("Combine parcels, templates and constraints")
    for i_template in index2:
        this_template_id = template_ids[i_template]
        fit_indicator = ones(index1.size, dtype="bool8")
        if has_constraint_dataset:
            generic_land_use_type_id = generic_land_use_type_ids[i_template]
            for constraint_type, constraint in parcel_dataset.development_constraints[generic_land_use_type_id].iteritems():
                template_attribute = development_template_dataset.get_attribute(constraint_type)[i_template]  #density converted to constraint variable name
                if template_attribute == 0:
                    continue
                min_constraint = constraint[:, 0].copy()
                max_constraint = constraint[:, 1].copy()
                ## treat -1 as unconstrainted
                w_unconstr = min_constraint == -1
                if w_unconstr.any():
                    min_constraint[w_unconstr] = template_attribute
                
                w_unconstr = max_constraint == -1
                if w_unconstr.any():
                    max_constraint[w_unconstr] = template_attribute

                fit_indicator = logical_and(fit_indicator, 
                                            logical_and(template_attribute >= min_constraint,
                                                        template_attribute <= max_constraint))
                

                if constraint_type == "units_per_acre":
                    res_units_capacity = parcel_dataset.get_attribute("parcel_sqft")[index1] * max_constraint / 43560.0 
                    debug.print_debug("template_id %s (GLU ID %s) max total residential capacity %s, %s of them fit constraints " % (this_template_id, generic_land_use_type_id, res_units_capacity.sum(), (res_units_capacity * fit_indicator).sum() ), 12)
                else:
                    non_res_capacity = parcel_dataset.get_attribute("parcel_sqft")[index1] * max_constraint
                    debug.print_debug("template_id %s (GLU ID %s) max total non residential capacity %s, %s of them fit constraints " % (this_template_id, generic_land_use_type_id, non_res_capacity.sum(), (non_res_capacity * fit_indicator).sum() ), 12)
                
        proposal_parcel_ids = concatenate((proposal_parcel_ids, parcel_ids[index1[fit_indicator]]))
        proposal_template_ids = concatenate( (proposal_template_ids, resize(array([this_template_id]), fit_indicator.sum())))
        
    logger.end_block()
    proposals = _create_project_proposals(proposal_parcel_ids, proposal_template_ids)
    proposals = _subset_by_filter(proposals)

    # eliminate proposals with zero units_proposed
    units_proposed = proposals.compute_variables(["urbansim_parcel.development_project_proposal.units_proposed"],
                                                 dataset_pool = dataset_pool)
    where_up_greater_zero = where(units_proposed > 0)[0]
    if where_up_greater_zero.size > 0:
        proposals.subset_by_index(where_up_greater_zero, flush_attributes_if_not_loaded=False)
    
    logger.log_status("proposal set created with %s proposals." % proposals.size())
    #proposals.flush_dataset_if_low_memory_mode()
    return proposals
    
from opus_core.tests import opus_unittest
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import array, int32
from numpy import ma

class Tests(opus_unittest.OpusTestCase):
    ACRE = 43560
    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(
            table_name='development_templates',
            table_data={
                'template_id': array([1,2,3,4]),
                'project_size': array([0, 1999, 2000, 10]),
                'building_type_id': array([1, 1, 2, 3]),
                "density_type":  array(['units_per_acre', 'units_per_acre', 'far',  'units_per_acre']),                
                'density':array([0.6, 2.0, 10, 5]),
                'percent_land_overhead':array([0, 10, 0, 20]),
                'land_sqft_min': array([0, 10, 4, 30],dtype=int32) * self.ACRE,
                'land_sqft_max': array([2, 20, 8, 100],dtype=int32) * self.ACRE
            }
        )
        storage.write_table(
            table_name='parcels',
            table_data={
                "parcel_id": array([1,   2,    3]),
                "lot_size":  array([0,   2005, 23]),
                "vacant_land_area": array([1, 50,  200],dtype=int32)* self.ACRE,
            }
        )
        storage.write_table(
            table_name='development_project_proposals',
            table_data={
                "proposal_id":array([1,  2,  3,  4, 5,  6, 7, 8, 9, 10, 11, 12]),
                "parcel_id":  array([1,  2,  3,  1, 2, 3,  1, 2, 3, 1, 2, 3 ]),
                "template_id":array([1,  1,  1,  2, 2, 2,  3, 3, 3, 4, 4, 4]),
                "units_proposed": array([1, 1, 1, 0, 36, 36, 0, 3484800, 3484800,0, 200, 400])
            }
        )

        self.dataset_pool = DatasetPool(package_order=['urbansim_parcel', 'urbansim'],
                                   storage=storage)
        parcels = self.dataset_pool.get_dataset('parcel')
        templates = self.dataset_pool.get_dataset('development_template')
        self.dataset = create_from_parcel_and_development_template(parcels, templates, dataset_pool=self.dataset_pool,
                                                                   resources=None)

    def test_create(self):
        proposals = self.dataset_pool.get_dataset("development_project_proposal")
        where_valid_units = where(proposals.get_attribute("units_proposed") > 0)[0]
        self.assert_(ma.allequal(self.dataset.get_id_attribute(), proposals.get_id_attribute()[where_valid_units]))
        self.assert_(ma.allequal(self.dataset.get_attribute("parcel_id"), 
                                 proposals.get_attribute("parcel_id")[where_valid_units]))
        self.assert_(ma.allequal(self.dataset.get_attribute("template_id"), 
                                 proposals.get_attribute("template_id")[where_valid_units]))


    def test_compute(self):

        self.dataset.compute_variables("development_template.project_size",
                              dataset_pool=self.dataset_pool)
        values = self.dataset.get_attribute("project_size")
        should_be = array([0, 0,  0, 1999,  1999, 2000, 2000, 10, 10])
        
        self.assert_(ma.allequal( values, should_be),
                     msg = "Error in " + "development_template.project_size")

        self.dataset.compute_variables("parcel.lot_size",
                              dataset_pool=self.dataset_pool)
        values = self.dataset.get_attribute("lot_size")
        #should_be = array([0, 0,  0, 0,  2005, 2005,2005,2005, 23, 23, 23, 23])
        should_be = array([0, 2005, 23, 2005, 23,  2005, 23, 2005, 23])        
        self.assert_(ma.allequal( values, should_be),
                     msg = "Error in " + "parcel.lot_size")


if __name__=='__main__':
    opus_unittest.main()
