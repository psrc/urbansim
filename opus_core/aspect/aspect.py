# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE 

class Aspect(object):
    def apply(self, *args, **kwargs):
        raise NotImplementedError("Aspect method 'apply' not "
            "implemented.")