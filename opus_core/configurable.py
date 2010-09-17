# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.configuration import Configuration
from inspect import getmembers, isroutine

class Configurable(object):
    """The base class for configurable objects.
    """
    
    def __new__(cls, *args, **kwargs):
        an_instance = object.__new__(cls)
        default_config = Configuration(an_instance.get_configuration())["init"]
        config = None
        if "model_configuration" in kwargs.keys():
            config = kwargs["model_configuration"]
            del kwargs["model_configuration"]
        an_instance.model_configuration = default_config.merge_defaults_with_arguments_and_config(
                                config, **kwargs)
                                
        if 'run' in map(lambda (name, obj): name, getmembers(an_instance, isroutine)):
            run_method = an_instance.run
            def config_run_method (*req_args, **opt_args):
                default_config = Configuration(an_instance.get_configuration())["run"]
                an_instance.model_configuration = default_config.merge_defaults_with_arguments_and_config(
                                an_instance.model_configuration, **opt_args)
                results = run_method(*req_args, **opt_args)                
                return results
            an_instance.run = config_run_method                        
        return an_instance
    
    def get_configuration(self):
        return {"init":{},
                "run":{},
                "estimate":{}}