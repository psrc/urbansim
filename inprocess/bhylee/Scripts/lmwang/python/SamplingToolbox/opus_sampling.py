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
import configure_path
from numarray import array, asarray, arange, concatenate, zeros, ones, \
                     sometrue, where, equal, not_equal, nonzero, NumArray, \
             reshape, sum, cumsum, sort, searchsorted
from numarray.random_array import randint, seed
from dataset import DataSet, SetAttribute
from sampling_functions import *

class SamplingToolbox:
    """Class for sampling individual and entity indices from datasetset object"""
    
    def __init__(self, agent_set=None, random_seed=None):
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

        if random_seed is not None: seed(random_seed[0],random_seed[1])

        if agent_set is not None:
            if not isinstance(agent_set, DataSet):
                raise TypeError, "agent_set must be of type DataSet defined in OpusCore."
            self.agent_set = agent_set
            self.N = self.agent_set.size()
            self.sampled_individual_index = arange(self.agent_set.size())
    
    def sample_individuals(self, dataset, N=0, sampling_method='SRS', weight_array=None, strata_array=None, \
                  sample_size=1, sample_rate=None):
        """
        sample individuals from dataset object with given sampling method and sample size

        dataset - dataset object to sample individuals from
        N - number of individuals to be sampled, if N < 0 or N greater than size of dataset, sample all dataset 
        sampling_method - string name for one of the implemented sampling methods, including
                          'SRS' for Simple Random Sampling,
                  'weighted'for weighted sampling, and
                  'stratified' for stratified sampling
        weight_array - required for weighted sampling, the array used to weight sampling
        strata_array - required for stratified sampling, the array used to defined stratum
        sample_size - used in stratified sampling, to specified how many individuals are sampled in every stratum
        sample_rate - used in stratified sampling, to specified the rate of sampling in every stratum
        """
        
        if not isinstance(dataset, DataSet):
            raise TypeError, "dataset must be of type DataSet defined in OpusCore."

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
            self.N = N
            return self.sampled_individual_index
        elif sampling_method == 'weighted':
            #weight_array = self.agent_set.get_attribute(weight_attribute)
            self.sampled_individual_index = self.Weighted_Sampling(self.agent_set, N, weight_array)
            self.N = N
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
              sample_size=1, sample_rate=None, include_current_choice=True):
        """
        sample entities from entity object for each individuals in self.agent_set with given sample size and sampling method

        choice_set - dataset object to sample alternatives (choices) from
        J - number of alternatives to be sampled
        sampling_method - string name for one of the implemented sampling methods, including
                          'SRS' for Simple Random Sampling,
                  'weighted'for weighted sampling, and
                  'stratified' for stratified sampling
        weight_array - required for weighted sampling, the array used to weight sampling
        strata_array - required for stratified sampling, the array used to defined stratum
        sample_size - used in stratified sampling, to specified how many individuals are sampled in every stratum
        sample_rate - used in stratified sampling, to specified the rate of sampling in every stratum
        include_current_choice - boolean value to indicate if the entities that individuals currently reside are included
                                 in the sample
        """
        
        if not isinstance(choice_set, DataSet):
            raise TypeError, "dataset must be of type DataSet defined in OpusCore."
        self.choice_set = choice_set
        
        if len(self.sampled_individual_index) == 0:
            raise RuntimeError, "Need to specify individual dataset before sample_choiceset."
        if len(self.sampled_individual_index) <> self.N:
            self.N = len(self.sampled_individual_index)
            raise RuntimeError, "Number of individuals sampled is inconsistent; \
            Need to specify individual dataset before sample_choiceset."
        
        for id_name in self.choice_set.id_name:
            if id_name not in self.agent_set.attribute_names:
                raise RuntimeError, "id_name of choice_set %s cannot be found in attribute_names of individual." \
                      % id_name
        
        if self.choice_set.size() <= J:
            raise RuntimeError, "number of entities %s is not enough to sample %s alternatives" % (self.choice_set.size(), J)
        elif J < 0:
            raise RuntimeError, "cannot sample less than 0 alternatives"

        if sampling_method == 'SRS':
            self.sampled_choiceset_index = self.Alt_Weighted_Sampling(self.choice_set, J, \
                                          include_current_choice=include_current_choice)
            self.J = self.sampled_choiceset_index.shape[1]
            return self.sampled_choiceset_index
        elif sampling_method == 'weighted':
            #weight_array = self.choice_set.get_attribute(weight_attribute)
            self.sampled_choiceset_index = self.Alt_Weighted_Sampling(self.choice_set, J, weight_array, include_current_choice)
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
                                         weight_array=weight_array, include_current_choice=include_current_choice)
            self.J = self.sampled_choiceset_index.shape[1]
            return self.sampled_choiceset_index

        else:
            raise RuntimeWarning, "Unsupported Sampling Method: %s ." % sampling_method
        

    def SRS_Sampling(self, dataset, N):
        """Simple Random Sampling"""
        #return _sample_1d_array_of_non_repeat_random_num(arange(dataset.size()), N)
        return SampleNoReplace(arange(dataset.size()), N)

    def Weighted_Sampling(self, dataset, N, weight_array):
        """Weighted Sampling"""
        #return _sample_1d_array_of_non_repeat_random_num(arange(dataset.size()), N, weight_array=weight_array)
        prob_array = weight_array/sum(weight_array)
        return ProbSampleNoReplace(arange(dataset.size()), N, prob_array)
    
    def Stratified_Sampling(self, dataset, strata_array, sample_size=1, sample_rate=None, weight_array=None):
        """Stratifited Sampling"""
        #strata_array = strata_array.astype(Int16)
        sampled_individual_index = array([])
        unique_strata = unique_values(strata_array)
        for this_stratum in unique_strata:
            indices_in_stratum = where(equal(strata_array, this_stratum))[0]
            counts = len(indices_in_stratum)
            if sample_rate is not None:
                stratum_sample_size = int(counts * sample_rate)
            else:
                stratum_sample_size = sample_size

            if weight_array is not None:
                stratum_weight_array = weight_array[indices_in_stratum]
            else:
                stratum_weight_array = None
                
            if counts < stratum_sample_size:
                print "Warning: Stratum %s has only %s counts and is unable to sample %s individuals. Sample %s instead." \
                      % (this_stratum, counts, stratum_sample_size, counts)
                stratum_sample_size = counts
            if stratum_sample_size > 0:
                if stratum_weight_array is not None:
                    prob_array = stratum_weight_array/sum(stratum_weight_array)
                else:
                    prob_array = None
                    
                sampled_individual_index = concatenate(\
                    (sampled_individual_index, \
                    #self._sample_1d_array_of_non_repeat_random_num(\
                    ProbSampleNoReplace(\
                    indices_in_stratum, stratum_sample_size, prob_array)
                    ))

        return sampled_individual_index
        
     def Alt_SRS_Sampling(self, dataset, J, include_current_choice=True):
        """Simple Random Sampling for alternatives"""
        return self.Alt_Weighted_Sampling(self, dataset, J, include_current_choice=include_current_choice)
    
    def Alt_Weighted_Sampling(self, dataset, J, weight_array=None, include_current_choice=True):
        """weighted sampling for alternatives"""
        
        sampled_choiceset_index = zeros((self.N, J))-1
        selected_choice = zeros((self.N, J))
        #if include_current_choice, sample J - 1 alternatives and put the current choices at the beginning of sampled_choiceset_index
        if include_current_choice:
            selected_choice[:,0] = ones((self.N,))
            J = J - 1
        #since id_name is now a list of attribute_names, this function only uses the first item in the list to match agents and their current location(choice)
            selected_choice_ids = self.agent_set.get_attribute(self.choice_set.id_name[0])[self.sampled_individual_index]
        selected_choice_index = [self.choice_set.id_mapping[id] for id in selected_choice_ids]

        #if self.N > J: #compare number of rows to columns, and use sampling by row or by column respectly for performance
        sampled_choiceset_index = sample_2d_array_of_non_repeat_random_num_by_column(\
            arange(self.choice_set.size()),(self.N, J), init=asarray(selected_choice_index), \
            weight_array=weight_array)
#         else:
#             sampled_choiceset_index = self._sample_2d_array_of_non_repeat_random_num_by_row\
#                          (arange(self.choice_set.size()),(self.N, J), init=asarray(selected_choice_index), \
#                           weight_array=weight_array)
        if include_current_choice:
            sampled_choiceset_index = concatenate(\
                (array(selected_choice_index, shape=(self.N,1)), \
                sampled_choiceset_index),axis=1)

        self.selected_choice = selected_choice
        return sampled_choiceset_index

    def Alt_Stratified_Sampling(self, dataset, strata_array, sample_size=1, sample_rate=None, weight_array=None, include_current_choice=True):
        """Stratifited Sampling for alternatives"""
        #strata_array = strata_array.astype(Int16)
        #JC = 1
        #sampled_choiceset_index = zeros((self.N, JC))-1
        #selected_choice = zeros((self.N, JC))

        #if include_current_choice:
        #    selected_choice[:,0] = ones((self.N,))
        #    J = J - 1

        #since id_name is now a list of attribute_names, this function only uses the first item in the list to match agents and their current location(choice)
            selected_choice_ids = self.agent_set.get_attribute(self.choice_set.id_name[0])[self.sampled_individual_index]
        selected_choice_index = [self.choice_set.id_mapping[id] for id in selected_choice_ids]

        sampled_choiceset_index = array(selected_choice_index, shape=(self.N,1))
        
        unique_strata = unique_values(strata_array)
        for this_stratum in unique_strata:
            indices_in_stratum = where(equal(strata_array, this_stratum))[0]
            counts = len(indices_in_stratum)
            if sample_rate is not None:
                stratum_sample_size = int(counts * sample_rate)
            else:
                stratum_sample_size = sample_size

            if weight_array is not None:
                stratum_weight_array = weight_array[indices_in_stratum]
            else:
                stratum_weight_array = None
                
            if counts < stratum_sample_size:
                print "Warning: Stratum %s has only %s counts and is unable to sample %s individuals. Sample %s instead." \
                      % (this_stratum, counts, stratum_sample_size, counts)
                stratum_sample_size = counts
            if stratum_sample_size > 0:
                sampled_choiceset_index = concatenate(\
                    (sampled_choiceset_index, \
                     sample_2d_array_of_non_repeat_random_num_by_column(\
                         indices_in_stratum, (self.N, stratum_sample_size), init=asarray(selected_choice_index), \
                         weight_array=stratum_weight_array)
                     ),axis=1)
                
        selected_choice = zeros(sampled_choiceset_index.shape)

        if include_current_choice:
            selected_choice[:,0] = ones(sampled_choiceset_index.shape[0])
        else:
            sampled_choiceset_index = sampled_choiceset_index[:,1:]
            selected_choice = selected_choice[:,1:]
        self.selected_choice = selected_choice
        return sampled_choiceset_index
    
import os, sys
import unittest
#from store.storage_creator import StorageCreator
from gridcellset.gridcells import GridcellSet
from householdset.households import HouseholdSet

class SamplingToolboxTest(unittest.TestCase):
    dirEugene = os.environ['OPUSHOME'] + "/UrbanSim4/data/flt/Eugene_1980_baseyear"
#    storage_dictionary = Resources({"in_base":dirEugene})
#    in_storage = StorageCreator().get_storage("Flt", storage_dictionary)
#    resources = Resources({"in_storage":in_storage})
#    gcs = GridcellSet(resources)
    gcs = GridcellSet(in_storage_type = "flt", in_base = dirEugene)
    gcs.load_dataset(attributes=SetAttribute.ALL)
    hhs = HouseholdSet(in_storage_type = "flt", in_base = dirEugene)
    hhs.load_dataset(attributes=SetAttribute.ALL)

    def testSRS_Sampling(self):
        n = 500
        st = SamplingToolbox(random_seed=(1,1))
        st.sample_individuals(self.gcs, n)
        print st.N
        print st.sampled_individual_index
        self.assertEqual(len(st.sampled_individual_index), n, msg ="Number of individual sampled not equal to the specified arguments")

    def testWeighted_Sampling(self):
        n = 500
        st = SamplingToolbox(random_seed=(1,1))
        weight_array = self.gcs.get_attribute('residential_units')
        st.sample_individuals(self.gcs, n, sampling_method='weighted', weight_array=weight_array)
        print st.N
        print st.sampled_individual_index
        self.assertEqual(len(st.sampled_individual_index), n, msg ="Number of individual sampled not equal to the specified arguments")

    def testStratifited_Sampling(self):
        n = 2
        st = SamplingToolbox(random_seed=(1,1))
        strata_array = self.gcs.get_attribute('zone_id')        
        st.sample_individuals(self.gcs, n, sampling_method='stratified', strata_array=strata_array, \
                     sample_rate=.1) #, weight_attribute='residential_units')
        print st.N
        print st.sampled_individual_index
        print self.gcs.get_attribute('zone_id')[st.sampled_individual_index]
        self.assertEqual(len(st.sampled_individual_index), st.N, msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_SRS_Sampling_by_column(self):
        j = 10
         st = SamplingToolbox(self.hhs)
        st.sample_choiceset(self.gcs, J=j, sampling_method='SRS')
        self.assertEqual(st.sampled_choiceset_index.shape, (self.hhs.size(), j), msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_Weighted_Sampling_by_column(self):
        j = 10
         st = SamplingToolbox(self.hhs)
        weight_array = self.gcs.get_attribute('residential_units')    
        ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='weighted', weight_array=weight_array)
        self.assertEqual(ASample.shape, (self.hhs.size(), j), msg ="Number of individual sampled not equal to the specified arguments")

     def testAlt_Stratified_Sampling_by_column(self):
        n=1000; j = 10
         st = SamplingToolbox()
        weight_array = self.hhs.get_attribute('persons')
        strata_array = self.gcs.get_attribute('zone_id')                
        st.sample_individuals(self.hhs, n, sampling_method='weighted', weight_array=weight_array)        
        ASample = st.sample_choiceset(self.gcs, J=1, sampling_method='stratified', strata_array= strata_array) #,weight_attribute='residential_units')
        print "%s*%s" % (st.N, st.J)
        self.assertEqual(ASample.shape, (st.N, st.J), msg ="Number of individual sampled not equal to the specified arguments")

#      def testAlt_SRS_Sampling_by_row(self):
#         n = 5; j = 10
#         st = SamplingToolbox()
#         ISample = st.sample_individual(self.hhs, n)
#          ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='SRS')
#         self.assertEqual(ASample.shape, (n, j), msg ="Number of individual sampled not equal to the specified arguments")

#      def testAlt_Weighted_Sampling_by_row(self):
#         n = 5; j = 10
#         st = SamplingToolbox()
#         ISample = st.sample_individual(self.hhs, n)
#               weight_array = self.gcs.get_attribute('persons')
#          ASample = st.sample_choiceset(self.gcs, J=j, sampling_method='weighted', weight_array=weight_array)
#         self.assertEqual(ASample.shape, (n, j), msg ="Number of individual sampled not equal to the specified arguments")
        
if __name__ == "__main__":
    unittest.main()
    