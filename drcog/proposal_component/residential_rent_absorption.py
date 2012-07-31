# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable

class residential_rent_absorption(Variable):
    """
    """
    def dependencies(self):
        return ["tenure_id = (proposal_component.proposal_component_id > 0) * 1",  #tenure_id == 2 for own
                "bayarea_proposal_component.submarket_id",
                "_residential_rent_absorption = bayarea_proposal_component.disaggregate(bayarea.submarket.residential_absorption)",
                ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds['_residential_rent_absorption']
