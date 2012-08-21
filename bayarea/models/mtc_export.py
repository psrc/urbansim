# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley
# See opus_core/LICENSE 

from opus_core.model import Model
import os, glob, shutil
from opus_core.logger import logger, block, log_block
from opus_core.session_configuration import SessionConfiguration
from opus_core.simulation_state import SimulationState
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.csv_storage import csv_storage
from opus_core.variables.variable_name import VariableName
import bayarea.travel_model.mtc_common as mtc_common

flip_urbansim_to_tm_variable_mappling = True

@log_block()
class MTCExport(Model):
    """ 
    # This model prepares the TazData, PopSynHousehold, PopSynPerson, and
    # WalkAccessBuffers from opus bay area land use model output.
    #
    # The MTC travel model input specifications can be found here:
    # http://mtcgis.mtc.ca.gov/foswiki/Main/DataDictionary
    """
    model_name = "MTCExport"

    def __init__(self, data_to_export=None):
        logger.log_status("INITIALIZING")
        print data_to_export
        self.data_to_export = data_to_export

    def run(self, year=None, years_to_run=[]):
        if year not in years_to_run or self.data_to_export == None:
            return

        sim_state = SimulationState()
        cache_directory = sim_state.get_cache_directory()
        logger.log_status("HA HA HA " + str(year) + " " + cache_directory)
        attribute_cache = AttributeCache()
        dataset_pool = SessionConfiguration().get_dataset_pool()
        out_dir = os.path.join(cache_directory, "mtc_data")

        out_storage = csv_storage(storage_location=out_dir)
        for data_fname, variable_mapping in self.data_to_export.iteritems():
            if not flip_urbansim_to_tm_variable_mappling:
                col_names = variable_mapping.values()
                variables_aliases = ["=".join(mapping[::-1]) for mapping in \
                                     variable_mapping.iteritems()]
            else:
                col_names = variable_mapping.keys()
                variables_aliases = ["=".join(mapping) for mapping in \
                                     variable_mapping.iteritems()]

            dataset_name = VariableName(variables_aliases[0]).get_dataset_name()
            dataset = dataset_pool.get_dataset(dataset_name)
            dataset.compute_variables(variables_aliases)

            org_fname = os.path.join(out_dir, "%s.computed.csv" % data_fname)
            new_fname = os.path.join(out_dir, "%s%s.csv" % (year,data_fname))
            block_msg = "Writing {} for travel model to {}".format(data_fname,
                                                                   new_fname)
            with block(block_msg):
                dataset.write_dataset(attributes=col_names,
                                    out_storage=out_storage,
                                    out_table_name=data_fname)
                #rename & process header
                shutil.move(org_fname, new_fname)
                os.system("sed 's/:[a-z][0-9]//g' -i %s" % new_fname)
            return

