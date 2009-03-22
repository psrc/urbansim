# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.resources import Resources
from numpy import where, arange, take, ones, newaxis, ndarray, zeros, concatenate, resize
from opus_core.samplers.constants import UNPLACED_ID
from opus_core.sampling_toolbox import prob2dsample, probsample_noreplace, normalize
from opus_core.sampling_toolbox import nonzerocounts
from opus_core.logger import logger
from opus_core.sampler import Sampler

class weighted_sampler(Sampler):

    def run(self, dataset1, dataset2, index1=None, index2=None, sample_size=10, weight=None,
            include_chosen_choice=False, resources=None):
        """this function samples number of sample_size (scalar value) alternatives from dataset2
        for agent set specified by dataset1.
        If index1 is not None, only samples alterantives for agents with indices in index1;
        if index2 is not None, only samples alternatives from indices in index2.
        sample_size specifies number of alternatives to be sampled for each agent.
        weight, to be used as sampling weight, is either an attribute name of dataset2, or a 1d
        array of the same length as index2 or 2d array of shape (index1.size, index2.size).

        Also refer to document of interaction_dataset"""

        local_resources = Resources(resources)
        local_resources.merge_if_not_None(
                {"dataset1": dataset1, "dataset2": dataset2,
                "index1":index1, "index2": index2,
                "sample_size": sample_size, "weight": weight,
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
        include_chosen_choice = local_resources.get("include_chosen_choice",  False)
        J = local_resources["sample_size"]
        if include_chosen_choice:
            J = J - 1
        weight = local_resources.get("weight", None)

        if index1.size == 0 or index2.size == 0:
            err_msg = "either choice size or agent size is zero, return None"
            logger.log_warning(err_msg)
            return (None, None)

        if isinstance(weight, str):
            choice.compute_variables(weight, resources=local_resources)
            weight=choice.get_attribute(weight)
            rank_of_weight = 1
        elif isinstance(weight, ndarray):
            rank_of_weight = weight.ndim
        elif weight is None:
            weight = ones(index2.size)
            rank_of_weight = 1
        else:
            err_msg = "unkown weight type"
            logger.log_error(err_msg)
            raise TypeError, err_msg

        if (weight.size <> index2.size) and (weight.shape[rank_of_weight-1] <> index2.size):
            if weight.shape[rank_of_weight-1] == choice.size():
                if rank_of_weight == 1:
                    weight = take(weight, index2)
                if rank_of_weight == 2:
                    weight = take(weight, index2, axis=1)
            else:
                err_msg = "weight array size doesn't match to size of dataset2 or its index"
                logger.log_error(err_msg)
                raise ValueError, err_msg

        prob = normalize(weight)

        #chosen_choice = ones(index1.size) * UNPLACED_ID
        chosen_choice_id = agent.get_attribute(choice.get_id_name()[0])[index1]
        #index_of_placed_agent = where(greater(chosen_choice_id, UNPLACED_ID))[0]
        chosen_choice_index = choice.try_get_id_index(chosen_choice_id, return_value_if_not_found=-1)

        if rank_of_weight == 1: # if weight_array is 1d, then each agent shares the same weight for choices
            replace = False           # no repeat sampling
            if nonzerocounts(weight) < J:
                logger.log_warning("weight array dosen't have enough non-zero counts, use sample with replacement")
                replace = True
            sampled_index = prob2dsample( index2, sample_size=(index1.size, J),
                                        prob_array=prob, exclude_index=chosen_choice_index,
                                        replace=replace, return_indices=True )
            #return index2[sampled_index]

        if rank_of_weight == 2:
            sampled_index = zeros((index1.size,J), dtype="int32") - 1
            for i in range(index1.size):
                replace = False          # no repeat sampling
                i_prob = prob[i,:]
                if nonzerocounts(i_prob) < J:
                    logger.log_warning("weight array dosen't have enough non-zero counts, use sample with replacement")
                    replace = True

                chosen_index_to_index2 = where(index2 == chosen_choice_index[i])[0]
                #exclude_index passed to probsample_noreplace needs to be indexed to index2
                sampled_index[i,:] = probsample_noreplace( index2, sample_size=J, prob_array=i_prob,
                                                     exclude_index=chosen_index_to_index2,
                                                     return_indices=True )
        sampled_index = index2[sampled_index]
        chosen_choice = None
        if include_chosen_choice:
            sampled_index = concatenate((chosen_choice_index[:,newaxis],sampled_index), axis=1)
            chosen_choice = chosen_choice_index
            chosen_choice[chosen_choice_index>UNPLACED_ID] = 0 #make chosen_choice index to sampled_index, instead of choice (as chosen_choice_index does)
                                                               #since the chosen choice index is attached to the first column, the chosen choice should be all zeros
                                                              #for valid chosen_choice_index
        return (sampled_index, chosen_choice)


from opus_core.tests import opus_unittest
from numpy import array, all, alltrue, not_equal, equal, repeat, int32
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
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
    households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

    # create gridcells
    gridcells = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name="gridcell")


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
            sample_results = weighted_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, sample_size=sample_size, weight="weight",include_chosen_choice=icc)
            # get results
            sampler = sample_results[0]
            self.assertEqual(sampler.shape, (index1.size, sample_size))
            if icc:
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)
                chosen_choice_index = resize(array([UNPLACED_ID], dtype="int32"), index1.shape)
                w = where(sample_results[1]>=0)[0]
                # for 64 bit machines, need to coerce the type to int32 -- on a
                # 32 bit machine the astype(int32) doesn't do anything
                chosen_choice_index[w] = sampler[w, sample_results[1][w]].astype(int32)
                assert alltrue(equal(placed_agents_index, chosen_choice_index))
                sampler = sampler[:,1:]
            assert alltrue([x in index2 for x in sampler.ravel()])
            assert all(not_equal(weight[sampler], 0.0)), "elements with zero weight in the sample"

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
            sampled_index, chosen_choices = weighted_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, sample_size=sample_size, weight=weight,include_chosen_choice=icc)
            self.assertEqual(sampled_index.shape, (index1.size, sample_size))

            if icc:
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)

                chosen_choice_index = resize(array([UNPLACED_ID], dtype="int32"), index1.shape)
                w = where(chosen_choices>=0)[0]
                chosen_choice_index[w] = sampled_index[w, chosen_choices[w]].astype(int32)
                assert alltrue(equal(placed_agents_index, chosen_choice_index))
                sampled_index = sampled_index[:,1:]
            assert alltrue([x in index2 for x in sampled_index.ravel()])
            for j in range(sample_size):
                assert all(not_equal(weight[j, sampled_index[j,:]], 0.0)), "elements with zero weight in the sample"

if __name__ == "__main__":
    opus_unittest.main()
