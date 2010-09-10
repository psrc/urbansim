# Opus/UrbanSim urban simulation software.
# Copyright (C) 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where

class units_proposed_fraction(Variable):
    """Total units (as real numbers) proposed (residential units, and/or non residential sqft) 
    for the proposed development project,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available.
    """
    _return_type = "float32"

    def dependencies(self):
        return [
                "urbansim_parcel.development_project_proposal.land_area_taken",
                "density = development_project_proposal.disaggregate(urbansim_parcel.development_template.density)",
                "density_convertor = development_project_proposal.disaggregate(urbansim_parcel.development_template.density_converter)",  # land area is in sqft
                "usable_ratio = (1- development_project_proposal.disaggregate(development_template.percent_land_overhead) / 100.0).astype(float32)",
                 ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        return ds.get_attribute("land_area_taken") * ds.get_attribute("usable_ratio") * ds.get_attribute("density") * ds.get_attribute("density_convertor")

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)

