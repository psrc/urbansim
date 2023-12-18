# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE


from opus_core.resources import Resources
from opus_core.session_configuration import SessionConfiguration
from opus_core.datasets.dataset_pool import DatasetPool
from numpy import where, arange, take, ones, newaxis, ndarray, zeros, concatenate, resize
from numpy import searchsorted, column_stack
from opus_core.samplers.constants import UNPLACED_ID, DTYPE
from opus_core.sampling_toolbox import prob2dsample, probsample_noreplace, normalize
from opus_core.sampling_toolbox import nonzerocounts
from opus_core.misc import lookup
from opus_core.logger import logger
from opus_core.sampler import Sampler
from opus_core.datasets.interaction_dataset import InteractionDataset
from opus_core.variables.variable_name import VariableName
            
class weighted_sampler(Sampler):

    def run(self, dataset1, dataset2, index1=None, index2=None, sample_size=10, weight=None,
            include_chosen_choice=False, with_replacement=False, resources=None, dataset_pool=None):
        
        """this function samples number of sample_size (scalar value) alternatives from dataset2
        for agent set specified by dataset1.
        If index1 is not None, only samples alterantives for agents with indices in index1;
        if index2 is not None, only samples alternatives from indices in index2.
        sample_size specifies number of alternatives to be sampled for each agent.
        weight, to be used as sampling weight, is either an attribute name of dataset2, or a 1d
        array of the same length as index2 or 2d array of shape (index1.size, index2.size).

        Also refer to document of interaction_dataset"""

        if dataset_pool is None:
            try:
                sc = SessionConfiguration()
                dataset_pool=sc.get_dataset_pool()
            except:
                dataset_pool = DatasetPool()
        
        local_resources = Resources(resources)
        local_resources.merge_if_not_None(
                {"dataset1": dataset1, "dataset2": dataset2,
                "index1":index1, "index2": index2,
                "sample_size": sample_size, "weight": weight,
                "with_replacement": with_replacement,
                "include_chosen_choice": include_chosen_choice})

        local_resources.check_obligatory_keys(['dataset1', 'dataset2', 'sample_size'])
        agent = local_resources["dataset1"]
        index1 = local_resources.get("index1", None)
        if index1 is None:
            index1 = arange(agent.size())
        choice = local_resources["dataset2"]
        index2 = local_resources.get("index2", None)
        if index2 is None:
            index2 = arange(choice.size())
            
        if index1.size == 0 or index2.size == 0:
            err_msg = "either choice size or agent size is zero, return None"
            logger.log_warning(err_msg)
            return None
        
        include_chosen_choice = local_resources.get("include_chosen_choice",  False)
        J = local_resources["sample_size"]
        if include_chosen_choice:
            J = J - 1
            
        with_replacement = local_resources.get("with_replacement")
            
        weight = local_resources.get("weight", None)
        if isinstance(weight, str):
            if weight in choice.get_known_attribute_names():
                weight=choice.get_attribute(weight)
                rank_of_weight = 1 
            else:
                varname = VariableName(weight)
                if varname.get_dataset_name() == choice.get_dataset_name():
                    weight=choice.compute_variables(weight, dataset_pool=dataset_pool)
                    rank_of_weight = 1
                elif varname.get_interaction_set_names() is not None:
                    ## weights can be an interaction variable
                    interaction_dataset = InteractionDataset(local_resources)
                    weight=interaction_dataset.compute_variables(weight, dataset_pool=dataset_pool)
                    rank_of_weight = 2
                    assert(len(weight.shape) >= rank_of_weight)
                else:
                    err_msg = ("weight is neither a known attribute name "
                               "nor a simple variable from the choice dataset "
                               "nor an interaction variable: '%s'" % weight)
                    logger.log_error(err_msg)
                    raise ValueError(err_msg)
        elif isinstance(weight, ndarray):
            rank_of_weight = weight.ndim
        elif not weight:  ## weight is None or empty string
            weight = ones(index2.size)
            rank_of_weight = 1
        else:
            err_msg = "unkown weight type"
            logger.log_error(err_msg)
            raise TypeError(err_msg)

        if (weight.size != index2.size) and (weight.shape[rank_of_weight-1] != index2.size):
            if weight.shape[rank_of_weight-1] == choice.size():
                if rank_of_weight == 1:
                    weight = take(weight, index2)
                if rank_of_weight == 2:
                    weight = take(weight, index2, axis=1)
            else:
                err_msg = "weight array size doesn't match to size of dataset2 or its index"
                logger.log_error(err_msg)
                raise ValueError(err_msg)

        prob = normalize(weight)

        #chosen_choice = ones(index1.size) * UNPLACED_ID
        chosen_choice_id = agent.get_attribute(choice.get_id_name()[0])[index1]
        #index_of_placed_agent = where(greater(chosen_choice_id, UNPLACED_ID))[0]
        chosen_choice_index = choice.try_get_id_index(chosen_choice_id, return_value_if_not_found=UNPLACED_ID)
        chosen_choice_index_to_index2 = lookup(chosen_choice_index, index2, index_if_not_found=UNPLACED_ID)
        
        if rank_of_weight == 1: # if weight_array is 1d, then each agent shares the same weight for choices
            replace = with_replacement           # sampling with no replacement 
            non_zero_counts = nonzerocounts(weight)
            if non_zero_counts < J:
                logger.log_warning("weight array dosen't have enough non-zero counts, use sample with replacement")
                replace = True
            if non_zero_counts > 0:
                sampled_index = prob2dsample( index2, sample_size=(index1.size, J),
                                        prob_array=prob, exclude_index=chosen_choice_index_to_index2,
                                        replace=replace, return_index=True )
            else:
                # all alternatives have a zero weight
                sampled_index = zeros((index1.size, 0), dtype=DTYPE)
            #return index2[sampled_index]

        if rank_of_weight == 2:
            sampled_index = zeros((index1.size,J), dtype=DTYPE) - 1
                
            for i in range(index1.size):
                replace = with_replacement          # sampling with/without replacement
                i_prob = prob[i,:]
                if nonzerocounts(i_prob) < J:
                    logger.log_warning("weight array dosen't have enough non-zero counts, use sample with replacement")
                    replace = True

                #exclude_index passed to probsample_noreplace needs to be indexed to index2
                sampled_index[i,:] = probsample_noreplace( index2, sample_size=J, prob_array=i_prob,
                                                     exclude_index=chosen_choice_index_to_index2[i],
                                                     return_index=True )
        sampling_prob = take(prob, sampled_index)
        sampled_index_within_prob = sampled_index.copy()
        sampled_index = index2[sampled_index]
        is_chosen_choice = zeros(sampled_index.shape, dtype="bool")
        #chosen_choice = -1 * ones(chosen_choice_index.size, dtype="int32")
        if include_chosen_choice:
            sampled_index = column_stack((chosen_choice_index[:,newaxis],sampled_index))
            is_chosen_choice = zeros(sampled_index.shape, dtype="bool")
            is_chosen_choice[chosen_choice_index!=UNPLACED_ID, 0] = 1
            #chosen_choice[where(is_chosen_choice)[0]] = where(is_chosen_choice)[1]
            ## this is necessary because prob is indexed to index2, not to the choice set (as is chosen_choice_index)
            sampling_prob_for_chosen_choices = take(prob, chosen_choice_index_to_index2[:, newaxis])
            ## if chosen choice chosen equals unplaced_id then the sampling prob is 0
            sampling_prob_for_chosen_choices[where(chosen_choice_index==UNPLACED_ID)[0],] = 0.0
            sampling_prob = column_stack([sampling_prob_for_chosen_choices, sampling_prob])
        
        interaction_dataset = self.create_interaction_dataset(dataset1, dataset2, index1, sampled_index)
        interaction_dataset.add_attribute(sampling_prob, '__sampling_probability')
        interaction_dataset.add_attribute(is_chosen_choice, 'chosen_choice')
        
        if local_resources.get("include_mnl_bias_correction_term",  False):
            if include_chosen_choice:
                sampled_index_within_prob = column_stack((chosen_choice_index_to_index2[:,newaxis],sampled_index_within_prob))
            interaction_dataset.add_mnl_bias_correction_term(prob, sampled_index_within_prob)
        
        ## to get the older returns
        #sampled_index = interaction_dataset.get_2d_index()
        #chosen_choices = UNPLACED_ID * ones(index1.size, dtype="int32") 
        #where_chosen = where(interaction_dataset.get_attribute("chosen_choice"))
        #chosen_choices[where_chosen[0]]=where_chosen[1]
        #return (sampled_index, chosen_choice)
        
        return interaction_dataset
    
from opus_core.tests import opus_unittest
from numpy import array, all, alltrue, not_equal, equal, repeat, int32, where
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
    
    def setUp(self):
        storage = StorageFactory().get_storage('dict_storage')
    
        storage.write_table(table_name='households',
            table_data={
                'household_id': arange(10)+1,
                'grid_id': arange(-1, 9, 1)+1,
                'lucky':array([1,0,1, 0,1,1, 1,1,0, 0])
                }
            )
    
        storage.write_table(table_name='gridcells',
            table_data={
                'grid_id': arange(15)+1,
                'filter':array([0,1,1, 1,1,1, 1,1,1, 0,1,0, 1,1,1]),
                'weight':array([0.1,9,15, 2,5,1, 6,2.1,.3, 4,3,1, 10,8,7])
                }
            )
    
        #create households
        self.households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")
    
        # create gridcells
        self.gridcells = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name="gridcell")


    def test_1d_weight_array(self):
        """"""
        sample_size = 5
        # check the individual gridcells
        # This is a stochastic model, so it may legitimately fail occassionally.
        index1 = where(self.households.get_attribute("lucky"))[0]
        index2 = where(self.gridcells.get_attribute("filter"))[0]
        weight=self.gridcells.get_attribute("weight")
        for icc in [0,1]: #include_chosen_choice?
            #icc = sample([0,1],1)
            sampler_ret = weighted_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, sample_size=sample_size, weight="weight",include_chosen_choice=icc)
            # get results
            sampled_index = sampler_ret.get_2d_index()
            chosen_choices = UNPLACED_ID * ones(index1.size, dtype=DTYPE) 
            where_chosen = where(sampler_ret.get_attribute("chosen_choice"))
            chosen_choices[where_chosen[0]]=where_chosen[1]

            sample_results = sampled_index, chosen_choices
            sampled_index = sample_results[0]
            self.assertEqual(sampled_index.shape, (index1.size, sample_size))
            if icc:
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)
                chosen_choice_index = resize(array([UNPLACED_ID], dtype=DTYPE), index1.shape)
                w = where(chosen_choices>=0)[0]
                # for 64 bit machines, need to coerce the type to int32 -- on a
                # 32 bit machine the astype(int32) doesn't do anything
                chosen_choice_index[w] = sampled_index[w, chosen_choices[w]]
                self.assertTrue( alltrue(equal(placed_agents_index, chosen_choice_index)) )
                sampled_index = sampled_index[:,1:]
            
            self.assertTrue( alltrue(lookup(sampled_index.ravel(), index2, index_if_not_found=UNPLACED_ID)!=UNPLACED_ID) )
            self.assertTrue( all(not_equal(weight[sampled_index], 0.0)) )

    def test_2d_weight_array(self):
        #2d weight
        sample_size = 5
        n = self.households.size()
        index1 = where(self.households.get_attribute("lucky"))[0]
        index2 = where(self.gridcells.get_attribute("filter"))[0]
        lucky = self.households.get_attribute("lucky")
        weight = repeat(self.gridcells.get_attribute("weight")[newaxis, :], n, axis=0)
        for i in range(n):
            weight[i,:] += lucky[i]

        for icc in [0,1]:
            sampler_ret = weighted_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, sample_size=sample_size, weight=weight,include_chosen_choice=icc)

            sampled_index = sampler_ret.get_2d_index()
            chosen_choices = UNPLACED_ID * ones(index1.size, dtype=DTYPE) 
            where_chosen = where(sampler_ret.get_attribute("chosen_choice"))
            chosen_choices[where_chosen[0]]=where_chosen[1]

            self.assertEqual(sampled_index.shape, (index1.size, sample_size))

            if icc:
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)

                chosen_choice_index = resize(array([UNPLACED_ID], dtype=DTYPE), index1.shape)
                w = where(chosen_choices>=0)[0]
                chosen_choice_index[w] = sampled_index[w, chosen_choices[w]]
                self.assertTrue( alltrue(equal(placed_agents_index, chosen_choice_index)) )
                sampled_index = sampled_index[:,1:]
                
            self.assertTrue( alltrue(lookup(sampled_index.ravel(), index2, index_if_not_found=UNPLACED_ID)!=UNPLACED_ID) )

            for j in range(sample_size):
                self.assertTrue( all(not_equal(weight[j, sampled_index[j,:]], 0.0)) )

if __name__ == "__main__":
    opus_unittest.main()
