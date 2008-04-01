#! /projects/urbansim/third-party/ActivePython/bin/python

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


import os,sys
from numarray import array, asarray, arange, concatenate, zeros, ones, \
             alltrue, sometrue, where, equal, less_equal, not_equal, nonzero, NumArray, \
             reshape, sum, cumsum, sort, searchsorted, NewAxis, Float64
from numarray.random_array import randint, seed, random
from opus.core.dataset import DataSet, AttributeMetaData
from opus.core.sampling_functions_new import *
from opus.core.miscellaneous import DebugPrinter

UNPLACED = 0.0

class SamplingToolbox:
    """Class for sampling individual and entity indices from opus.core.datasetset object"""
    
    def __init__(self, agent_set=None, random_seed=None, debuglevel=0):
        """
        agent_set - dataset object, required when sampling entities without running sampling_indivudal first,
          in this case, sampling_entity will sample entities for every agent in the agent dataset;
        random_seed - tuple to initialize random seed
        """
        
        self.sampled_individual_index = array([])  #index of sampled agents in agent_set
        self.sampled_choiceset_index = array([])      #2d index of sampled entities in entity dataset
        self.selected_choice = array([])           #2d matrix indicating if sampled_choiceset_index is selected
        self.sampling_prob = array([])             #TODO: sampling probability of each entity in stratified sampling
        self.agent_set = array([])
        self.choice_set = array([])
        self.N = 0                                 #number of sampled agents
        self.J = 0                                 #number of sampled choices

        self.debug = DebugPrinter(debuglevel)
        
        if random_seed is not None: seed(random_seed[0],random_seed[1])

        if agent_set is not None:
            if not isinstance(agent_set, DataSet):
                raise TypeError, "agent_set must be of type DataSet defined in core."
            self.agent_set = agent_set
            self.N = self.agent_set.size()
            self.sampled_individual_index = arange(self.agent_set.size())
    
    def sample_individuals(self, dataset, N=0, sampling_method='SRS', weight_array=None, strata_array=None, \
                  sample_size=1, sample_rate=None):
        """
        sample individuals from opus.core.dataset object with given sampling method and sample size

        dataset - dataset object to sample individuals from
        N - number of individuals to be sampled, if N < 0 or N greater than size of dataset, sample all dataset 
        sampling_method - string name for one of the implemented sampling methods, including
                  'SRS' for Simple Random Sampling,
                  'weighted'for weighted sampling, and
                  'stratified' for stratified sampling
        weight_array - required for weighted sampling, the array used to weight sampling, 
        strata_array - required for stratified sampling, the array used to defined stratum
        sample_size - used in stratified sampling, to specified how many individuals are sampled in each stratum
        sample_rate - used in stratified sampling, to specified the rate of sampling in each stratum
        """
        
        if not isinstance(dataset, DataSet):
            raise TypeError, "dataset must be of type DataSet defined in core."

        self.agent_set = dataset
        if self.agent_set.size() <= N:
            print 'Size of dataset %s is smaller than sample size %s, \
            return the indices for the whole population of individuals' % (self.agent_set.size(), N)
            self.sampled_individual_index = arange(self.agent_set.size())
            self.N = self.agent_set.size()
            return self.sampled_individual_index
        elif N < 0:
            print 'sample size < 0, return the indices for the whole population of individuals'
            self.sampled_individual_index = arange(self.agent_set.size())
            self.N = self.agent_set.size()
            return self.sampled_individual_index

        if sampling_method == 'SRS':
            self.sampled_individual_index = self.SRS_Sampling(self.agent_set, N)
            self.N = self.sampled_individual_index.size()
            return self.sampled_individual_index
        elif sampling_method == 'weighted':
            #weight_array = self.agent_set.get_attribute(weight_attribute)
            self.sampled_individual_index = self.Weighted_Sampling(self.agent_set, N, weight_array)
            self.N = self.sampled_individual_index.size()
            return self.sampled_individual_index
        elif sampling_method == 'stratified':
            #strata_array = self.agent_set.get_attribute(strata_attribute)
            #if weight_attribute is not None:
            #       weight_array = self.agent_set.get_attribute(weight_attribute)
            #else:
            #    weight_array = None
            self.sampled_individual_index = self.Stratified_Sampling(self.agent_set, strata_array, \
                                         sample_size=sample_size, sample_rate=sample_rate,\
                                         weight_array=weight_array)
            self.N = self.sampled_individual_index.size()
            return self.sampled_individual_index
        else:
            raise RuntimeWarning, "Unsupported Sampling Method: %s ." % sampling_method

    def sample_choiceset(self, choice_set, J=0, sampling_method='SRS', weight_array=None, strata_array=None, \
              sample_size=1, sample_rate=None):
        """
        sample choiceset from choice_set object for each individuals whose indices are in self.sampled_individual_index
        with given size of alternatives and sampling method

        choice_set - dataset object to sample alternatives (choices) set from
        J - number of alternatives to be sampled, current choice included.
        sampling_method - string name for one of the implemented sampling methods, including
                  'SRS' for Simple Random Sampling,
                  'weighted'for weighted sampling, and
                  'stratified' for stratified sampling
        weight_array - required for weighted sampling, the array used to weight sampling
        strata_array - required for stratified sampling, the array used to defined stratum
        sample_size - used in stratified sampling, to specified how many individuals are sampled in every stratum
        sample_rate - used in stratified sampling, to specified the rate of sampling in every stratum
        """
        
        
        if not isinstance(choice_set, DataSet):
            raise TypeError, "dataset must be of type DataSet defined in core."
        self.choice_set = choice_set
        
        if len(self.sampled_individual_index) == 0:
            raise RuntimeError, "Need to specify agent dataset before sample_choiceset.\n \
            please either specify agent_set in the class constructor or call sample_individuals method first. "

        assert self.sampled_individual_index.size() == self.N
            #raise RuntimeError, "Number of individuals sampled is inconsistent with sampled_individual_index. \
            #Need to specify individual dataset before sample_choiceset."
        
        for id_name in self.choice_set.get_id_name():
            if not ((id_name in self.agent_set.get_attribute_names()) or \
                    (id_name in self.agent_set.get_nonderived_attribute_names())):
                raise RuntimeError, "id_name of choice_set %s cannot be found in attribute_names of individual." \
                      % id_name
        
        if self.choice_set.size() <= J:
            raise RuntimeError, "number of entities %s is not enough to sample %s alternatives" % (self.choice_set.size(), J)
        elif J < 0:
            raise RuntimeError, "cannot sample less than 0 alternatives"

        if sampling_method == 'SRS':
            self.sampled_choiceset_index = self.Alt_SRS_Sampling(self.choice_set, J)
            self.J = self.sampled_choiceset_index.shape[1]
            return self.sampled_choiceset_index
        elif sampling_method == 'weighted':
            #weight_array = self.choice_set.get_attribute(weight_attribute)
            self.sampled_choiceset_index = self.Alt_Weighted_Sampling(self.choice_set, J, weight_array)
            self.J = self.sampled_choiceset_index.shape[1]
            return self.sampled_choiceset_index
        elif sampling_method == 'stratified':
            #strata_array = self.choice_set.get_attribute(strata_attribute)
            #if weight_attribute is not None:
                #weight_array = self.choice_set.get_attribute(weight_attribute)
            #else:
                #weight_array = None
            self.sampled_choiceset_index = self.Alt_Stratified_Sampling(self.choice_set, strata_array, \
                                         sample_size=sample_size, sample_rate=sample_rate,\
                                         weight_array=weight_array)
            self.J = self.sampled_choiceset_index.shape[1]
            return self.sampled_choiceset_index

        else:
            raise RuntimeWarning, "Unsupported Sampling Method: %s ." % sampling_method
        
    def sample_choice(self, choice_set, prob_array):
        """Choose an alternative for each agent from choice_set given the probability in prob_array"""
        if choice_set.shape <> prob_array.shape:
            raise RuntimeError, "the shapes of choice_set and prob_array must be the same."

        rows,cols = choice_set.shape

#         if not alltrue(sum(prob_array, axis=1) == ones(rows)):
#             raise RuntimeError, "probabilities over choiceset for each agent must add up to 1."

        cumprob_array = cumsum(prob_array, axis=1)
        R = random((rows,1))
        match = (R<cumprob_array)
        #select the first match in search

        z = zeros((rows,1))
        shift = concatenate((z, match), axis=1)[:,:-1]
        choose_index = ( (match - shift) == 1 )
        
        if not alltrue(sum(choose_index, axis=1) == ones(rows)):
            raise RuntimeError, "each agent can have only one choice."
        
        return choice_set[choose_index][:,NewAxis]

    def SRS_Sampling(self, dataset, N):
        """Simple Random Sampling"""

        return SampleNoReplaceL(arange(dataset.size()), N)

    def Weighted_Sampling(self, dataset, N, weight_array):
        """Weighted Sampling"""

        prob_array = weight_array / float(sum(weight_array))
        return ProbSampleNoReplaceL(arange(dataset.size()), N, prob_array)
    
    def Stratified_Sampling(self, dataset, strata_array, sample_size=1, sample_rate=None, weight_array=None, debuglevel=0):
        """Stratifited Sampling"""

        #strata_array = strata_array.astype(Int16)
        sampled_individual_index = array([])
        unique_strata = unique_values(strata_array)
        for this_stratum in unique_strata:
            indices_in_stratum = where(equal(strata_array, this_stratum))[0]
            counts = len(indices_in_stratum)

            if sample_rate is not None:
                stratum_sample_size = int(round(counts * sample_rate))
            else:
                stratum_sample_size = sample_size

            if counts < stratum_sample_size:
                self.debug.print_debug( "Warning: there are less counts(%s) than sample_size %s for stratum %s."\
                 % (counts, stratum_sample_size, this_stratum), 1)
                stratum_sample_size = counts
                pass    ## it'll be catched in function ProbSampleNoReplaceL, so pass here                

            if weight_array is not None:
                stratum_weight_array = weight_array[indices_in_stratum].astype(Float64)
                if sum(stratum_weight_array) == 0.0:
                    self.debug.print_debug("Warning: the weight_array for stratum %s are all zeros, and are skipped."\
                                           % (this_stratum), 1)
                    continue
                
                prob_array = stratum_weight_array / sum(stratum_weight_array)
                # we must have more non zero prob_array entries than stratum_sample_size
                prob_array_size = sum(where(prob_array>0, 1, 0))
                if stratum_sample_size > prob_array_size:
                    self.debug.print_debug("Warning: there are less non-zero entries(%s) in weight_array than sample_size(%s) for stratum %s"\
                     % (prob_array_size, stratum_sample_size, this_stratum), 1)
                    stratum_sample_size = prob_array_size
                    pass    ## it'll be catched in function ProbSampleNoReplaceL, so pass here
            else:
                stratum_weight_array = None
                prob_array = None
            
            #print this_stratum, stratum_sample_size
            if stratum_sample_size > 0:
                sampled_individual_index = concatenate(\
                    (sampled_individual_index, \
                     ProbSampleNoReplaceL(indices_in_stratum, stratum_sample_size, prob_array)
                     ))

        return sampled_individual_index
        
    def Alt_SRS_Sampling(self, dataset, J):
        """Simple Random Sampling for alternatives"""
        
        weight_array = ones(dataset.size()).astype(Float64)
        return self.Alt_Weighted_Sampling(dataset, J, weight_array)
    
    def Alt_Weighted_Sampling(self, dataset, J, weight_array=None):
        """Weighted Sampling for alternatives"""

        sampled_choiceset_index = zeros((self.N, J)) - 1
        selected_choice = zeros((self.N, J))

        selected_choice[:,0] = ones((self.N,))
        J = J - 1

        # TODO::weight_array could be moved below and calculated for each agent
        weight_array_sum = sum(weight_array)
        if weight_array is not None and  weight_array_sum <> 0:
            prob_array = weight_array / weight_array_sum
            # we must have more non zero prob_array entries than sample_size
            assert J <=  sum(where(prob_array>0, 1, 0))
        else:
            weight_array = None
            prob_array = None

        #since id_name is now a list of attribute_names, this function only uses the first item in the list to match agents
        #and their current location(choice)
        selected_choice_ids = self.agent_set.get_attribute(self.choice_set.id_name[0])[self.sampled_individual_index]

        unplaced_agent_index = where(less_equal(selected_choice_ids, UNPLACED))[0]
        #sample a place for unplaced agents as "selected" choice
        if unplaced_agent_index.size() > 0:
            sampled_choice_index = ProbSampleReplaceL(\
                arange(self.choice_set.size()), unplaced_agent_index.size(), prob_array=prob_array)
            selected_choice_ids[unplaced_agent_index] = self.choice_set.get_id_attribute()[sampled_choice_index]
            # set their select_choice indicators to zeros, to differentiate them from real selected choices
            selected_choice[unplaced_agent_index,0] = zeros((unplaced_agent_index.size(),))

        selected_choice_index = self.choice_set.get_id_index(selected_choice_ids)


        #this alternative method sampling alternatives for one agent at one time,
        #it's suitable when we need to use different weight for alternatives for each agent,
        #but it's much slower than Prob2dSampleNoReplaceL function (about 150 times slower)
#         for i in range(self.N):
#             i_selected_index = selected_choice_index[i]
#             sampled_choices = ProbSampleNoReplaceL(\
#                    arange(self.choice_set.size()), J, prob_array=prob_array, exclude_index=i_selected_index)
            
#             sampled_choiceset_index[i, 1:] = sampled_choices

        sampled_choiceset_index[:,1:] = Prob2dSampleNoReplaceL(arange(self.choice_set.size()), (self.N, J), \
                                                               prob_array=prob_array, exclude_index=selected_choice_index)

        sampled_choiceset_index[:,0] = selected_choice_index
        
        self.sampled_choiceset_index = sampled_choiceset_index
        self.selected_choice = selected_choice
        
        return sampled_choiceset_index

    def Alt_Stratified_Sampling(self, dataset, strata_array, sample_size=1, sample_rate=None, weight_array=None):
        """Stratifited Sampling for alternatives"""
        #strata_array = strata_array.astype(Int16)

        #because sample_size is not determined yet, initialize only the first column
        #sampled_choiceset_index = zeros((self.N, 1))-1
        selected_choice = ones((self.N, 1))
        sampling_prob = zeros((self.N, 1))
        sampled_choiceset_index = zeros((self.N, 1))-1

        #since id_name is now a list of attribute_names, this function only uses the first item in the list to match agents
        #and their current location(choice)
        selected_choice_ids = self.agent_set.get_attribute(self.choice_set.id_name[0])[self.sampled_individual_index]

        unplaced_agent_index = where(less_equal(selected_choice_ids, UNPLACED))[0]
        #sample a place for unplaced agents as "selected" choice
        if unplaced_agent_index.size() > 0:
            sampled_choice_index = ProbSampleReplaceL(\
                arange(self.choice_set.size()), unplaced_agent_index.size(), prob_array=weight_array)
            selected_choice_ids[unplaced_agent_index] = self.choice_set.get_id_attribute()[sampled_choice_index]
            # set their select_choice indicators to zeros, to differentiate them from real selected choices
            selected_choice[unplaced_agent_index,0] = zeros((unplaced_agent_index.size(),))

        selected_choice_index = self.choice_set.get_id_index(selected_choice_ids)
        
        unique_strata = unique_values(strata_array)
        #TODO:: determine of choiceset size

        for this_stratum in unique_strata:
            indices_in_stratum = where(equal(strata_array, this_stratum))[0]
            counts = indices_in_stratum.size()

            if sample_rate is not None:
                stratum_sample_size = int(round(counts * sample_rate))
            else:
                stratum_sample_size = sample_size

            if counts < stratum_sample_size:
                self.debug.print_debug( "Warning: there are less counts(%s) than sample_size %s for stratum %s."\
                 % (counts, stratum_sample_size, this_stratum), 0)
                stratum_sample_size = counts

            if weight_array is not None:
                stratum_weight_array = weight_array[indices_in_stratum].astype(Float64)
                if sum(stratum_weight_array) == 0.0:
                    self.debug.print_debug("Warning: the weight_array for stratum %s are all zeros, and are skipped."\
                                           % (this_stratum), 0)
                    continue
                
                prob_array = stratum_weight_array / sum(stratum_weight_array)
                # we must have more non zero prob_array entries than stratum_sample_size
                prob_array_size = sum(where(prob_array>0, 1, 0))
                if stratum_sample_size > prob_array_size:
                    self.debug.print_debug("Warning: there are less non-zero entries(%s) in weight_array than sample_size(%s) for stratum %s"\
                     % (prob_array_size, stratum_sample_size, this_stratum), 1)
                    stratum_sample_size = prob_array_size
            else:
                stratum_weight_array = None
                prob_array = None


            #this alternative method samples alternatives for one agent at one time,
            #it's suitable when we need to use different weight for alternatives for each agent,
            #but it's much slower than Prob2dSampleNoReplaceL function (about 150 times slower)
#             for i in range(self.N):
#                 # special process for currently chooosing stratum, for example, select none, or select more
#                 #TODO:: what if we have unplaced agents?
#                 i_selected_index = selected_choice_index[i]
#                 selected_stratum = strata_array[i_selected_index]  #if selected_choice[i,0] = 1
#                 i_stratum_sample_size = stratum_sample_size
#                 if this_stratum == selected_stratum:
#                     # sample one less from selected_stratum (because we already have a selected one); or whatever process desirable, e.g. sample 3 more
#                     i_stratum_sample_size = stratum_sample_size - 1
#                     sampling_prob[i,0] = i_stratum_sample_size / float(counts)
#                     #continue   

#                 # we must have more non zero prob_array entries than i_stratum_sample_size
#                 #assert i_stratum_sample_size <=  sum(where(prob_array>0, 1, 0))
                
#                 if i_stratum_sample_size > 0:
#                     #import pdb;pdb.set_trace()
#                     proposed_index = ProbSampleNoReplaceL(indices_in_stratum, i_stratum_sample_size, prob_array, exclude_index=i_selected_index)
#                     #print sampled_choiceset_index[i].shape, proposed_index.shape
#                     sampled_choiceset_index[i, j:j+i_stratum_sample_size] = proposed_index
                
#                sampling_prob[i, j:j+i_stratum_sample_size] = i_stratum_sample_size / float(counts)

            sampled_choiceset_index[:, j:j+stratum_sample_size] = Prob2dSampleNoReplaceL(\
                indices_in_stratum, (self.N, stratum_sample_size), prob_array, exclude_index=selected_choice_index)
            sampling_prob[:, j:j+stratum_sample_size] = stratum_sample_size / float(counts)

            j += stratum_sample_size
            
        temp_selected_choice = zeros(sampled_choiceset_index.shape)
        temp_selected_choice[:,0] = selected_choice[:,0]
        selected_choice = temp_selected_choice
        
        self.sampled_choiceset_index = sampled_choiceset_index
        self.selected_choice = selected_choice
        self.sampling_prob = sampling_prob

        return sampled_choiceset_index
    
