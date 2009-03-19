# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

from opus_core.aspect.aspect import Aspect

class DatasetAspect(Aspect):
    def apply(self, dataset):
        raise NotImplementedError("DatasetAspect method 'apply' not "
            "implemented.")