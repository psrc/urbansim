# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from math import ceil

class ExportStorage(object):
    '''Manages the transfer of data from one storage object to another.'''
    
    def export(self, in_storage, out_storage, **kwargs):
        
        dataset_names = in_storage.get_table_names()
        
        with logger.block('Exporting tables'):
            logger.log_status("Reading tables from '%s'" % in_storage.get_storage_location())
            
            if not dataset_names:
                logger.log_warning('This location has no tables to export!')
                logger.log_warning('Did you specify a location containing the data for a single year?')
            else:
                for dataset_name in dataset_names:
                    self.export_dataset(dataset_name, in_storage, out_storage, **kwargs)
        
    def export_dataset(self, dataset_name, in_storage, out_storage, overwrite=True, out_dataset_name=None, nchunks = 1, **kwargs):
        if not overwrite and dataset_name in out_storage.get_table_names():
            logger.log_note('Dataset %s ignored because it already exists in OPUS' % dataset_name)
            return
        with logger.block('Exporting dataset %s' % dataset_name):
            if out_dataset_name is None:
                out_dataset_name = dataset_name
            cols_in_this_chunk = in_storage.ALL_COLUMNS
            if nchunks > 1:
                colnames = in_storage.get_column_names(dataset_name)
                chunk_size = int(ceil(len(colnames) / float(nchunks)))
            for chunk in range(nchunks):
                if nchunks > 1:
                    cols_in_this_chunk = colnames[int(chunk*chunk_size):int((chunk+1)*chunk_size)]
                with logger.block('Loading %s - chunk %s out of %s' % (dataset_name, chunk+1, nchunks)):
                    values_from_storage = in_storage.load_table(dataset_name, column_names=cols_in_this_chunk)
                    length = len(values_from_storage) and len(list(values_from_storage.values())[0])
                    if  length == 0:
                        logger.log_warning("Dataset %s ignored because it's empty" % dataset_name)
                        return
                with logger.block('Storing %s' % dataset_name):
                    if chunk > 0:
                        kwargs['mode'] = out_storage.APPEND
                    out_storage.write_table(out_dataset_name, values_from_storage, **kwargs)
            logger.log_note("Exported %s records for dataset %s" % (length, dataset_name))
        
from opus_core.tests import opus_unittest


class TestExportStorage(opus_unittest.OpusTestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    ### TODO:
    def test_export_storage(self):
        pass


if __name__ == '__main__':
    opus_unittest.main()
