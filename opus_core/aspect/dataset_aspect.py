# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

from opus_core.aspect.aspect import Aspect

class DatasetAspect(Aspect):
    def apply(self, dataset):
        raise NotImplementedError("DatasetAspect method 'apply' not "
            "implemented.")