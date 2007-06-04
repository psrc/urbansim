#
# UrbanSim software. Copyright (C) 1998-2007 University of Washington
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

from numpy import array, arange, ndarray, float32, zeros
from opus_core.misc import DebugPrinter
from opus_core.model import Model
from opus_core.datasets.dataset import DatasetSubset
from opus_core.logger import logger
from opus_core.chunk_specification import ChunkSpecification
from math import ceil
from time import time

class ChunkModel(Model):
    """ Class for processing a model in chunks.
    """

    debug = DebugPrinter(0)
    __default_records_per_chunk = 1000

    model_short_name="ChunkM" # abbreviation of the model

    def run(self, chunk_specification, dataset, dataset_index=None, result_array_type=float32, **kwargs):
        """ 'chunk_specification' - determines number of chunks to use when computing over
                the dataset set.
            'dataset' - an object of class Dataset that is to be chunked.
            'dataset_index' - index of individuals in dataset to be chunked.
            'result_array_type' - type of the resulting array. Can be any numerical type of numpy array.
            **kwargs - keyword arguments.
            The method chunks dataset_index in the desired number of chunks (minimum is 1) and for each chunk it calls the method
            'run_chunk'. The order of the individuals entering the chunking is determined by the method 'get_agents_order'.
        """
        if dataset_index==None:
            dataset_index=arange(dataset.size())
        if not isinstance(dataset_index,ndarray):
            dataset_index=array(dataset_index)
        logger.log_status("Total number of individuals: %s" % dataset_index.size)
        result_array = zeros(dataset_index.size, dtype=result_array_type)

        if dataset_index.size <= 0:
            logger.log_status("Nothing to be done.")
            return result_array

        all_indexed_individuals = DatasetSubset(dataset, dataset_index)
        ordered_agent_indices = self.get_agents_order(all_indexed_individuals)# set order of individuals in chunks

        # TODO: Remove next six lines after we inherit chunk specification as a text string.
        if (chunk_specification is None):
            chunk_specification = {'nchunks':1}
        chunker = ChunkSpecification(chunk_specification)
        nchunks = chunker.nchunks(dataset_index)
        chunksize = int(ceil(all_indexed_individuals.size()/float(nchunks)))
        for ichunk in range(nchunks):
            logger.start_block("%s chunk %d out of %d."
                               % (self.model_short_name, (ichunk+1), nchunks))
            try:
                chunk_agent_indices = ordered_agent_indices[arange((ichunk*chunksize),
                                                                   min((ichunk+1)*chunksize,
                                                                       all_indexed_individuals.size()))]
                logger.log_status("Number of agents in this chunk: %s" % chunk_agent_indices.size)
                result_array[chunk_agent_indices] = self.run_chunk(dataset_index[chunk_agent_indices],
                                                                   dataset, **kwargs).astype(result_array_type)
            finally:
                logger.end_block()

        return result_array

    def get_agents_order(self, dataset):
        """ Return desired order of individuals within a dataset containig only agents for chunking.
        """
        return arange(dataset.size())

    def run_chunk(self, index, dataset, *args, **kwargs):
        raise NotImplementedError, "Method 'run_chunk' for this model not implemented."

