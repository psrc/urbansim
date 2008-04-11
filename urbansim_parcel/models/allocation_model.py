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

from opus_core.allocation_model import AllocationModel as AM
from inprocess.jrayers.excel_document import ExcelDocument
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset

class AllocationModel(AM):
    def prepare_for_run(self, dataset=None, control_totals=None, excel_path=None, excel_data_info={}, esri_storage_location=None,
                        dataset_name=None, dataset_pool=None):
        
        if control_totals is None:
            print "geting excel document data"
            excel_doc = ExcelDocument()
            excel_doc.open(excel_path)
            
            #list_of_column_names = ['year', 'persons']
            #list_of_ranges = ['d22:d32', 'k22:k32']
            control_total_data = excel_doc.get_dict_table_from_column_names_and_ranges(excel_data_info)
            
            #print control_total_data
            
            print "getting dict storage"
            dict_storage = StorageFactory().get_storage('dict_storage')
            dict_storage.write_table(table_name = 'control_totals', table_data = control_total_data)

            print "getting control total data as 'dataset'"
            control_totals = Dataset(in_storage = dict_storage, in_table_name = 'control_totals', id_name='year')

        if dataset is None:
            print "getting esri storage"
            esri_storage = StorageFactory().get_storage('esri_storage', storage_location=esri_storage_location)
                        
            print "getting hotel data as 'dataset'"
            dataset = Dataset(in_storage=esri_storage, in_table_name=dataset_name, id_name=dataset_name+'_id', dataset_name=dataset_name)
        
        dataset_pool.add_datasets_if_not_included({dataset_name:dataset, control_totals.get_dataset_name():control_totals})
        
        return (dataset, control_totals)