# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

import os
import shutil
from opus_core.storage_factory import StorageFactory
from opus_core.datasets.dataset import Dataset
from opus_core.variables.attribute_type import AttributeType
from opus_core.logger import logger

class SpatialTableJoin:
    """ Do a table join on spatial data.
    """
    def run(self, spatial_table_name, storage_type, data_path, dataset, attribute_names, join_attribute=None, new_table_name=None, 
            files_to_copy_postfix=['shp', 'shx']):
        logger.start_block('Run SpatialTableJoin')
        storage = StorageFactory().get_storage(type=storage_type, storage_location=data_path)
        spatial_dataset = Dataset(in_storage=storage, in_table_name=spatial_table_name, dataset_name='spatial_dataset', id_name=[])
        spatial_dataset.join(dataset, name=attribute_names, join_attribute=join_attribute, metadata=AttributeType.PRIMARY)
        if new_table_name is None:
            out_table_name = spatial_table_name
        else:
            out_table_name = new_table_name
            for postfix in files_to_copy_postfix:
                file_name = os.path.join(data_path, '%s.%s' % (spatial_table_name, postfix))
                if os.path.exists(file_name):
                    new_file_name = os.path.join(data_path, '%s.%s' % (new_table_name, postfix))
                    logger.log_status('Copying %s into %s.' % (file_name, new_file_name))
                    shutil.copy(file_name, new_file_name)
        logger.log_status('New table written into %s/%s.' % (data_path, out_table_name))
        spatial_dataset.write_dataset(out_storage=storage, out_table_name=out_table_name, attributes=AttributeType.PRIMARY)
        logger.end_block()
        
if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser(description="""Does a table join on spatial table and attribute(s) of given dataset. 
Output is written into either the same table or to a table of the given name. Files of the same name as the spatial table 
but different suffix can be copied under the new name.
""")
    parser.add_option('-t', "--spatial-table-name", dest="spatial_table_name", action="store", type="string",
                      help="Table name containing spatial geography information (without postfix).")
    parser.add_option("--storage-type", dest="storage_type", action="store", type="string",
                      help="Storage type of the spatial table, such as dbf_storage, esri_storage.")
    parser.add_option("--data-path", dest="data_path", action="store", type="string",
                      help="Directory where the spatial table lives.")
    parser.add_option("--dataset-name", dest="dataset_name", action="store", type="string", default=None,
                      help="Dataset name that contains attributes to be added to the spatial table. If it is not given, options dataset-table-name and dataset-id-name must be given.")
    parser.add_option("--cache-directory", dest="cache_directory", action="store", type="string",
                      help="Cache directory containing the dataset given by dataset-name.")
    parser.add_option('-a', "--attribute-names", dest="attribute_names", action="store", type="string",
                      help="Name(s) of the attributes to be added to the spatial table. If it's a list, use this format (with no spaces and with the backslashes!):[\\'attr1\\',\\'attr2\\']")
    parser.add_option("--join-attribute", dest="join_attribute", action="store", type="string", default=None, 
                      help="Attribute name of the spatial table which is matched to the id-attribute of dataset.")
    parser.add_option('-n', "--new-table-name", dest="new_table_name", action="store", type="string", default=None,
                      help="Name of the resulting table (without postfix).")
    parser.add_option("--files-to-copy-postfix", dest="files_to_copy_postfix", action="store", type="string", default=[],
                      help="List of postfices of the spatial table to be copied. Use this format (with no spaces and with the backslashes!):[\\'shp\\',\\'sbx\\']")
    parser.add_option("--dataset-table-name", dest="dataset_table_name", action="store", type="string", default=None,
                      help="Dataset table name (should be given if option dataset-name is missing).")
    parser.add_option("--dataset-id-name", dest="dataset_id_name", action="store", type="string", default=[],
                      help="Dataset id name (should be given if option dataset-name is missing).")

    (options, args) = parser.parse_args()
    
    from opus_core.datasets.dataset_pool import DatasetPool
    pool_storage=StorageFactory().get_storage('flt_storage', storage_location=options.cache_directory)
    dataset_pool=DatasetPool(storage=pool_storage)
    try:
        dataset = dataset_pool.get_dataset(options.dataset_name)
    except:
        try:
            id_name = eval(options.dataset_id_name) # in case it is a list
        except:
            id_name = options.dataset_id_name
        dataset = Dataset(in_storage=pool_storage, in_table_name=options.dataset_table_name, id_name=id_name)
    try:
        attr_names = eval(options.attribute_names) # in case it is a list
    except:
        attr_names = options.attribute_names

    try:
        postfices = eval(options.files_to_copy_postfix) # in case it is a list
    except:
        postfices = options.files_to_copy_postfix
    if not isinstance(postfices, list):
        postfices = [postfices]

    SpatialTableJoin().run(spatial_table_name=options.spatial_table_name, storage_type=options.storage_type, 
                           data_path=options.data_path, dataset=dataset, attribute_names=attr_names, 
                           join_attribute=options.join_attribute, new_table_name=options.new_table_name,
                           files_to_copy_postfix=postfices)
    
            
        