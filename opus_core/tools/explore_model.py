# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
from opus_core.misc import get_config_from_opus_path
from opus_core.logger import logger
from opus_core.configurations.xml_configuration import XMLConfiguration
from opus_core.simulation.model_explorer import ModelExplorer

class ModelExplorerOptionGroup:
    def __init__(self, usage="python %prog [options] ", 
                 description="Runs the given model for the given year, using data from given directory. Options -y and -d are mandatory. Furthermore, either -c or -x must be given."):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-m", "--model", dest="model_name", default = None,
                               action="store", help="Name of the model to run.")
        self.parser.add_option("-y", "--year", dest="year", default = None,
                               action="store", help="Year for which the model should run.")
        self.parser.add_option("-d", "--directory", dest="cache_directory", default = None,
                               action="store", help="Cache directory to be used for the run. Use the keyword 'BASE', if the base year data should be used.")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default = None,
                               action="store", help="Full path to an XML configuration file (must also provide a scenario name using -s). Either -x or -c must be given.")
        self.parser.add_option("-s", "--scenario_name", dest="scenario_name", default=None, 
                                help="Name of the scenario. Must be given if option -x is used.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining a configuration in dictionary format. Either -c or -x must be given.")
        self.parser.add_option("--group", dest="model_group", default = None,
                               action="store", help="Name of the model group")

def main():    
    import sys
    option_group = ModelExplorerOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()

    if options.year is None:
        raise StandardError, "Year (argument -y) must be given."
    if options.cache_directory is None:
        raise StandardError, "Cache directory (argument -d) must be given."
    if (options.configuration_path is None) and (options.xml_configuration is None):
        raise StandardError, "Configuration path (argument -c) or XML configuration (argument -x) must be given."
    if (options.scenario_name is None) and (options.xml_configuration is not None):
        raise StandardError, "No scenario given (argument -s). Must be specified if option -x is used."
    if options.xml_configuration is not None:
        xconfig = XMLConfiguration(options.xml_configuration)
    else:
        xconfig = None
    if options.configuration_path is None:
        config = None
    else:
        config = get_config_from_opus_path(options.configuration_path)
        
    if options.cache_directory == 'BASE':
        cache_directory = None
    else:
        cache_directory = options.cache_directory
    explorer = ModelExplorer(model=options.model_name, year=int(options.year),
                                 scenario_name=options.scenario_name, 
                                 model_group=options.model_group,
                                 configuration=config,
                                 xml_configuration=xconfig, 
                                 cache_directory=cache_directory)

    explorer.run()
    return explorer

if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    ex = main()
    #ex.export_probabilities(submodel=13, filename="elcm_13.txt", attributes_ds1=["sector_id"], attributes_ds2=["parcel_id"])