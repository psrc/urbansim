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
from opus_core import paths
import numpy as np

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
        self.data_to_export = data_to_export

    def run(self, year=None, years_to_run=[], configuration=None):
        if year not in years_to_run or self.data_to_export == None:
            return

        cache_directory = configuration['cache_directory']
        simulation_state = SimulationState()
        simulation_state.set_cache_directory(cache_directory)
        simulation_state.set_current_time(year)
        attribute_cache = AttributeCache()
        package_order=configuration['dataset_pool_configuration'].package_order
        dataset_pool = SessionConfiguration(new_instance=True,
                                            package_order=package_order,
                                            in_storage=attribute_cache
                                            ).get_dataset_pool()
        out_dir = os.path.join(cache_directory, "mtc_data")

        out_storage = csv_storage(storage_location=out_dir)

        # Adjust the age distribution per ABAG/MTC's specifications
        age_control_dir = os.path.join(paths.OPUS_DATA_PATH, configuration['project_name'], "ageControl")
        age_control_storage = csv_storage(storage_location=age_control_dir)
        age_control_files = os.listdir(age_control_dir)
        years = np.array([int(os.path.basename(x).replace("tazData", "").replace(".csv", "")) for x in glob.glob(os.path.join(age_control_dir, "tazData*.csv"))])
        closest_year = years[np.argmin(np.abs(years - [year]*len(years)))]
        if closest_year != year:
            logger.log_warning("Could not find age control data for " + str(year) +
                               ".  Choosing nearest year " + str(closest_year) + ".")

        age_control_table = age_control_storage.load_table("tazData" + str(closest_year), lowercase=False)

        # Calculate the ABAG shares of person by age
        age_categories = ['AGE0004', 'AGE0519', 'AGE2044', 'AGE4564', 'AGE65P']
        age_category_sums = dict((k, age_control_table[k].sum()) for k in age_categories)
        total = sum(age_category_sums.values())
        abag_age_category_shares = dict((k, age_category_sums[k]/total) for k in age_categories)

        for data_fname, variable_mapping in self.data_to_export.items():

            if not flip_urbansim_to_tm_variable_mappling:
                col_names = list(variable_mapping.values())
                variables_aliases = ["=".join(mapping[::-1]) for mapping in \
                                     variable_mapping.items()]
            else:
                col_names = list(variable_mapping.keys())
                variables_aliases = ["=".join(mapping) for mapping in \
                                     variable_mapping.items()]

            dataset_name = VariableName(variables_aliases[0]).get_dataset_name()
            dataset = dataset_pool.get_dataset(dataset_name)
            dataset.compute_variables(variables_aliases)

            if data_fname == "ABAGData":
                logger.log_status("Adjusting ABAGData to match age controls")
                age_category_sums = dict((k, dataset[k].sum()) for k in age_categories)
                total = sum(age_category_sums.values())
                us_age_category_shares = dict((k, age_category_sums[k]/total) for k in age_categories)
                adjustments = dict((k, abag_age_category_shares[k]/us_age_category_shares[k]) for k in age_categories)
                diff = np.zeros(dataset.n)
                for k in age_categories:
                    before = dataset[k]
                    dataset[k] = np.array([round(v*adjustments[k]) for v in dataset.get_attribute(k)])
                    diff += (dataset[k] - before)
                dataset["TOTPOP"] += diff
                dataset["HHPOP"] += diff
                logger.log_status("NOTE: Adjusted total population by %d (%2.3f%%) due to rounding error." %
                                  (int(diff.sum()), diff.sum()*100/total))

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

