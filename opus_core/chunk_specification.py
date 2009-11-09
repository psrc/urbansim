# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from math import ceil
from numpy import array, ndarray
from opus_core.logger import logger

class ChunkSpecification(object):
    """
    A specification used to determine the number of chunks to use in a
    ChunkModel.
    """
    _data = None

    def __init__(self, config):
        """
        config is a Configuration containing either:
        'nchunks':<value>, or
        'records_per_chunk':<value>
        config also may be a string representation of a dictionary, e.g. "{'nchunks':3}"
        """
        if isinstance(config, str):
            config = eval(config)
        for spec_type in ['records_per_chunk', 'nchunks']:
            if spec_type in config:
                self._data = {
                    'func_name':'self._%s' % spec_type,
                    spec_type:config[spec_type]
                    }
                return
        else:
            logger.log_warning('Invalid ChunkSpecification configuration: %s' % config)

    def _nchunks(self, dataset):
        return self._data['nchunks']

    def _records_per_chunk(self, dataset):
        return int(ceil(self.get_dataset_size(dataset) / float(self._data['records_per_chunk'])))

    def nchunks(self, dataset=None):
        if self._data:
            return eval(self._data['func_name'])(dataset)
        else:
            return 1

    def chunk_size(self, dataset=None):
        nchunks = self.nchunks(dataset)
        return int(ceil(self.get_dataset_size(dataset) / float(nchunks)))

    def get_dataset_size(self, dataset):
        if isinstance(dataset, ndarray):
            return dataset.size # dataset is an numpy array
        return dataset.size() # dataset is instance of Dataset

from opus_core.tests import opus_unittest


class ChunkSpecificationTests(opus_unittest.OpusTestCase):
    def test_nchunks_for_nchunks(self):
        spec = ChunkSpecification({'nchunks':3})
        self.assertEqual(3, spec.nchunks())
        spec = ChunkSpecification("{'nchunks':3}")
        self.assertEqual(3, spec.nchunks())

    def test_configuration(self):
        from opus_core.configuration import Configuration
        spec = ChunkSpecification(Configuration({'nchunks':3}))
        self.assertEqual(3, spec.nchunks())

    def test_test_invalid_spec(self):
        from opus_core.configuration import Configuration
        logger.enable_hidden_error_and_warning_words()
        spec = ChunkSpecification(Configuration({'fnchunks':3}))
        logger.disable_hidden_error_and_warning_words()

    def test_nchunks_for_records_per_chunk(self):
        dataset = MockDataset(1000)
        spec = ChunkSpecification({'records_per_chunk':10})
        self.assertEqual(100, spec.nchunks(dataset=dataset))
        spec = ChunkSpecification({'records_per_chunk':999})
        self.assertEqual(2, spec.nchunks(dataset=dataset))
        spec = ChunkSpecification({'records_per_chunk':1001})
        self.assertEqual(1, spec.nchunks(dataset=dataset))

        dataset = MockDataset(0)
        spec = ChunkSpecification({'records_per_chunk':10})
        self.assertEqual(0, spec.nchunks(dataset=dataset))

        dataset = array(1000*[0])
        spec = ChunkSpecification({'records_per_chunk':10})
        self.assertEqual(100, spec.nchunks(dataset=dataset))

class MockDataset(object):
    def __init__(self, size):
        self._size = size
    def size(self):
        return self._size

if __name__ == '__main__':
    opus_unittest.main()