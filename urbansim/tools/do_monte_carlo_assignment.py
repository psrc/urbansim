# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
from urbansim.models.monte_carlo_assignment_model import MonteCarloAssignmentModel
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
import sys

class AssignmentOptionGroup:
    def __init__(self, usage="python %prog <-c /cache/directory> <-i individual_table_name> <-f fraction_table_name> <--id-name1=dataset1_id> <--id-name2=dataset2_id> [--fraction-attribute-name=fraction] [--help]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-c", "--cache-directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory containing cache for the simulated years")
        self.parser.add_option("-i", "--individual-table", dest="individual_table", default = None, type="str",
                               action="store", help="name of the cache table containing individuals to be assigned")
        self.parser.add_option("-f", "--fraction-table", dest="fraction_table", default = None, type="str",
                               action="store", help="name of the cache table containing fraction of dataset1 in dataset2")
        self.parser.add_option("--id-name1", dest="id_name1", default = None, type="str",
                               action="store", help="the id_name of dataset1, which individuals have already been assigned to")
        self.parser.add_option("--id-name2", dest="id_name2", default = None, type="str",
                               action="store", help="the id_name of dataset2, which individuals will be assigned to")
        self.parser.add_option("--fraction-attribute-name", dest="fraction_attribute_name", default = "fraction", type="str",
                               action="store", help="the attribute name in fraction table containing the fraction of dataset1 in dataset2, by default fraction")
        
if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    option_group = AssignmentOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    if options.cache_directory is None:
        parser.print_usage()
        sys.exit()

    individual_table = options.individual_table
    fraction_table = options.fraction_table
    fraction_attribute_name = options.fraction_attribute_name
    storage = StorageFactory().get_storage('flt_storage', storage_location=options.cache_directory)
    individual_dataset = Dataset(in_storage=storage, id_name=[], in_table_name=individual_table)
    fraction_dataset = Dataset(in_storage=storage, id_name=[], in_table_name=fraction_table)
    
    MonteCarloAssignmentModel().run(individual_dataset, fraction_dataset, 
                                    id_name1=options.id_name1, id_name2=options.id_name2,
                                    fraction_attribute_name=options.fraction_attribute_name)
    
    individual_dataset.write_dataset(out_storage=storage, out_table_name=individual_table, attributes=[options.id_name2])
    