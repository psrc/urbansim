# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005, 2006, 2007, 2008, 2009 University of Washington
# See opus_docs/LICENSE 

class AttributeType(object):
    PRIMARY = 1
    COMPUTED = 2
    LAG = 3
    EXOGENOUS = 4
    
class InteractionAttributeType(object):
    OWNER_AGENT = 1
    OWNER_CHOICE = 2
    OWNER_INTERACTION = 3
    