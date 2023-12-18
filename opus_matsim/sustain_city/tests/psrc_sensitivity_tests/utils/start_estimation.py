# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from optparse import OptionParser
from opus_core.misc import get_config_from_opus_path
from opus_core.logger import logger
from opus_core.configurations.xml_configuration import XMLConfiguration
from urbansim.estimation.estimation_runner import EstimationRunner

class EstimationOptionGroup:
    ''' Runs Estimation for a desiered model (like HLCM)
        IT'S RECOMMANDED TO USE OPUS GUI IN ORDER TO RUN ESTIMATIONS !!!
    '''
    
    def __init__(self, usage="python %prog [options]", description=""):
            
        self.parser = OptionParser(usage=usage, description=description)
        self.parser.add_option("-m", "--model", dest="model_name", default = None,
                               action="store", help="Name of the model to be estimated")
        self.parser.add_option("-s", "--specification", dest="specification", default = None,
                               action="store", help="Specification module containing model specification in a dictionary format")
        self.parser.add_option("-x", "--xml-configuration", dest="xml_configuration", default = None,
                               action="store", help="Full path to an XML configuration file. One of the options -s and -x should be given, otherwise the specification is taken from cache.")
        self.parser.add_option("-c", "--configuration-path", dest="configuration_path", default=None, 
                               help="Opus path to Python module defining a configuration in dictionary format. One of the options -c and -x must be given.")
        self.parser.add_option("--save-results", dest="save_results", default=False, action="store_true", 
                               help="Results will be saved in the output configuration (if given) and in the cache")
        self.parser.add_option("--group", dest="model_group", default = None,
                               action="store", help="Name of the model group")
        
if __name__ == '__main__':
    try: import wingdbstub
    except: pass
    option_group = EstimationOptionGroup()
    parser = option_group.parser
    (options, args) = parser.parse_args()
    if options.model_name is None:
        raise Exception("Model name (argument -m) must be given.")
    if (options.configuration_path is None) and (options.xml_configuration is None):
        raise Exception("Configuration path (argument -c) or XML configuration (argument -x) must be given.")
    if (options.specification is None) and (options.xml_configuration is None):
        logger.log_warning("No specification given (arguments -s or -x). Specification taken from the cache.")
    if options.xml_configuration is not None:
        xconfig = XMLConfiguration(options.xml_configuration)
    else:
        xconfig = None
    if options.configuration_path is None:
        config = None
    else:
        config = get_config_from_opus_path(options.configuration_path)
    estimator = EstimationRunner(model=options.model_name, 
                                 specification_module=options.specification, 
                                 xml_configuration=xconfig, 
                                 model_group=options.model_group,
                                 configuration=config,
                                 save_estimation_results=options.save_results)
    estimator.estimate()
    er = estimator
    
    ds = er.get_data_as_dataset()
    ds.summary()
    ds.get_attribute("ln_residential_units").shape
    
    estimator.create_prediction_success_table(summarize_by="fazdistrict_id=building.disaggregate(faz.fazdistrict_id, intermediates=[zone, parcel])")

    estimator.create_prediction_success_table(summarize_by="area_type_id=building.disaggregate(zone.area_type_id, intermediates=[parcel])")
