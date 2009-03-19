# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.resources import Resources
from numpy import where, arange, take, ones, concatenate
from numpy import newaxis, ndarray, zeros, array, rank, float32
from opus_core.misc import unique_values
from opus_core.samplers.constants import *
from opus_core.sampling_toolbox import prob2dsample, probsample_noreplace, normalize
from opus_core.sampling_toolbox import nonzerocounts
from opus_core.logger import logger
from opus_core.sampler import Sampler
import copy

class stratified_sampler(Sampler):
    def __init__(self):
        """
        initialize internal attributes
        """
        self.sampled_index = None
        self.chosen_choice = None
        self._sampling_probability = None
        self._stratum_id = None

    def run(self, dataset1, dataset2, index1=None, index2=None, stratum=None, weight=None,
            sample_size=1, sample_size_from_each_stratum=None, sample_size_from_chosen_stratum=None, sample_rate=None,
            include_chosen_choice=False, resources=None):
        """this function samples number of sample_size (scalar value) alternatives from dataset2
        for agent set specified by dataset1.
        If index1 is not None, only samples alterantives for agents with indices in index1;
        if index2 is not None, only samples alternatives from indices in index2.
        sample_size specifies number of alternatives to be sampled from each stratum, and is overwritten
          by sample_size_from_each_stratum if it's not None
        weight, to be used as sampling weight, is either an attribute name of dataset2, or a 1d
        array of the same length as index2 or 2d array of shape (index1.size, index2.size).

        Also refer to document of interaction_dataset"""
        local_resources = Resources(resources)
        local_resources.merge_if_not_None(
                {"dataset1": dataset1, "dataset2": dataset2,
                "index1":index1, "index2": index2,
                "stratum":stratum, "weight": weight,
                "sample_size": sample_size,
                "sample_size_from_each_stratum": sample_size_from_each_stratum,
                "sample_size_from_chosen_stratum": sample_size_from_chosen_stratum,
                "sample_rate": sample_rate,
                "include_chosen_choice": include_chosen_choice})

        local_resources.check_obligatory_keys(['dataset1', 'dataset2'])
        index1 = local_resources.get("index1", None)

        agent = dataset1

        if index1 is None:
            agent.get_id_attribute()
            index1 = arange(agent.size())

        choice = local_resources["dataset2"]
        index2 = local_resources.get("index2", None)

        if index2 is None:
            choice.get_id_attribute()
            index2 = arange(choice.size())

        if index1.size == 0 or index2.size == 0:
            err_msg = "either choice size or agent size is zero, return None"
            logger.log_warning(err_msg)
            return (None, None)

        include_chosen_choice = local_resources.get("include_chosen_choice",  False)
        weight = local_resources.get("weight", None)

        if isinstance(weight, str):
            choice.compute_variables(weight,
                resources = local_resources )
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
                weight = take(weight, index2)
            else:
                err_msg = "weight array size doesn't match to size of dataset2 or its index"
                logger.log_error(err_msg)
                raise ValueError, err_msg

        prob = normalize(weight)

        stratum = local_resources.get("stratum", None)
        if isinstance(stratum, str):
            choice.compute_variables(stratum,
                resources = local_resources )
            stratum=choice.get_attribute(stratum)

        #chosen_choice = ones(index1.size) * UNPLACED_ID
        chosen_choice_id = agent.get_attribute(choice.get_id_name()[0])[index1]
        #index_of_placed_agent = where(greater(chosen_choice_id, UNPLACED_ID))[0]
        chosen_choice_index = choice.try_get_id_index(chosen_choice_id, return_value_if_not_found=-1)

        ##TODO: check all chosen strata are in selectable strata
        #i.e. chosen_choice_index is in index2
        chosen_stratum = ones(chosen_choice_index.size, dtype="int32") * NO_STRATUM_ID
        chosen_stratum[where(chosen_choice_index!=-1)] = stratum[chosen_choice_index[where(chosen_choice_index!=-1)]]
        selectable_strata = stratum[index2]
        unique_strata = unique_values(selectable_strata)
        unique_strata = unique_strata[where(unique_strata!=NO_STRATUM_ID)]

#        if rank_of_weight == 2:
#            raise RuntimeError, "stratified sampling for 2d weight is unimplemented yet"

#        sampled_index = zeros((index1.size,1)) - 1

        sample_rate = local_resources.get("sample_rate", None)
        sample_size = local_resources.get("sample_size", None)
        sample_size_from_each_stratum = local_resources.get("sample_size_from_each_stratum", None)
        if sample_size_from_each_stratum is None:
            sample_size_from_each_stratum = sample_size
        strata_sample_size = ones(unique_strata.size, dtype="int32") * sample_size_from_each_stratum
        if sample_rate is not None:
            raise UnSupportedError, "unimplemented"
            ##BUG: to be finished
            num_elements_in_strata = histogram(selectable_strata, unique_strata)
            strata_sample_size = round(num_elements_in_strata * sample_rate)

        sample_size_from_chosen_stratum = local_resources.get("sample_size_from_chosen_stratum", None)
        if sample_size_from_chosen_stratum is None:
            strata_sample_pairs = array(map(lambda x,y: [x,y], unique_strata, strata_sample_size))
            if rank_of_weight == 1:
                sampled_index = self._sample_by_stratum(index1, index2, selectable_strata, prob,
                                                        chosen_choice_index, strata_sample_pairs)
            elif rank_of_weight == 2:
                sampled_index = self._sample_by_agent_and_stratum(index1, index2, selectable_strata, prob,
                                                                  chosen_choice_index, strata_sample_pairs)
        else:
            strata_sample_setting = zeros((index1.size,unique_strata.size,2), dtype="int32")
            for i in range(index1.size):
                agents_strata_sample_size = copy.copy(strata_sample_size)
                agents_strata_sample_size[where(unique_strata==chosen_stratum[i])] = sample_size_from_chosen_stratum
                strata_sample_pairs = array(map(lambda x,y: [x,y], unique_strata, agents_strata_sample_size))
                strata_sample_setting[i,...] = strata_sample_pairs

            sampled_index = self._sample_by_agent_and_stratum(index1, index2, selectable_strata, prob,
                                                              chosen_choice_index, strata_sample_setting)
        chosen_choice = None
        if include_chosen_choice:
            sampled_index = concatenate((chosen_choice_index[:,newaxis],sampled_index), axis=1)
            chosen_choice = zeros(chosen_choice_index.shape, dtype="int32") - 1
            chosen_choice[where(chosen_choice_index>UNPLACED_ID)] = 0 #make chosen_choice index to sampled_index, instead of choice (as chosen_choice_index does)
                                                                      #since the chosen choice index is attached to the first column, the chosen choice should be all zeros
                                                                      #for valid chosen_choice_index

            chosen_probability = zeros((chosen_choice_index.size,),dtype=float32) - 1
            for stratum in unique_strata:
                w = chosen_stratum==stratum
                chosen_probability[w] = (prob[chosen_choice_index[w]] / prob[selectable_strata==stratum].sum()).astype(float32)
            self._sampling_probability = concatenate((chosen_probability[:,newaxis], self._sampling_probability), axis=1)
            self._stratum_id = concatenate((chosen_stratum[:,newaxis], self._stratum_id), axis=1)
        return (sampled_index, chosen_choice)


    def _sample_by_stratum(self, index1, index2, stratum, prob_array, chosen_choice_index, strata_sample_setting):
        """stratum by stratum stratified sampling, suitable for 1d prob_array and sample_size is the same for all agents"""
        if prob_array.ndim <> 1:
            raise RuntimeError, "_sample_by_stratum only suitable for 1d prob_array"

        sampled_index = zeros((index1.size,1), dtype="int32") - 1
        self._sampling_probability = zeros((index1.size,1),dtype=float32)
        self._stratum_id = ones((index1.size,1), dtype="int32") * NO_STRATUM_ID
        for this_stratum, this_size in strata_sample_setting:
            index_not_in_stratum = where(stratum!=this_stratum)[0]
            this_prob = copy.copy(prob_array)

            this_prob[index_not_in_stratum] = 0.0
            this_prob = normalize(this_prob)

            replace = False           # non-repeat sampling
            if nonzerocounts(this_prob) < this_size:
                logger.log_warning("weight array dosen't have enough non-zero counts, sample with replacement")
                replace = True

            this_sampled_index = prob2dsample( index2, sample_size=(index1.size, this_size),
                                                      prob_array=this_prob, exclude_index=chosen_choice_index,
                                                      replace=replace, return_indices=True )
            sampled_index = concatenate( (sampled_index,
                                          this_sampled_index),
                                          axis=1)
            self._sampling_probability = concatenate( (self._sampling_probability,
                                                       this_prob[this_sampled_index]),
                                                       axis=1)
            self._stratum_id = concatenate( (self._stratum_id,
                                             ones( (this_sampled_index.size,1) , dtype="int32") * this_stratum ),
                                             axis=1)

        self._sampling_probability = self._sampling_probability[:, 1:]
        self._stratum_id = self._stratum_id[:, 1:]
        return index2[sampled_index[:, 1:]]

    def _sample_by_agent_and_stratum(self, index1, index2, stratum, prob_array, chosen_choice_index, strata_sample_setting):
        """agent by agent and stratum by stratum stratified sampling, suitable for 2d prob_array and/or sample_size varies for agents
        this method is slower than _sample_by_stratum, for simpler stratified sampling use _sample_by_stratum instead"""

        rank_of_prob = rank(prob_array)
        rank_of_strata = rank(strata_sample_setting)

        J = self.__determine_sampled_index_size(strata_sample_setting, rank_of_strata)
        sampled_index = zeros((index1.size,J), dtype="int32") - 1
        self._sampling_probability = zeros( (index1.size,J ), dtype=float32)
        self._stratum_id = ones( (index1.size,J) , dtype="int32") * NO_STRATUM_ID

        for i in range(index1.size):
            if rank_of_strata == 3:
                strata_sample_pairs = strata_sample_setting[i, :]
            else:
                strata_sample_pairs = strata_sample_setting

            if rank_of_prob == 2:
                prob = prob_array[i, :]
            else:
                prob = prob_array

            j = 0
            for (this_stratum, this_size) in strata_sample_pairs:
                if this_size <= 0: continue
                index_not_in_stratum = where(stratum!=this_stratum)[0]
                this_prob = copy.copy(prob)

                this_prob[index_not_in_stratum] = 0.0
                this_prob = normalize(this_prob)

                if nonzerocounts(this_prob) < this_size:
                    logger.log_warning("weight array dosen't have enough non-zero counts, use sample with replacement")

                chosen_index_to_index2 = where(index2 == chosen_choice_index[i])[0]
                #exclude_index passed to probsample_noreplace needs to be indexed to index2
                this_sampled_index = probsample_noreplace( index2, sample_size=this_size,
                                                          prob_array=this_prob, exclude_index=chosen_index_to_index2,
                                                          return_indices=True )
                sampled_index[i,j:j+this_size] = this_sampled_index

                self._sampling_probability[i,j:j+this_size] = this_prob[this_sampled_index]
                self._stratum_id[i,j:j+this_size] = ones( (this_sampled_index.size,) , dtype="int32") * this_stratum

                j += this_size

        return index2[sampled_index]

    def __determine_sampled_index_size(self, strata_sample_setting, rank_of_strata):
        """determin the maximum number of column in sampled_index"""
        maxc = 0
        if rank_of_strata == 3:
            for i in range(strata_sample_setting.shape[0]):
                t = sum([y for x,y in strata_sample_setting[i,:]])
                if t > maxc: maxc = t
        else:
            maxc = sum([y for x,y in strata_sample_setting])

        return maxc


from opus_core.tests import opus_unittest
from numpy import all, alltrue, not_equal, equal, int32
from opus_core.datasets.dataset import Dataset
from opus_core.samplers.constants import *
from opus_core.storage_factory import StorageFactory


class Test(opus_unittest.OpusTestCase):
    storage = StorageFactory().get_storage('dict_storage')

    storage.write_table(table_name='households',
        table_data={
            'household_id': arange(10)+1,
            'grid_id': array([-1] + range(1, 10)),
            'lucky':array([1,0,1, 0,1,1, 1,1,0, 0])
            }
        )

    storage.write_table(table_name='gridcells',
        table_data={
            "grid_id": arange(15)+1,
            "filter":array([0,1,1, 1,1,1, 1,1,1, 0,1,0, 1,1,1]),
            "weight":array([0.1,9,15, 2,5,1, 6,2.1,.3, 4,3,1, 10,8,7]),
            "stratum_id":array([1,1,5, 2,3,4, 3,2,4, 3,1,2, -1,4,5])
            }
        )

    households = Dataset(in_storage=storage, in_table_name='households', id_name="household_id", dataset_name="household")

    # create gridcells
    num_strata = 5
    gridcells = Dataset(in_storage=storage, in_table_name='gridcells', id_name="grid_id", dataset_name="gridcell")

    def test_1d_weight_array(self):
        """"""
        # check the individual gridcells
        # This is a stochastic model, so it may legitimately fail occassionally.
        index1 = where(self.households.get_attribute("lucky"))[0]
        index2 = where(self.gridcells.get_attribute("filter"))[0]
        weight=self.gridcells.get_attribute("weight")
        for icc in [0,1]:
            #icc = sample([0,1],1)   #include_chosen_choice?
            sample_results = stratified_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, stratum="stratum_id", sample_size=1, weight="weight",
                            include_chosen_choice=icc)
            # get results
            sampler = sample_results[0]
            if icc:
                self.assertEqual(sampler.shape, (index1.size,self.num_strata+1))
            else:
                self.assertEqual(sampler.shape, (index1.size,self.num_strata))

            if icc:
                self.assertEqual( sample_results[1].size, index1.size)
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)
                chosen_choice_index = UNPLACED_ID * ones(index1.shape, dtype="int32")
                w = where(sample_results[1]>=0)[0]
                # for 64 bit machines, need to coerce the type to int32 -- on a
                # 32 bit machine the astype(int32) doesn't do anything
                chosen_choice_index[w] = sampler[w, sample_results[1][w]].astype(int32)
                assert alltrue(equal(placed_agents_index, chosen_choice_index))
                sampler = sampler[:,1:]
            assert alltrue([x in index2 for x in sampler.ravel()])
            assert all(not_equal(weight[sampler], 0.0)), "elements with zero weight in the sample"

    def test_1d_weight_array_variant_sample_size(self):

        sample_size_from_chosen_stratum = 2
        index1 = where(self.households.get_attribute("lucky"))[0]
        index2 = where(self.gridcells.get_attribute("filter"))[0]
        weight=self.gridcells.get_attribute("weight")
        for icc in [0,1]:

            #icc = sample([0,1],1)   #include_chosen_choice?
            sample_results = stratified_sampler().run(dataset1=self.households, dataset2=self.gridcells, index1=index1,
                            index2=index2, stratum="stratum_id", sample_size=0,
                            sample_size_from_chosen_stratum = sample_size_from_chosen_stratum,
                            weight="weight",include_chosen_choice=icc)
            # get results
            sampler = sample_results[0]
            if icc:
                self.assertEqual(sampler.shape, (index1.size,sample_size_from_chosen_stratum+1))
            else:
                self.assertEqual(sampler.shape, (index1.size,sample_size_from_chosen_stratum))

            if icc:
                self.assertEqual( sample_results[1].size, index1.size)
                placed_agents_index = self.gridcells.try_get_id_index(
                                        self.households.get_attribute("grid_id")[index1],UNPLACED_ID)
                chosen_choice_index = UNPLACED_ID * ones(index1.shape, dtype="int32")
                w = where(sample_results[1]>=0)[0]
                chosen_choice_index[w] = sampler[w, sample_results[1][w]].astype(int32)
                assert alltrue(equal(placed_agents_index, chosen_choice_index))
                sampler = sampler[:,1:]
            assert alltrue([x in index2 for x in sampler.ravel()])
            assert all(not_equal(weight[sampler], 0.0)), "elements with zero weight in the sample"

if __name__ == "__main__":
    opus_unittest.main()
