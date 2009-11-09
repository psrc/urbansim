# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import where, arange, take, ones, newaxis, ndarray, zeros, concatenate, resize 
from numpy import searchsorted, empty, digitize, column_stack
from numpy.random import rand
from opus_core.samplers.constants import UNPLACED_ID
from opus_core.sampling_toolbox import prob2dsample, probsample_noreplace, normalize
from opus_core.sampling_toolbox import nonzerocounts
from opus_core.logger import logger
from opus_core.misc import ncumsum, lookup
from opus_core.samplers.weighted_sampler import weighted_sampler
from opus_core.datasets.interaction_dataset import InteractionDataset
from urbansim.abstract_variables.abstract_frequency_by_category import get_category_and_frequency

class weighted_sampler_by_category(weighted_sampler):

    def run(self, dataset1, dataset2, index1=None, index2=None, sample_size=10, weight=None,
            include_chosen_choice=None, with_replacement=True, resources=None, dataset_pool=None):
        """
        
        
        this function samples number of sample_size (scalar value) alternatives from dataset2
        for agent set specified by dataset1.
        If index1 is not None, only samples alterantives for agents with indices in index1;
        if index2 is not None, only samples alternatives from indices in index2.
        sample_size specifies number of alternatives to be sampled for each agent.
        weight, to be used as sampling weight, is either an attribute name of dataset2, or a 1d
        array of the same length as index2 or 2d array of shape (index1.size, index2.size).

        Also refer to document of interaction_dataset"""

        if dataset_pool is None:
            sc = SessionConfiguration()
            try:
                dataset_pool=sc.get_dataset_pool()
            except:
                dataset_pool = DatasetPool(sc.package_order)

        local_resources = Resources(resources)
        local_resources.merge_if_not_None(
                {"dataset1": dataset1, "dataset2": dataset2,
                "index1":index1, "index2": index2,
                "sample_size": sample_size, "weight": weight,
                "with_replacement": with_replacement,
                "include_chosen_choice": include_chosen_choice})

        local_resources.check_obligatory_keys(['dataset1', 'dataset2', 'sample_size'])
        agent = local_resources["dataset1"]
        choice = local_resources["dataset2"]
        index1 = local_resources.get("index1", None)
        if index1 is None:
            index1 = arange(agent.size())
        index2 = local_resources.get("index2", None)
        if index2 is None:
            index2 = arange(choice.size())
            
        if index1.size == 0 or index2.size == 0:
            err_msg = "either choice size or agent size is zero, return None"
            logger.log_warning(err_msg)
            return (None, None)        

        agent_category_definition = local_resources.get("agent_category_definition", [])
        choice_category_definition = local_resources.get("choice_category_definition", [])
        agent_filter_attribute = local_resources.get("agent_filter_attribute", None)
        category_inflating_factor = local_resources.get("category_inflating_factor", 10)

        frequency, unique_agent_category_id, unique_choice_category_id, agent_category_id, choice_category_id = \
                get_category_and_frequency(agent, agent_category_definition,
                                           choice, choice_category_definition,
                                           agent_filter_attribute, category_inflating_factor,
                                           dataset_pool=dataset_pool)
         
        include_chosen_choice = local_resources.get("include_chosen_choice",  False)
        chosen_choice_id = agent.get_attribute(choice.get_id_name()[0])[index1]
        chosen_choice_index = choice.try_get_id_index(chosen_choice_id, return_value_if_not_found=-1)
        chosen_choice_index_to_index2 = lookup(chosen_choice_index, index2, index_if_not_found=UNPLACED_ID)
        
        J = local_resources["sample_size"]
        if include_chosen_choice:
            J = J - 1
        local_resources.merge_with_defaults({'with_replacement': with_replacement})
        with_replacement = local_resources.get("with_replacement")
        
        sampled_index = empty((index1.size, J), dtype="int32")
        sampling_prob = empty((index1.size, J), dtype="float64")
        
        _digitize, _where,  _normalize = digitize, where, normalize
        _ncumsum, _rand, _searchsorted = ncumsum, rand, searchsorted   #speed hack
        for i in range(unique_agent_category_id.size):
            category_id = unique_agent_category_id[i]
            agents_in_this_category = _where(agent_category_id[index1] == category_id)[0]
            num_agents = agents_in_this_category.size
            if num_agents == 0: continue
            #import pdb; pdb.set_trace()
            
            ## divide frequency by the mean frequency to avoid overflow
            weights = frequency[i, _digitize(choice_category_id[index2], unique_choice_category_id)-1]  / frequency[i, :].mean()
            prob = _normalize(weights)
            index = _searchsorted(_ncumsum(prob), _rand(num_agents * J)).reshape(-1, J)

            if not with_replacement:
                raise NotImplementedError, "Sample without replacement is not implemented for this sampler yet."
                #    nz = nonzero(prob)[0].size
                #    if J < nz:
                    #        ## number of non zero weight less than alternatives, sample with replacement
                    #        logger.log_warning("There are %s non zero weights and are less than the number of alternatives proposed %s. " % (nz, J) + 
                    #                           "Sample with replacement instead.")
                    #        continue
                    #    i=0; max_iterations=200
                    #    while True:
                        #        index = sort(index, axis=1)
                        #        where_repeats = nonzero( logical_not(diff(index, axis=1)) ) 
                        #        num_repeats = where_repeats[0].size
                        #        if num_repeats == 0: break
                        #        index[where_repeats] = _searchsorted(_rand(num_repeats), prob)
                        #        i += 1
                        #        if i > max_iterations:
                            #            logger.log_warning("weight_sampler_by_category is unable to sample %i alternatives without replacement in %i iterations; " % \
                                    #                               (J, max_iterations) + 
                            #                               "give up sampling without replacement and results may contain replacement."
                            #                              )
                            #            break

            sampled_index[agents_in_this_category, :] = index
            sampling_prob[agents_in_this_category, :] = prob[index] 

        sampled_index = index2[sampled_index]
        is_chosen_choice = zeros(sampled_index.shape, dtype="bool")
        #chosen_choice = -1 * ones(chosen_choice_index.size, dtype="int32")
        if include_chosen_choice:
            sampled_index = column_stack((chosen_choice_index[:,newaxis],sampled_index))
            is_chosen_choice[chosen_choice_index!=UNPLACED_ID, 0] = 1
            
            sampling_prob_for_chosen_choices = take(prob, chosen_choice_index_to_index2[:, newaxis])
            ## if chosen choice chosen is unplaced has the sampling prob is 0
            sampling_prob_for_chosen_choices[where(chosen_choice_index==UNPLACED_ID)[0],] = 0.0
            sampling_prob = column_stack([sampling_prob_for_chosen_choices, sampling_prob])
            
        #chosen_choice[where(is_chosen_choice)[0]] = where(is_chosen_choice)[1]
        
        interaction_dataset = self.create_interaction_dataset(dataset1, dataset2, index1, sampled_index)
        interaction_dataset.add_attribute(sampling_prob, '__sampling_probability')
        interaction_dataset.add_attribute(is_chosen_choice, 'chosen_choice')

        ## to get the older returns
        #sampled_index = interaction_dataset.get_2d_index()
        #chosen_choices = UNPLACED_ID * ones(index1.size, dtype="int32") 
        #where_chosen = where(interaction_dataset.get_attribute("chosen_choice"))
        #chosen_choices[where_chosen[0]]=where_chosen[1]
        #return (sampled_index, chosen_choice)
        
        return interaction_dataset

from opus_core.tests import opus_unittest
from numpy import array, all, alltrue, not_equal, equal, repeat, int32
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):

    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')

        storage.write_table(table_name='households',
            table_data={
                'household_id': arange(10)+1,
              #  'household_id':array([1, 2, 3, 4, 5, 6, 7, 8]),
              #  'income'      :array([1, 3, 2, 1, 3, 8, 5, 4]),
              # #'category_id' :array([1, 2, 2, 1, 2, 3, 3, 2]),
              #  'building_id' :array([1, 2, 4, 3, 3, 2, 4, 2]),
              ##'large_area_id':array([1, 1, 2, 3, 3, 1, 2, 1]),
              #  
                'grid_id': arange(-1, 9, 1)+1,
                'lucky':array([1,0,1, 0,1,1, 1,1,0, 0])
                }
            )

        storage.write_table(table_name='gridcells',
            table_data={
                #'building_id':    array([1, 2, 3, 4]),
                #'large_area_id':  array([1, 1, 3, 2]),

                'grid_id': arange(15)+1,
                'filter':array([0,1,1, 1,1,1, 1,1,1, 0,1,0, 1,1,1]),
                'weight':array([0.1,9,15, 2,5,1, 6,2.1,.3, 4,3,1, 10,8,7])
                }
            )
        dataset_pool = SessionConfiguration(in_storage=storage).get_dataset_pool()

        #create households
        self.households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

        # create gridcells
        self.gridcells = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name="gridcell")
        dataset_pool.replace_dataset('household', self.households)
        dataset_pool.replace_dataset('gridcell', self.gridcells)

    def test_1(self):
        """"""
        sample_size = 5
        # check the individual gridcells
        # This is a stochastic model, so it may legitimately fail occassionally.
        index1 = where(self.households.get_attribute("lucky"))[0]
        #index2 = where(self.gridcells.get_attribute("filter"))[0]
        weight=self.gridcells.get_attribute("weight")
        estimation_config = {"agent_category_definition":["household.lucky"],
                             "choice_category_definition":["gridcell.filter+1"]
                            }
        for icc in [0,1]: #include_chosen_choice?
            #icc = sample([0,1],1)
            sampler_ret = weighted_sampler_by_category().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                                                                sample_size=sample_size,
                                                                include_chosen_choice=icc, resources=estimation_config)
            # get results
            sampled_index = sampler_ret.get_2d_index()
            chosen_choices = UNPLACED_ID * ones(index1.size, dtype="int32") 
            where_chosen = where(sampler_ret.get_attribute("chosen_choice"))
            chosen_choices[where_chosen[0]]=where_chosen[1]

            self.assertEqual(sampled_index.shape, (index1.size, sample_size))
            if icc:
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)
                chosen_choice_index = resize(array([UNPLACED_ID], dtype="int32"), index1.shape)
                w = where(chosen_choices>=0)[0]
                # for 64 bit machines, need to coerce the type to int32 -- on a
                # 32 bit machine the astype(int32) doesn't do anything
                chosen_choice_index[w] = sampled_index[w, chosen_choices[w]].astype(int32)
                self.assert_( alltrue(equal(placed_agents_index, chosen_choice_index)) )
                sampled_index = sampled_index[:,1:]
                
            self.assert_( alltrue(lookup(sampled_index.ravel(), arange(self.gridcells.size()), index_if_not_found=UNPLACED_ID)!=UNPLACED_ID) )
            self.assert_( all(not_equal(weight[sampled_index], 0.0)) )
                
if __name__ == "__main__":
    opus_unittest.main()
