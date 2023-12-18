# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from numpy import zeros, concatenate, array, where, ndarray, sort, ones, all,empty, isnan, isinf, asarray
from opus_core.misc import unique
from opus_core.models.choice_model import ChoiceModel
from opus_core.samplers.constants import NO_STRATUM_ID
from opus_core.logger import logger

class HierarchicalChoiceModel(ChoiceModel):
    """ Choice model with hierarchical structure, such as nested logit."""
    
    model_name = "Hierarchical Choice Model"
    model_short_name ="HChoiceM"
    nest_id_name = "nest_id"

    def __init__(self, choice_set, nested_structure=None, stratum=None, **kwargs):
        """'nested_structure' is a dictionary with keys being the nest identifiers and each value being
        a list of identifiers of the elemental alternatives belonging to that nest.
        'stratum' is either a string giving the name of variable/expression determining 
        the membership of choice's elements to nests. Or, it is an array of the size as choice set
        giving directly the membership of choice's elements to nests.
        Either 'nested_structure' or 'stratum' must be given.
        All arguments of the Choice Model can be used.
        """
        ChoiceModel.__init__(self, choice_set, **kwargs)
        self.create_nested_and_tree_structure(nested_structure, stratum, **kwargs)
        self.set_model_interaction(**kwargs)
        
    def set_choice_set_size(self, **kwargs):
        if self.sampler_size is None:
            self.sampler_size = 0
            for nest, values in self.nested_structure.items():
                self.sampler_size += len(values)
        ChoiceModel.set_choice_set_size(self, **kwargs)
        
    def get_number_of_elemental_alternatives(self):
        return self.membership_in_nests[0].shape[1]
        
    def create_nested_and_tree_structure(self, nested_structure=None, stratum=None, **kwargs):
        strat = stratum
        if isinstance(strat, str):
            strat = self.choice_set.compute_variables(strat, dataset_pool=self.dataset_pool)
        elif strat is not None:
            strat = array(strat)
            
        if strat is not None:
            strat[strat<=0] = NO_STRATUM_ID # valid stratum must be larger than 0
        if nested_structure is None:
            if strat is None:
                raise Exception("Either 'nested_structure' or 'stratum' must be given.")
            sampler_size = None
            if self.sampler_class is not None:
                sampler_size = self.sampler_size
            self.nested_structure = create_nested_structure_from_list(strat, self.choice_set, sampler_size, 
                                                                      valid_strata_larger_than=NO_STRATUM_ID)
        else:
            self.nested_structure = nested_structure
            if self.sampler_class is not None and self.sampler_size is not None:
                for nest, values in self.nested_structure.items():
                    self.nested_structure[nest] = values[0:self.sampler_size]

        self.number_of_nests = len(self.nested_structure)
                
        if strat is None:
            strat = create_stratum_from_nests(self.nested_structure, self.choice_set)
        if self.estimate_config.get('stratum', None) is None:
            self.estimate_config['stratum'] = strat
        if self.run_config.get('stratum', None) is None:
            self.run_config['stratum'] = strat
        # Uncomment the following line when the stratified sampler can handle an array for sample_size_from_each_stratum.
        # Right now it can handle only single number.
        #sample_size_for_each_stratum = array(map(lambda x: len(self.nested_structure[x]), self.nested_structure.keys()))
        sample_size_for_each_stratum = len(self.nested_structure[list(self.nested_structure.keys())[0]])
        if self.estimate_config.get("sample_size_from_each_stratum", None) is None:
            self.estimate_config["sample_size_from_each_stratum"] = sample_size_for_each_stratum
        if self.run_config.get("sample_size_from_each_stratum", None) is None:
            self.run_config["sample_size_from_each_stratum"] = sample_size_for_each_stratum
        
    def init_membership_in_nests(self):
        self.membership_in_nests = create_tree_structure_from_dict(self.nested_structure)
        self.estimate_config['membership_in_nests'] = self.membership_in_nests
        self.run_config['membership_in_nests'] = self.membership_in_nests
        
    def set_model_interaction(self, **kwargs):
        self.model_interaction = ModelInteractionHM(self, kwargs.get('interaction_pkg',"opus_core"), self.choice_set)
        
    def run_chunk(self, agents_index, agent_set, specification, coefficients):
        self.add_logsum_to_specification(specification, coefficients)
        self.init_membership_in_nests()
        return ChoiceModel.run_chunk(self, agents_index, agent_set, specification, coefficients)
    
    def estimate(self, specification, *args, **kwargs):
        self.init_membership_in_nests()
        # This is because there will be __logsum_ variables in the specification when configured from the GUI,
        # in order to define starting values. They are not supposed to be included there.
        self.delete_logsum_from_specification(specification)
        return ChoiceModel.estimate(self, specification, *args, **kwargs)
    
    def add_logsum_to_specification(self, specification, coefficients):
        idx = where(array([x.startswith('__logsum_') for x in coefficients.get_names()]))[0]
        if specification.get_equations().size > 0:
            eqid = min(specification.get_equations())
        else:
            eqid = None
        for i in idx:
            submodel = None
            if coefficients.get_submodels().size > 0:
                submodel = coefficients.get_submodels()[i]
            specification.add_item('__logsum', coefficients.get_names()[i], submodel=submodel,
                                   equation = eqid, other_fields={'dim_%s' % self.nest_id_name: int(coefficients.get_names()[i][9:])})
            
    def delete_logsum_from_specification(self, specification):
        variable_names = specification.get_variable_names()
        idx = where(array([x.startswith('__logsum_') for x in variable_names]))[0]
        specification.delete(variable_names[idx])
        
    def run_sampler_class(self, agent_set, index1=None, index2=None, sample_size=None, weight=None, 
                          include_chosen_choice=False, resources=None):
        index, chosen_choice = self.sampler_class.run(agent_set, self.choice_set, index1=index1, index2=index2, sample_size=sample_size,
                                      weight=weight, include_chosen_choice=include_chosen_choice, resources=resources)
        if 'get_sampled_stratum' not in dir(self.sampler_class):
            return index, chosen_choice
        
        sampled_stratum = self.sampler_class.get_sampled_stratum()
        if not is_same_for_all_agents(sampled_stratum):           
            self.membership_in_nests = create_3D_tree_structure_from_stratum(sampled_stratum, self.nested_structure)
            self.estimate_config['membership_in_nests'] = self.membership_in_nests
            self.run_config['membership_in_nests'] = self.membership_in_nests
        return index, chosen_choice
                    
    def estimate_step(self):
        self.set_correct_for_sampling()
        self.init_membership_in_nests()
        result = ChoiceModel.estimate_step(self)
        self.add_logsum_to_coefficients(result)
        return result
        
    def set_correct_for_sampling(self):
        if self.sampler_class is None:
            return
        self.estimate_config['correct_for_sampling'] = True
        stratum_sample_size = self.estimate_config["sample_size_from_each_stratum"]
        keys = sort(list(self.nested_structure.keys()))
        self.estimate_config["sampling_rate"] = ones(self.number_of_nests)
        self.estimate_config["keys"] = keys
        self.estimate_config["sampling_size"] = ones(self.number_of_nests)
        self.estimate_config["sampling_nest_size"] = ones(self.number_of_nests)
        self.estimate_config["stratum_id"] = self.sampler_class._stratum_id
        this_sample_size = stratum_sample_size
        for nest in range(self.number_of_nests):
            idx = where(self.estimate_config['stratum'] == keys[nest])[0]
            if isinstance(stratum_sample_size, ndarray):
                this_sample_size = stratum_sample_size[nest]
            self.estimate_config["sampling_rate"][nest] = this_sample_size/float(idx.size)
            self.estimate_config["sampling_size"][nest] = this_sample_size
            self.estimate_config["sampling_nest_size"][nest] = idx.size
            
    def add_logsum_to_coefficients(self, estimation_results):
        for submodel, res in estimation_results.items():
            idx = where(array([x.startswith('__logsum') for x in res['coefficient_names']]))[0]
            for i in idx:
                om = {}
                for om_name, om_values in res['other_measures'].items():
                    om[om_name]=om_values[i]
                self.coefficients.add_item(res['coefficient_names'][i], res['estimators'][i], 
                                       res['standard_errors'][i], submodel=submodel, 
                                       other_measures=om)
                
    def get_nested_structure(self):
        return self.nested_structure
    
    def get_all_data(self, submodel, nest=None):
        data = self.model_interaction.get_data(submodel)
        if nest is None:
            return data
        return data[:,:,:,self.model_interaction.specified_coefficients.other_dimensions_mapping['dim_%s' % self.nest_id_name][nest]]

    def simulate_chunk(self):
        """ Like ChoiceModel, but here we need to simulate probabilities directly in the submodel loop, 
         because the logsums are passed directly from utilities to probabilities.
         Does not work with availability and prices.
         """
        self.debug.print_debug("Compute variables ...",4)
        self.increment_current_status_piece()
        self.model_interaction.compute_variables()
        
        logger.log_status("Choice set size: %i" % self.get_choice_set_size())
        
        coef = {}
        index = self.run_config["index"]
        self.debug.print_debug("Simulate ...",4)
        choices = empty((self.observations_mapping["index"].size,), dtype='int32')

        for submodel in self.model_interaction.get_submodels():
            self.model_interaction.prepare_data_for_simulation(submodel)
            coef[submodel] = self.model_interaction.get_submodel_coefficients(submodel)
            self.coefficient_names[submodel] = self.model_interaction.get_variable_names_for_simulation(submodel)
            self.debug.print_debug("   submodel: %s   nobs: %s" % (submodel, self.observations_mapping[submodel].size), 5)
            self.increment_current_status_piece()
            if self.model_interaction.is_there_data(submodel): # observations for this submodel available
                self.run_config.merge({"specified_coefficients": coef[submodel]})
                coef_vals = coef[submodel].get_coefficient_values()
                coef_names = coef[submodel].get_coefficient_names()
                data = self.get_all_data(submodel)

                nan_index = where(isnan(data))[2]
                inf_index = where(isinf(data))[2]
                vnames = asarray(coef[submodel].get_variable_names())
                if nan_index.size > 0:
                    nan_var_index = unique(nan_index)
                    data = nan_to_num(data)
                    logger.log_warning("NaN(Not A Number) is returned from variable %s; it is replaced with %s." % (vnames[nan_var_index], nan_to_num(nan)))
                    #raise ValueError, "NaN(Not a Number) is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % vnames[nan_var_index]
                if inf_index.size > 0:
                    inf_var_index = unique(inf_index)
                    data = nan_to_num(data)
                    logger.log_warning("Inf is returned from variable %s; it is replaced with %s." % (vnames[inf_var_index], nan_to_num(inf)))                    
                    #raise ValueError, "Inf is returned from variable %s; check the model specification table and/or attribute values used in the computation for the variable." % vnames[inf_var_index]
                    
                choices[self.observations_mapping[submodel], :] = self.upc_sequence.run(data, coef_vals, resources=self.run_config)

        if self.run_config.get("export_simulation_data", False):
            self.export_probabilities(self.upc_sequence.probabilities, 
                                      self.run_config.get("simulation_data_file_name", './choice_model_data.txt'))
       
        if self.compute_demand_flag:
            self.compute_demand(self.upc_sequence.probabilities)

        return choices

from opus_core.choice_model import ModelInteraction
class ModelInteractionHM(ModelInteraction):
    def create_specified_coefficients(self, coefficients, specification, choice_ids=None):
        for nest, ids in self.model.nested_structure.items():
            specification.copy_equations_for_dim_if_needed(ids, 'dim_%s' % self.model.nest_id_name, nest)
        return ModelInteraction.create_specified_coefficients(self, coefficients, specification, choice_ids)
            

def create_tree_structure_from_dict(nested_structure):
    levels = 1
    tree_structure = {}
    ns = nested_structure
    while len(ns) > 0: # get number of levels from the first branch
        value = ns[list(ns.keys())[0]]
        if not isinstance(value, dict):
            break
        levels +=1
        ns = ns[list(ns.keys())[0]]
    if levels > 1:
        raise Exception("Support for nested structure with more than one level is not implemented.")
            
    ns = nested_structure
    lns = len(ns)
    current_ts_l = 0
    keys = sort(list(ns.keys()))
    for ins in range(lns):
        lchi = len(ns[keys[ins]])
        if tree_structure.get(current_ts_l, None) is None:
            tree_structure[current_ts_l] = zeros((lns, lchi), dtype='bool8')
        else:
            tree_structure[current_ts_l] = concatenate((tree_structure[current_ts_l], zeros((tree_structure[current_ts_l].shape[0], lchi), dtype='bool8')), axis=1)
        tree_structure[current_ts_l][ins, -lchi:] = True
            
    return tree_structure
    
def create_3D_tree_structure_from_stratum(stratum, nested_structure):
    result = {}
    current_ts_l = 0
    lns = len(nested_structure)
    keys = sort(list(nested_structure.keys()))
    result[current_ts_l] = zeros((stratum.shape[0], lns, stratum.shape[1]), dtype='bool8')
    for nest in range(lns):
        idx = where(stratum == keys[nest])
        result[current_ts_l][idx[0],nest,idx[1]] = 1
    return result
    
def create_nested_structure_from_list(stratum, choice_set, sampler_size=None, valid_strata_larger_than=None):
    nested_structure = {}
    values = choice_set.get_id_attribute()
    unique_v = sort(unique(stratum))
    if valid_strata_larger_than is not None:
        unique_v = unique_v[where(unique_v>valid_strata_larger_than)]
    count=1
    choice_ids = choice_set.get_id_attribute()
    for nest in unique_v:
        w = where(stratum == nest)[0]
        if sampler_size is not None:
            c = min(w.size, sampler_size)
            nested_structure[nest] = list(range(count, count+c))
            count += c
        else:
            nested_structure[nest] = choice_ids[w]
        
    return nested_structure
        
def create_stratum_from_nests(nested_structure, choice_set):
    result = zeros(choice_set.size())
    for nest, values in nested_structure.items():
        for v in values:
            result[where(result == v)] = nest
    return result
    
def is_same_for_all_agents(stratum):
    for i in range(stratum.shape[1]):
        if not all(stratum[:,i] == stratum[0,i]):
            return False
    return True
    
from opus_core.tests import opus_unittest
from numpy import array
from numpy import ma
class HierarchicalChoiceModelTests(opus_unittest.OpusTestCase):
    def test_create_tree_structure_1level(self):
        nested_structure = {0: [1,2,3,4], 1: [5,6,7]}
        ts = create_tree_structure_from_dict(nested_structure)
        should_be = array([[1,1,1,1,0,0,0], [0,0,0,0,1,1,1]])
        self.assertTrue(ma.allequal(ts[0], should_be), "Error in test_create_tree_structure_1level.")

                
if __name__ == '__main__':
    opus_unittest.main()       
