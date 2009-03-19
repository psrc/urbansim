# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.allocation_model import AllocationModel as AM
from opus_core.store.excel_document import ExcelDocument
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset_factory import DatasetFactory
from opus_core.datasets.dataset import Dataset
from opus_core.logger import logger

class AllocationModel(AM):
    def prepare_for_run(self, dataset=None, control_totals=None, weight_attribute=None, excel_path=None, excel_sheet_number=1, excel_data_info={}, esri_storage_location=None,
                        dataset_name=None, current_year=0, datasets_and_weights_in_years=None, dataset_pool=None):
        """
        If dataset is not given, it is loaded from the esri storage. In such a case, dataset_name should be the name of the shape file (without postfix).
        If control_totals is not given, it is loaded from an excel table.
        datasets_and_weights_in_years is a dictionary with years as keys and tuples of dataset_name and weight attribute as values.
        If its given and it has a value for the current year, its value overwrites the arguments 'dataset_name' and 'weight_attribute'.
        The method returns a tuple wit three elements: dataset (Dataset object), control_totals (Dataset object), weight_attribute (string)
        Those are going to be used in the run method.
        """
        if control_totals is None:
            logger.log_status("Getting data from Excel for AllocationModel")
            excel_doc = ExcelDocument()
            excel_doc.open(excel_path)
            excel_doc.set_sheet(excel_sheet_number)

            control_total_data = excel_doc.get_dict_table_from_column_names_and_ranges(excel_data_info)
            excel_doc.close()
            excel_doc.quit()
            del excel_doc
            
            dict_storage = StorageFactory().get_storage('dict_storage')
            dict_storage.write_table(table_name = 'control_totals', table_data = control_total_data)

            control_totals = Dataset(in_storage = dict_storage, in_table_name = 'control_totals', id_name='year')

        if datasets_and_weights_in_years is not None and current_year in datasets_and_weights_in_years.keys():
            dataset_name, weight_attribute = datasets_and_weights_in_years[current_year]
            dataset = None
            
        if dataset is None:
            logger.log_status("Getting data from esri_storage for AllocationModel")
            esri_storage = StorageFactory().get_storage('esri_storage', storage_location=esri_storage_location)
                        
           #Was: dataset = Dataset(in_storage=esri_storage, in_table_name=dataset_name, id_name=dataset_name+'_id', dataset_name=dataset_name)
            dataset = DatasetFactory().search_for_dataset(dataset_name, dataset_pool.get_package_order(), arguments={'in_storage': esri_storage, 'id_name':dataset_name+'_id'} )
        dataset_pool.add_datasets_if_not_included({dataset_name:dataset, control_totals.get_dataset_name():control_totals})
        
        return (dataset, control_totals, weight_attribute)