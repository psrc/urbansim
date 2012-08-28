# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.datasets.dataset import DatasetSubset
from opus_core.regression_model import RegressionModel
from urbansim_parcel.datasets.development_project_proposal_dataset import DevelopmentProjectProposalDataset
from urbansim_parcel.datasets.development_project_proposal_dataset import create_from_parcel_and_development_template
from urbansim_parcel.datasets.development_project_proposal_component_dataset import create_from_proposals_and_template_components
from numpy import exp, arange, logical_and, zeros, ones, where, array, float32, int16, int32, concatenate, inf, in1d
from opus_core.variables.attribute_type import AttributeType
from opus_core.logger import logger
import re

class DevelopmentProjectProposalRegressionModel(RegressionModel):
    """Generic regression model on development project proposal dataset
    """
    model_name = "Development Project Proposal Regression Model"
    model_short_name = "PDPRM"
    outcome_attribute_name = "regression_result"
    defalult_value = array([0], dtype="int32")  
    # or defalult_value = 0.0, use 1 element array to control the type of the outcome attribute
    
    def __init__(self, regression_procedure="opus_core.linear_regression", 
                 filter_attribute=None,
                 submodel_string="building_type_id", 
                 outcome_attribute_name=None,
                 model_name=None,
                 model_short_name=None,
                 run_config=None, 
                 estimate_config=None, 
                 debuglevel=0, dataset_pool=None):
        self.filter = filter_attribute
        if model_name is not None:
            self.model_name = model_name
        if model_short_name is not None:
            self.model_short_name = model_short_name
        if outcome_attribute_name is not None:
            self.outcome_attribute_name = outcome_attribute_name
        
        RegressionModel.__init__(self, 
                                 regression_procedure=regression_procedure, 
                                 submodel_string=submodel_string, 
                                 run_config=run_config, 
                                 estimate_config=estimate_config, 
                                 debuglevel=debuglevel, dataset_pool=dataset_pool)
                    
    def run(self, specification, coefficients, dataset, index=None, chunk_specification=None, 
             data_objects=None, run_config=None, debuglevel=0):
        """ For info on the arguments see RegressionModel.
        dataset should be an instance of DevelopmentProjectProposalDataset, if it isn't,
        create dataset on the fly with parcel and development template
        index and self.filter_attribute (passed in __init___) are relative to dataset
        """
        if data_objects is not None:
            self.dataset_pool.add_datasets_if_not_included(data_objects)
        proposal_component_set = create_from_proposals_and_template_components(dataset, 
                                                           self.dataset_pool.get_dataset('development_template_component'))
        
        self.dataset_pool.replace_dataset(proposal_component_set.get_dataset_name(), proposal_component_set)
        #proposal_component_set.flush_dataset_if_low_memory_mode()
        #dataset.flush_dataset_if_low_memory_mode()
        
        result = RegressionModel.run(self, specification, coefficients, dataset, 
                                         index=index, chunk_specification=chunk_specification, data_objects=data_objects,
                                         run_config=run_config, debuglevel=debuglevel)

        if re.search("^ln_", self.outcome_attribute_name): # if the outcome attr. name starts with 'ln_'
                                                           # the results will be exponentiated.
            self.outcome_attribute_name = self.outcome_attribute_name[3:len(self.outcome_attribute_name)]
            result = exp(result)

        if self.outcome_attribute_name not in dataset.get_known_attribute_names():
            dataset.add_primary_attribute(self.defalult_value + zeros(dataset.size()),
                                             self.outcome_attribute_name)
        
        dataset.set_values_of_one_attribute(self.outcome_attribute_name, 
                                                 result, index=index)
        self.correct_infinite_values(dataset, self.outcome_attribute_name)
        return dataset            
            
    def prepare_for_run(self, dataset_pool, 
                        create_proposal_set=True,
                        parcel_filter_for_new_development=None, 
                        parcel_filter_for_redevelopment=None, 
                        template_filter=None,
                        spec_replace_module_variable_pair=None,
                        proposed_units_variable="urbansim_parcel.development_project_proposal.units_proposed",
                        **kwargs):
        """create development project proposal dataset from parcels and development templates.
        spec_replace_module_variable_pair is a tuple with two elements: module name, variable within the module
        that contans a dictionary of model variables to be replaced in the specification.
        """
        specification, coefficients, dummy = RegressionModel.prepare_for_run(self, **kwargs)
        try:
            existing_proposal_set_parent = dataset_pool.get_dataset('development_project_proposal')
            if 'units_proposed' not in existing_proposal_set_parent.get_known_attribute_names():
                ## compute 'units_proposed' and add it as a primary attribute (as it may be missing when loaded from the base_year_data)
                units_proposed = existing_proposal_set_parent.compute_variables(proposed_units_variable, dataset_pool)
                existing_proposal_set_parent.add_attribute(units_proposed, "units_proposed", AttributeType.PRIMARY)
            
            #load proposals whose status_id are not of id_tentative or id_not_available
            available_idx = where(in1d(existing_proposal_set_parent.get_attribute("status_id"), 
                                       array([DevelopmentProjectProposalDataset.id_active,
                                              DevelopmentProjectProposalDataset.id_proposed,
                                              DevelopmentProjectProposalDataset.id_planned,
                                              DevelopmentProjectProposalDataset.id_with_velocity])))[0]
            existing_proposal_set = DatasetSubset(existing_proposal_set_parent, available_idx)
            # Code updated by Hanyi Li, MAG 6/8/2010
            # Replacing the cached 'development_project_proposal' dataset with
            # the filtered dataset 'existing_proposal_set'
            dataset_pool.replace_dataset(existing_proposal_set_parent.get_dataset_name(), existing_proposal_set)
        except:
            existing_proposal_set = None
        
        parcels = dataset_pool.get_dataset('parcel')
        templates = dataset_pool.get_dataset('development_template')

        # It is important that during this method no variable flushing happens, since
        # we create datasets of the same name for different purposes (new development and redevelopment)
        # and flushing would mix them up
        flush_variables_current = SimulationState().get_flush_datasets()
        SimulationState().set_flush_datasets(False)
        
        # Code added by Jesse Ayers, MAG, 9/14/2009
        # Getting an index of parcels that have actively developing projects (those on a velocity function)
        # and making sure that new proposals are not generated for them
        if existing_proposal_set and existing_proposal_set.size()>0:
            parcels_with_proposals = existing_proposal_set.get_attribute('parcel_id')
            parcels_with_proposals_idx = parcels.get_id_index(parcels_with_proposals)
            if parcel_filter_for_new_development is not None:
                if parcel_filter_for_new_development[parcel_filter_for_new_development.find('=')+1] == '=':
                    filter = 'flter = numpy.logical_and(parcel.number_of_agents(development_project_proposal) == 0, %s)' % parcel_filter_for_new_development
                else:
                    parcel_filter_for_new_development = parcel_filter_for_new_development[parcel_filter_for_new_development.find('=')+1:].lstrip()
                    filter = 'flter = numpy.logical_and(parcel.number_of_agents(development_project_proposal) == 0, %s)' % parcel_filter_for_new_development
                index1 = where(parcels.compute_variables(filter))[0]

        else:
            if parcel_filter_for_new_development is not None:
                index1 = where(parcels.compute_variables(parcel_filter_for_new_development))[0]
            else:
                index1 = None
            
        if template_filter is not None:
            try:
                index2 = where(templates.compute_variables(template_filter))[0]
            except Exception, e:
                logger.log_warning( "template_filter is set to %s, but there is an error when computing it: %s"
                                   % (template_filter, e) )
                index2 = None
        else:
            index2 = None
            
        if create_proposal_set:
            logger.start_block("Creating proposals for new development")
            proposal_set = create_from_parcel_and_development_template( parcels, templates, 
                                                              filter_attribute=self.filter,
                                                              parcel_index = index1,
                                                              template_index = index2,
                                                              proposed_units_variable=proposed_units_variable,
                                                              dataset_pool=dataset_pool,
                                                              resources = kwargs.get("resources", None) )
            proposal_set.add_attribute( zeros(proposal_set.size(), dtype=int16), "is_redevelopment", AttributeType.PRIMARY )
            # Line added by Jesse Ayers, MAG, 7/20/2009
            # adding a primary attribute to catch a later computation
            proposal_set.add_attribute( zeros(proposal_set.size(), dtype=int32), "total_land_area_taken", AttributeType.PRIMARY )
            logger.end_block()
            if parcel_filter_for_redevelopment is not None:
                logger.start_block("Creating proposals for re-development")
                buildings = dataset_pool.get_dataset('building')
                land_area = buildings.get_attribute("land_area").copy()
                parcels.compute_variables(parcel_filter_for_redevelopment, dataset_pool=dataset_pool)
                is_redevelopment = parcels.get_attribute( parcel_filter_for_redevelopment) > 0
                buildings_parcel_ids = buildings.get_attribute( "parcel_id" )
                index_in_parcels = parcels.get_id_index(buildings_parcel_ids)
                demolished_buildings_index = where(is_redevelopment[index_in_parcels])[0]                   
                buildings.set_values_of_one_attribute("land_area", zeros(demolished_buildings_index.size), 
                                                     index=demolished_buildings_index )
                redev_proposal_set = create_from_parcel_and_development_template(parcels, templates, 
                                                                  filter_attribute=self.filter,
                                                                  parcel_index = where(is_redevelopment)[0],
                                                                  template_index = index2,
                                                                  proposed_units_variable=proposed_units_variable,
                                                                  dataset_pool=dataset_pool,
                                                                  resources = kwargs.get("resources", None))
                
                if(kwargs.get('accept_only_larger_proposals_for_redevelopment', False)):
                    # remove proposals that are smaller than the current building in the parcel
                    remove_proposals = where(redev_proposal_set.compute_variables(['urbansim_parcel.development_project_proposal.building_sqft <= development_project_proposal.disaggregate(urbansim_parcel.parcel.building_sqft)'],
                                                         dataset_pool=dataset_pool))[0]
                    if remove_proposals.size > 0:
                        redev_proposal_set.remove_elements(remove_proposals)
                        logger.log_status('%s proposals smaller than existing buildings, therefore removed.' %  remove_proposals.size)
                redev_proposal_set.add_attribute( ones(redev_proposal_set.size(), dtype=int16), "is_redevelopment", AttributeType.PRIMARY)
                proposal_set.join_by_rows(redev_proposal_set, require_all_attributes=False, change_ids_if_not_unique=True)
                ###roll back land_area of buildings
                buildings.set_values_of_one_attribute("land_area", land_area[demolished_buildings_index], 
                                                     index=demolished_buildings_index )
                logger.end_block()
        
            if existing_proposal_set is not None and existing_proposal_set.size() > 0: # add existing proposals to the created ones
                proposal_set.join_by_rows(existing_proposal_set, require_all_attributes=False, change_ids_if_not_unique=True)
        else:
            proposal_set = existing_proposal_set
            proposal_set._set_my_class_attributes(parcels, templates, index1)
            
        dataset_pool.replace_dataset(proposal_set.get_dataset_name(), proposal_set)
        
        if spec_replace_module_variable_pair is not None:
            exec("from %s import %s as spec_replacement" % (spec_replace_module_variable_pair[0], 
                                                            spec_replace_module_variable_pair[1]))
            specification.replace_variables(spec_replacement)

        # switch flush_variables to the original value
        SimulationState().set_flush_datasets(flush_variables_current)
        return (proposal_set, specification, coefficients)
        
