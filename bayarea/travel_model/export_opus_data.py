# Opus/UrbanSim urban simulation software.
# Copyright (C) 2012 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger, block, log_block

@log_block()
def export_opus_data(config, year):
    """ 
    # This script prepares the TazData, PopSynHousehold, PopSynPerson, and
    # WalkAccessBuffers from opus bay area land use model output.
    #
    # The MTC travel model input specifications can be found here:
    # http://mtcgis.mtc.ca.gov/foswiki/Main/DataDictionary

    """
    
    tm_config = config['travel_model_configuration']
    data_to_export = tm_config[''] 
    data_exchange_dir = tm_config[year]['data_exchange_dir']
    for data_file, variables in data_to_export.iteritems():
        data = {} #ordered_dict?
        data_file = os.path.join(data_exchange_dir, data_file)
        dataset_name = variables[0].split(".")[0]
        dataset = dataset_pool.get_dataset(dataset_name)
        dataset.compute_variables(variables)
        for alias, variable in zip(aliases, variables):
            data[alias] = dataset[variable]
        with block("Writing data file {} for travel model".format(data_file)):
            to_csv(data, data_file)

if __name__ == "__main__":
    from optparse import OptionParser
    from opus_core.resources import Resources
    from opus_core.file_utilities import get_resources_from_file
    parser = OptionParser()
    parser.add_option("-r", "--resources", dest="resources_file_name", action="store", type="string",
                      help="Name of file containing resources")
    parser.add_option("-y", "--year", dest="year", action="store", type="int",
                      help="Year in which to 'run' the travel model")
    (options, args) = parser.parse_args()
    resources = Resources(get_resources_from_file(options.resources_file_name))

    export_opus_data(resources, options.year)    

