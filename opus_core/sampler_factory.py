# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE

from opus_core.model_component_creator import ModelComponentCreator

class SamplerFactory(ModelComponentCreator):

    def get_sampler(self, method, debuglevel=0):
        """'method determines the name of sampling subclass in forma package.subdir.name 
        (e.g. opus_core.samplers.weighted_sampler, ...). There has to be a module in the subdir directory
        of that name that contains a class of the same name. 
        """
        return self.get_model_component(method, debuglevel=debuglevel)
