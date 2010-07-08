# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.choice_model import ChoiceModel
from opus_core.specified_coefficients import SpecifiedCoefficients, SpecifiedCoefficientsFor1Submodel
from opus_core.datasets.dataset import Dataset, DatasetSubset
from opus_core.variables.variable_name import VariableName
from numpy import indices, int16, array, ones, put, repeat, arange, zeros
from numpy import float32, where, log, int8
from opus_core.logger import logger

class LandCoverChangeModel(ChoiceModel):
    def __init__(self, choice_set, utilities="opus_core.linear_utilities",
                    probabilities="opus_core.mnl_probabilities",
                    choices="opus_core.random_choices",
                    interaction_pkg="biocomplexity.datasets",
                    submodel_string="lct",
                    choice_attribute_name="lct",
                    run_config=None, estimate_config=None,
                    debuglevel=0):
        self.choice_attribute_name = VariableName(choice_attribute_name)
        ChoiceModel.__init__(self, choice_set=choice_set, utilities=utilities,
                probabilities=probabilities, choices=choices,
                submodel_string=submodel_string,
                interaction_pkg=interaction_pkg,
                choice_attribute_name=self.choice_attribute_name.get_alias(),
                run_config=run_config, estimate_config=estimate_config,
                debuglevel=debuglevel)

    def run(self, specification, coefficients, agent_set,
            agents_index=None, chunk_specification=None,
            data_objects=None, run_config=None, debuglevel=0):
        self.lct_probabilities = {}
        for ichoice in range(self.choice_set.size()):
            probname = "probs_" + str(self.choice_set.get_id_attribute()[ichoice])
            if  probname not in agent_set.get_known_attribute_names():
                agent_set.add_attribute(name=probname, data=zeros(agent_set.size(), dtype=float32))
        result = ChoiceModel.run(self,specification, coefficients, agent_set,
                agents_index=agents_index, chunk_specification=chunk_specification,
                data_objects=data_objects, run_config=run_config,
                debuglevel=debuglevel)
        ## next four lines creates recoded lct (shifts index)....
        changed_idx = where(result>0)[0]
        if agents_index is None:
            agents_index = arange(agent_set.size())
        agent_set.modify_attribute(data=result[changed_idx].astype(int8),
                                    name=self.choice_attribute_name.get_alias(),
                                    index=agents_index[changed_idx]) ## <-------------- lct recode occurs here
        agent_set.compute_variables("biocomplexity.land_cover.lct_recoded")
        return result

    def run_chunk(self, index, agent_set, *args, **kwargs): # **kwargs hold EquationSpecification and Coefficients objects
        result = ChoiceModel.run_chunk(self, index, agent_set, *args, **kwargs) ## choice_model.py, Ln 159
        # store probabilities
#        logger.log_status("choice set size: %s" % self.choice_set.size())
        for ichoice in range(self.choice_set.size()):
            probname = "probs_" + str(self.choice_set.get_id_attribute()[ichoice])
            try: # because some problem (need to investigate it)
                agent_set.modify_attribute(name=probname, data=self.get_probabilities()[:,ichoice], index=index)
            except:
                logger.log_warning("Something wrong with probabilities for choice %s" % self.choice_set.get_id_attribute()[ichoice])
        return result

    def estimate(self, specification, agent_set_year1, agent_set_year2, agents_index=None,
                  procedure="opus_core.bhhh_mnl_estimation", calibrate_constants=False,
                  data_objects=None, estimate_config=None, debuglevel=0):
        """Set calibrate_constants to True only if agent_set_year1 is the full dataset. Otherwise,
        the calibration can be done separately by calling the method "calibrate" with the full dataset.
        """
        if self.choice_attribute_name.get_alias() not in agent_set_year2.get_known_attribute_names():
            agent_set_year2.compute_variables([self.choice_attribute_name])
        if self.submodel_string not in agent_set_year1.get_known_attribute_names():
            agent_set_year1.compute_variables([self.submodel_string])
        lct_y2 = agent_set_year2.get_attribute(self.choice_attribute_name)
        attributes_switched = False
        if self.submodel_string == self.choice_attribute_name.get_alias():
            new_submodel_string = self.choice_attribute_name.get_alias() + "_start"
            original_submodel_string = self.submodel_string
            agent_set_year1.add_attribute(name=new_submodel_string,
                                 data=agent_set_year1.get_attribute(original_submodel_string).astype(int16))
            agent_set_year1.add_attribute(name=original_submodel_string, data=lct_y2.astype(int16))
            self.submodel_string = new_submodel_string
            attributes_switched = True
        self.specification = specification
        results =  ChoiceModel.estimate(self,specification, agent_set_year1,
                agents_index, procedure, data_objects, estimate_config, debuglevel=debuglevel)
        if calibrate_constants:
            self.calibrate(agent_set_year1, agent_set_year2, agents_index)
        if attributes_switched:
            agent_set_year1.add_attribute(name=self.choice_attribute_name.get_alias() + "_end",
                                           data=agent_set_year1.get_attribute(self.choice_attribute_name))
            agent_set_year1.add_attribute(name=original_submodel_string,
                                           data=agent_set_year1.get_attribute(new_submodel_string))
            agent_set_year1.delete_one_attribute(new_submodel_string)
        return self.coefficients, results[1]

    def get_choice_index_for_estimation(self, agent_set, agents_index=None,
                                         agent_subset=None, submodels=[1]):
        # need to work on this - return indicies of filtered choices
        nchoices = self.get_choice_set_size()
        index = (-1*ones((agents_index.size, nchoices))).astype("int32")
        self.selected_choice = zeros((agents_index.size,), dtype="int32")
        for submodel in submodels:
            if self.observations_mapping[submodel].size > 0:
                eqs = self.specification.get_equations_for_submodel(submodel).astype(int16)
                idx = self.choice_set.get_id_index(eqs)
                for i in arange(idx.size):
                    index[self.observations_mapping[submodel],i] = idx[i]
                selchoice = agent_set.get_attribute_by_index(self.choice_attribute_name,
                                                             agents_index[self.observations_mapping[submodel]])
                self.selected_choice[self.observations_mapping[submodel]] = \
                       self.choice_set.get_id_index(selchoice)
        return index

    def get_calibration_constants(self, agent_set1, agent_set2, agents_index):
        if agents_index is None:
            agents_index = arange(agent_set1.size())

        self.specified_coefficients = self.get_specified_coefficients() # used to pull coefficients used in estimation
        submodels = self.specified_coefficients.get_submodels()
        choices = self.choice_set.get_id_attribute()
        result = zeros((len(submodels),len(choices)), dtype=float32)
        if self.choice_attribute_name.get_alias() not in agent_set1.get_known_attribute_names():
            agent_set1.compute_variables([self.choice_attribute_name])
        if self.choice_attribute_name.get_alias() not in agent_set2.get_known_attribute_names():
            agent_set2.compute_variables([self.choice_attribute_name])
        for isubmodel in range(len(submodels)):
            spec_coef = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients, submodels[isubmodel])
            agents_in_subset_idx = agents_index[self.observations_mapping[submodels[isubmodel]]]
            all_agents_choices1 = agent_set1.get_attribute(self.choice_attribute_name)
            all_agents_choices2 = agent_set2.get_attribute(self.choice_attribute_name)
            all_agents_choices = all_agents_choices2[all_agents_choices1 == submodels[isubmodel]]
            agents_choices = all_agents_choices2[agents_in_subset_idx]
            for ichoice in range(len(choices)):
                if ichoice in spec_coef.get_equations_index(): ## returns full set of choices  - leave 
                    ## uncommented if line 464-5 in spec_coeffs.py are uncommented
                    ## comment and uncomment subsequent if..then in lines 464-5 are commented
                    ## because we want only those corresponding to choices in spec.py - see following line 
#                if ichoice in spec_coef.get_non_zero_equations(): ## new method to pull only those submodels specified by spec.py file
                    n = where(agents_choices == choices[ichoice])[0].size
                    if n > 0:
                        m = where(all_agents_choices == choices[ichoice])[0].size
                        result[isubmodel,ichoice]=log((m/float(all_agents_choices.size))/(n/float(agents_in_subset_idx.size)))
        return result

    def calibrate(self, agent_set1, agent_set2, agents_index):
        calibration_constants = self.get_calibration_constants(agent_set1, agent_set2,
                                                                agents_index)
#        print calibration_constants
        self.specified_coefficients.add_calibration_constants(calibration_constants)
        self.coefficients.fill_coefficients(self.specified_coefficients)
        return self.coefficients

    def simulate_submodel(self, data, coefficients, submodel=0):
        result = ChoiceModel.simulate_submodel(self, data, coefficients, submodel)
        self.lct_probabilities[submodel] = self.upc_sequence.get_probabilities()
        return result

    def get_probabilities(self):
        result = zeros((self.observations_mapping["index"].size,self.choice_set.size()), dtype=float32)
        self.specified_coefficients = self.get_specified_coefficients() # used to pull coefficients used in estimation
        for submodel in self.lct_probabilities.keys():
            coef = SpecifiedCoefficientsFor1Submodel(self.specified_coefficients,submodel)
            index = coef.get_equations_index()
            for i in range(index.size):
                result[self.observations_mapping[submodel], index[i]] = self.lct_probabilities[submodel][:,i]
        return result
