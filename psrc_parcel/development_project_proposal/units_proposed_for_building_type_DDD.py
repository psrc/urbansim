# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class units_proposed_for_building_type_DDD(Variable):
    
    def __init__(self, building_type_id):
        Variable.__init__(self)
        self.building_type = building_type_id
        
    def dependencies(self):
        return ["_units_proposed_for_%s = development_project_proposal.aggregate(urbansim_parcel.development_project_proposal_component.units_proposed * (development_project_proposal_component.building_type_id == %s))" % (self.building_type, self.building_type)]

    def compute(self,  dataset_pool):
        return self.get_dataset()["_units_proposed_for_%s" % self.building_type]

    