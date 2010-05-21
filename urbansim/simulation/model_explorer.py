# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.logger import logger
from opus_core.configuration import Configuration
from opus_core.resources import Resources
from opus_core.simulation_state import SimulationState
from opus_core.session_configuration import SessionConfiguration
from opus_core.store.attribute_cache import AttributeCache
from opus_core.store.utils.cache_flt_data import CacheFltData
from opus_core.generic_model_explorer import GenericModelExplorer
from urbansim.model_coordinators.model_system import ModelSystem
from opus_core.choice_model import ChoiceModel


class ModelExplorer(GenericModelExplorer):
    def __init__(self, model, year, scenario_name=None, model_group=None, configuration=None, xml_configuration=None, 
                 cache_directory=None):
        self.model_group = model_group
        self.explored_model = model
 
        if configuration is None:
            if xml_configuration is None:
                raise StandardError, "Either dictionary based or XML based configuration must be given."
            config = xml_configuration.get_run_configuration(scenario_name)
        else:
            config = Configuration(configuration)
            
        dependent_models = config['models_configuration'][model]['controller'].get('dependencies', [])
        config['models'] = dependent_models
        if model_group is None:
            config['models'] = config['models'] + [{model: ["run"]}]
        else:
            config['models'] = config['models'] + [{model: {"group_members": [{model_group: ["run"]}]}}]
        
        config['years'] = [year, year]
        config["datasets_to_cache_after_each_model"]=[]
        config['flush_variables'] = False
        
        self.config = Resources(config)
        self.xml_configuration = xml_configuration
        
        cache = False
        if cache_directory is None:
            cache_directory = self.config['creating_baseyear_cache_configuration'].cache_directory_root
            cache = True
        self.simulation_state = SimulationState(new_instance=True, base_cache_dir=cache_directory)
        
        if cache:
            self.config['cache_directory'] = self.simulation_state.get_cache_directory()
            CacheFltData().run(self.config)
        else:
            self.config['cache_directory'] = cache_directory
        
        SessionConfiguration(new_instance=True,
                             package_order=self.config['dataset_pool_configuration'].package_order,
                             in_storage=AttributeCache())
        
    def run(self):
        self.model_system = ModelSystem()
        self.model_system.run(self.config, write_datasets_to_cache_at_end_of_year=False)
        logger.log_status("Data cache in %s" % self.simulation_state.get_cache_directory())
        
    def get_agents_for_simulation(self):
        return self.get_active_agent_set()
        
    def get_model_name(self):
        return (self.explored_model, self.model_group)
        
    def get_specification(self):
        return self.get_model().get_specified_coefficients().specification
    
    def get_probabilities(self, submodel=-2):
        model = self.get_model()
        if isinstance(model, ChoiceModel):
            return model.get_probabilities_and_choices(submodel)
        print '\nMethod is implemented only for ChoiceModels.\n'

    def export_probabilities(self, submodel=-2, filename='./choice_model.txt'):
        """Export probabilities and choices into a file."""
        
        model = self.get_model()
        if isinstance(model, ChoiceModel):
            model.export_probabilities(submodel, file_name=filename)
        else:
            print '\nMethod is implemented only for ChoiceModels.\n'