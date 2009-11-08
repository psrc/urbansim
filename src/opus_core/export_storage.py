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

from opus_core.logger import logger


class ExportStorage(object):
    def export(self, in_storage, out_storage):
        
        ### TODO: get_dataset_names is not part of the standard Storage interface!
        dataset_names = in_storage.get_dataset_names()
        
        logger.start_block('Exporting tables')
        logger.log_status("Reading tables from '%s'" % in_storage.get_storage_location())
        
        if not dataset_names:
            logger.log_warning('This location has no tables to export!')
            logger.log_warning('Did you specify a location containing the data for a single year?')
        else:
            for dataset_name in dataset_names:
                self.export_dataset(dataset_name, in_storage, out_storage)
                
        logger.end_block()
        
    def export_dataset(self, dataset_name, in_storage, out_storage):
        logger.start_block('Exporting dataset %s' % dataset_name)
        try:
            values_from_storage = in_storage.load_table(dataset_name)
            
            out_storage.write_table(dataset_name, values_from_storage)
        finally:
            logger.end_block()
        
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