# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

def opusRun(progressCB,logCB,params):
    param_dict = {}
    for key, val in params.items():
        param_dict[str(key)] = str(val)
    
    