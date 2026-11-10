# Opus/UrbanSim urban simulation software.
# Copyright (C) 2010-2011 University of California, Berkeley, 2005-2009 University of Washington
# See opus_core/LICENSE

from opus_core.variables.variable import Variable
from numpy import where, clip, asarray

# Template land overhead (new streets, stormwater, open-space tracts) is only needed when a parcel
# is large enough to be subdivided. Parcel areas exclude critical areas and existing right-of-way,
# so small infill lots get no overhead. The overhead is 0 below OVERHEAD_LAND_MIN, the full
# template value above OVERHEAD_LAND_MAX, and linear in between (in sqft).
OVERHEAD_LAND_MIN = 0.5 * 43560
OVERHEAD_LAND_MAX = 2.0 * 43560

def size_adjusted_overhead(percent_overhead, land_area, land_min=OVERHEAD_LAND_MIN, land_max=OVERHEAD_LAND_MAX):
    """Return the template's percent_land_overhead (in %) scaled by the land area (sqft) taken by the project."""
    scale = clip((asarray(land_area, dtype="float64") - land_min) / float(land_max - land_min), 0, 1)
    return percent_overhead * scale

class units_proposed_fraction(Variable):
    """Total units (as real numbers) proposed (residential units, and/or non residential sqft)
    for the proposed development project,
    depending on whether the proposed projects will be prorated or not, part or all of the
    units will be available.
    The template's land overhead is applied according to the land area taken (see size_adjusted_overhead);
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
        # 30% overhead: none up to 0.5 acre, half at 1.25 acres, full from 2 acres on
        result = size_adjusted_overhead(30, array([0, 7000, 0.5*self.ACRE, 1.25*self.ACRE, 2*self.ACRE, 10*self.ACRE]))
        self.assertTrue((abs(result - array([0, 0, 0, 15, 30, 30])) < 1e-6).all())

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
        should_be = array([land[0] * 1.0 * 6 / self.ACRE,     # small lot: no overhead
                           land[1] * 0.85 * 6 / self.ACRE,    # 1.25 acre: half of 30%
                           land[2] * 0.7 * 6 / self.ACRE,     # 5 acres: full 30%
                           land[0] * 1.0 * 2,                 # FAR template, small lot
                           land[1] * 0.9 * 2,                 # FAR template, half of 20%
                           land[2] * 0.8 * 2,                 # FAR template, full 20%
                           4])                                # units per lot: no land involved
        tester.test_is_close_for_variable_defined_by_this_module(self, should_be)

if __name__=='__main__':
    opus_unittest.main()

