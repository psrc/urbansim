# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, clip, asarray

# Template land overhead covers land not available for buildings: on large parcels new streets,
# stormwater and open-space tracts needed for subdivision; on all parcels the sidewalks and street
# area that parcel_sqft includes (parcel_sqft excludes critical areas but not right-of-way).
# OVERHEAD_SMALL_SHARE is the share of the template overhead applied to parcels up to OVERHEAD_LAND_MIN;
# the full overhead applies from OVERHEAD_LAND_MAX on, linear in between (land in sqft).
# OVERHEAD_SMALL_SHARE = 1 means the overhead does not depend on parcel size;
# 0 means no overhead on small parcels (use where parcels exclude right-of-way).
OVERHEAD_SMALL_SHARE = 1.0
OVERHEAD_LAND_MIN = 0.5 * 43560
OVERHEAD_LAND_MAX = 2.0 * 43560

def size_adjusted_overhead(percent_overhead, land_area, land_min=OVERHEAD_LAND_MIN, land_max=OVERHEAD_LAND_MAX,
                           small_share=OVERHEAD_SMALL_SHARE):
    """Return the template's percent_land_overhead (in %) scaled by the land area (sqft) taken by the project."""
    ramp = clip((asarray(land_area, dtype="float64") - land_min) / float(land_max - land_min), 0, 1)
    return percent_overhead * (small_share + (1 - small_share) * ramp)

class units_proposed_fraction(Variable):
    """Total units (as real numbers) proposed (residential units, and/or non residential sqft)
    for the proposed development project,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available.
    The template's land overhead is applied as set by size_adjusted_overhead (by default to all parcels);
    lot coverage is not used, as density and FAR are defined over the whole lot.
    """
    _return_type = "float32"

    def dependencies(self):
        return [
                "urbansim_parcel.development_project_proposal.land_area_taken",
                "density = development_project_proposal.disaggregate(urbansim_parcel.development_template.density)",
                "density_convertor = development_project_proposal.disaggregate(urbansim_parcel.development_template.density_converter)",  # land area is in sqft
                "percent_land_overhead = development_project_proposal.disaggregate(development_template.percent_land_overhead)",
                "density_is_units_per_lot = development_project_proposal.disaggregate(urbansim_parcel.development_template.is_units_per_lot)"
                 ]

    def compute(self, dataset_pool):
        ds = self.get_dataset()
        land_area = ds.get_attribute("land_area_taken")
        usable_ratio = 1 - size_adjusted_overhead(ds.get_attribute("percent_land_overhead"), land_area) / 100.0
        return where(ds.get_attribute("density_is_units_per_lot"), ds.get_attribute("density"),
                     land_area * usable_ratio * ds.get_attribute("density") * ds.get_attribute("density_convertor"))

    def post_check(self, values, dataset_pool):
        self.do_check("x >= 0", values)


from opus_core.tests import opus_unittest
from opus_core.tests.utils.variable_tester import VariableTester
from numpy import array, int32

class Tests(opus_unittest.OpusTestCase):
    ACRE = 43560
    def test_size_adjusted_overhead(self):
        land = array([0, 7000, 0.5*self.ACRE, 1.25*self.ACRE, 2*self.ACRE, 10*self.ACRE])
        # small_share = 1: 30% everywhere
        result = size_adjusted_overhead(30, land, small_share=1)
        self.assertTrue((abs(result - 30) < 1e-6).all())
        # small_share = 0: none up to 0.5 acre, half at 1.25 acres, full from 2 acres on
        result = size_adjusted_overhead(30, land, small_share=0)
        self.assertTrue((abs(result - array([0, 0, 0, 15, 30, 30])) < 1e-6).all())
        # small_share = 0.5: 15% up to 0.5 acre, 22.5% at 1.25 acres, 30% from 2 acres on
        result = size_adjusted_overhead(30, land, small_share=0.5)
        self.assertTrue((abs(result - array([15, 15, 15, 22.5, 30, 30])) < 1e-6).all())

    def test_my_inputs(self):
        tester = VariableTester(
            __file__,
            package_order=['urbansim_parcel', 'urbansim'],
            test_data={
            'development_template':
            {
                'template_id': array([1, 2, 3]),
                "density_type":  array(['units_per_acre', 'far', 'units_per_lot']),
                'density': array([6, 2.0, 4]),
                'percent_land_overhead': array([30, 20, 10]),
                'land_sqft_min': array([0, 0, 0], dtype=int32),
                'land_sqft_max': array([100, 100, 100], dtype=int32) * self.ACRE
            },
            'parcel':
            {
                "parcel_id":        array([1, 2, 3]),
                "vacant_land_area": array([7000, int(1.25*self.ACRE), 5*self.ACRE], dtype=int32),
            },
            'development_project_proposal':
            {
                "proposal_id": array([1, 2, 3, 4, 5, 6, 7]),
                "parcel_id":   array([1, 2, 3, 1, 2, 3, 3]),
                "template_id": array([1, 1, 1, 2, 2, 2, 3]),
            }
        })
        land = array([7000, int(1.25*self.ACRE), 5*self.ACRE])
        # share of overhead applied given the module setting OVERHEAD_SMALL_SHARE
        share = size_adjusted_overhead(1.0, land)
        should_be = array([land[0] * (1 - 0.3*share[0]) * 6 / self.ACRE,  # 30% overhead, small lot
                           land[1] * (1 - 0.3*share[1]) * 6 / self.ACRE,  # 1.25 acre
                           land[2] * 0.7 * 6 / self.ACRE,                 # 5 acres: always full 30%
                           land[0] * (1 - 0.2*share[0]) * 2,              # FAR template, 20% overhead, small lot
                           land[1] * (1 - 0.2*share[1]) * 2,              # FAR template, 1.25 acre
                           land[2] * 0.8 * 2,                             # FAR template, 5 acres: full 20%
                           4])                                            # units per lot: no land involved
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()

