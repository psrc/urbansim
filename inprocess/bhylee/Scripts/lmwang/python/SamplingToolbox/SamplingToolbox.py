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
from numarray import *
from numarray.random_array import randint, seed
import path_configuration

from misc.miscellaneous import DebugPrinter
from household.household import HouseholdSet, HouseholdSubset
from grid.Gridcells import GridcellSet
from geographies import GeographySet, GeographySubset

class SamplingToolbox:
    """Class for creating Random alternative sample set"""
    
    def __init__(self, agents, gridcells, geographies=None, J=10, N=5000, sampling_method=(0,0), debuglevel=0):
        """Arguments
             agentset - object of class HouseholdSet or EmploymentSet
             gridset - object of class GridcellSet
             J - the number of alternatives sampled
             N - the number of agents (household, employment) sampled, if N < 1 then includes all agents
             sampling_method - a tuple indicating sampling method for agents and alternatives
             
             #prob_base - fields on whose probablity distribution sampling agents based 

           Usage
             aSample = SamplingToolbox(Households, Gridcells, J=10, N=5000)
             aSample.sampling_agents()
             aSample.sampling_alt()
        """
        
        self.agents = agents
        self.gridcells = gridcells
        self.geographies = geographies
        if self.gridcells.id_field_name not in self.agents.attribute_names:
            raise RuntimeError, self.gridcells.id_field_name + " not found in households attribute_names."
        
        if N <= 0 or N > self.agents.n:
            self.N = self.agents.n
        else:
            self.N = N
        self.J = J
        self.sampled_agent_idx = array([])
        self.sampling_method = {}
        self.sampling_method['agent'] = sampling_method[0]
        self.sampling_method['alt'] = sampling_method[1]

        self.debug = DebugPrinter(debuglevel)
        
    
    def sampling_agents(self):
        """sampling agents from agentset based on sampling_method['agent']"""
        self.debug.print_debug("Sample agents ...",2)
        sampling_method = self.sampling_method['agent']
        if self.agents.n <= self.N:
            self.sampled_agent_idx = arange(self.agents.n)
            return 1
        
        if sampling_method == 0: #random sampling
            self.sampled_agent_idx = self.sample_1d_array_of_non_repeat_random_num(0,self.agents.n,self.N)
        elif sampling_method == 1:  #distribution based sampling
            pass
            
        self.debug.print_debug("Sample agents done.",3)

    def sampling_alt(self):
        """sampling alternative set for sampled agents"""
        self.debug.print_debug("Sample gridcells ...",2)
        # sample from only gridcells with residential units > 0
        ##TODO: in stratified sampling,this criteria will cause KeyError since it eliminates some gridcells
        #self.gridcells.subset_where_variable_larger_than_threshold("residential_units",0)
        self.choiceset_idx = zeros((self.N,self.J))-1
            #selected choice is always at the first column
        self.selected_choice = zeros((self.N,self.J))
        self.selected_choice[:,0] = ones((self.N,))
        
        #the gridcell index where agents are located
            selected_grid_ids = self.agents.get_attribute(self.gridcells.id_field_name)[self.sampled_agent_idx]
        selected_gridcell_index = [self.gridcells.id_mapping[id] for id in selected_grid_ids]
        
        if self.sampled_agent_idx.size() <> self.N:
            raise RuntimeError, "Error: run SamplingToolbox.sampling_agents() to sample agents first."
        
        sampling_method = self.sampling_method['alt']
        if sampling_method == 0: #random sampling
            if self.N > self.J:
                self.choiceset_idx = self.sample_2d_array_of_non_repeat_random_num_by_column\
                         (0,self.gridcells.n,(self.N, self.J-1), init=asarray(selected_gridcell_index))
            else:
                self.choiceset_idx = self.sample_2d_array_of_non_repeat_random_num_by_row\
                         (0,self.gridcells.n,(self.N, self.J-1), init=asarray(selected_gridcell_index))
                
        elif sampling_method == 1: #sampling alternatives proportional to residential_units
            self.choiceset_idx[:,0] = selected_gridcell_index
            sum_attr = cumsum(self.gridcells.get_attribute("residential_units"))
            for j in range(1,self.J,1):
                dup_index = arange(self.N)
                sample_bin = sample_int = zeros(dup_index.shape)-1
                while sometrue(dup_index):
                    sample_bin[dup_index] = randint(0,sum_attr[-1],shape=dup_index.shape)
                    sample_int[dup_index] = searchsorted(sum_attr,sample_bin[dup_index])
                    dup_index = self.find_duplicates2(sample_int, self.choiceset_idx)
                self.choiceset_idx[:,j] = sample_int

        elif sampling_method == 2: #stratified sampling
            selected_geography_index = asarray([self.geographies.id_mapping[id] for id in selected_grid_ids])
            selected_geography_id = self.geographies.get_attribute(self.geographies.geography_type)[selected_geography_index]
            #remove NULL from self.geographies.area
            del self.geographies.area[-2]
            num_samples_from_self_geography = self.J - len(self.geographies.area)
            if num_samples_from_self_geography > 0:
                samples_from_self_geography = zeros((self.N,num_samples_from_self_geography)) - 1
            
            #sample_set = zero((selected_geography_id.size(),self.J)) - 1    # initialize
            j = 0
            for geography_id in self.geographies.area.keys():
                indices_not_in_this_geography = where(not_equal(selected_geography_id, geography_id))[0]
                indices_in_this_geography = where(equal(selected_geography_id, geography_id))[0]
                geography_subset = self.geographies.subset_by_geography_id(geography_id)
                self.choiceset_idx[indices_not_in_this_geography, j] = asarray(geography_subset.index)[\
                    randint(0,geography_subset.n,(indices_not_in_this_geography.size(),))]
                j += 1
                #import pdb; pdb.set_trace()
                for i in range(num_samples_from_self_geography):
                    dup_index = arange(len(indices_in_this_geography))
                    samples_from_this_geography = zeros(dup_index.size()) - 1
                    while sometrue(dup_index):
                        samples_from_this_geography[dup_index] = asarray(geography_subset.index)[\
                            randint(0,geography_subset.n,(dup_index.size(),))]
                        dup_index = self.find_duplicates2(samples_from_this_geography, \
                                         selected_geography_index[indices_in_this_geography])
                    samples_from_self_geography[indices_in_this_geography,i] = samples_from_this_geography
            self.choiceset_idx = sort(self.choiceset_idx)
            self.choiceset_idx[:,0] = selected_geography_index
            if num_samples_from_self_geography > 0:
                self.choiceset_idx[:,1:num_samples_from_self_geography] = samples_from_self_geography
            self.choiceset_idx = self.do_index_remapping(self.choiceset_idx, self.geographies, self.gridcells)

        self.choiceset_idx_tran = transpose(self.choiceset_idx)
        self.debug.print_debug("Sample gridcells done.",3)

    def do_index_remapping(self, index_array, geographies, gridcells, id_field="grid_id"):
        """mapping indice in index_array of geographies to gridcells"""
        keep_shape = index_array.shape
        ids = geographies.get_attribute(id_field)[index_array.flat]
        return reshape(asarray([gridcells.id_mapping[id] for id in ids]), keep_shape)

    def sample_2d_array_of_non_repeat_random_num_by_column(self, min, max, sample_size, init=None):
        """create non-repeat 2d-array random num 

        sample an array of non repeat integer numbers of sample_size between min and max
        non-repeat to init array too.

        min - minimum integer (included)
        max - maximum integer (not included)
        sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row.
        init - array representing values should not appear in sampled array
        """

        output = zeros(sample_size)-1    #initialize
        if init is not None:
            if not (type(init) == NumArray):
                init = asarray(init)
            if init.shape[0] <> sample_size[0]:
                raise ValueError, "init should have the same number of rows as sample_size[0]"
            cols = init.size()/init.shape[0]    #get the num of cols in init
            init.resize((sample_size[0],cols))
            output = concatenate((init,output),axis=1)    #attach init to the beginning of output

        compared_set = output
        for j in range(sample_size[1], 0, -1):
            dup_index = arange(sample_size[0])
            sample_int = zeros(dup_index.shape)-1  #initialize
            
            while sometrue(dup_index):
                sample_int[dup_index] = randint(min,max,dup_index.shape)
                dup_index = self.find_duplicates2(sample_int,compared_set)

            output[:,-j] = sample_int
            compared_set = output

        return output

    def find_duplicates2(self, checking_set, compared_set):
         """find indices of duplicate values at checking_set"""

        checking_set = asarray(checking_set)
        cols = checking_set.size()/checking_set.shape[0]
        if cols <> 1:
            raise ValueError, "Array checking_set must be a rank-1 array"
        compared_set = asarray(compared_set)
        if compared_set.shape[0] <> checking_set.shape[0]:
            raise ValueError, "Arrays have incompatible shapes"

        checking_set = reshape(checking_set,(compared_set.shape[0],-1))
        is_duplicates = where(equal(checking_set, compared_set,),1,0)
        has_duplicates = sum(is_duplicates, axis=1)
        dup_idx = nonzero(has_duplicates)
        if dup_idx[0].size() > 0:
            self.debug.print_debug("found repeats at index: ",5)
            self.debug.print_debug(dup_idx[0],5)
        return dup_idx[0]


    def sample_2d_array_of_non_repeat_random_num_by_row(self, min, max, sample_size, init=None):
        """create non-repeat 2d-array random num 

        sample an array of non repeat integer numbers of sample_size between min and max
        non-repeat to init array too.

        min - minimum integer (included)
        max - maximum integer (not included)
        sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row.
        init - array representing values should not appear in sampled array
        """

        sample_set = zeros(sample_size)-1
        if init is not None:
            if not (type(init) == NumArray):
                init = asarray(init)
            if init.shape[0] <> sample_size[0]:
                raise RuntimeError, "init should have the same number of rows as sample_size[0]"
            cols = init.size()/init.shape[0]    #get the num of cols in init
            init.resize((sample_size[0],cols))
            sample_set = concatenate((init,sample_set),axis=1)
            
            for j in range(sample_size[0]):
                sample_set[j,:] = self.sample_1d_array_of_non_repeat_random_num\
                          (min,max,sample_size=sample_size[1],init=init[j,...])
        else:
            for j in range(sample_size[0]):
                sample_set[j,:] = sample_1d_array_of_non_repeat_random_num\
                          (min,max,sample_size=sample_size[1])
        
        return sample_set

    def sample_1d_array_of_non_repeat_random_num(self,min,max,sample_size,init=None):
        """sample one 1d array of non-repeat random numbers

        sample an array of non repeat integer numbers of sample_size between min and max
        non-repeat to init array too.

        min - minimum integer (included)
        max - maximum integer (not included)
        sample_size - number representing the sample_size
        init - array representing values should not appear in sampled array
        """
        
        if init is not None:
            if not (type(init)==NumArray):
                init = asarray(init)
            init = init.flat
            if sometrue(self.find_duplicates(init)):
                print "Warning: init includes duplicates and will be replaced!"
        else:
            init = asarray([])

        dup_idx = arange(sample_size) + init.size()
        sample_idx = concatenate((init, zeros(dup_idx.shape)-1))
        while sometrue(dup_idx):
            sample_idx[dup_idx] = randint(min,max,dup_idx.shape)
            dup_idx = self.find_duplicates(sample_idx)
        return sample_idx
    
    def find_duplicates(self,checking_set):
        """find index of duplicate values in a list or array"""
        
        checking_set = asarray(checking_set)
        checking_set = checking_set.flat   #convert to a rank-1 array
        
        allsum = zeros(checking_set.shape)
        allone = ones(checking_set.shape)
        for a in checking_set:
            allsum += where(equal(checking_set, a), 1, 0)
        has_duplicates = allsum-allone
        dup_idx = nonzero(has_duplicates)
        if dup_idx[0].size() > 0:
            self.debug.print_debug("found repeats at index: ",5)
            self.debug.print_debug(dup_idx[0],5)            
        return dup_idx[0]

    def write_sampleset_to_file(self,filename='./sampleset.csv'):
        pass


if __name__ == "__main__":

    import time
    from glob import glob
    from multiDB.MultiDB import DbConnection

    print "run tests..."
    
    #indb = "Eugene_baseyear"
    indb = "PSRC_2000_baseyear_sampling_script_testbed_lmwang"    
    db_host_name=os.environ['MYSQLHOSTNAME']
    db_user_name=os.environ['MYSQLUSERNAME']
    db_password =os.environ['MYSQLPASSWORD']
    
    print "Connecting database ..."
    Con = DbConnection(db=indb, hostname=db_host_name, username=db_user_name, 
               password=db_password)
    
    bdir = "./households_export"
    
    households = HouseholdSet(database_connection=Con, obs=100, randomflag=1, base_directory=bdir)
    gridcells = GridcellSet(database_connection=Con, base_directory=bdir)
    fazdistricts = GeographySet(database_connection=Con, geography_type="fazdistrict")
    
    sample = SamplingToolbox(households,gridcells,geographies=fazdistricts,sampling_method=(0,2),N=20,debuglevel=5)

    start_time1 = time.time()
    sample.sampling_agents()
    sample.sampling_alt()
    end_time1 = time.time()
    
    sampled_hhs = HouseholdSubset(households,sample.sampled_agent_idx)
    print "sampled household index (", sample.sampled_agent_idx.size(), "/", households.n, "):"
    print sample.sampled_agent_idx
    print "sampled household_id:"
    print sampled_hhs.get_attribute('household_id')
    print "which respectively resides at grid_id:"
    print sampled_hhs.get_attribute('grid_id')
    print "alternative set:"
    print gridcells.get_attribute_by_index("grid_id",sample.choiceset_idx)
    print "the selected choice matrix:"
    print sample.selected_choice

    print "1 Elapsed time (fast)= " + str(end_time1 - start_time1)
    
        #clear up the exported files and directory
    if len(glob(bdir)) > 0:
        map(lambda x: os.remove(x), glob(bdir+'/*'))
        os.rmdir(bdir) 


#=============================================unsed code===============================================

#     def sample_2d_array_of_non_repeat_random_num_by_column2(self, min, max, sample_size, init=None):
#         """create non-repeat random sample from population

#         sample an array of non repeat integer numbers of sample_size between min and max
#         non-repeat to init array too.

#         min - minimum integer (included)
#         max - maximum integer (not included)
#         sample_size - tuple representing the sample size with (rows, columns), non-repeat at each row.
#         init - array representing values should not appear in sampled array
#         """

#         if init is not None:
#             if not (type(init) == NumArray):
#                 init = asarray(init)
#             if init.shape[0] <> sample_size[0]:
#                 raise ValueError, "init should have the same number of rows as sample_size[0]"
#             cols = init.size()/init.shape[0]    #get the num of cols in init
#             init.resize((sample_size[0],cols))

#         sample_set = zeros(sample_size)-1
#         dup_idx = indices(sample_size)
#         m,n = (dup_idx[0].flat,dup_idx[1].flat)
#         while sometrue(m) or sometrue(n):
#             sample_set[m,n] = randint(min,max,shape=(m.size(),))
#             dup_idx = self.find_duplicates21(sample_set,init)
#             m,n = (dup_idx[0].flat,dup_idx[1].flat)
#         sample_set = concatenate((init,sample_set),axis=1)
#         return sample_set

#     def find_duplicates21(self,checking_set,compared_set):
#         """find index of duplicate values"""
        
#         checking_set = asarray(checking_set)
#         cols = checking_set.size()/checking_set.shape[0]

#         compared_set = asarray(compared_set)
#         if compared_set.shape[0] <> checking_set.shape[0]:
#             raise ValueError, "Arrays have incompatible shapes"

#         checking_set = reshape(checking_set,(checking_set.shape[0],-1))
#         compared_set = reshape(compared_set,(compared_set.shape[0],-1))
#         compared_set = concatenate((compared_set,checking_set),axis = 1)

#         allsum = zeros(checking_set.shape)
#         allone = ones(checking_set.shape)
#         for j in range(cols):
#             checking_col = reshape(checking_set[:,j],(-1,1))
#             is_duplicates = where(equal(checking_col, compared_set), 1, 0)
#             allsum[:,j] = sum(is_duplicates, axis=1)

#         has_duplicates = allsum-allone
#         dup_idx = nonzero(has_duplicates)
#         if dup_idx[0].size() > 0:
#             self.debug.print_debug("found repeats at index: ",5)
#             self.debug.print_debug(dup_idx[0],5)            
#         return dup_idx
