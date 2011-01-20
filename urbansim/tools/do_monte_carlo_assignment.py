# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
#from urbansim.models.monte_carlo_assignment_model import MonteCarloAssignmentModel
from opus_core.datasets.dataset import Dataset
from opus_core.storage_factory import StorageFactory
from opus_core.logger import logger
from opus_core.model import Model
from opus_core.sampling_toolbox import sample_replace
from numpy.random import random
from numpy import searchsorted, where, ones, allclose, array, logical_and, arange
from numpy import concatenate
from opus_core.sampling_toolbox import normalize
import sys

class MonteCarloAssignmentModel(Model):
    """Assign individuals from one geography (dataset1) to another (dataset2) with
    probablity equal to fractions of dataset1 in dataset2 through a Monte Carlo process.
    
    For Example, assign individual households from blockgroup to zone by the fractions
    of blockgroup in zones.  See unittest below for details.
    """
    
    model_name = "Monte Carlo Assignment Model"
    model_short_name = "MCAM"

    def run(self, individual_dataset, counts_dataset, fraction_dataset, id_name1='blockgroup_id', 
            id_name2='zone_id', fraction_attribute_name='fraction', out_storage=None):
        
        """
        """
        assert id_name1 in individual_dataset.get_known_attribute_names()
        if id_name2 not in individual_dataset.get_known_attribute_names():           
            individual_dataset.add_primary_attribute(-1*ones(individual_dataset.size()), id_name2)
        
        lucky_household_index = array([], dtype="int32")
        hh_zone_id = array([], dtype="int32")
        output_data = {}
        
        logger.start_block("Start assigning individuals")
        zone_ids = counts_dataset.get_attribute(id_name2)
        building_types = counts_dataset.get_attribute("building_type_id")
        households = counts_dataset.get_attribute("households")
        for zone_id, building_type, n in zip(zone_ids, building_types, households):
            logger.log_status("n(%s=%i & %s=%i) = %s:" % (id_name2, zone_id, "building_type_id", building_type, n))
            fraction_index = where(fraction_dataset.get_attribute(id_name2) == zone_id)
            
            blockgroup_ids = fraction_dataset.get_attribute_by_index(id_name1, fraction_index)
            fractions = fraction_dataset.get_attribute_by_index(fraction_attribute_name, fraction_index)
            for blockgroup_id, fraction in zip(blockgroup_ids, fractions):
                nn = int(round(n * fraction))
                logger.log_status("\tfrac(%s=%s) = %s, n = %s" % ("blockgroup_id", blockgroup_id, fraction, nn) )
                if nn >= 1:
                    suitable_household_index = where(logical_and(
                                                             individual_dataset.get_attribute(id_name1) == blockgroup_id,
                                                             individual_dataset.get_attribute("building_type_id") == building_type 
                                                             ))[0]
                    logger.log_status("\t\t sample %s from %s suitable households" % (nn, suitable_household_index.size))
                    if suitable_household_index.size == 0:
                        logger.log_warning("\tNo suitable households")
                        continue
                    lucky_household_index = concatenate((lucky_household_index, sample_replace(suitable_household_index, nn)))
                    hh_zone_id = concatenate((hh_zone_id, [zone_id]*nn))
                    
        for attribute_name in individual_dataset.get_known_attribute_names():
            output_data[attribute_name] = individual_dataset.get_attribute_by_index(attribute_name, lucky_household_index)
        output_data["original_household_id"] = output_data["household_id"]
        output_data["household_id"] = 1 + arange(lucky_household_index.size)
        output_data["zone_id"] = hh_zone_id
        
        storage = StorageFactory().get_storage('dict_storage')
        storage.write_table(table_name="households", table_data=output_data)
        output_dataset = Dataset(in_storage=storage, id_name=["household_id"], in_table_name="households")
        output_dataset.write_dataset(out_storage=out_storage, out_table_name="households")


class AssignmentOptionGroup:
    def __init__(self, usage="python %prog <-c /cache/directory> <-i individual_table_name> <-f fraction_table_name> <--id-name1=dataset1_id> <--id-name2=dataset2_id> [--fraction-attribute-name=fraction] [--help]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-c", "--cache-directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory containing cache for the simulated years")
        self.parser.add_option("-i", "--individual-table", dest="individual_table", default = None, type="str",
                               action="store", help="name of the cache table containing individuals to be assigned")
        self.parser.add_option("-t", "--counts-table", dest="counts_table", default = None, type="str",
                               action="store", help="name of the cache table containing total number of individuals in id-name2")
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
    counts_table = options.counts_table
    fraction_table = options.fraction_table
    fraction_attribute_name = options.fraction_attribute_name
    storage = StorageFactory().get_storage('flt_storage', storage_location=options.cache_directory)
    individual_dataset = Dataset(in_storage=storage, id_name=[], in_table_name=individual_table)
    counts_dataset = Dataset(in_storage=storage, id_name=[], in_table_name=counts_table)
    fraction_dataset = Dataset(in_storage=storage, id_name=[], in_table_name=fraction_table)
    
    MonteCarloAssignmentModel().run(individual_dataset, counts_dataset, fraction_dataset, 
                                    id_name1=options.id_name1, id_name2=options.id_name2,
                                    fraction_attribute_name=options.fraction_attribute_name,
                                    out_storage=storage)
    
    individual_dataset.write_dataset(out_storage=storage, out_table_name=individual_table, attributes=[options.id_name2])
    