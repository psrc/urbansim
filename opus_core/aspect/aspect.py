# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

class Aspect(object):
    def apply(self, *args, **kwargs):
        raise NotImplementedError("Aspect method 'apply' not "
            "implemented.")